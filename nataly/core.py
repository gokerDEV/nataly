"""
Core functionality for the Nataly library.

This module contains the main functions and classes that form the core
of the Nataly library.
"""

from typing import Any, Dict, List, Optional, Union


class NatalyCore:
    """Main class for Nataly core functionality."""
    
    def __init__(self, name: str = "Nataly"):
        """Initialize the NatalyCore instance.
        
        Args:
            name: The name for this instance
        """
        self.name = name
        self._data: Dict[str, Any] = {}
    
    def add_data(self, key: str, value: Any) -> None:
        """Add data to the core instance.
        
        Args:
            key: The key to store the data under
            value: The value to store
        """
        self._data[key] = value
    
    def get_data(self, key: str) -> Optional[Any]:
        """Retrieve data from the core instance.
        
        Args:
            key: The key to retrieve data for
            
        Returns:
            The stored value or None if not found
        """
        return self._data.get(key)
    
    def list_data(self) -> List[str]:
        """List all available data keys.
        
        Returns:
            List of all stored keys
        """
        return list(self._data.keys())
    
    def clear_data(self) -> None:
        """Clear all stored data."""
        self._data.clear()


def example_function() -> str:
    """Example function demonstrating basic functionality.
    
    Returns:
        A greeting message
    """
    return "Hello from Nataly!"


def process_data(data: Union[str, List, Dict]) -> Dict[str, Any]:
    """Process various types of data and return metadata.
    
    Args:
        data: The data to process
        
    Returns:
        Dictionary containing metadata about the processed data
    """
    result = {
        "type": type(data).__name__,
        "length": len(data) if hasattr(data, "__len__") else None,
        "processed": True
    }
    
    if isinstance(data, str):
        result["word_count"] = len(data.split())
    elif isinstance(data, (list, dict)):
        result["item_count"] = len(data)
    
    return result


# Convenience functions
def create_core(name: str = "Nataly") -> NatalyCore:
    """Create a new NatalyCore instance.
    
    Args:
        name: The name for the core instance
        
    Returns:
        A new NatalyCore instance
    """
    return NatalyCore(name)


__all__ = [
    "NatalyCore",
    "example_function", 
    "process_data",
    "create_core"
] 