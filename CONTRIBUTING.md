# Contributing to MusicMood

Thank you for your interest in MusicMood! This is primarily a portfolio project, but contributions, suggestions, and feedback are welcome.

## 🎯 Project Purpose

This project demonstrates:
- Multi-agent AI system architecture
- Production-grade Python development
- Docker containerization
- CI/CD best practices
- LangChain framework usage

## 🐛 Reporting Issues

Found a bug? Have a suggestion? Please:

1. Check if the issue already exists
2. Create a detailed issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Docker version)
   - Relevant logs

## 💡 Suggesting Enhancements

Ideas for improvements are welcome! Consider:

- Performance optimizations
- New AI model integrations
- Additional music sources
- UI/UX improvements
- Documentation clarifications

## 🔧 Development Setup

### Prerequisites

- Python 3.11+
- Docker Desktop
- Poetry
- Git

### Local Development

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/MusicMood.git
   cd MusicMood
   ```

2. **Install Dependencies**
   ```bash
   poetry install
   poetry shell
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Run Tests**
   ```bash
   pytest tests/
   ```

## 📝 Code Style

- **Python**: Follow PEP 8
- **Type Hints**: Use throughout
- **Docstrings**: Google style
- **Formatting**: Black (line length 100)
- **Linting**: Ruff

```bash
# Format code
black app/ --line-length 100

# Lint
ruff check app/
```

## 🧪 Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for >80% coverage

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html
```

## 📦 Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

3. **Test Locally**
   ```bash
   # Run tests
   pytest
   
   # Test Docker build
   docker-compose build
   
   # Verify everything works
   .\start-app.ps1 start
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: clear description of changes"
   ```
   
   Commit message format:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `refactor:` Code refactoring
   - `test:` Test changes
   - `chore:` Maintenance

5. **Push & Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a Pull Request with:
   - Clear title and description
   - Link to related issues
   - Screenshots (if UI changes)

## 🔍 Code Review

PRs will be reviewed for:
- ✅ Code quality and style
- ✅ Test coverage
- ✅ Documentation completeness
- ✅ Docker functionality
- ✅ CI pipeline success

## 📚 Documentation

When adding features, update:
- README.md (if user-facing)
- Code docstrings
- API documentation (if endpoints change)
- SETUP_GUIDE.md (if setup changes)

## 🚀 Release Process

Releases follow semantic versioning:
- `v1.0.0` - Major release
- `v1.1.0` - Minor (new features)
- `v1.0.1` - Patch (bug fixes)

## ❓ Questions?

- Check existing [documentation](README.md)
- Review [issues](https://github.com/YOUR_USERNAME/MusicMood/issues)
- Open a discussion for general questions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to MusicMood! 🎵**
