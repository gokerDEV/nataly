# nataly/chart.py
# High-level class to manage all data and analyses for a single astrological chart.

import datetime
from collections import defaultdict
from typing import List, Dict, Optional, Union, Any

from .engine import AstroEngine
from .constants import (
    PLANET_NAMES, AXES_NAMES, MODALITIES, ELEMENTS, POLARITIES, 
    create_orb_config, ALL_BODY_NAMES, BODY_TYPE_MAPPINGS, VALID_BODY_TYPES, BODY_TYPES
)
from .models import Body, House, Aspect, BodyFilter

class NatalChart:
    """
    A high-level interface class that manages all astrological data and
    analyses for a single birth chart.
    """
    
    def __init__(self, person_name: str, dt_utc: datetime.datetime, lat: float, lon: float, orb_config=None, ephe_path: str = './nataly/ephe'):
        """
        Creates a NatalChart object and performs all essential calculations.
        
        Args:
            person_name: Name of the person
            dt_utc: Birth date and time in UTC
            lat: Latitude of birth location
            lon: Longitude of birth location
            orb_config: OrbConfig object or dict for orb settings
            ephe_path: Path to ephemeris files
        """
        self.name = person_name
        self.datetime_utc = dt_utc
        self.latitude = lat
        self.longitude = lon

        engine = AstroEngine(orb_config, ephe_path)
        self.bodies_dict, self.houses = engine.get_planets_and_houses(dt_utc, lat, lon)
        # Calculate aspects between all celestial bodies
        self.aspects = engine.get_aspects(self.bodies_dict)

        self.planets = [b for b in self.bodies_dict.values() if b.name in PLANET_NAMES]
        self.axes = {b.name: b for b in self.bodies_dict.values() if b.name in AXES_NAMES}
        self.ascendant = self.axes.get("AC")
        self.midheaven = self.axes.get("MC")

        self._calculate_distributions()
        # Calculate element-modality matrix
        self._calculate_element_modality_matrix()

    def _calculate_distributions(self):
        """Calculates distributions for elements, modalities, polarities, quadrants, and hemispheres."""
        bodies_for_distribution = self.planets + ([self.ascendant] if self.ascendant else [])
        self.element_distribution = defaultdict(lambda: {'count': 0, 'bodies': []})
        self.modality_distribution = defaultdict(lambda: {'count': 0, 'bodies': []})
        self.polarity_distribution = defaultdict(lambda: {'count': 0, 'bodies': []})
        self.quadrant_distribution = defaultdict(lambda: {'count': 0, 'bodies': []})
        self.hemisphere_distribution = defaultdict(lambda: {'count': 0, 'bodies': []})

        for body in bodies_for_distribution:
            if body and body.sign:
                self.element_distribution[body.sign.element]['bodies'].append(body)
                self.modality_distribution[body.sign.modality]['bodies'].append(body)
                self.polarity_distribution[body.sign.polarity]['bodies'].append(body)
            if body.name not in AXES_NAMES:
                if 1 <= body.house <= 3: self.quadrant_distribution['1st ◵']['bodies'].append(body)
                elif 4 <= body.house <= 6: self.quadrant_distribution['2nd ◶']['bodies'].append(body)
                elif 7 <= body.house <= 9: self.quadrant_distribution['3rd ◷']['bodies'].append(body)
                elif 10 <= body.house <= 12: self.quadrant_distribution['4th ◴']['bodies'].append(body)
                if body.house in [1, 2, 3, 10, 11, 12]: self.hemisphere_distribution['East ←']['bodies'].append(body)
                else: self.hemisphere_distribution['West →']['bodies'].append(body)
                if 1 <= body.house <= 6: self.hemisphere_distribution['North ↓']['bodies'].append(body)
                else: self.hemisphere_distribution['South ↑']['bodies'].append(body)
        
        for dist in [self.element_distribution, self.modality_distribution, self.polarity_distribution, self.quadrant_distribution, self.hemisphere_distribution]:
            for key in dist:
                dist[key]['count'] = len(dist[key]['bodies'])

    def _calculate_element_modality_matrix(self):
        """Calculates the 2D distribution of planets by element and modality."""
        self.element_modality_matrix = {
            el: {mod: {'count': 0, 'bodies': []} for mod in MODALITIES}
            for el in ELEMENTS
        }
        # Use only 10 major planets for matrix (astrological standard)
        planets_for_matrix = [b for b in self.planets if b.name in PLANET_NAMES]
        
        for body in planets_for_matrix:
            if body and body.sign:
                element = body.sign.element
                modality = body.sign.modality
                if element in self.element_modality_matrix and modality in self.element_modality_matrix[element]:
                    self.element_modality_matrix[element][modality]['bodies'].append(body)
                    self.element_modality_matrix[element][modality]['count'] += 1

    def get_body_by_name(self, name: str) -> Optional[Body]:
        """Returns a celestial body or axis object by its name from the central dictionary."""
        return self.bodies_dict.get(name)

    def get_bodies_by_type(self, body_type: BODY_TYPES) -> List[Body]:
        """
        Returns all celestial bodies of a specific type.
        
        Args:
            body_type: One of the valid body types from BODY_TYPE_MAPPINGS
            
        Returns:
            List of Body objects of the specified type
        """
        # Validate body_type against VALID_BODY_TYPES
        if body_type not in VALID_BODY_TYPES:
            raise ValueError(f"Invalid body_type: {body_type}. Valid types are: {VALID_BODY_TYPES}")
        
        return [b for b in self.bodies_dict.values() if b.body_type == body_type]

    def get_planets(self, include_luminaries: bool = True) -> List[Body]:
        """
        Returns planets with optional luminary filtering.
        
        Args:
            include_luminaries: If True, includes luminaries (Sun, Moon). If False, excludes them.
        
        Returns:
            List of Body objects (planets + optionally luminaries)
        """
        if include_luminaries:
            return [b for b in self.bodies_dict.values() if b.body_type in ["Planet", "Luminary"]]
        else:
            return [b for b in self.bodies_dict.values() if b.body_type == "Planet"]

    def get_luminaries(self) -> List[Body]:
        """Returns all luminaries (Sun and Moon)."""
        return [b for b in self.bodies_dict.values() if b.body_type == "Luminary"]

    def get_asteroids(self) -> List[Body]:
        """Returns all asteroids."""
        return [b for b in self.bodies_dict.values() if b.body_type == "Asteroid"]

    def get_axes(self) -> List[Body]:
        """Returns all chart axes."""
        return [b for b in self.bodies_dict.values() if b.body_type == "Axis"]

    def get_lunar_nodes(self) -> List[Body]:
        """Returns all lunar nodes."""
        return [b for b in self.bodies_dict.values() if b.body_type == "LunarNode"]

    def get_lilith_bodies(self) -> List[Body]:
        """Returns all Lilith bodies."""
        return [b for b in self.bodies_dict.values() if b.body_type == "Lilith"]

    def get_bodies(self, filter_config: Optional[Union[BodyFilter, Dict[str, Any]]] = None) -> List[Body]:
        """
        Returns all celestial bodies with optional filtering.
        
        Args:
            filter_config: BodyFilter object or dict with filter parameters
            
        Returns:
            List of Body objects matching the filter criteria
        """
        if filter_config is None:
            return list(self.bodies_dict.values())
        
        # Convert dict to BodyFilter if needed
        if isinstance(filter_config, dict):
            filter_config = BodyFilter(**filter_config)
        
        return [b for b in self.bodies_dict.values() if filter_config.matches(b)]

    def get_bodies_by_names(self, names: List[str]) -> List[Body]:
        """Returns celestial bodies by their names."""
        return [b for b in self.bodies_dict.values() if b.name in names]

    def get_bodies_by_signs(self, signs: List[str]) -> List[Body]:
        """Returns celestial bodies in specific signs."""
        return [b for b in self.bodies_dict.values() if b.sign.name in signs]

    def get_bodies_by_elements(self, elements: List[str]) -> List[Body]:
        """Returns celestial bodies in specific elements."""
        return [b for b in self.bodies_dict.values() if b.sign.element in elements]

    def get_bodies_by_modalities(self, modalities: List[str]) -> List[Body]:
        """Returns celestial bodies in specific modalities."""
        return [b for b in self.bodies_dict.values() if b.sign.modality in modalities]

    def get_bodies_by_houses(self, houses: List[int]) -> List[Body]:
        """Returns celestial bodies in specific houses."""
        return [b for b in self.bodies_dict.values() if b.house in houses]

    def get_bodies_by_dignities(self, dignities: List[str]) -> List[Body]:
        """Returns celestial bodies with specific dignities."""
        return [b for b in self.bodies_dict.values() if b.dignity in dignities]

    def get_retrograde_bodies(self) -> List[Body]:
        """Returns all retrograde celestial bodies."""
        return [b for b in self.bodies_dict.values() if b.is_retrograde]

    def get_direct_bodies(self) -> List[Body]:
        """Returns all direct (non-retrograde) celestial bodies."""
        return [b for b in self.bodies_dict.values() if not b.is_retrograde]

    def get_bodies_in_house(self, house_number: int) -> List[Body]:
        """Returns all celestial bodies in a specific house."""
        return [b for b in self.bodies_dict.values() if b.house == house_number]

    def get_bodies_in_sign(self, sign_name: str) -> List[Body]:
        """Returns all celestial bodies in a specific sign."""
        return [b for b in self.bodies_dict.values() if b.sign.name == sign_name]

    def get_bodies_in_element(self, element: str) -> List[Body]:
        """Returns all celestial bodies in a specific element."""
        return [b for b in self.bodies_dict.values() if b.sign.element == element]

    def get_bodies_in_modality(self, modality: str) -> List[Body]:
        """Returns all celestial bodies in a specific modality."""
        return [b for b in self.bodies_dict.values() if b.sign.modality == modality]

    def get_bodies_with_dignity(self, dignity: str) -> List[Body]:
        """Returns all celestial bodies with a specific dignity."""
        return [b for b in self.bodies_dict.values() if b.dignity == dignity]

    def __repr__(self):
        """String representation of the NatalChart."""
        return f"NatalChart(name='{self.name}', datetime_utc={self.datetime_utc}, lat={self.latitude}, lon={self.longitude})" 