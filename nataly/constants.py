# nataly/constants.py
# Contains static astrological data and rules for the library.

import swisseph as swe
from typing import Literal

# =====================
# ZODIAC SIGNS
# =====================
SIGNS = {
    "Aries":       {"name": "Aries",       "symbol": "♈", "element": "Fire",   "modality": "Cardinal", "polarity": "Positive", "classic_ruler": "Mars", "modern_ruler": "Mars"},
    "Taurus":      {"name": "Taurus",      "symbol": "♉", "element": "Earth",  "modality": "Fixed",    "polarity": "Negative", "classic_ruler": "Venus", "modern_ruler": "Venus"},
    "Gemini":      {"name": "Gemini",      "symbol": "♊", "element": "Air",    "modality": "Mutable",  "polarity": "Positive", "classic_ruler": "Mercury", "modern_ruler": "Mercury"},
    "Cancer":      {"name": "Cancer",      "symbol": "♋", "element": "Water",  "modality": "Cardinal", "polarity": "Negative", "classic_ruler": "Moon", "modern_ruler": "Moon"},
    "Leo":         {"name": "Leo",         "symbol": "♌", "element": "Fire",   "modality": "Fixed",    "polarity": "Positive", "classic_ruler": "Sun", "modern_ruler": "Sun"},
    "Virgo":       {"name": "Virgo",       "symbol": "♍", "element": "Earth",  "modality": "Mutable",  "polarity": "Negative", "classic_ruler": "Mercury", "modern_ruler": "Mercury"},
    "Libra":       {"name": "Libra",       "symbol": "♎", "element": "Air",    "modality": "Cardinal", "polarity": "Positive", "classic_ruler": "Venus", "modern_ruler": "Venus"},
    "Scorpio":     {"name": "Scorpio",     "symbol": "♏", "element": "Water",  "modality": "Fixed",    "polarity": "Negative", "classic_ruler": "Mars", "modern_ruler": "Pluto"},
    "Sagittarius": {"name": "Sagittarius", "symbol": "♐", "element": "Fire",   "modality": "Mutable",  "polarity": "Positive", "classic_ruler": "Jupiter", "modern_ruler": "Jupiter"},
    "Capricorn":   {"name": "Capricorn",   "symbol": "♑", "element": "Earth",  "modality": "Cardinal", "polarity": "Negative", "classic_ruler": "Saturn", "modern_ruler": "Saturn"},
    "Aquarius":    {"name": "Aquarius",    "symbol": "♒", "element": "Air",    "modality": "Fixed",    "polarity": "Positive", "classic_ruler": "Saturn", "modern_ruler": "Uranus"},
    "Pisces":      {"name": "Pisces",      "symbol": "♓", "element": "Water",  "modality": "Mutable",  "polarity": "Negative", "classic_ruler": "Jupiter", "modern_ruler": "Neptune"},
}

# =====================
# TYPE DEFINITIONS
# =====================
BODY_TYPES = Literal["Planet", "Asteroid", "Axis", "LunarNode", "Lilith", "Luminary"]

# =====================
# ASTROLOGICAL BODY GROUPS
# =====================
# General Astrological Groups (for Semantic Filtering)
# These groups are for general-purpose filtering and categorization based on astrological meaning.
# They can be used to filter bodies in a user interface or for interpretive logic.
ASTROLOGICAL_BODY_GROUPS = {
    "luminaries": ["Sun", "Moon"],
    "personal_planets": ["Mercury", "Venus", "Mars"],
    "social_planets": ["Jupiter", "Saturn"],
    "generational_planets": ["Uranus", "Neptune", "Pluto"],
    "main_asteroids": ["Ceres", "Pallas", "Juno", "Vesta"],
    "centaur_asteroids": ["Chiron"],
    "lunar_nodes": ["True Node", "Mean Node", "South Node"],
    "chart_angles": ["AC", "MC", "IC", "DC"],
    "hypothetical_points": ["Lilith"],
    "all_planets": [
        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", 
        "Uranus", "Neptune", "Pluto"
    ],
    "all_asteroids": ["Ceres", "Pallas", "Juno", "Vesta", "Chiron"],
}

# =====================
# CELESTIAL BODY SYMBOLS
# =====================
LUMINARIES_SYMBOLS = {"Sun": "☉", "Moon": "☽"}
PERSONAL_PLANETS_SYMBOLS = {"Mercury": "☿", "Venus": "♀", "Mars": "♂"}
SOCIAL_PLANETS_SYMBOLS = {"Jupiter": "♃", "Saturn": "♄"}
TRANSPERSONAL_PLANETS_SYMBOLS = {"Uranus": "♅", "Neptune": "♆", "Pluto": "♇"}
ASTEROIDS_SYMBOLS = {"Ceres": "⚳", "Pallas": "⚴", "Juno": "⚵", "Vesta": "⚶", "Chiron": "⚷"}
LUNAR_NODES_SYMBOLS = {"True Node": "☊", "South Node": "☋", "Mean Node": "☊"}
LILITH_SYMBOLS = {"Lilith": "⚸"}
ANGLES_SYMBOLS = {"AC": "AC", "MC": "MC", "IC": "IC", "DC": "DC"}

