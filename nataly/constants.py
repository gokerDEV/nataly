# nataly/constants.py
# Contains static astrological data and rules for the library.

from .models import Sign, OrbConfig
import swisseph as swe
from typing import Literal

# --- TYPE DEFINITIONS ---
BODY_TYPES = Literal["Planet", "Asteroid", "Axis", "LunarNode", "Lilith", "Luminary"]

# --- ZODIAC SIGNS ---
SIGNS = {
    "Aries":       Sign(name="Aries",       symbol="♈", element="Fire",   modality="Cardinal", polarity="Positive", classic_ruler="Mars", modern_ruler="Mars"),
    "Taurus":      Sign(name="Taurus",      symbol="♉", element="Earth",  modality="Fixed",    polarity="Negative", classic_ruler="Venus", modern_ruler="Venus"),
    "Gemini":      Sign(name="Gemini",      symbol="♊", element="Air",    modality="Mutable",  polarity="Positive", classic_ruler="Mercury", modern_ruler="Mercury"),
    "Cancer":      Sign(name="Cancer",      symbol="♋", element="Water",  modality="Cardinal", polarity="Negative", classic_ruler="Moon", modern_ruler="Moon"),
    "Leo":         Sign(name="Leo",         symbol="♌", element="Fire",   modality="Fixed",    polarity="Positive", classic_ruler="Sun", modern_ruler="Sun"),
    "Virgo":       Sign(name="Virgo",       symbol="♍", element="Earth",  modality="Mutable",  polarity="Negative", classic_ruler="Mercury", modern_ruler="Mercury"),
    "Libra":       Sign(name="Libra",       symbol="♎", element="Air",    modality="Cardinal", polarity="Positive", classic_ruler="Venus", modern_ruler="Venus"),
    "Scorpio":     Sign(name="Scorpio",     symbol="♏", element="Water",  modality="Fixed",    polarity="Negative", classic_ruler="Mars", modern_ruler="Pluto"),
    "Sagittarius": Sign(name="Sagittarius", symbol="♐", element="Fire",   modality="Mutable",  polarity="Positive", classic_ruler="Jupiter", modern_ruler="Jupiter"),
    "Capricorn":   Sign(name="Capricorn",   symbol="♑", element="Earth",  modality="Cardinal", polarity="Negative", classic_ruler="Saturn", modern_ruler="Saturn"),
    "Aquarius":    Sign(name="Aquarius",    symbol="♒", element="Air",    modality="Fixed",    polarity="Positive", classic_ruler="Saturn", modern_ruler="Uranus"),
    "Pisces":      Sign(name="Pisces",      symbol="♓", element="Water",  modality="Mutable",  polarity="Negative", classic_ruler="Jupiter", modern_ruler="Neptune"),
}

# --- CELESTIAL BODY SYMBOLS ---

# LUMINARIES - Most important celestial bodies
LUMINARIES_SYMBOLS = {
    "Sun": "☉",          # U+2609 - Sun
    "Moon": "☽",         # U+263D - Moon
}

# MAJOR PLANETS - Classical and modern planets
MAJOR_PLANETS_SYMBOLS = {
    "Mercury": "☿",      # U+263F - Mercury
    "Venus": "♀",        # U+2640 - Venus
    "Mars": "♂",         # U+2642 - Mars
    "Jupiter": "♃",      # U+2643 - Jupiter
    "Saturn": "♄",       # U+2644 - Saturn
    "Uranus": "♅",       # U+2645 - Uranus
    "Neptune": "♆",      # U+2646 - Neptune
    "Pluto": "♇",        # U+2647 - Pluto
}

# ASTEROIDS - Minor planets
ASTEROIDS_SYMBOLS = {
    "Ceres": "⚳",        # U+26B3 - Ceres (1)
    "Pallas": "⚴",       # U+26B4 - Pallas (2)
    "Juno": "⚵",         # U+26B5 - Juno (3)
    "Vesta": "⚶",        # U+26B6 - Vesta (4)
    "Chiron": "⚷",       # U+26B7 - Chiron (2060)

}

# LUNAR NODES - Moon's orbital nodes
LUNAR_NODES_SYMBOLS = {
    "True Node": "☊",    # U+260A - North Node (True)
    "South Node": "☋",   # U+260B - South Node
    "Mean Node": "☊",    # U+260A - North Node (Mean)
}

