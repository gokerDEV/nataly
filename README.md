# Nataly

A Python library called Nataly.

## Installation

You can install Nataly using pip:

```bash
pip install nataly
```

For development installation:

```bash
git clone https://github.com/gokerDEV/nataly.git
cd nataly
pip install -e .
```

## Usage

```python
from nataly import core

# Example usage
result = core.example_function()
print(result)
```

## Development

To set up the development environment:

```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Format code:
```bash
black nataly/
```

Lint code:
```bash
flake8 nataly/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite
6. Submit a pull request

## Version History

- 0.1.0: Initial release 