# =====================
# ORB-SPECIFIC GROUPS (for 5x5 Matrix)
# =====================
# These dictionaries provide consistent, named groups for filtering and configuration.

# Orb-Specific Groups (for 5x5 Matrix)
# These groups are designed to EXACTLY mirror the structure of the astro.com orb matrix.
# They are the primary keys used in the ORB_CONFIGS dictionary.
ORB_BODY_GROUPS = {
    # Corresponds to rows for Sun (☉) and Moon (☽) in the astro.com orb matrix.
    "orb_luminaries": ["Sun", "Moon"],
    
    # Corresponds to rows for Mercury (☿), Venus (♀), and Mars (♂).
    "orb_personal": ["Mercury", "Venus", "Mars"],

    # Corresponds to rows for Jupiter (♃) and Saturn (♄).
    "orb_social": ["Jupiter", "Saturn"],

    # Corresponds to rows for Uranus (♅), Neptune (♆), Pluto (♇), and Chiron (⚷).
    "orb_transpersonal_chiron": ["Uranus", "Neptune", "Pluto", "Chiron"],

    # Corresponds to rows for Ascendant (AC), Midheaven (MC), and Node (☊).
    "orb_points": ["AC", "MC", "IC", "DC", "True Node", "Mean Node"],

    # Fallback group for bodies not in the main matrix, like other asteroids and Lilith.
    "orb_other_bodies": ["Ceres", "Pallas", "Juno", "Vesta", "Lilith"]
}

# =====================
# ORB ASPECT GROUPS
# =====================
ORB_ASPECT_GROUPS = {
    "major": ["Conjunction", "Opposition", "Square", "Trine"],
    "sextile": ["Sextile"],
    "adjustment": ["Semisextile", "Quincunx"],
    "tension": ["Sesquiquadrate", "Semisquare"],
    "creative": ["Quintile", "Biquintile"],
}

# =====================
# ASPECT DATA
# =====================
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

# =====================
# ZODIAC SIGN DEGREES
# =====================
ZODIAC_SIGN_DEGREES = {
    "Aries": 0, "Taurus": 30, "Gemini": 60, "Cancer": 90, "Leo": 120, "Virgo": 150,
    "Libra": 180, "Scorpio": 210, "Sagittarius": 240, "Capricorn": 270, "Aquarius": 300, "Pisces": 330,
}

# =====================
# ORB CONFIGURATIONS (5x5 Matrix)
# =====================
# This structure mirrors the astro.com orb matrix for aspect calculations.
# Orbs from Liz Greene, used as the default setting on astro.com (chart type 2.AT, 2.GW, etc.).
ORB_CONFIGS = {
    'Default': {
        'orb_luminaries': {
            'major': 10.0, 'sextile': 6.0, 'adjustment': 3.0, 'tension': 3.0, 'creative': 2.0
        },
        'orb_personal': {
            'major': 10.0, 'sextile': 6.0, 'adjustment': 3.0, 'tension': 3.0, 'creative': 2.0
        },
        'orb_social': {
            'major': 10.0, 'sextile': 6.0, 'adjustment': 3.0, 'tension': 3.0, 'creative': 2.0
        },
        'orb_transpersonal_chiron': {
            'major': 10.0, 'sextile': 6.0, 'adjustment': 3.0, 'tension': 3.0, 'creative': 2.0
        },
        'orb_other_bodies': {
            'major': 3.0,  'sextile': 2.0, 'adjustment': 1.5, 'tension': 1.5, 'creative': 1.0
        },
        'orb_points': {
            'major': 0.0,  'sextile': 0.0, 'adjustment': 0.0, 'tension': 0.0, 'creative': 0.0
        }
    },
    # Orbs from the 'Classical' setting on astro.com (chart type 2.A).
    'Classical': {
        'orb_luminaries': {
            'major': 9.0, 'sextile': 5.0, 'adjustment': 3.0, 'tension': 1.5, 'creative': 1.0
        },
        'orb_personal': {
            'major': 7.0, 'sextile': 5.0, 'adjustment': 3.0, 'tension': 1.5, 'creative': 1.0
        },
        'orb_social': {
            'major': 9.0, 'sextile': 5.0, 'adjustment': 3.0, 'tension': 1.5, 'creative': 1.0
        },
        'orb_transpersonal_chiron': {
            'major': 5.0, 'sextile': 5.0, 'adjustment': 3.0, 'tension': 1.5, 'creative': 1.0
        },
        'orb_other_bodies': {
            'major': 2.0, 'sextile': 1.5, 'adjustment': 1.0, 'tension': 1.0, 'creative': 0.5
        },
        'orb_points': {
            'major': 0.0, 'sextile': 0.0, 'adjustment': 0.0, 'tension': 0.0, 'creative': 0.0
        }
    }
}

