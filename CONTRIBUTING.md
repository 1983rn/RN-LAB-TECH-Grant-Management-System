# Contributing to Grant Management System - Python Version

Thank you for your interest in contributing to the Grant Management System! This document provides guidelines for contributors.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Flask, HTML, CSS, and JavaScript

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/grant-management-system.git
   cd grant-management-system/python-app
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

## Development Guidelines

### Code Style

Follow these coding standards:

#### Python
- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use meaningful variable and function names

#### JavaScript
- Use ES6+ features
- Use camelCase for variables and functions
- Use meaningful names
- Add comments for complex logic

#### HTML/CSS
- Use semantic HTML5 tags
- Follow BEM methodology for CSS classes
- Use Tailwind CSS classes when possible
- Keep HTML structure clean and readable

### Project Structure

```
python-app/
├── app.py                 # Main Flask application
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── tests/                # Test files
├── templates/           # HTML templates
├── static/              # Static assets (CSS, JS, images)
├── data/                # JSON data files
├── docs/                # Documentation
└── scripts/             # Utility scripts
```

### Git Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add export to CSV functionality
fix: resolve budget calculation error
docs: update API documentation
```

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_app.py

# Run with coverage
python -m pytest --cov=app tests/
```

### Writing Tests

- Write tests for all new features
- Test both success and error cases
- Use descriptive test names
- Keep tests simple and focused

Example:
```python
def test_add_credit_entry(self):
    """Test adding a new credit entry"""
    credit_data = {
        'date': '2026-01-15',
        'month': 'January',
        'lineItems': [{'subItemDescription': 'Test', 'amount': 1000}],
        'remarks': 'Test credit',
        'financialYear': '2026-2027'
    }
    
    response = self.app.post('/add_credit',
                           data=json.dumps(credit_data),
                           content_type='application/json')
    
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertTrue(data['success'])
```

## Documentation

### Updating Documentation

- Keep API documentation up to date
- Update README.md for major changes
- Add inline comments for complex code
- Update deployment guides as needed

### Documentation Files

- `README.md` - Project overview and setup
- `docs/API.md` - API documentation
- `docs/DEPLOYMENT.md` - Deployment guide
- `CONTRIBUTING.md` - This file

## Pull Request Process

### Before Submitting

1. **Run Tests**
   ```bash
   python -m pytest tests/
   ```

2. **Check Code Style**
   ```bash
   flake8 app.py
   black app.py
   ```

3. **Test Manually**
   - Test all new features
   - Test edge cases
   - Verify no regressions

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Manual testing completed
- [ ] No regressions detected

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Code Review Guidelines

### For Reviewers

1. **Check Functionality**
   - Does the code work as intended?
   - Are there any edge cases missed?

2. **Check Code Quality**
   - Is the code readable and maintainable?
   - Are there any security concerns?
   - Is performance acceptable?

3. **Check Tests**
   - Are tests comprehensive?
   - Do tests cover edge cases?

### For Authors

1. **Respond to Feedback**
   - Address all review comments
   - Explain design decisions
   - Update code as needed

2. **Keep PRs Focused**
   - One feature per PR
   - Keep changes minimal
   - Avoid unrelated changes

## Release Process

1. **Version Bump**
   - Update version in `package.json`
   - Create release notes

2. **Tag Release**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Deploy**
   - Follow deployment guide
   - Test in staging first

## Getting Help

- Create an issue for bugs or feature requests
- Ask questions in discussions
- Check existing documentation first

## Community Guidelines

- Be respectful and inclusive
- Welcome new contributors
- Provide constructive feedback
- Focus on what's best for the project

Thank you for contributing!
