# Contributing to LLM Cognitive Profiling Framework

Thank you for your interest in contributing to the LLM Cognitive Profiling Framework! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists in the [Issues](https://github.com/yourusername/llm-cognitive-framework/issues) section
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Enhancements

1. Check existing [Issues](https://github.com/yourusername/llm-cognitive-framework/issues) for similar suggestions
2. Create a new issue with the `enhancement` label
3. Describe the enhancement and its benefits
4. Provide use cases if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes following the coding standards
4. Add tests for new functionality
5. Update documentation as needed
6. Commit with clear messages:
   ```bash
   git commit -m "feat: add new cognitive metric for attention span"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Open a Pull Request

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/llm-cognitive-framework.git
   cd llm-cognitive-framework
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   python -m spacy download en_core_web_sm
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [pylint](https://pylint.org/) for linting
- Maximum line length: 100 characters

### Code Format

Run before committing:
```bash
black .
pylint src/
```

### Docstrings

Use Google-style docstrings:
```python
def calculate_metric(data: List[float], method: str = "mean") -> float:
    """Calculate a cognitive metric from response data.
    
    Args:
        data: List of numerical values from analysis
        method: Calculation method ('mean', 'median', 'weighted')
        
    Returns:
        Calculated metric value
        
    Raises:
        ValueError: If method is not recognized
    """
```

### Type Hints

Use type hints for all function signatures:
```python
from typing import Dict, List, Optional

def analyze_responses(
    responses: List[Dict[str, str]], 
    model_name: Optional[str] = None
) -> Dict[str, float]:
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_analyzer.py::test_specific_function
```

### Writing Tests

- Place tests in `tests/` directory
- Mirror source structure
- Use descriptive test names
- Include edge cases
- Aim for >80% coverage

Example:
```python
def test_cognitive_analyzer_identifies_reasoning_patterns():
    """Test that analyzer correctly identifies reasoning patterns."""
    analyzer = CognitiveAnalyzer()
    response = "Therefore, we can conclude that..."
    result = analyzer._identify_reasoning_style(response)
    assert result['deductive'] > 0
    assert result['dominant'] == 'deductive'
```

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test additions or fixes
- `chore:` Maintenance tasks

Examples:
```
feat: add support for Llama models
fix: correct metric calculation for working memory
docs: update API documentation
test: add tests for task generator
```

## Project Structure

When adding new features, maintain the project structure:

```
src/
├── models/         # Model interfaces
├── tasks/          # Task generators
├── analysis/       # Response analyzers
├── metrics/        # Metric calculators
├── visualization/  # Visualizers
└── utils/          # Utilities

tests/
├── test_models/
├── test_tasks/
├── test_analysis/
├── test_metrics/
└── test_integration/
```

## Adding New Models

To add support for a new LLM:

1. Create interface in `src/models/`
2. Add configuration in `config/config.yaml`
3. Update `README.md` with setup instructions
4. Add tests in `tests/test_models/`
5. Update requirements if needed

## Adding New Cognitive Metrics

To add a new cognitive metric:

1. Define metric in `src/metrics/metric_calculator.py`
2. Add analysis method in `src/analysis/cognitive_analyzer.py`
3. Create visualization in `src/visualization/profile_visualizer.py`
4. Add tests
5. Update documentation

## Documentation

- Update docstrings for all changes
- Update README.md for user-facing changes
- Add examples for new features
- Update configuration documentation

## Release Process

1. Update version in `setup.py` and `src/__init__.py`
2. Update CHANGELOG.md
3. Create release PR
4. After merge, tag release:
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1"
   git push origin v1.0.1
   ```

## Getting Help

- Open an issue for questions
- Join discussions in the Issues section
- Contact: tislam38@gatech.edu

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