# =====================
# DERIVED LISTS AND MAPPINGS
# =====================
# Combine all symbol dictionaries into one master dictionary.
BODY_SYMBOLS = {
    **LUMINARIES_SYMBOLS, 
    **PERSONAL_PLANETS_SYMBOLS, 
    **SOCIAL_PLANETS_SYMBOLS,
    **TRANSPERSONAL_PLANETS_SYMBOLS, 
    **ASTEROIDS_SYMBOLS, 
    **LUNAR_NODES_SYMBOLS,
    **LILITH_SYMBOLS, 
    **ANGLES_SYMBOLS
}

# List of all body names used in the system.
ALL_BODY_NAMES = list(BODY_SYMBOLS.keys())

# Map each body name to its astrological type.
BODY_TYPE_MAPPINGS = {
    **{name: "Luminary" for name in LUMINARIES_SYMBOLS.keys()},
    **{name: "Planet" for name in {
        **PERSONAL_PLANETS_SYMBOLS, 
        **SOCIAL_PLANETS_SYMBOLS, 
        **TRANSPERSONAL_PLANETS_SYMBOLS}.keys()
    },
    **{name: "Asteroid" for name in ASTEROIDS_SYMBOLS.keys()},
    **{name: "LunarNode" for name in LUNAR_NODES_SYMBOLS.keys()},
    **{name: "Lilith" for name in LILITH_SYMBOLS.keys()},
    **{name: "Axis" for name in ANGLES_SYMBOLS.keys()},
}
VALID_BODY_TYPES = list(set(BODY_TYPE_MAPPINGS.values()))

SIGN_NAMES_BY_DEGREE = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", 
    "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# =====================
# DIGNITY RULES
# =====================
DIGNITY_RULES = {
    "domicile": {
        "Sun": "Leo", "Moon": "Cancer", "Mercury": ["Gemini", "Virgo"], "Venus": ["Taurus", "Libra"], 
        "Mars": "Aries", "Jupiter": "Sagittarius", "Saturn": "Capricorn", "Uranus": "Aquarius", 
        "Neptune": "Pisces", "Pluto": "Scorpio"
    },
    "exaltation": {
        "Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo", "Venus": "Pisces", "Mars": "Capricorn", 
        "Jupiter": "Cancer", "Saturn": "Libra", "Uranus": "Scorpio", "Neptune": "Leo", "Pluto": "Aries"
    },
    "detriment": {
        "Sun": "Aquarius", "Moon": "Capricorn", "Mercury": ["Sagittarius", "Pisces"], 
        "Venus": ["Scorpio", "Aries"], "Mars": "Libra", "Jupiter": "Gemini", "Saturn": "Cancer", 
        "Uranus": "Leo", "Neptune": "Virgo", "Pluto": "Taurus"
    },
    "fall": {
        "Sun": "Libra", "Moon": "Scorpio", "Mercury": "Pisces", "Venus": "Virgo", "Mars": "Cancer", 
        "Jupiter": "Capricorn", "Saturn": "Aries", "Uranus": "Taurus", "Neptune": "Aquarius", 
        "Pluto": "Virgo"
    }
}

MODALITIES = ["Cardinal", "Fixed", "Mutable"]
ELEMENTS = ["Fire", "Earth", "Air", "Water"]
POLARITIES = ["Positive", "Negative"]

# =====================
# SWISS EPHEMERIS MAPPING
# =====================
# Mapping of body names to Swiss Ephemeris constants.
# Based on Swiss Ephemeris documentation: https://www.astro.com/swisseph/swephprg.htm#_Toc112597363
PLANET_MAPPING_SWE = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, 
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, 
    "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, 
    "Pluto": swe.PLUTO, "Ceres": 17, "Pallas": 18, "Juno": 19, "Vesta": 20, 
    "Chiron": 15, "Pholus": swe.PHOLUS, "True Node": swe.TRUE_NODE, 
    "Mean Node": swe.MEAN_NODE, "AC": swe.ASC, "MC": swe.MC,
    # Note: IC, DC, South Node, and Lilith are calculated programmatically, not directly fetched.
    "IC": None, "DC": None, "South Node": None, "Lilith": None,
}