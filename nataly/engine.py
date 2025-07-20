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

    def _get_categorized_orb(self, aspect_name: str, p1_name: str, p2_name: str) -> float:
        """Determine appropriate orb for a planet pair and aspect."""
        if p1_name in ANGLES or p2_name in ANGLES:
            category = 'angles'
        elif p1_name in LUMINARIES or p2_name in LUMINARIES:
            category = 'luminaries'
        else:
            category = 'planets'
        
        category_config = getattr(self.orb_config, category, {})
        return category_config.get(aspect_name, 0)

    def _calculate_angular_difference(self, lon1: float, lon2: float) -> float:
        """Calculate the shortest angular distance between two longitudes."""
        diff = abs(lon1 - lon2)
        return min(diff, 360 - diff)

    def get_planets_and_houses(self, dt_utc, lat, lon) -> (Dict[str, Body], List[House]):
        """Calculate planetary positions and house cusps."""
        jd_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60.0)
        raw_house_cusps, ascmc = swe.houses(jd_utc, lat, lon, b'P')
        house_cusps = list(raw_house_cusps)
        bodies_dict = {}

        for name in ALL_BODY_NAMES:
            planet_id = PLANET_MAPPING_SWE.get(name)
            lon_val, speed = 0.0, 0.0

            if name in AXES_NAMES:
                if name == "AC": lon_val = ascmc[0]
                elif name == "MC": lon_val = ascmc[1]
                elif name == "IC": lon_val = (ascmc[1] + 180) % 360
                elif name == "DC": lon_val = (ascmc[0] + 180) % 360
                else: continue
            elif name == "South Node":
                if "True Node" in bodies_dict:
                    lon_val = (bodies_dict["True Node"].longitude + 180) % 360
                    speed = bodies_dict["True Node"].speed
                else: continue
            elif planet_id is not None:
                try:
                    full_output, _ = swe.calc_ut(jd_utc, planet_id, swe.FLG_SPEED)
                    lon_val, speed = full_output[0], full_output[3]
                except Exception: continue
            else: continue

            sign = self._get_sign_from_longitude(lon_val)
            house = self._get_house_from_longitude(lon_val, house_cusps)
            dignity = self._get_dignity(name, sign.name)
            body_type = self._get_body_type(name)

            bodies_dict[name] = Body(
                name=name, body_type=body_type, longitude=lon_val, speed=speed,
                is_retrograde=speed < 0 and name not in AXES_NAMES,
                sign=sign, house=house, dignity=dignity
            )

        houses_list = []
        for i in range(12):
            cusp_lon = house_cusps[i]
            sign = self._get_sign_from_longitude(cusp_lon)
            classic_ruler = bodies_dict.get(sign.classic_ruler)
            modern_ruler = bodies_dict.get(sign.modern_ruler) if sign.modern_ruler else None
            houses_list.append(House(
                id=i + 1, cusp_longitude=cusp_lon, sign=sign,
                classic_ruler=classic_ruler, modern_ruler=modern_ruler,
                classic_ruler_house=classic_ruler.house if classic_ruler else None,
                modern_ruler_house=modern_ruler.house if modern_ruler else None
            ))
        return bodies_dict, houses_list

    def get_aspects(self, bodies1: Dict[str, Body], bodies2: Dict[str, Body] = None) -> List[Aspect]:
        """
        Calculates aspects by finding the closest aspect type for each pair of bodies,
        ignoring orb limits to find all potential aspects for comparison.
        """
        if bodies2 is None:
            bodies2 = bodies1
        
        aspects = []
        processed_pairs = set()
        b1_items, b2_items = list(bodies1.values()), list(bodies2.values())

        for body1 in b1_items:
            for body2 in b2_items:
                if body1.name == body2.name:
                    continue
                
                pair_key = tuple(sorted((body1.name, body2.name)))
                if pair_key in processed_pairs:
                    continue
                processed_pairs.add(pair_key)

                angular_diff = self._calculate_angular_difference(body1.longitude, body2.longitude)
                
                best_match = None
                smallest_orb_abs = float('inf')

                # First, try to find a major aspect within reasonable orb
                major_aspects = ["Conjunction", "Opposition", "Trine", "Square", "Sextile"]
                for aspect_name in major_aspects:
                    if aspect_name in ASPECT_DATA:
                        aspect_data = ASPECT_DATA[aspect_name]
                        current_orb_abs = abs(angular_diff - aspect_data["angle"])
                        # Major aspects get priority if orb is reasonable (within 10 degrees)
                        if current_orb_abs < 10.0 and current_orb_abs < smallest_orb_abs:
                            smallest_orb_abs = current_orb_abs
                            best_match = (aspect_name, aspect_data)
                
                # If no major aspect found, find the aspect with the smallest absolute orb
                if best_match is None:
                    for aspect_name, aspect_data in ASPECT_DATA.items():
                        current_orb_abs = abs(angular_diff - aspect_data["angle"])
                        if current_orb_abs < smallest_orb_abs:
                            smallest_orb_abs = current_orb_abs
                            best_match = (aspect_name, aspect_data)
                
                if best_match:
                    aspect_name, aspect_data = best_match
                    is_applying = self._is_aspect_applying(body1, body2, aspect_data["angle"], angular_diff)
                    
                    # Calculate the orb with correct sign
                    # Positive orb = applying, negative orb = separating
                    orb_magnitude = abs(angular_diff - aspect_data["angle"])
                    actual_orb = orb_magnitude if is_applying else -orb_magnitude
                    
                    aspects.append(Aspect(
                        body1=body1,
                        body2=body2,
                        aspect_type=aspect_name,
                        symbol=aspect_data["symbol"],
                        orb=actual_orb,
                        is_applying=is_applying
                    ))
        return aspects

    def _is_aspect_applying(self, body1: Body, body2: Body, aspect_angle: float, angular_diff: float) -> bool:
        """
        Determines if an aspect is applying or separating.
        """
        if abs(body1.speed) > abs(body2.speed):
            faster_body, slower_body = body1, body2
        else:
            faster_body, slower_body = body2, body1
            
        if abs(faster_body.speed) < 0.001:  # Very slow or stationary
            return True

        # Calculate the direction of the faster body's movement
        # Positive speed = moving forward (increasing longitude)
        # Negative speed = moving backward (decreasing longitude)
        
        # Calculate the current angular distance
        current_distance = angular_diff
        
        # Calculate what the distance would be if the faster body moved slightly
        # in the direction of its current movement
        movement_direction = 1 if faster_body.speed > 0 else -1
        small_movement = 0.1  # Small test movement
        
        # Simulate a small movement of the faster body
        new_faster_lon = (faster_body.longitude + movement_direction * small_movement) % 360
        new_distance = self._calculate_angular_difference(new_faster_lon, slower_body.longitude)
        
        # If the distance is decreasing, the aspect is applying
        # If the distance is increasing, the aspect is separating
        return new_distance < current_distance