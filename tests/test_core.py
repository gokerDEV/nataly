"""
Tests for the core module of Nataly library.
"""

import pytest
from nataly.core import NatalyCore, example_function, process_data, create_core
from nataly.constants import ASTROLOGICAL_BODY_GROUPS, ANGLES_SYMBOLS, SIGNS


class TestNatalyCore:
    """Test cases for NatalyCore class."""
    
    def test_init(self):
        """Test NatalyCore initialization."""
        core = NatalyCore()
        assert core.name == "Nataly"
        assert core._data == {}
        
        core = NatalyCore("TestCore")
        assert core.name == "TestCore"
    
    def test_add_and_get_data(self):
        """Test adding and retrieving data."""
        core = NatalyCore()
        
        # Test adding data
        core.add_data("test_key", "test_value")
        assert core.get_data("test_key") == "test_value"
        
        # Test getting non-existent key
        assert core.get_data("non_existent") is None
        
        # Test adding different types
        core.add_data("number", 42)
        core.add_data("list", [1, 2, 3])
        core.add_data("dict", {"a": 1, "b": 2})
        
        assert core.get_data("number") == 42
        assert core.get_data("list") == [1, 2, 3]
        assert core.get_data("dict") == {"a": 1, "b": 2}
    
    def test_list_data(self):
        """Test listing data keys."""
        core = NatalyCore()
        assert core.list_data() == []
        
        core.add_data("key1", "value1")
        core.add_data("key2", "value2")
        
        keys = core.list_data()
        assert len(keys) == 2
        assert "key1" in keys
        assert "key2" in keys
    
    def test_clear_data(self):
        """Test clearing all data."""
        core = NatalyCore()
        core.add_data("key1", "value1")
        core.add_data("key2", "value2")
        
        assert len(core.list_data()) == 2
        
        core.clear_data()
        assert len(core.list_data()) == 0
        assert core.get_data("key1") is None


class TestCoreFunctions:
    """Test cases for core module functions."""
    
    def test_example_function(self):
        """Test example_function."""
        result = example_function()
        assert result == "Hello from Nataly!"
        assert isinstance(result, str)
    
    def test_process_data_string(self):
        """Test process_data with string input."""
        data = "Hello world"
        result = process_data(data)
        
        assert result["type"] == "str"
        assert result["length"] == 11
        assert result["processed"] is True
        assert result["word_count"] == 2
    
    def test_process_data_list(self):
        """Test process_data with list input."""
        data = [1, 2, 3, 4, 5]
        result = process_data(data)
        
        assert result["type"] == "list"
        assert result["length"] == 5
        assert result["processed"] is True
        assert result["item_count"] == 5
    
    def test_process_data_dict(self):
        """Test process_data with dictionary input."""
        data = {"a": 1, "b": 2, "c": 3}
        result = process_data(data)
        
        assert result["type"] == "dict"
        assert result["length"] == 3
        assert result["processed"] is True
        assert result["item_count"] == 3
    
    def test_create_core(self):
        """Test create_core function."""
        core = create_core()
        assert isinstance(core, NatalyCore)
        assert core.name == "Nataly"
        
        core = create_core("CustomName")
        assert core.name == "CustomName"


if __name__ == "__main__":
    pytest.main([__file__]) 