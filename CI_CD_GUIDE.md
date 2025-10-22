# CI/CD Pipeline Guide

## Overview

MusicMood uses GitHub Actions for continuous integration and deployment. The pipeline includes automated testing, code quality checks, security scanning, Docker image building, and deployment automation.

---

## Workflows

### 1. CI - Build and Test (`ci-build-test.yml`)

**Trigger:** Push to `main`/`develop`, Pull Requests  
**Purpose:** Validate code quality and run tests

#### Jobs:

**Code Quality:**
- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)

**Unit Tests:**
- Runs pytest with coverage
- Uses PostgreSQL and Redis test services
- Uploads coverage to Codecov

**Docker Build Test:**
- Builds both backend and frontend images
- Uses Docker layer caching for speed
- Validates Dockerfiles without pushing

**Security Scan:**
- Trivy vulnerability scanner
- Safety check for Python dependencies
- Uploads results to GitHub Security

### 2. CD - Docker Build & Push (`cd-docker-push.yml`)

**Trigger:** Push to `main`, Tags (`v*.*.*`)  
**Purpose:** Build and publish Docker images

#### Jobs:

**Build and Push:**
- Builds both images with Buildx
- Pushes to GitHub Container Registry (ghcr.io)
- Tags: latest, version tags, branch names, commit SHA

**Create Release:**
- Creates GitHub releases for version tags
- Auto-generates release notes

### 3. CodeQL Analysis (`codeql-analysis.yml`)

**Trigger:** Push, PRs, Weekly schedule  
**Purpose:** Security and code quality analysis

- Scans Python code for vulnerabilities
- Extended security queries
- Results visible in GitHub Security tab

### 4. PR Validation (`pr-validation.yml`)

**Trigger:** Pull request events  
**Purpose:** Automated PR checks

- Validates PR title format (conventional commits)
- Checks PR size (max 1000 lines)
- Auto-labels based on changed files
- Checks for merge conflicts

### 5. Stale Issues (`stale.yml`)

**Trigger:** Daily schedule  
**Purpose:** Manage inactive issues/PRs

- Marks issues stale after 30 days
- Marks PRs stale after 14 days
- Closes after 7 additional days

### 6. Dependabot Auto-Merge (`dependabot-auto-merge.yml`)

**Trigger:** Dependabot PRs  
**Purpose:** Auto-merge non-major dependency updates

- Auto-approves minor/patch updates
- Requires manual review for major updates

---

## Setup Instructions

### 1. GitHub Repository Secrets

Add these secrets in **Settings → Secrets and variables → Actions**:

```
SPOTIFY_CLIENT_ID         - Your Spotify API client ID
SPOTIFY_CLIENT_SECRET     - Your Spotify API client secret
CODECOV_TOKEN            - Codecov upload token (optional)
```

### 2. Enable GitHub Container Registry

1. Go to **Settings → Packages**
2. Make packages public (for public images)
3. Grant workflow write access

### 3. Enable GitHub Security Features

1. Go to **Settings → Code security and analysis**
2. Enable:
   - Dependabot alerts
   - Dependabot security updates
   - CodeQL analysis
   - Secret scanning

### 4. Branch Protection Rules

For `main` branch (**Settings → Branches → Add rule**):

```yaml
Branch name pattern: main

Protections:
☑ Require a pull request before merging
  ☑ Require approvals: 1
  ☑ Dismiss stale approvals
☑ Require status checks to pass
  ☑ Require branches to be up to date
  Status checks:
    - Code Quality & Linting
    - Unit Tests
    - Docker Build Test
☑ Require conversation resolution
☑ Require signed commits (recommended)
☑ Include administrators (optional)
```

---

## Workflow Triggers

### Automatic Triggers

| Workflow | Push (main) | Push (develop) | PR | Tag | Schedule |
|----------|-------------|----------------|----|----|----------|
| CI Build & Test | ✅ | ✅ | ✅ | ❌ | ❌ |
| Docker Push | ✅ | ❌ | ❌ | ✅ | ❌ |
| CodeQL | ✅ | ✅ | ✅ | ❌ | Weekly |
| PR Validation | ❌ | ❌ | ✅ | ❌ | ❌ |
| Stale | ❌ | ❌ | ❌ | ❌ | Daily |

### Manual Triggers

All workflows support `workflow_dispatch` for manual execution:
- Go to **Actions** tab
- Select workflow
- Click **Run workflow**

---

## Docker Image Tags

Images are published to `ghcr.io/OWNER/musicmood-backend` and `ghcr.io/OWNER/musicmood-frontend`

### Tag Strategy

| Trigger | Tags Created | Example |
|---------|--------------|---------|
| Push to main | `latest` | `ghcr.io/owner/musicmood-backend:latest` |
| Push to branch | `branch-name` | `ghcr.io/owner/musicmood-backend:develop` |
| Tag v1.2.3 | `1.2.3`, `1.2`, `1`, `latest` | `ghcr.io/owner/musicmood-backend:1.2.3` |
| Commit SHA | `main-abc1234` | `ghcr.io/owner/musicmood-backend:main-abc1234` |

### Pull Images

