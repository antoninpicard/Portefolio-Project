"""
Network Monitor Module - Monitors network traffic and detects anomalies
"""
import logging
import threading
import time
import random

logger = logging.getLogger("CyberGuard.network")

class NetworkMonitor:
    """
    Network monitoring system that captures and analyzes network traffic
    Integrates with the threat detector to identify potential security issues
    """
    
    def __init__(self, threat_detector):
        """
        Initialize the network monitor
        
        Args:
            threat_detector: Instance of ThreatDetector for analyzing traffic
        """
        self.threat_detector = threat_detector
        self.is_monitoring = False
        self.monitor_thread = None
        self.devices = {}  # Connected devices cache
        logger.info("Network monitor initialized")
    
    def start_monitoring(self):
        """Start the network monitoring process in a background thread"""
        if self.is_monitoring:
            logger.warning("Network monitoring already running")
            return False
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        logger.info("Network monitoring started")
        return True
    
    def stop_monitoring(self):
        """Stop the network monitoring process"""
        if not self.is_monitoring:
            logger.warning("Network monitoring not running")
            return False
        
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        logger.info("Network monitoring stopped")
        return True
    
    def _monitoring_loop(self):
        """Main monitoring loop that runs in a background thread"""
        logger.info("Monitoring loop started")
        
        while self.is_monitoring:
            try:
                # Scan for connected devices
                self._scan_devices()
                
                # Capture and analyze network traffic
                network_data = self._capture_traffic()
                if network_data:
                    threats = self.threat_detector.detect_threats(network_data)
                    self._handle_threats(threats)
                
                # Sleep before next scan
                time.sleep(10)  # Scan every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(30)  # Longer sleep on error
    
    def _scan_devices(self):
        """Scan the network for connected devices"""
        # In a real implementation, this would use tools like nmap or ARP scanning
        # For this demo, we'll simulate finding devices
        
        # Simulated device discovery
        logger.debug("Scanning for connected devices")
        
        # Update device cache with simulated data
        self.devices = {
            "192.168.1.101": {"mac": "AA:BB:CC:11:22:33", "name": "Living Room TV", "status": "safe"},
            "192.168.1.102": {"mac": "AA:BB:CC:11:22:44", "name": "Kitchen Tablet", "status": "safe"},
            "192.168.1.103": {"mac": "AA:BB:CC:11:22:55", "name": "Home Office PC", "status": "safe"},
            "192.168.1.104": {"mac": "AA:BB:CC:11:22:66", "name": "Unknown Device", "status": "unknown"}
        }
        
        # Randomly add or remove a device to simulate network changes
        if random.random() < 0.1:  # 10% chance
            if random.random() < 0.5:  # 50% chance to add
                new_ip = f"192.168.1.{random.randint(105, 150)}"
                self.devices[new_ip] = {
                    "mac": f"AA:BB:CC:11:{random.randint(10, 99)}:{random.randint(10, 99)}",
                    "name": "New Device",
                    "status": "unknown"
                }
                logger.info(f"New device detected: {new_ip}")
            else:  # 50% chance to remove
                if len(self.devices) > 1:
                    ip_to_remove = random.choice(list(self.devices.keys()))
                    del self.devices[ip_to_remove]
                    logger.info(f"Device disconnected: {ip_to_remove}")
    
    def _capture_traffic(self):
        """Capture network traffic for analysis"""
        # In a real implementation, this would use packet capture libraries
        # For this demo, we'll simulate network traffic data
        
        logger.debug("Capturing network traffic")
        
        # Simulated network traffic data
        # This would be much more complex in a real implementation
        traffic_data = {
            "timestamp": time.time(),
            "flows": [
                {
                    "source_ip": "192.168.1.103",
                    "dest_ip": "142.250.180.78",  # Google
                    "source_port": 52413,
                    "dest_port": 443,
                    "protocol": "TCP",
                    "bytes_sent": 1420,
                    "bytes_received": 4270
                },
                {
                    "source_ip": "192.168.1.101",
                    "dest_ip": "23.23.86.44",  # Streaming service
                    "source_port": 59321,
                    "dest_port": 443,
                    "protocol": "TCP",
                    "bytes_sent": 8240,
                    "bytes_received": 1572864
                }
            ]
        }
        
        # Occasionally inject suspicious traffic for testing
        if random.random() < 0.05:  # 5% chance
            suspicious_traffic = {
                "source_ip": "192.168.1.104",
                "dest_ip": "192.168.1.1",  # Router
                "source_port": random.randint(50000, 60000),
                "dest_port": 22,  # SSH
                "protocol": "TCP",
                "bytes_sent": 320,
                "bytes_received": 120,
                "flags": ["SYN"]  # Port scanning behavior
            }
            traffic_data["flows"].append(suspicious_traffic)
            logger.debug("Suspicious traffic detected in capture")
        
        return traffic_data
    
    def _handle_threats(self, threats):
        """Handle detected threats"""
        if not threats:
            return
        
        for threat in threats:
            if threat['type'] == 'normal':
                continue
                
            logger.warning(f"Threat detected: {threat['type']} (Confidence: {threat['confidence']:.2f}, Severity: {threat['severity']})")
            
            # In a real implementation, this would trigger alerts, block traffic, etc.
            # For this demo, we'll just log the threat
            
            # Update device status if applicable
            for ip, device in self.devices.items():
                if random.random() < 0.8:  # 80% chance to associate with the unknown device
                    self.devices[ip]["status"] = "suspicious"
                    logger.info(f"Device {ip} marked as suspicious")
