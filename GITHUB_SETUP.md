# GitHub Setup Instructions

## Steps to upload project to GitHub:

### 1. Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Repository name: `simple-port-checker`
4. Description: `Optimized and secure Flask service for checking port availability`
5. Make it Public or Private (your choice)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these files)
7. Click "Create repository"

### 2. Connect and Push to GitHub
After creating the repository, run these commands:

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/cyberc00n/simple-port-checker.git

# Push to GitHub
git push -u origin main
```

### 3. Verify Upload
- Go to your GitHub repository
- Check that all files are uploaded correctly
- Verify README.md is displayed properly

## Repository Structure
```
simple-port-checker/
├── README.md              # Project documentation
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Optimized Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .dockerignore         # Docker ignore patterns
├── .gitignore           # Git ignore patterns
├── env.example          # Environment variables example
└── GITHUB_SETUP.md      # This file
```

## Docker Hub Integration
The project is already available on Docker Hub:
- **Repository**: `cybercoon90/simple-port-checker`
- **Latest**: `cybercoon90/simple-port-checker:latest`
- **Version 1.1.0**: `cybercoon90/simple-port-checker:v1.1.0`

## Features
- ✅ Optimized Docker image (86MB)
- ✅ Python 3.12 with security fixes
- ✅ Multi-stage build
- ✅ Non-root user for security
- ✅ Rate limiting and authentication
- ✅ Health check endpoint
- ✅ English localization 