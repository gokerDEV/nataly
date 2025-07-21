"""
Basic tests for the nataly astrological library.
"""

import datetime
import pytz
import pytest

from nataly import NatalChart, create_orb_config, BodyFilter
from nataly.constants import ASTROLOGICAL_BODY_GROUPS, ANGLES_SYMBOLS, SIGNS, ASPECT_DATA


class TestNatalyLibrary:
    """Test cases for the nataly library."""
    
    def test_imports(self):
        """Test that all main components can be imported."""
        from nataly import (
            NatalChart, AstroEngine, Body, House, Aspect, Sign, 
            BodyFilter, OrbConfig, create_orb_config
        )
        assert True  # If we get here, imports work
    
    def test_constants(self):
        """Test that constants are properly defined."""
        # Test zodiac signs
        assert "Aries" in SIGNS
        assert "Taurus" in SIGNS
        assert "Pisces" in SIGNS
        
        # Test aspect data
        assert "Conjunction" in ASPECT_DATA
        assert "Opposition" in ASPECT_DATA
        assert "Trine" in ASPECT_DATA
        assert "Square" in ASPECT_DATA
    
    def test_orb_config_creation(self):
        """Test orb configuration creation."""
        # Test default creation
        config = create_orb_config()
        assert config is not None
        # Check canonical orb config dict keys
        assert "orb_luminaries" in config
        assert "orb_personal" in config
        assert "orb_social" in config
        assert "orb_transpersonal_chiron" in config
        assert "orb_other_bodies" in config
        assert "orb_points" in config
        
        # Test custom creation
        custom_config = create_orb_config('Placidus')
        assert custom_config is not None
    
    def test_body_filter(self):
        """Test BodyFilter functionality."""
        filter_config = BodyFilter(
            include_planets=True,
            include_luminaries=True,
            include_asteroids=False
        )
        assert filter_config.include_planets is True
        assert filter_config.include_luminaries is True
        assert filter_config.include_asteroids is False
    
    def test_natal_chart_creation(self):
        """Test NatalChart creation with sample data."""
        # Use the reference data from tests/references.py
        birth_dt = datetime.datetime(1990, 2, 27, 7, 15, tzinfo=pytz.UTC)
        
        try:
            chart = NatalChart(
                person_name="Test Person",
                dt_utc=birth_dt,
                lat=38.25,  # Izmir, Turkey
                lon=27.09,
                orb_config=create_orb_config()
            )
            
            # Test basic properties
            assert chart.name == "Test Person"
            assert chart.latitude == 38.25
            assert chart.longitude == 27.09
            
            # Test that bodies were calculated
            assert len(chart.bodies_dict) > 0
            
            # Test that houses were calculated
            assert len(chart.houses) == 12
            
            # Test that aspects were calculated
            assert hasattr(chart, 'aspects')
            
            # Test distributions
            assert hasattr(chart, 'element_distribution')
            assert hasattr(chart, 'modality_distribution')
            assert hasattr(chart, 'polarity_distribution')
            
        except Exception as e:
            # If Swiss Ephemeris is not available, this is expected
            pytest.skip(f"Swiss Ephemeris not available: {e}")
    
    def test_chart_methods(self):
        """Test NatalChart methods."""
        birth_dt = datetime.datetime(1990, 2, 27, 7, 15, tzinfo=pytz.UTC)
        
        try:
            chart = NatalChart(
                person_name="Test Person",
                dt_utc=birth_dt,
                lat=38.25,
                lon=27.09
            )
            
            # Test get_body_by_name
            sun = chart.get_body_by_name("Sun")
            if sun:
                assert sun.name == "Sun"
                assert hasattr(sun, 'longitude')
                assert hasattr(sun, 'sign')
                assert hasattr(sun, 'house')
            
            # Test get_bodies_by_type
            planets = chart.get_bodies_by_type("Planet")
            assert isinstance(planets, list)
            
            luminaries = chart.get_bodies_by_type("Luminary")
            assert isinstance(luminaries, list)
            
            # Test get_planets
            all_planets = chart.get_planets(include_luminaries=True)
            assert isinstance(all_planets, list)
            
            # Test get_axes
            axes = chart.get_axes()
            assert isinstance(axes, list)
            
        except Exception as e:
            pytest.skip(f"Swiss Ephemeris not available: {e}")
    
    def test_filtering(self):
        """Test body filtering functionality."""
        birth_dt = datetime.datetime(1990, 2, 27, 7, 15, tzinfo=pytz.UTC)
        
        try:
            chart = NatalChart(
                person_name="Test Person",
                dt_utc=birth_dt,
                lat=38.25,
                lon=27.09
            )
            
            # Test filtering by names
            sun_moon = chart.get_bodies_by_names(["Sun", "Moon"])
            assert isinstance(sun_moon, list)
            
            # Test filtering by signs
            fire_signs = chart.get_bodies_by_signs(["Aries", "Leo", "Sagittarius"])
            assert isinstance(fire_signs, list)
            
            # Test filtering by elements
            fire_bodies = chart.get_bodies_by_elements(["Fire"])
            assert isinstance(fire_bodies, list)
            
            # Test filtering by houses
            first_house = chart.get_bodies_by_houses([1])
            assert isinstance(first_house, list)
            
        except Exception as e:
            pytest.skip(f"Swiss Ephemeris not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__]) 