```bash
# Latest
docker pull ghcr.io/OWNER/musicmood-backend:latest

# Specific version
docker pull ghcr.io/OWNER/musicmood-backend:1.0.0

# Branch
docker pull ghcr.io/OWNER/musicmood-backend:develop
```

---

## Local Testing

### Run Tests Locally

```bash
# Install dependencies
poetry install --with dev

# Code quality checks
poetry run black --check app/
poetry run isort --check-only app/
poetry run flake8 app/
poetry run mypy app/

# Run tests with coverage
poetry run pytest tests/ -v --cov=app --cov-report=term

# Security scan
poetry run safety check
```

### Test Docker Build Locally

```bash
# Build images
docker-compose build

# Run tests in containers
docker-compose run --rm backend pytest tests/
```

---

## Release Process

### Creating a Release

1. **Update version in `pyproject.toml`:**
   ```toml
   [tool.poetry]
   version = "1.0.0"
   ```

2. **Create and push git tag:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. **Automatic actions:**
   - CI runs tests
   - Docker images built and pushed
   - GitHub release created with notes

4. **Manual steps:**
   - Review auto-generated release notes
   - Add highlights and breaking changes
   - Publish release

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **Major (1.0.0):** Breaking changes
- **Minor (1.1.0):** New features, backwards compatible
- **Patch (1.1.1):** Bug fixes, backwards compatible

---

## Monitoring

### GitHub Actions Dashboard

- **Actions tab:** View all workflow runs
- **Status badges:** Add to README
- **Notifications:** Configure in GitHub settings

### Status Badges

Add to README.md:

```markdown
![CI](https://github.com/OWNER/musicmood/workflows/CI%20-%20Build%20and%20Test/badge.svg)
![Docker](https://github.com/OWNER/musicmood/workflows/CD%20-%20Docker%20Build%20%26%20Push/badge.svg)
![CodeQL](https://github.com/OWNER/musicmood/workflows/CodeQL%20Analysis/badge.svg)
```

### Security Alerts

- **Security tab:** View Dependabot and CodeQL alerts
- **Email notifications:** Auto-enabled for security issues

---

## Troubleshooting

### Workflow Fails on Tests

1. Check test logs in Actions tab
2. Run tests locally: `poetry run pytest tests/ -v`
3. Check environment variables are set
4. Verify PostgreSQL and Redis are accessible

### Docker Build Fails

1. Check Dockerfile syntax
2. Verify all files in build context
3. Check .dockerignore excludes
4. Clear cache: `docker-compose build --no-cache`

### Cannot Push Docker Images

1. Check GITHUB_TOKEN permissions
2. Verify Container Registry is enabled
3. Check package visibility settings
4. Ensure workflow has `packages: write` permission

### Dependabot PRs Not Auto-Merging

1. Check branch protection rules allow auto-merge
2. Verify Dependabot has merge permissions
3. Check if update is major version (requires manual review)

---

## Best Practices

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add user authentication
fix: Resolve playlist generation bug
docs: Update API documentation
style: Format code with black
refactor: Simplify mood analysis logic
test: Add tests for curator service
chore: Update dependencies
ci: Update GitHub Actions workflow
```

### Pull Requests

- Keep PRs small and focused
- Link related issues
- Add tests for new features
- Update documentation
- Ensure CI passes before requesting review

### Code Review

- Review within 24-48 hours
- Test changes locally
- Check for security issues
- Verify documentation updates
- Approve or request changes

---

## Advanced Configuration

### Custom Workflow Jobs

Add custom jobs to `.github/workflows/`:

```yaml
name: Custom Job
on:
  push:
    branches: [ main ]

jobs:
  custom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Custom step
        run: echo "Custom logic here"
```

### Environment-Specific Deployments

Create deployment workflows for staging/production:

```yaml
name: Deploy to Production
on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://musicmood.app
    steps:
      - name: Deploy
        run: |
          # Deployment commands
```

### Matrix Testing

Test across multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

---

## Cost Optimization

GitHub Actions minutes are free for public repos, but for private repos:

### Optimize Build Times

1. **Use caching:**
   - Poetry dependencies
   - Docker layers
   - pip packages

2. **Parallelize jobs:**
   - Run independent jobs concurrently
   - Use matrix strategies

3. **Skip unnecessary runs:**
   - Use path filters
   - Skip CI for docs-only changes

### Example Path Filter

```yaml
on:
  push:
    paths:
      - 'app/**'
      - 'tests/**'
      - 'pyproject.toml'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

---

## Security

### Secrets Management

- Never commit secrets to repository
- Use GitHub encrypted secrets
- Rotate secrets periodically
- Use separate secrets for dev/staging/prod

### Dependency Security

- Dependabot auto-updates dependencies
- CodeQL scans for vulnerabilities
- Trivy scans Docker images
- Safety checks Python packages

### Supply Chain Security

- Pin action versions to commit SHAs
- Use verified actions from marketplace
- Review Dependabot PRs before merging
- Enable signed commits

---

## Support

For CI/CD issues:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Search [GitHub Actions docs](https://docs.github.com/actions)
4. Open an issue with `ci-cd` label
