"""
Tests for the utils module of Nataly library.
"""

import json
import logging
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from nataly.utils import (
    create_directory,
    format_timestamp,
    get_file_info,
    load_from_json,
    save_to_json,
    setup_logging,
    validate_data,
)


class TestLogging:
    """Test cases for logging functionality."""
    
    def test_setup_logging(self):
        """Test logging setup."""
        # Test basic setup
        setup_logging("INFO")
        logger = logging.getLogger("nataly.utils")
        assert logger.level == logging.INFO
        
        # Test with file handler
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            log_file = f.name
        
        try:
            setup_logging("DEBUG", log_file)
            logger = logging.getLogger("nataly.utils")
            assert logger.level == logging.DEBUG
        finally:
            Path(log_file).unlink(missing_ok=True)


class TestJsonOperations:
    """Test cases for JSON operations."""
    
    def test_save_and_load_json(self):
        """Test saving and loading JSON data."""
        test_data = {
            "string": "test",
            "number": 42,
            "list": [1, 2, 3],
            "dict": {"a": 1, "b": 2}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            # Test saving
            result = save_to_json(test_data, filepath)
            assert result is True
            
            # Test loading
            loaded_data = load_from_json(filepath)
            assert loaded_data == test_data
            
            # Test loading non-existent file
            non_existent = load_from_json("non_existent.json")
            assert non_existent is None
            
        finally:
            Path(filepath).unlink(missing_ok=True)
    
    def test_save_json_with_indent(self):
        """Test saving JSON with custom indentation."""
        test_data = {"a": 1, "b": 2}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            save_to_json(test_data, filepath, indent=4)
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Check that content is properly formatted
            parsed = json.loads(content)
            assert parsed == test_data
            
        finally:
            Path(filepath).unlink(missing_ok=True)


class TestDataValidation:
    """Test cases for data validation."""
    
    def test_validate_data(self):
        """Test data validation functionality."""
        # Test None data
        assert validate_data(None) is False
        
        # Test valid data without required keys
        assert validate_data("test") is True
        assert validate_data(42) is True
        assert validate_data([1, 2, 3]) is True
        
        # Test dict with required keys
        data = {"a": 1, "b": 2, "c": 3}
        assert validate_data(data, ["a", "b"]) is True
        assert validate_data(data, ["a", "b", "c"]) is True
        assert validate_data(data, ["a", "b", "c", "d"]) is False


class TestTimestampFormatting:
    """Test cases for timestamp formatting."""
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        # Test with None (current time)
        timestamp_str = format_timestamp()
        assert isinstance(timestamp_str, str)
        assert len(timestamp_str) > 0
        
        # Test with specific timestamp
        dt = datetime(2023, 1, 1, 12, 30, 45)
        timestamp_str = format_timestamp(dt)
        assert timestamp_str == "2023-01-01 12:30:45"


class TestDirectoryOperations:
    """Test cases for directory operations."""
    
    def test_create_directory(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = Path(temp_dir) / "test_subdir"
            
            # Test creating new directory
            result = create_directory(new_dir)
            assert result is True
            assert new_dir.exists()
            assert new_dir.is_dir()
            
            # Test creating existing directory
            result = create_directory(new_dir)
            assert result is True


class TestFileInfo:
    """Test cases for file information."""
    
    def test_get_file_info_existing_file(self):
        """Test getting info for existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filepath = f.name
            f.write(b"test content")
        
        try:
            info = get_file_info(filepath)
            
            assert info["exists"] is True
            assert info["size"] > 0
            assert isinstance(info["modified"], datetime)
            assert isinstance(info["created"], datetime)
            assert info["is_file"] is True
            assert info["is_dir"] is False
            assert info["extension"] == ""
            assert info["name"] == Path(filepath).name
            assert info["parent"] == str(Path(filepath).parent)
            
        finally:
            Path(filepath).unlink(missing_ok=True)
    
    def test_get_file_info_non_existent(self):
        """Test getting info for non-existent file."""
        info = get_file_info("non_existent_file.txt")
        assert info["exists"] is False
    
    def test_get_file_info_directory(self):
        """Test getting info for directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            info = get_file_info(temp_dir)
            
            assert info["exists"] is True
            assert info["is_file"] is False
            assert info["is_dir"] is True
            assert info["name"] == Path(temp_dir).name


if __name__ == "__main__":
    pytest.main([__file__]) 