# LILITH - Black Moon
LILITH_SYMBOLS = {
    "Lilith": "⚸",       # U+26B8 - Black Moon Lilith
    "Black Moon": "⚸",   # U+26B8 - Black Moon (alternative name)
}

# ANGLES - Birth chart angles
ANGLES_SYMBOLS = {
    "AC": "AC",          # Ascendant
    "MC": "MC",          # Midheaven
    "IC": "IC",          # Imum Coeli
    "DC": "DC",          # Descendant
}

# --- BODY TYPE MAPPINGS ---
BODY_TYPE_MAPPINGS = {
    # Luminaries
    **{name: "Luminary" for name in LUMINARIES_SYMBOLS.keys()},
    # Major Planets
    **{name: "Planet" for name in MAJOR_PLANETS_SYMBOLS.keys()},
    # Asteroids
    **{name: "Asteroid" for name in ASTEROIDS_SYMBOLS.keys()},
    # Lunar Nodes
    **{name: "LunarNode" for name in LUNAR_NODES_SYMBOLS.keys()},
    # Lilith
    **{name: "Lilith" for name in LILITH_SYMBOLS.keys()},
    # Angles
    **{name: "Axis" for name in ANGLES_SYMBOLS.keys()},
}

# --- VALID BODY TYPES ---
VALID_BODY_TYPES = list(set(BODY_TYPE_MAPPINGS.values()))

# --- COMPLETE SYMBOL LIST ---
BODY_SYMBOLS = {
    # Luminaries
    **LUMINARIES_SYMBOLS,
    # Major Planets
    **MAJOR_PLANETS_SYMBOLS,
    # Asteroids
    **ASTEROIDS_SYMBOLS,
    # Lunar Nodes
    **LUNAR_NODES_SYMBOLS,
    # Lilith
    **LILITH_SYMBOLS,
    # Angles
    **ANGLES_SYMBOLS,
}

# --- CATEGORIZED NAME LISTS ---

# LUMINARIES
LUMINARIES = list(LUMINARIES_SYMBOLS.keys())

# MAJOR PLANETS
MAJOR_PLANETS = list(MAJOR_PLANETS_SYMBOLS.keys())

# ASTEROIDS
ASTEROIDS = list(ASTEROIDS_SYMBOLS.keys())

# LUNAR NODES
LUNAR_NODES = list(LUNAR_NODES_SYMBOLS.keys())

# LILITH
LILITH_BODIES = list(LILITH_SYMBOLS.keys())

# ANGLES
ANGLES = list(ANGLES_SYMBOLS.keys())

# ALL PLANETS (Luminaries + Major Planets)
PLANETS = LUMINARIES + MAJOR_PLANETS

# ALL CELESTIAL BODIES (Planets + Asteroids + Lunar Nodes + Lilith)
ALL_BODIES = PLANETS + ASTEROIDS + LUNAR_NODES + LILITH_BODIES

# ALL CELESTIAL BODIES + ANGLES
ALL_BODY_NAMES = ALL_BODIES + ANGLES

# --- BACKWARD COMPATIBILITY ---
# Legacy code compatibility
PLANET_SYMBOLS = {**LUMINARIES_SYMBOLS, **MAJOR_PLANETS_SYMBOLS, **ASTEROIDS_SYMBOLS, **LUNAR_NODES_SYMBOLS}
PLANET_NAMES = list(PLANET_SYMBOLS.keys())
AXES_NAMES = ANGLES

SIGN_NAMES_BY_DEGREE = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# --- DIGNITY RULES ---
DIGNITY_RULES = {
    "domicile": {
        "Sun": "Leo", "Moon": "Cancer", "Mercury": ["Gemini", "Virgo"], "Venus": ["Taurus", "Libra"],
        "Mars": "Aries", "Jupiter": "Sagittarius", "Saturn": "Capricorn",
        "Uranus": "Aquarius", "Neptune": "Pisces", "Pluto": "Scorpio"
    },
    "exaltation": {
        "Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo", "Venus": "Pisces",
        "Mars": "Capricorn", "Jupiter": "Cancer", "Saturn": "Libra",
        "Uranus": "Scorpio", "Neptune": "Leo", "Pluto": "Aries"
    },
    "detriment": {
        "Sun": "Aquarius", "Moon": "Capricorn", "Mercury": ["Sagittarius", "Pisces"],
        "Venus": ["Scorpio", "Aries"], "Mars": "Libra", "Jupiter": "Gemini", "Saturn": "Cancer",
        "Uranus": "Leo", "Neptune": "Virgo", "Pluto": "Taurus"
    },
    "fall": {
        "Sun": "Libra", "Moon": "Scorpio", "Mercury": "Pisces", "Venus": "Virgo",
        "Mars": "Cancer", "Jupiter": "Capricorn", "Saturn": "Aries",
        "Uranus": "Taurus", "Neptune": "Aquarius", "Pluto": "Virgo"
    }
}

