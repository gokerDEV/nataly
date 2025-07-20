# nataly/engine.py
# The core astrological calculation engine.

import swisseph as swe
import os
from typing import List, Dict

from .models import Body, House, Aspect, Sign, OrbConfig
from .constants import (
    SIGNS, SIGN_NAMES_BY_DEGREE, DIGNITY_RULES, ASPECT_DATA, 
    PLANET_NAMES, AXES_NAMES, ALL_BODY_NAMES, MAJOR_ASPECTS, 
    PLANET_MAPPING_SWE, ORB_CONFIGS, ANGLES, LUMINARIES,
    BODY_TYPE_MAPPINGS, create_orb_config
)


class AstroEngine:
    """Core class that performs all astrological calculations and returns structured data models."""
    
    def __init__(self, orb_config=None, ephe_path='./nataly/ephe'):
        """
        Initialize the astrological engine.
        
        Args:
            orb_config: OrbConfig object or dict for orb settings
            ephe_path: Path to ephemeris files
        """
        if orb_config is None:
            orb_config = create_orb_config()
        elif isinstance(orb_config, dict):
            orb_config = OrbConfig.from_dict(orb_config)
        
        self.orb_config = orb_config
        self.ephe_path = ephe_path
        
        if not os.path.exists(self.ephe_path) or not os.listdir(self.ephe_path):
            print(f"⚠️  WARNING: Ephemeris files not found in '{self.ephe_path}' directory!")
            print("📥 To download ephemeris files:")
            print("   1. Go to https://www.astro.com/swisseph/swedownload_j.htm")
            print("   2. Download 'seas_18.se1' file from 'Swiss Ephemeris Files' section")
            print("   3. Place the downloaded file in './ephe' directory")
            print("   4. Required ephemeris files (should be in nataly/ephe/):")
            print("      - 'seas_18.se1' (Saturn ephemeris)")
            print("      - 'sepl_18.se1' (Pluto ephemeris)")
            print("      - 'semo_18.se1' (Moon ephemeris)")
            print("      - 'seplm18.se1' (Pluto-Moon ephemeris)")
            print("      - 'semom18.se1' (Moon-Moon ephemeris)")
            print("   5. Using default Moshier ephemeris for now (less accurate)")
            print()
        swe.set_ephe_path(self.ephe_path)

    def _get_sign_from_longitude(self, longitude: float) -> Sign:
        """Get zodiac sign from longitude."""
        sign_index = int(longitude / 30)
        sign_name = SIGN_NAMES_BY_DEGREE[sign_index]
        return SIGNS[sign_name]

    def _get_house_from_longitude(self, longitude: float, house_cusps: List[float]) -> int:
        """Get house number from longitude using house cusps."""
        ac_longitude = house_cusps[0]
        normalized_longitude = (longitude - ac_longitude + 360) % 360
        for i in range(12):
            cusp_start = (house_cusps[i] - ac_longitude + 360) % 360
            cusp_end = (house_cusps[(i + 1) % 12] - ac_longitude + 360) % 360
            if cusp_end < cusp_start:
                if normalized_longitude >= cusp_start or normalized_longitude < cusp_end:
                    return i + 1
            elif cusp_start <= normalized_longitude < cusp_end:
                return i + 1
        return 12

    def _get_dignity(self, body_name: str, sign_name: str) -> str:
        """Get planetary dignity (domicile, exaltation, detriment, fall)."""
        for dignity, rules in DIGNITY_RULES.items():
            if body_name in rules:
                rule_sign = rules[body_name]
                if isinstance(rule_sign, list) and sign_name in rule_sign:
                    return dignity
                if rule_sign == sign_name:
                    return dignity
        return ""

    def _get_body_type(self, body_name: str) -> str:
        """Get the type of celestial body."""
        return BODY_TYPE_MAPPINGS.get(body_name, "Planet")

    def _get_orb_category(self, p1_name: str, p2_name: str) -> str:
        """Determine appropriate orb category for planet pair."""
        if p1_name in ANGLES or p2_name in ANGLES:
            return 'angles'
        elif p1_name in LUMINARIES or p2_name in LUMINARIES:
            return 'luminaries'
        else:
            return 'planets'

    def _get_categorized_orb(self, aspect_name: str, p1_name: str, p2_name: str) -> float:
        """Get categorized orb value."""
        category = self._get_orb_category(p1_name, p2_name)
        category_config = getattr(self.orb_config, category, {})
        return category_config.get(aspect_name, 0)

    def _calculate_angular_difference(self, lon1: float, lon2: float) -> float:
        """Calculate shortest angular distance between two positions."""
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def get_planets_and_houses(self, dt_utc, lat, lon) -> (Dict[str, Body], List[House]):
        """Calculate planetary positions and house cusps."""
        jd_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60.0)
        raw_house_cusps, ascmc = swe.houses(jd_utc, lat, lon, b'P')
        house_cusps = list(raw_house_cusps)
        bodies_dict = {}
        
        for name in ALL_BODY_NAMES:
            planet_id = PLANET_MAPPING_SWE.get(name)
            
            # Special calculation for angles
            if name in AXES_NAMES:
                if name == "AC":
                    lon = ascmc[0]
                elif name == "MC":
                    lon = ascmc[1]
                elif name == "IC":
                    # IC = MC + 180°
                    lon = (ascmc[1] + 180) % 360
                elif name == "DC":
                    # DC = AC + 180°
                    lon = (ascmc[0] + 180) % 360
                else:
                    continue  # Unknown angle
                speed = 0.0
            # Special calculation for South Node (True Node + 180°)
            elif name == "South Node":
                true_node_body = bodies_dict.get("True Node")
                if true_node_body:
                    lon = (true_node_body.longitude + 180) % 360
                    speed = true_node_body.speed  # Same speed as True Node
                else:
                    continue  # True Node not calculated yet, skip
            # Celestial bodies calculable with Swiss Ephemeris
            elif planet_id is not None:
                try:
                    full_output, _ = swe.calc_ut(jd_utc, planet_id, swe.FLG_SPEED)
                    lon, speed = full_output[0], full_output[3]
                except Exception as e:
                    print(f"⚠️ Warning: Could not calculate position for {name}: {e}")
                    continue
            else:
                # Skip celestial bodies without Swiss Ephemeris mapping
                print(f"⚠️ Warning: No Swiss Ephemeris mapping for {name}, skipping...")
                continue
            
            sign = self._get_sign_from_longitude(lon)
            house = self._get_house_from_longitude(lon, house_cusps)
            dignity = self._get_dignity(name, sign.name)
            body_type = self._get_body_type(name)
            
            bodies_dict[name] = Body(
                name=name, 
                body_type=body_type,
                longitude=lon, 
                speed=speed,
                is_retrograde=speed < 0 and name not in AXES_NAMES,
                sign=sign, 
                house=house, 
                dignity=dignity
            )
        
        houses_list = []
        for i in range(12):
            cusp_lon = house_cusps[i]
            sign = self._get_sign_from_longitude(cusp_lon)
            classic_ruler_name = sign.classic_ruler
            modern_ruler_name = sign.modern_ruler
            
            classic_ruler_body = bodies_dict.get(classic_ruler_name)
            modern_ruler_body = bodies_dict.get(modern_ruler_name) if modern_ruler_name != classic_ruler_name else None
            
            houses_list.append(House(
                id=i + 1, 
                cusp_longitude=cusp_lon, 
                sign=sign,
                classic_ruler=classic_ruler_body,
                modern_ruler=modern_ruler_body,
                classic_ruler_house=classic_ruler_body.house if classic_ruler_body else None,
                modern_ruler_house=modern_ruler_body.house if modern_ruler_body else None
            ))
        return bodies_dict, houses_list

    def get_aspects(self, bodies1: Dict[str, Body], bodies2: Dict[str, Body] = None) -> List[Aspect]:
        """Calculate aspects between celestial bodies."""
        if bodies2 is None:
            bodies2 = bodies1
        
        aspects = []
        b1_items = list(bodies1.values())
        b2_items = list(bodies2.values())

        for i, body1 in enumerate(b1_items):
            for j, body2 in enumerate(b2_items):
                if i >= j:  # Avoid duplicate calculations
                    continue
                
                # Calculate angular difference
                angular_diff = self._calculate_angular_difference(body1.longitude, body2.longitude)
                
                # Find matching aspect
                for aspect_name, aspect_data in ASPECT_DATA.items():
                    aspect_angle = aspect_data["angle"]
                    aspect_symbol = aspect_data["symbol"]
                    
                    # Get orb for this aspect and planet pair
                    orb = self._get_categorized_orb(aspect_name, body1.name, body2.name)
                    
                    # Check if within orb
                    if abs(angular_diff - aspect_angle) <= orb:
                        # Determine if applying or separating
                        is_applying = self._is_aspect_applying(body1, body2, aspect_angle)
                        
                        aspects.append(Aspect(
                            body1=body1,
                            body2=body2,
                            aspect_type=aspect_name,
                            symbol=aspect_symbol,
                            orb=angular_diff - aspect_angle,
                            is_applying=is_applying
                        ))
                        break  # Found matching aspect, move to next pair
        
        return aspects

    def _is_aspect_applying(self, body1: Body, body2: Body, aspect_angle: float) -> bool:
        """Determine if an aspect is applying or separating."""
        # This is a simplified implementation
        # In a more sophisticated version, you'd need to consider the direction of movement
        # For now, we'll use a simple heuristic based on speed
        if body1.speed == 0 and body2.speed == 0:
            return True  # Static bodies, consider as applying
        
        # If one body is moving and the other isn't, the moving body determines the direction
        if body1.speed != 0 and body2.speed == 0:
            return body1.speed > 0
        elif body2.speed != 0 and body1.speed == 0:
            return body2.speed > 0
        
        # If both are moving, use the faster one
        if abs(body1.speed) > abs(body2.speed):
            return body1.speed > 0
        else:
            return body2.speed > 0 