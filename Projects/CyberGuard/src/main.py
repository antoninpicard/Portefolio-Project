#!/usr/bin/env python3
"""
CyberGuard - Main Application Entry Point
"""
import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

# Import CyberGuard modules
from api.routes import register_routes
from network.monitor import NetworkMonitor
from ml.threat_detector import ThreatDetector

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("cyberguard.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CyberGuard")

def create_app():
    """Initialize and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Register API routes
    register_routes(app)
    
    # Add error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

def main():
    """Main application entry point"""
    logger.info("Starting CyberGuard...")
    
    # Initialize threat detection model
    threat_detector = ThreatDetector()
    threat_detector.load_model()
    
    # Initialize network monitor
    network_monitor = NetworkMonitor(threat_detector)
    network_monitor.start_monitoring()
    
    # Start the API server
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    
    logger.info(f"CyberGuard API server running on port {port}")

if __name__ == "__main__":
    main()