# --- COMPLETE ASPECT DATA ---
ASPECT_DATA = {
    "Conjunction":    {"angle": 0,    "symbol": "☌"}, 
    "Opposition":     {"angle": 180,  "symbol": "☍"},
    "Trine":          {"angle": 120,  "symbol": "△"}, 
    "Square":         {"angle": 90,   "symbol": "□"},
    "Sextile":        {"angle": 60,   "symbol": "⚹"}, 
    "Quincunx":       {"angle": 150,  "symbol": "⚺"},
    "Sesquiquadrate": {"angle": 135,  "symbol": "⚼"}, 
    "Semisquare":     {"angle": 45,   "symbol": "∠"},
    "Semisextile":    {"angle": 30,   "symbol": "⚻"}, 
    "Quintile":       {"angle": 72,   "symbol": "Q"},
    "Biquintile":     {"angle": 144,  "symbol": "bQ"},
}

MAJOR_ASPECTS = ["Conjunction", "Opposition", "Square", "Trine"]

MODALITIES = ["Cardinal", "Fixed", "Mutable"]
ELEMENTS = ["Fire", "Earth", "Air", "Water"]
POLARITIES = ["Positive", "Negative"]

# --- SWISS EPHEMERIS MAPPING ---
# Based on Swiss Ephemeris documentation: https://www.astro.com/swisseph/swephprg.htm#_Toc112597363
PLANET_MAPPING_SWE = {
    # Luminaries
    "Sun": swe.SUN,              # SE_SUN = 0
    "Moon": swe.MOON,            # SE_MOON = 1
    
    # Major Planets
    "Mercury": swe.MERCURY,      # SE_MERCURY = 2
    "Venus": swe.VENUS,          # SE_VENUS = 3
    "Mars": swe.MARS,            # SE_MARS = 4
    "Jupiter": swe.JUPITER,      # SE_JUPITER = 5
    "Saturn": swe.SATURN,        # SE_SATURN = 6
    "Uranus": swe.URANUS,        # SE_URANUS = 7
    "Neptune": swe.NEPTUNE,      # SE_NEPTUNE = 8
    "Pluto": swe.PLUTO,          # SE_PLUTO = 9
    
    # Asteroids
    "Ceres": 17, # swe.CERES
    "Pallas": 18, # swe.PALLAS
    "Juno": 19, # swe.JUNO
    "Vesta": 20, # swe.VESTA
    "Chiron": 15, # swe.CHIRON
    # "Ceres": swe.CERES,          # SE_CERES = 10
    # "Pallas": swe.PALLAS,        # SE_PALLAS = 11
    # "Juno": swe.JUNO,            # SE_JUNO = 12
    # "Vesta": swe.VESTA,          # SE_VESTA = 13
    # "Chiron": swe.CHIRON,        # SE_CHIRON = 15
    "Pholus": swe.PHOLUS,        # SE_PHOLUS = 16
    
    
    # Lunar Nodes
    "True Node": swe.TRUE_NODE,  # SE_TRUE_NODE = 11 (True Node)
    "Mean Node": swe.MEAN_NODE,  # SE_MEAN_NODE = 10
    
    # Note: Eris is not available in standard Swiss Ephemeris
    # Note: South Node is calculated as True Node + 180°
    # Note: Lilith/Black Moon are calculated separately (not in Swiss Ephemeris)
    # Note: Angles (AC, MC, IC, DC) are calculated separately
    
    # Angles (calculated separately, not from Swiss Ephemeris)
    "AC": swe.ASC,               # Ascendant
    "MC": swe.MC,                # Midheaven
    "IC": None,                  # Imum Coeli (calculated as MC + 180°)
    "DC": None,                  # Descendant (calculated as AC + 180°)
    
    # Additional bodies available in Swiss Ephemeris (optional)
    "Earth": swe.EARTH,          # SE_EARTH = 14
    "Mean Apogee": swe.MEAN_APOG, # SE_MEAN_APOG = 12
    "Osculating Apogee": swe.OSCU_APOG, # SE_OSCU_APOG = 13
    "Interpolated Apogee": swe.INTP_APOG, # SE_INTP_APOG = 21
    "Interpolated Perigee": swe.INTP_PERG, # SE_INTP_PERG = 22
}

