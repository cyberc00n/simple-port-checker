# Simple Port Checker API

🚀 **Optimized and secure** Flask service for checking port 80 and 443 availability on IP addresses.

## ✨ Features

- ✅ Port 80 and 443 availability check
- ✅ IP address validation (IPv4 only)
- ✅ JSON API for integration
- ✅ Token authentication
- ✅ Rate limiting
- ✅ Docker support
- ✅ Environment variables
- ✅ Logging
- ✅ **Optimized Docker image (86MB)**
- ✅ **Security: Python 3.12, non-root user**

## 🐳 Docker Hub

Image available on Docker Hub: **`cybercoon90/simple-port-checker`**

```bash
# Run latest version
docker run -p 8080:8080 cybercoon90/simple-port-checker:latest

# Run specific version
docker run -p 8080:8080 cybercoon90/simple-port-checker:v1.0.0

# With environment variables
docker run -p 8080:8080 \
  -e API_TOKEN="your-secret-token" \
  -e PORT_CHECK_TIMEOUT=10 \
  cybercoon90/simple-port-checker:latest
```

## 📦 Installation

### Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker Compose

```bash
cp env.example .env
# Edit .env with your settings
docker-compose up -d
```

### Docker (local build)

```bash
docker build -t simple-port-checker .
docker run -p 8080:8080 --env-file .env simple-port-checker
```

## 🚀 Usage

### Local

```bash
source venv/bin/activate
export API_TOKEN="your-secret-token"
python app.py
```

### Docker

```bash
docker-compose up -d
# or
docker run -p 8080:8080 --env-file .env cybercoon90/simple-port-checker:latest
```

Service will be available at: http://localhost:8080

## 🔌 API Endpoints

### GET /
API information

### GET /health
Service health check (no authentication required)

### GET /check
Check ports on localhost (requires authentication)

### GET /check/<ip>
Check ports on specified IP (requires authentication)

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/check/8.8.8.8
```

**Response:**
```json
{
  "host": "8.8.8.8",
  "timestamp": "2024-01-15T10:30:00.123456",
  "ports": {
    "80": {"open": true, "status": "open"},
    "443": {"open": true, "status": "open"}
  },
  "summary": {
    "all_open": true,
    "any_open": true
  }
}
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Host to bind | `0.0.0.0` |
| `PORT` | Port to bind | `8080` |
| `FLASK_ENV` | Flask environment | `production` |
| `API_TOKEN` | Authentication token | - |
| `PORTS_TO_CHECK` | Ports to check (comma-separated) | `80,443` |
| `RATE_LIMIT_REQUESTS` | Rate limit requests | `100` |
| `RATE_LIMIT_WINDOW` | Rate limit window (seconds) | `3600` |
| `PORT_CHECK_TIMEOUT` | Port check timeout (seconds) | `5` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🔒 Security

- All endpoints (except `/health`) require Bearer token authentication
- Rate limiting: 50 requests per hour, 200 per day
- Only IPv4 addresses are accepted
- Configure firewall to restrict access
- **Docker image runs as non-root user**
- **Uses Python 3.12 with security fixes**

## 🐳 Docker Optimizations

### Image size: 86MB (18% reduction compared to previous version)

**Key optimizations:**
- ✅ Python 3.12 (more secure and efficient)
- ✅ Multi-stage build
- ✅ Alpine virtual packages (auto-cleanup of build dependencies)
- ✅ Docker layer optimization
- ✅ `.dockerignore` to exclude unnecessary files
- ✅ Non-root user for security
- ✅ Minimal runtime dependencies

### Image layers:
- Alpine Linux: ~8.51MB
- Python 3.12: ~43.3MB
- Application dependencies: ~27.8MB
- Runtime dependencies: ~5.36MB
- Application code: ~6.87kB

## 📋 Requirements

- Python 3.12+
- Flask 3.0.0+
- Docker (optional)

## 🔄 Versioning

- `latest` - latest stable version
- `v1.1.0` - version 1.1.0 with English localization
- `v1.0.0` - version 1.0.0 with security optimizations 