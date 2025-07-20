# nataly/__init__.py
# Main package initialization for the nataly astrology library.

from .chart import NatalChart
from .engine import AstroEngine
from .models import Body, House, Aspect, Sign, BodyFilter, OrbConfig
from .constants import (
    create_orb_config, set_default_orb_config, 
    SIGNS, BODY_SYMBOLS, PLANET_SYMBOLS, PLANET_NAMES, AXES_NAMES,
    ASPECT_DATA, MAJOR_ASPECTS, DIGNITY_RULES,
    MODALITIES, ELEMENTS, POLARITIES,
    LUMINARIES, MAJOR_PLANETS, ASTEROIDS, LUNAR_NODES, LILITH_BODIES, ANGLES,
    PLANETS, ALL_BODIES, ALL_BODY_NAMES,
    BODY_TYPE_MAPPINGS, VALID_BODY_TYPES, BODY_TYPES
)
from .config import NatalyConfig, get_config, set_ephe_path, get_ephe_path, create_config

__version__ = "0.1.0"
__author__ = "Göker"
__email__ = "goker@goker.dev"
__description__ = "A comprehensive astrology library for natal chart calculations and analysis"

# Main exports
__all__ = [
    # Core classes
    "NatalChart",
    "AstroEngine", 
    "Body",
    "House",
    "Aspect",
    "Sign",
    "BodyFilter",
    "OrbConfig",
    
    # Configuration functions
    "create_orb_config",
    "set_default_orb_config",
    
    # Configuration management
    "NatalyConfig",
    "get_config",
    "set_ephe_path",
    "get_ephe_path",
    "create_config",
    
    # Constants and data
    "SIGNS",
    "BODY_SYMBOLS", 
    "PLANET_SYMBOLS",
    "PLANET_NAMES",
    "AXES_NAMES",
    "ASPECT_DATA",
    "MAJOR_ASPECTS",
    "DIGNITY_RULES",
    "MODALITIES",
    "ELEMENTS", 
    "POLARITIES",
    
    # Categorized body lists
    "LUMINARIES",
    "MAJOR_PLANETS", 
    "ASTEROIDS",
    "LUNAR_NODES",
    "LILITH_BODIES",
    "ANGLES",
    "PLANETS",
    "ALL_BODIES",
    "ALL_BODY_NAMES",
    
    # Type definitions
    "BODY_TYPES",
    "BODY_TYPE_MAPPINGS",
    "VALID_BODY_TYPES",
] 