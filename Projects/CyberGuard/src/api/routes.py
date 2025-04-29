"""
API Routes for CyberGuard
"""
import logging
from flask import Blueprint, jsonify, request

logger = logging.getLogger("CyberGuard.api")

# Create blueprints for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def register_routes(app):
    """Register all API routes with the Flask app"""
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    
    logger.info("API routes registered")

# API endpoints for network status
@api_bp.route('/status', methods=['GET'])
def get_network_status():
    """Get the current network status"""
    return jsonify({
        "status": "healthy",
        "devices_connected": 12,
        "threats_detected": 0,
        "last_scan": "2025-04-28T09:30:45Z"
    })

@api_bp.route('/devices', methods=['GET'])
def get_connected_devices():
    """Get a list of all connected devices"""
    # In a real implementation, this would query the actual network
    devices = [
        {"id": "dev1", "name": "Living Room TV", "ip": "192.168.1.101", "status": "safe"},
        {"id": "dev2", "name": "Kitchen Tablet", "ip": "192.168.1.102", "status": "safe"},
        {"id": "dev3", "name": "Home Office PC", "ip": "192.168.1.103", "status": "safe"},
        {"id": "dev4", "name": "Unknown Device", "ip": "192.168.1.104", "status": "suspicious"}
    ]
    return jsonify({"devices": devices})

@api_bp.route('/threats', methods=['GET'])
def get_threats():
    """Get a list of detected threats"""
    threats = [
        {
            "id": "threat1",
            "timestamp": "2025-04-28T08:15:22Z",
            "device_id": "dev4",
            "type": "port_scan",
            "severity": "medium",
            "details": "Multiple port scan attempts detected"
        }
    ]
    return jsonify({"threats": threats})

# Authentication endpoints
@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    # This is a simplified example - real implementation would validate credentials
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    # Simulate successful login
    return jsonify({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example-token",
        "user": {"username": data['username'], "role": "admin"}
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    return jsonify({"message": "Logged out successfully"})
