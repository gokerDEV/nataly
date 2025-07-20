# nataly/models.py
# Contains the core data classes for the astrology library.

from dataclasses import dataclass
from typing import Optional, Literal, List, Dict, Any

@dataclass
class Sign:
    """Represents the static properties of a Zodiac sign."""
    name: str
    symbol: str
    element: str
    modality: str
    polarity: str
    classic_ruler: str  # Traditional ruling planet name
    modern_ruler: Optional[str] = None  # Modern ruling planet name

@dataclass
class Body:
    """Represents all calculated properties of a celestial body (planet, asteroid, axis, etc.)."""
    name: str
    body_type: Literal["Planet", "Asteroid", "Axis", "LunarNode", "Lilith", "Luminary"]
    longitude: float
    speed: float
    is_retrograde: bool
    sign: Sign
    house: int
    dignity: str = "" # e.g., "domicile", "detriment"

    @property
    def dms(self) -> str:
        """Returns the longitude in Degrees°Minutes' format within its sign."""
        deg_in_sign = self.longitude % 30
        deg = int(deg_in_sign)
        minute = int((deg_in_sign - deg) * 60)
        return f"{deg:02d}°{minute:02d}'"

    @property
    def signed_dms(self) -> str:
        """Returns the longitude in DD°Sign'MM' format."""
        return f"{self.dms} {self.sign.symbol}"

# Type aliases for better readability
Planet = Body
Asteroid = Body
Axis = Body
LunarNode = Body
Lilith = Body
Luminary = Body

@dataclass
class BodyFilter:
    """Filter configuration for celestial bodies."""
    # Body type filters
    include_planets: bool = True
    include_luminaries: bool = True
    include_asteroids: bool = True
    include_axes: bool = True
    include_lunar_nodes: bool = True
    include_lilith: bool = True
    
    # Specific body filters
    include_bodies: Optional[List[str]] = None  # Specific body names to include
    exclude_bodies: Optional[List[str]] = None  # Specific body names to exclude
    
    # Sign filters
    include_signs: Optional[List[str]] = None  # Specific signs to include
    exclude_signs: Optional[List[str]] = None  # Specific signs to exclude
    
    # Element filters
    include_elements: Optional[List[str]] = None  # Specific elements to include
    exclude_elements: Optional[List[str]] = None  # Specific elements to exclude
    
    # Modality filters
    include_modalities: Optional[List[str]] = None  # Specific modalities to include
    exclude_modalities: Optional[List[str]] = None  # Specific modalities to exclude
    
    # House filters
    include_houses: Optional[List[int]] = None  # Specific houses to include
    exclude_houses: Optional[List[int]] = None  # Specific houses to exclude
    
    # Dignity filters
    include_dignities: Optional[List[str]] = None  # Specific dignities to include
    exclude_dignities: Optional[List[str]] = None  # Specific dignities to exclude
    
    # Retrograde filter
    include_retrograde: Optional[bool] = None  # True/False/None (all)
    
    def matches(self, body: Body) -> bool:
        """Check if a body matches the filter criteria."""
        # Body type filters
        if body.body_type == "Planet" and not self.include_planets:
            return False
        if body.body_type == "Luminary" and not self.include_luminaries:
            return False
        if body.body_type == "Asteroid" and not self.include_asteroids:
            return False
        if body.body_type == "Axis" and not self.include_axes:
            return False
        if body.body_type == "LunarNode" and not self.include_lunar_nodes:
            return False
        if body.body_type == "Lilith" and not self.include_lilith:
            return False
        
        # Specific body filters
        if self.include_bodies and body.name not in self.include_bodies:
            return False
        if self.exclude_bodies and body.name in self.exclude_bodies:
            return False
        
        # Sign filters
        if self.include_signs and body.sign.name not in self.include_signs:
            return False
        if self.exclude_signs and body.sign.name in self.exclude_signs:
            return False
        
        # Element filters
        if self.include_elements and body.sign.element not in self.include_elements:
            return False
        if self.exclude_elements and body.sign.element in self.exclude_elements:
            return False
        
        # Modality filters
        if self.include_modalities and body.sign.modality not in self.include_modalities:
            return False
        if self.exclude_modalities and body.sign.modality in self.exclude_modalities:
            return False
        
        # House filters
        if self.include_houses and body.house not in self.include_houses:
            return False
        if self.exclude_houses and body.house in self.exclude_houses:
            return False
        
        # Dignity filters
        if self.include_dignities and body.dignity not in self.include_dignities:
            return False
        if self.exclude_dignities and body.dignity in self.exclude_dignities:
            return False
        
        # Retrograde filter
        if self.include_retrograde is not None and body.is_retrograde != self.include_retrograde:
            return False
        
        return True

@dataclass
class House:
    """Represents the properties of an astrological house."""
    id: int
    cusp_longitude: float
    sign: Sign
    classic_ruler: Optional[Body] = None # The Body object that classically rules this house
    modern_ruler: Optional[Body] = None # The Body object that modernly rules this house
    classic_ruler_house: Optional[int] = None # The house where the classic ruler is located
    modern_ruler_house: Optional[int] = None # The house where the modern ruler is located

    @property
    def dms(self) -> str:
        """Returns the cusp longitude in Degrees°Minutes' format within its sign."""
        deg_in_sign = self.cusp_longitude % 30
        deg = int(deg_in_sign)
        minute = int((deg_in_sign - deg) * 60)
        return f"{deg:02d}°{minute:02d}'"

@dataclass
class Aspect:
    """Represents an aspectual relationship between two celestial bodies."""
    body1: Body
    body2: Body
    aspect_type: str  # e.g., "Trine", "Square"
    symbol: str
    orb: float
    is_applying: bool

    @property
    def orb_str(self) -> str:
        """Returns the orb value in Degrees°Minutes' format."""
        orb_abs = abs(self.orb)
        deg = int(orb_abs)
        minute = int((orb_abs - deg) * 60)
        return f"{deg}°{minute:02d}'"

@dataclass
class OrbConfig:
    """Configurable orb settings for different celestial body types."""
    luminaries: dict
    angles: dict
    planets: dict
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'OrbConfig':
        """Create OrbConfig from dictionary."""
        return cls(
            luminaries=config_dict.get('luminaries', {}),
            angles=config_dict.get('angles', {}),
            planets=config_dict.get('planets', {})
        )
    
    def to_dict(self) -> dict:
        """Convert OrbConfig to dictionary."""
        return {
            'luminaries': self.luminaries,
            'angles': self.angles,
            'planets': self.planets
        } 