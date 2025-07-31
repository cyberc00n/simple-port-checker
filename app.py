from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import socket
import threading
import time
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def check_port(host, port, timeout=None):
    """
    Check port availability on specified host
    """
    if timeout is None:
        timeout = int(os.getenv('PORT_CHECK_TIMEOUT', 5))
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        logger.warning(f"Error checking port {port} on {host}: {e}")
        return False

def validate_token():
    """
    Validate token from Authorization header
    """
    api_token = os.getenv('API_TOKEN')
    if not api_token:
        logger.warning("API_TOKEN not set in environment variables")
        return False
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    
    # Support "Bearer <token>" or just "<token>" format
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
    else:
        token = auth_header
    
    return token == api_token

def validate_ip(host):
    """
    Check if host is a valid IP address
    """
    import re
    # Simple IPv4 validation
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, host):
        # Check each octet is in range 0-255
        octets = host.split('.')
        for octet in octets:
            if not (0 <= int(octet) <= 255):
                return False
        return True
    return False

@app.route('/')
def index():
    """
    Simple API info
    """
    ports_to_check = get_ports_to_check()
    return jsonify({
        'service': 'port-checker',
        'version': '1.0.0',
        'endpoints': {
            'health': 'GET /health - Service health check',
            'check_localhost': 'GET /check - Check ports on localhost (requires auth)',
            'check_ip': 'GET /check/<ip> - Check ports on specified IP (requires auth)'
        },
        'authentication': 'Bearer token required in Authorization header',
        'rate_limits': '50 requests per hour, 200 per day',
        'ports_to_check': ports_to_check
    })

@app.route('/check')
@limiter.limit("50 per hour")
def check_ports():
    """
    Check ports 80 and 443 on localhost
    """
    # Authentication check
    if not validate_token():
        logger.warning(f"Unauthorized access to /check from IP {request.remote_addr}")
        return jsonify({'error': 'Unauthorized'}), 401
    
    return check_ports_for_host('localhost')

def get_ports_to_check():
    """
    Get list of ports to check from environment variable
    """
    ports_str = os.getenv('PORTS_TO_CHECK', '80,443')
    try:
        ports = [int(port.strip()) for port in ports_str.split(',')]
        # Validate port range
        valid_ports = [port for port in ports if 1 <= port <= 65535]
        if not valid_ports:
            logger.warning("No valid ports found, using default: 80,443")
            return [80, 443]
        return valid_ports
    except ValueError:
        logger.warning("Invalid PORTS_TO_CHECK format, using default: 80,443")
        return [80, 443]

@app.route('/check/<host>')
@limiter.limit("50 per hour")
def check_ports_for_host(host):
    """
    Check configured ports on specified host
    """
    # Authentication check
    if not validate_token():
        logger.warning(f"Unauthorized access to /check/{host} from IP {request.remote_addr}")
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Check if host is a valid IP address
    if not validate_ip(host):
        logger.warning(f"Attempt to check non-IP address: {host} from IP {request.remote_addr}")
        return jsonify({
            'error': 'Only IP addresses are allowed',
            'host': host,
            'timestamp': datetime.now().isoformat()
        }), 403
    
    try:
        logger.info(f"Checking ports for {host} from IP {request.remote_addr}")
        
        # Get ports to check
        ports_to_check = get_ports_to_check()
        
        # Check each port
        port_results = {}
        all_open = True
        any_open = False
        
        for port in ports_to_check:
            port_open = check_port(host, port)
            port_results[str(port)] = {
                'open': port_open,
                'status': 'open' if port_open else 'closed'
            }
            all_open = all_open and port_open
            any_open = any_open or port_open
        
        result = {
            'host': host,
            'timestamp': datetime.now().isoformat(),
            'ports': port_results,
            'summary': {
                'all_open': all_open,
                'any_open': any_open
            }
        }
        
        logger.info(f"Port check result for {host}: {port_results}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error checking {host}: {e}")
        return jsonify({
            'error': str(e),
            'host': host,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health_check():
    """
    Service health check
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'port-checker',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("🚀 Starting Port Checker API...")
    print("📡 Available endpoints:")
    print("   - GET /          - API info")
    print("   - GET /check     - Check ports on localhost")
    print("   - GET /check/<ip> - Check ports on specified IP")
    print("   - GET /health    - Service health check")
    print(f"🌐 Service will be available at: http://{host}:{port}")
    print(f"🔧 Debug mode: {'Enabled' if debug else 'Disabled'}")
    
    if os.getenv('API_TOKEN'):
        print("🔐 Authentication: Enabled")
    else:
        print("⚠️  WARNING: API_TOKEN not set! Authentication disabled.")
    
    app.run(host=host, port=port, debug=debug) 