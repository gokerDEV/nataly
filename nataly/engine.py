# nataly/engine.py
# The core astrological calculation engine.

import swisseph as swe
import os
from typing import List, Dict

from .models import Body, House, Aspect, get_sign
from .constants import (
    SIGN_NAMES_BY_DEGREE, DIGNITY_RULES, ASPECT_DATA,
    ALL_BODY_NAMES, ANGLES_SYMBOLS, ASTROLOGICAL_BODY_GROUPS,
    PLANET_MAPPING_SWE,
    BODY_TYPE_MAPPINGS, ORB_BODY_GROUPS, ORB_ASPECT_GROUPS
)
from .config import create_orb_config

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
        self.orb_config = orb_config
        self.ephe_path = ephe_path
        swe.set_ephe_path(self.ephe_path)
        
        
        self.chart_angles = list(ASTROLOGICAL_BODY_GROUPS["chart_angles"])

    def _get_sign_from_longitude(self, longitude: float):
        """Get zodiac sign from longitude as a Sign object using get_sign."""
        sign_index = int(longitude / 30)
        sign_name = SIGN_NAMES_BY_DEGREE[sign_index]
        return get_sign(sign_name)

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
        # Use canonical orb config keys from ORB_BODY_GROUPS and ORB_CONFIGS
        # Determine which group each body belongs to
        def get_orb_group(name):
            for group_key, group_list in ORB_BODY_GROUPS.items():
                if name in group_list:
                    return group_key
            return None
        group1 = get_orb_group(p1_name)
        group2 = get_orb_group(p2_name)
        # Prefer the more restrictive group (if one is 'other', use the more specific)
        group = group1 or group2 or 'orb_other_bodies'
        # Fallback to orb_other_bodies if not found
        if group1 and group2:
            # If one is orb_other_bodies, prefer the other
            if group1 == 'orb_other_bodies':
                group = group2
            elif group2 == 'orb_other_bodies':
                group = group1
            else:
                group = group1  # default to group1
        # Map aspect to orb type
        if aspect_name in ORB_ASPECT_GROUPS['major']:
            orb_type = 'major'
        elif aspect_name in ORB_ASPECT_GROUPS['sextile']:
            orb_type = 'sextile'
        elif aspect_name in ORB_ASPECT_GROUPS['adjustment']:
            orb_type = 'adjustment'
        elif aspect_name in ORB_ASPECT_GROUPS['tension']:
            orb_type = 'tension'
        elif aspect_name in ORB_ASPECT_GROUPS['creative']:
            orb_type = 'creative'
        else:
            orb_type = 'major'  # fallback
        config = self.orb_config.get(group, {})
        return config.get(orb_type, 0)

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

            if name in self.chart_angles:
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
                is_retrograde=speed < 0 and name not in self.chart_angles,
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
        Calculates aspects using proper astrological orb limits and applying/separating logic.
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
                
                # Find all aspects within proper orb limits
                valid_aspects = []
                for aspect_name, aspect_data in ASPECT_DATA.items():
                    orb_diff = angular_diff - aspect_data["angle"]
                    orb_limit = self._get_categorized_orb(aspect_name, body1.name, body2.name)
                    
                    # Check if aspect is within orb limit
                    if abs(orb_diff) <= orb_limit:
                        valid_aspects.append((aspect_name, aspect_data, orb_diff))
                
                # Apply aspect conflict prevention
                best_aspect = self._resolve_aspect_conflicts(valid_aspects, body1, body2)
                
                if best_aspect:
                    aspect_name, aspect_data, orb_diff = best_aspect
                    
                    # Use orb_diff directly without applying/separating logic
                    # The sign of orb_diff indicates the direction from exact aspect
                    actual_orb = orb_diff
                    
                    # Determine applying/separating based on orb sign
                    # Positive orb_diff means we're past the exact aspect (separating)
                    # Negative orb_diff means we're before the exact aspect (applying)
                    is_applying = orb_diff < 0
                    
                    aspects.append(Aspect(
                        body1=body1,
                        body2=body2,
                        aspect_type=aspect_name,
                        symbol=aspect_data["symbol"],
                        orb=actual_orb,
                        is_applying=is_applying
                    ))
        return aspects

    def _resolve_aspect_conflicts(self, valid_aspects: List[tuple], body1: Body, body2: Body) -> tuple:
        """
        Resolve aspect conflicts using Astrodienst logic.
        Prevents weak aspects when stronger ones are present.
        """
        if not valid_aspects:
            return None
        
        # Sort by aspect strength (major aspects first)
        aspect_strength = {
            "Conjunction": 1, "Opposition": 2, "Trine": 3, "Square": 4, "Sextile": 5,
            "Quincunx": 6, "Semisquare": 7, "Sesquiquadrate": 8, "Semisextile": 9,
            "Quintile": 10, "Biquintile": 11
        }
        
        # Group aspects by strength
        aspect_groups = {}
        for aspect_name, aspect_data, orb_diff in valid_aspects:
            strength = aspect_strength.get(aspect_name, 99)
            if strength not in aspect_groups:
                aspect_groups[strength] = []
            aspect_groups[strength].append((aspect_name, aspect_data, orb_diff))
        
        # Check for conflicts and return the strongest aspect
        for strength in sorted(aspect_strength.values()):
            if strength in aspect_groups:
                aspects_in_group = aspect_groups[strength]
                
                # If multiple aspects in same strength group, choose the one with smallest orb
                if len(aspects_in_group) > 1:
                    aspects_in_group.sort(key=lambda x: abs(x[2]))
                
                # Check if this aspect conflicts with stronger aspects
                aspect_name = aspects_in_group[0][0]
                if not self._has_aspect_conflict(aspect_name, aspect_groups, strength):
                    return aspects_in_group[0]
        
        return None

    def _has_aspect_conflict(self, aspect_name: str, aspect_groups: dict, current_strength: int) -> bool:
        """
        Check if an aspect conflicts with stronger aspects.
        Only prevents very weak aspects when major ones exist.
        """
        # Define aspect conflicts (only prevent very weak aspects when major ones exist)
        conflicts = {
            "Semisextile": ["Conjunction", "Opposition", "Trine", "Square", "Sextile"],
            "Quincunx": ["Conjunction", "Opposition", "Trine", "Square", "Sextile"],
            "Quintile": ["Conjunction", "Opposition", "Trine", "Square", "Sextile"],
            "Biquintile": ["Conjunction", "Opposition", "Trine", "Square", "Sextile"]
        }
        
        if aspect_name not in conflicts:
            return False
        
        # Check if any conflicting stronger aspect exists
        for conflict_aspect in conflicts[aspect_name]:
            conflict_strength = {
                "Conjunction": 1, "Opposition": 2, "Trine": 3, "Square": 4, "Sextile": 5,
                "Quincunx": 6, "Semisquare": 7, "Sesquiquadrate": 8, "Semisextile": 9,
                "Quintile": 10, "Biquintile": 11
            }.get(conflict_aspect, 99)
            
            if conflict_strength < current_strength and conflict_strength in aspect_groups:
                return True
        
        return False