"""
Threat Detector Module - Uses machine learning to detect network threats
"""
import os
import logging
import numpy as np
import tensorflow as tf

logger = logging.getLogger("CyberGuard.ml")

class ThreatDetector:
    """
    Machine learning-based threat detection system
    Uses TensorFlow to analyze network traffic patterns and identify potential threats
    """
    
    def __init__(self, model_path=None):
        """Initialize the threat detector"""
        self.model = None
        self.model_path = model_path or os.path.join(os.path.dirname(__file__), 'models', 'threat_model.h5')
        self.labels = ['normal', 'port_scan', 'dos', 'brute_force', 'malware']
        logger.info("Threat detector initialized")
    
    def load_model(self):
        """Load the pre-trained threat detection model"""
        try:
            # In a real implementation, this would load an actual trained model
            # For this demo, we'll just log that it would happen
            logger.info(f"Would load model from: {self.model_path}")
            
            # Simulating model loading
            logger.info("Model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False
    
    def preprocess_data(self, network_data):
        """
        Preprocess network data for model input
        
        Args:
            network_data: Raw network traffic data
            
        Returns:
            Preprocessed data ready for model input
        """
        # In a real implementation, this would transform raw network data
        # into features the model can understand
        logger.debug("Preprocessing network data")
        
        # Simulated preprocessing
        return np.array([[0.2, 0.1, 0.05, 0.3, 0.1, 0.25]])
    
    def detect_threats(self, network_data):
        """
        Analyze network data to detect potential threats
        
        Args:
            network_data: Network traffic data to analyze
            
        Returns:
            List of detected threats with confidence scores
        """
        logger.debug("Analyzing network data for threats")
        
        # Preprocess the data
        processed_data = self.preprocess_data(network_data)
        
        # In a real implementation, this would run inference on the model
        # For this demo, we'll simulate model predictions
        
        # Simulated model prediction (confidence scores for each threat class)
        predictions = np.array([[0.85, 0.03, 0.05, 0.02, 0.05]])
        
        # Convert predictions to threat information
        threats = []
        for i, pred in enumerate(predictions[0]):
            if pred > 0.1:  # Threshold for reporting
                threats.append({
                    'type': self.labels[i],
                    'confidence': float(pred),
                    'severity': self._calculate_severity(self.labels[i], pred)
                })
        
        return threats
    
    def _calculate_severity(self, threat_type, confidence):
        """Calculate threat severity based on type and confidence"""
        # Different threat types have different base severity levels
        base_severity = {
            'normal': 0,
            'port_scan': 0.5,
            'dos': 0.8,
            'brute_force': 0.7,
            'malware': 0.9
        }
        
        # Calculate severity score (0-1)
        severity_score = base_severity.get(threat_type, 0.5) * confidence
        
        # Convert to categorical severity
        if severity_score < 0.3:
            return "low"
        elif severity_score < 0.6:
            return "medium"
        else:
            return "high"
