# nataly/config.py
# Configuration management for the nataly astrology library.

import os
from typing import Optional
from pathlib import Path
from .constants import ORB_CONFIGS

class NatalyConfig:
    """Configuration class for nataly library settings."""
    
    def __init__(self, ephe_path: Optional[str] = None):
        """
        Initialize nataly configuration.
        
        Args:
            ephe_path: Path to ephemeris files directory. If None, uses default.
        """
        self._ephe_path = ephe_path or self._get_default_ephe_path()
    
    @property
    def ephe_path(self) -> str:
        """Get the ephemeris files path."""
        return self._ephe_path
    
    @ephe_path.setter
    def ephe_path(self, path: str):
        """Set the ephemeris files path."""
        self._ephe_path = path
    
    def _get_default_ephe_path(self) -> str:
        """Get the default ephemeris files path."""
        # Get the directory where this config.py file is located
        current_dir = Path(__file__).parent
        default_path = str(current_dir / "ephe")
        return default_path
    
    def validate_ephe_path(self) -> bool:
        """Validate that the ephemeris path exists and contains required files."""
        if not os.path.exists(self._ephe_path):
            return False
        
        # Check for at least one ephemeris file
        required_files = [
            "seas_18.se1",  # Saturn ephemeris
            "sepl_18.se1",  # Pluto ephemeris
            "semo_18.se1",  # Moon ephemeris
            "seplm18.se1",  # Pluto-Moon ephemeris
            "semom18.se1",  # Moon-Moon ephemeris
        ]
        
        existing_files = os.listdir(self._ephe_path)
        return any(file in existing_files for file in required_files)
    
    def get_ephe_path(self) -> str:
        """Get the ephemeris path, with validation."""
        if not self.validate_ephe_path():
            print(f"⚠️  WARNING: Ephemeris files not found in '{self._ephe_path}' directory!")
            print("📥 To download ephemeris files:")
            print("   1. Go to https://www.astro.com/swisseph/swedownload_j.htm")
            print("   2. Download ephemeris files from 'Swiss Ephemeris Files' section")
            print("   3. Place the downloaded files in your ephemeris directory")
            print("   4. Required ephemeris files:")
            for file in ["seas_18.se1", "sepl_18.se1", "semo_18.se1", "seplm18.se1", "semom18.se1"]:
                print(f"      - '{file}'")
            print("   5. Using default Moshier ephemeris for now (less accurate)")
            print()
        
        return self._ephe_path

# Global configuration instance
_default_config = NatalyConfig()

def get_config() -> NatalyConfig:
    """Get the global configuration instance."""
    return _default_config

def set_ephe_path(path: str):
    """Set the global ephemeris path."""
    _default_config.ephe_path = path

def get_ephe_path() -> str:
    """Get the global ephemeris path."""
    return _default_config.get_ephe_path()

def create_config(ephe_path: Optional[str] = None) -> NatalyConfig:
    """Create a new configuration instance."""
    return NatalyConfig(ephe_path) 

def create_orb_config(system: str = 'Default', custom_orbs: dict = None):
    """Creates an orb configuration dictionary from a predefined system or a custom dictionary."""
    if custom_orbs:
        # In a real application, validate the custom_orbs structure here.
        return custom_orbs
    if system not in ORB_CONFIGS:
        system = 'Default'  # Fallback to the default system.
    return ORB_CONFIGS[system]

def set_default_orb_config(config):
    """Set the default orb configuration to be used globally."""
    global DEFAULT_ORB_CONFIG
    DEFAULT_ORB_CONFIG = config

# Initialize a default orb configuration on startup.
DEFAULT_ORB_CONFIG = create_orb_config('Default') 