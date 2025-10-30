# Deployment Guide

## GitHub-Only CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment without external cloud services.

## Available Workflows

### 1. Main CI/CD Pipeline (`.github/workflows/ci-cd.yml`)
- **Triggers**: Push to `main`/`develop`, Pull requests to `main`
- **Features**:
  - Code linting and testing
  - GitHub Pages deployment
  - Automated releases

### 2. Local Deployment Package (`.github/workflows/local-deploy.yml`)
- **Triggers**: Push to `main`, Manual trigger
- **Creates**: Ready-to-run deployment packages with setup scripts

### 3. GitHub Releases (`.github/workflows/github-releases.yml`)
- **Triggers**: Git tags (`v*`), Manual trigger
- **Creates**: Release packages with installation scripts

## Local Deployment Options

### Option 1: Quick Start Scripts

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Windows:**
```cmd
deploy.bat
```

### Option 2: Manual Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_actual_api_key" > .env
```

4. **Run application:**
```bash
python app.py
```

## GitHub Deployment Features

### GitHub Pages
- Automatically deploys to GitHub Pages on push to `main`
- Accessible at: `https://username.github.io/repository-name`

### GitHub Releases
- Creates downloadable packages
- Includes setup scripts for all platforms
- Version-tagged releases

### Artifacts
- Build artifacts stored for 30 days
- Downloadable deployment packages
- Automated packaging with dependencies

## Environment Variables

Required environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key

## Repository Secrets

Add these secrets in GitHub repository settings:
- `GEMINI_API_KEY`: Your API key for production deployment

## Deployment Process

1. **Development**: Work on `develop` branch
2. **Testing**: Create PR to `main` (triggers tests)
3. **Release**: Merge to `main` (triggers deployment)
4. **Versioning**: Create git tag for releases

## Local Development

```bash
git clone <repository-url>
cd <repository-name>
./deploy.sh  # or deploy.bat on Windows
```

## Troubleshooting

- Ensure Python 3.9+ is installed
- Check that all dependencies install correctly
- Verify API keys are set properly
- Check GitHub Actions logs for deployment issues