# --- ORB CONFIGURATIONS ---
ORB_CONFIGS = {
    'Placidus': {
        'luminaries': {
            'Conjunction': 10.0, 'Opposition': 10.0, 'Trine': 8.0, 'Square': 8.0,
            'Sextile': 6.0, 'Quincunx': 3.0, 'Sesquiquadrate': 3.0, 'Semisquare': 2.0,
            'Semisextile': 2.0, 'Quintile': 2.0, 'Biquintile': 2.0
        },
        'angles': {
            'Conjunction': 1.0, 'Opposition': 1.0, 'Trine': 1.0, 'Square': 1.0,
            'Sextile': 1.0, 'Quincunx': 1.0, 'Sesquiquadrate': 1.0, 'Semisquare': 1.0,
            'Semisextile': 1.0, 'Quintile': 1.0, 'Biquintile': 1.0
        },
        'planets': {
            'Conjunction': 8.0, 'Opposition': 8.0, 'Trine': 6.0, 'Square': 6.0,
            'Sextile': 4.0, 'Quincunx': 2.0, 'Sesquiquadrate': 2.0, 'Semisquare': 1.5,
            'Semisextile': 1.5, 'Quintile': 1.5, 'Biquintile': 1.5
        }
    },
    'Koch': {
        'luminaries': {
            'Conjunction': 10.0, 'Opposition': 10.0, 'Trine': 8.0, 'Square': 8.0,
            'Sextile': 6.0, 'Quincunx': 3.0, 'Sesquiquadrate': 3.0, 'Semisquare': 2.0,
            'Semisextile': 2.0, 'Quintile': 2.0, 'Biquintile': 2.0
        },
        'angles': {
            'Conjunction': 1.0, 'Opposition': 1.0, 'Trine': 1.0, 'Square': 1.0,
            'Sextile': 1.0, 'Quincunx': 1.0, 'Sesquiquadrate': 1.0, 'Semisquare': 1.0,
            'Semisextile': 1.0, 'Quintile': 1.0, 'Biquintile': 1.0
        },
        'planets': {
            'Conjunction': 8.0, 'Opposition': 8.0, 'Trine': 6.0, 'Square': 6.0,
            'Sextile': 4.0, 'Quincunx': 2.0, 'Sesquiquadrate': 2.0, 'Semisquare': 1.5,
            'Semisextile': 1.5, 'Quintile': 1.5, 'Biquintile': 1.5
        }
    }
}

# --- CONFIGURATION FUNCTIONS ---
def create_orb_config(system: str = 'Placidus', custom_orbs: dict = None) -> OrbConfig:
    """Create an OrbConfig object with specified system or custom orbs."""
    if custom_orbs:
        return OrbConfig.from_dict(custom_orbs)
    
    if system not in ORB_CONFIGS:
        system = 'Placidus'  # Default fallback
    
    return OrbConfig.from_dict(ORB_CONFIGS[system])

def set_default_orb_config(config: OrbConfig):
    """Set the default orb configuration globally."""
    global DEFAULT_ORB_CONFIG
    DEFAULT_ORB_CONFIG = config

# Initialize default orb config
DEFAULT_ORB_CONFIG = create_orb_config('Placidus') 

# # ZODIAC SIGN DEGREE OFFSETS
# ZODIAC_SIGN_DEGREES = {
#     "Aries": 0,
#     "Taurus": 30,
#     "Gemini": 60,
#     "Cancer": 90,
#     "Leo": 120,
#     "Virgo": 150,
#     "Libra": 180,
#     "Scorpio": 210,
#     "Sagittarius": 240,
#     "Capricorn": 270,
#     "Aquarius": 300,
#     "Pisces": 330,
# } 