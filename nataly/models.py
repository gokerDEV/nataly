# nataly/models.py
# Contains the core data classes for the astrology library.

from dataclasses import dataclass
from typing import Optional, Literal, List, Dict, Any
from .constants import SIGNS, ZODIAC_SIGN_DEGREES, ASTROLOGICAL_BODY_GROUPS



# --- Astrological Data Conversion Utilities ---

def parse_dms_to_decimal(dms_str: str) -> float:
    """
    Parses a Degrees-Minutes-Seconds string into decimal degrees.
    This function is designed to be robust and handle various DMS formats
    like "8°26'3\"", "27°8'57\"", or even just "35'46\"".

    Args:
        dms_str: The string representation of the degrees, minutes, and seconds.

    Returns:
        The value in decimal degrees as a float.
    """
    if not isinstance(dms_str, str):
        return 0.0
        
    dms_str = dms_str.strip()
    deg, mnt, sec = 0.0, 0.0, 0.0

    # Handles various DMS formats by replacing symbols and splitting.
    dms_str = dms_str.replace('°', 'd ').replace("'", "m ").replace('"', 's')
    parts = dms_str.split()

    for part in parts:
        try:
            if part.endswith('d'):
                deg = float(part[:-1])
            elif part.endswith('m'):
                mnt = float(part[:-1])
            elif part.endswith('s'):
                sec = float(part[:-1])
        except (ValueError, TypeError):
            continue # Skip parts that are not valid numbers

    return deg + mnt / 60.0 + sec / 3600.0

def parse_longitude_to_decimal(longitude_str: str, sign_name: Optional[str] = None) -> float:
    """
    Parses a longitude string (DMS) and an optional sign into absolute decimal degrees (0-360).
    This function combines DMS parsing with Zodiac sign offset calculation.

    Args:
        longitude_str: The DMS string (e.g., "8°26'3\"").
        sign_name: The name of the zodiac sign (e.g., "Pisces"). If provided, the result
                   will be the absolute longitude.

    Returns:
        The absolute longitude in decimal degrees.
    """
    decimal_in_sign = parse_dms_to_decimal(longitude_str)
    
    if sign_name and sign_name in ZODIAC_SIGN_DEGREES:
        sign_offset = ZODIAC_SIGN_DEGREES[sign_name]
        return (sign_offset + decimal_in_sign) % 360
    else:
        # If no sign is provided, return the decimal value as is.
        return decimal_in_sign

