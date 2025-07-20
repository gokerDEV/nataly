"""
Utility functions for the Nataly library.

This module contains helper functions and utilities that support
the main functionality of the Nataly library.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration for the library.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def save_to_json(data: Any, filepath: Union[str, Path], indent: int = 2) -> bool:
    """Save data to a JSON file.
    
    Args:
        data: The data to save
        filepath: Path to the output file
        indent: JSON indentation level
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        logger.info(f"Data saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to save data to {filepath}: {e}")
        return False


def load_from_json(filepath: Union[str, Path]) -> Optional[Any]:
    """Load data from a JSON file.
    
    Args:
        filepath: Path to the input file
        
    Returns:
        The loaded data or None if failed
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Data loaded from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Failed to load data from {filepath}: {e}")
        return None


def validate_data(data: Any, required_keys: Optional[List[str]] = None) -> bool:
    """Validate data structure.
    
    Args:
        data: The data to validate
        required_keys: List of required keys if data is a dictionary
        
    Returns:
        True if data is valid, False otherwise
    """
    if data is None:
        return False
    
    if required_keys and isinstance(data, dict):
        return all(key in data for key in required_keys)
    
    return True


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format a timestamp as a string.
    
    Args:
        timestamp: The timestamp to format, uses current time if None
        
    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def create_directory(path: Union[str, Path]) -> bool:
    """Create a directory if it doesn't exist.
    
    Args:
        path: The directory path to create
        
    Returns:
        True if successful, False otherwise
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created/verified: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return False


def get_file_info(filepath: Union[str, Path]) -> Dict[str, Any]:
    """Get information about a file.
    
    Args:
        filepath: Path to the file
        
    Returns:
        Dictionary containing file information
    """
    path = Path(filepath)
    
    if not path.exists():
        return {"exists": False}
    
    stat = path.stat()
    return {
        "exists": True,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "created": datetime.fromtimestamp(stat.st_ctime),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "extension": path.suffix,
        "name": path.name,
        "parent": str(path.parent)
    }


__all__ = [
    "setup_logging",
    "save_to_json",
    "load_from_json", 
    "validate_data",
    "format_timestamp",
    "create_directory",
    "get_file_info"
] 