def decimal_to_dms_string(decimal: float, format_type: str = 'position') -> str:
    """
    Converts decimal degrees to a formatted DMS string (e.g., "8°26'03\"").
    
    Args:
        decimal: The decimal degree value.
        format_type: 'position' for zodiac longitude (uses modulo 30), 
                     'speed' or 'orb' for absolute values.

    Returns:
        A formatted DMS string.
    """
    if format_type == 'position':
        decimal = decimal % 30  # Position within a 30-degree sign
    
    decimal = abs(decimal)
    
    degrees = int(decimal)
    minutes_decimal = (decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = int((minutes_decimal - minutes) * 60)
    
    return f"{degrees}°{minutes:02d}'{seconds:02d}\""


@dataclass
class Sign:
    """Represents the static properties of a Zodiac sign."""
    name: str
    symbol: str
    element: str
    modality: str
    polarity: str
    classic_ruler: str
    modern_ruler: Optional[str] = None


def get_sign(sign_name: str) -> Optional[Sign]:
    """Create a Sign object from a sign name using the canonical SIGNS dict from constants.py."""
    data = SIGNS.get(sign_name)
    if data:
        return Sign(**data)
    return None

@dataclass
class Body:
    """Represents all calculated properties of a celestial body."""
    name: str
    body_type: Literal["Planet", "Asteroid", "Axis", "LunarNode", "Lilith", "Luminary"]
    longitude: float
    speed: float
    is_retrograde: bool
    sign: Sign
    house: int
    dignity: str = ""

    @property
    def dms(self) -> str:
        """Returns the longitude in Degrees°Minutes'Seconds" format within its sign."""
        return decimal_to_dms_string(self.longitude, 'position')

    @property
    def signed_dms(self) -> str:
        """Returns the longitude in DD°Sign'MM'SS" format."""
        # This implementation is now more robust.
        # It calculates the values directly instead of parsing the output of another property.
        decimal_in_sign = self.longitude % 30
        degrees = int(decimal_in_sign)
        minutes_decimal = (decimal_in_sign - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = int((minutes_decimal - minutes) * 60)
        return f"{degrees}{self.sign.symbol}{minutes:02d}'{seconds:02d}\""

@dataclass
class BodyFilter:
    """Filter configuration for celestial bodies."""
    include_planets: bool = True
    include_luminaries: bool = True
    include_asteroids: bool = True
    include_axes: bool = True
    include_lunar_nodes: bool = True
    include_lilith: bool = True
    include_bodies: Optional[List[str]] = None
    exclude_bodies: Optional[List[str]] = None
    include_signs: Optional[List[str]] = None
    exclude_signs: Optional[List[str]] = None
    include_elements: Optional[List[str]] = None
    exclude_elements: Optional[List[str]] = None
    include_modalities: Optional[List[str]] = None
    exclude_modalities: Optional[List[str]] = None
    include_houses: Optional[List[int]] = None
    exclude_houses: Optional[List[int]] = None
    include_dignities: Optional[List[str]] = None
    exclude_dignities: Optional[List[str]] = None
    include_retrograde: Optional[bool] = None
    
    def matches(self, body: Body) -> bool:
        if body.body_type == "Planet" and not self.include_planets: return False
        if body.body_type == "Luminary" and not self.include_luminaries: return False
        if body.body_type == "Asteroid" and not self.include_asteroids: return False
        if body.body_type == "Axis" and not self.include_axes: return False
        if body.body_type == "LunarNode" and not self.include_lunar_nodes: return False
        if body.body_type == "Lilith" and not self.include_lilith: return False
        if self.include_bodies and body.name not in self.include_bodies: return False
        if self.exclude_bodies and body.name in self.exclude_bodies: return False
        if self.include_signs and body.sign.name not in self.include_signs: return False
        if self.exclude_signs and body.sign.name in self.exclude_signs: return False
        if self.include_elements and body.sign.element not in self.include_elements: return False
        if self.exclude_elements and body.sign.element in self.exclude_elements: return False
        if self.include_modalities and body.sign.modality not in self.include_modalities: return False
        if self.exclude_modalities and body.sign.modality in self.exclude_modalities: return False
        if self.include_houses and body.house not in self.include_houses: return False
        if self.exclude_houses and body.house in self.exclude_houses: return False
        if self.include_dignities and body.dignity not in self.include_dignities: return False
        if self.exclude_dignities and body.dignity in self.exclude_dignities: return False
        if self.include_retrograde is not None and body.is_retrograde != self.include_retrograde: return False
        return True

@dataclass
class House:
    """Represents the properties of an astrological house."""
    id: int
    cusp_longitude: float
    sign: Sign
    classic_ruler: Optional[Body] = None
    modern_ruler: Optional[Body] = None
    classic_ruler_house: Optional[int] = None
    modern_ruler_house: Optional[int] = None

    @property
    def dms(self) -> str:
        """Returns the cusp longitude in Degrees°Minutes'Seconds" format within its sign."""
        return decimal_to_dms_string(self.cusp_longitude, 'position')

@dataclass
class Aspect:
    """Represents an aspectual relationship between two celestial bodies."""
    body1: Body
    body2: Body
    aspect_type: str
    symbol: str
    orb: float
    is_applying: bool

    @property
    def orb_str(self) -> str:
        """Returns the orb value in Degrees°Minutes'Seconds" format with sign."""
        sign = "-" if self.orb < 0 else ""
        return sign + decimal_to_dms_string(self.orb, 'orb')

@dataclass
class OrbConfig:
    """Configurable orb settings for different celestial body types using Astrodienst's 5x5 matrix system."""
    luminaries: dict      # Sun, Moon
    major_planets: dict   # Mercury, Venus, Mars, Jupiter, Saturn
    outer_planets: dict   # Uranus, Neptune, Pluto
    asteroids: dict       # Chiron, etc.
    cardinal_angles: dict # AC, MC
    derived_angles: dict  # IC, DC
    
    # Aspect categories with proper names
    aspect_categories = {
        'major_aspects': ['Conjunction', 'Opposition', 'Trine', 'Square'], 
        'sextile': ['Sextile'],                                             
        'semisextile': ['Semisextile'],                                        
        'minor_aspects': ['Sesquiquadrate', 'Semisquare', 'Quincunx'],   
        'quintile_aspects': ['Quintile', 'Biquintile']                
    }
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'OrbConfig':
        return cls(
            luminaries=config_dict.get('luminaries', {}),
            major_planets=config_dict.get('major_planets', {}),
            outer_planets=config_dict.get('outer_planets', {}),
            asteroids=config_dict.get('asteroids', {}),
            cardinal_angles=config_dict.get('cardinal_angles', {}),
            derived_angles=config_dict.get('derived_angles', {})
        )
    
    def to_dict(self) -> dict:
        return {
            'luminaries': self.luminaries,
            'major_planets': self.major_planets,
            'outer_planets': self.outer_planets,
            'asteroids': self.asteroids,
            'angles': self.cardinal_angles,
        }
