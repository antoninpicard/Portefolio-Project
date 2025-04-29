#!/usr/bin/env python3
"""
SwarmDrone - WebSocket Bridge

This module creates a bridge between ROS and the web frontend using WebSockets.
It subscribes to relevant ROS topics and forwards the data to the web client.
"""

import rospy
import json
import threading
import numpy as np
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Path, Odometry
from std_msgs.msg import Bool, Float32MultiArray
import tf.transformations
import websocket_server
from websocket_server import WebsocketServer

class WebSocketBridge:
    """
    Bridge between ROS and WebSocket for communication with web frontend.
    """
    
    def __init__(self, num_drones=3, websocket_port=9090):
        """
        Initialize the WebSocket bridge.
        
        Args:
            num_drones: Number of drones in the swarm
            websocket_port: Port for the WebSocket server
        """
        rospy.init_node('websocket_bridge', anonymous=True)
        
        self.num_drones = num_drones
        self.websocket_port = websocket_port
        
        # Initialize WebSocket server
        self.server = WebsocketServer(host='0.0.0.0', port=websocket_port)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        
        # Start WebSocket server in a separate thread
        self.server_thread = threading.Thread(target=self.server.run_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Data storage for drone states
        self.drone_positions = np.zeros((num_drones, 3))
        self.drone_orientations = np.zeros((num_drones, 4))
        self.drone_velocities = np.zeros((num_drones, 3))
        self.drone_paths = [[] for _ in range(num_drones)]
        self.exploration_status = np.zeros(num_drones, dtype=bool)
        
        # Set up subscribers for drone data
        self.pose_subs = []
        self.path_subs = []
        
        for i in range(num_drones):
            # Subscribe to drone poses
            pose_sub = rospy.Subscriber(
                f'/drone_{i}/pose', 
                PoseStamped, 
                self.pose_callback, 
                callback_args=i
            )
            self.pose_subs.append(pose_sub)
            
            # Subscribe to drone planned paths
            path_sub = rospy.Subscriber(
                f'/drone_{i}/planned_path', 
                Path, 
                self.path_callback, 
                callback_args=i
            )
            self.path_subs.append(path_sub)
        
        # Subscribe to global exploration status
        rospy.Subscriber('/swarm/exploration_status', Float32MultiArray, self.status_callback)
        
        # Set up publisher for mission control commands from web client
        self.mission_pub = rospy.Publisher('/swarm/mission_control', Float32MultiArray, queue_size=10)
        
        # Timer for sending updates to clients
        self.update_timer = rospy.Timer(rospy.Duration(0.1), self.send_updates)
        
        rospy.loginfo("WebSocket bridge initialized on port %d", websocket_port)
    
    def new_client(self, client, server):
        """
        Callback for new WebSocket client connections.
        
        Args:
            client: Client information
            server: WebSocket server instance
        """
        rospy.loginfo("New client connected: %s", client['address'])
        
        # Send initial state to the new client
        self.send_initial_state(client)
    
    def client_left(self, client, server):
        """
        Callback for WebSocket client disconnections.
        
        Args:
            client: Client information
            server: WebSocket server instance
        """
        rospy.loginfo("Client disconnected: %s", client['address'])
    
    def message_received(self, client, server, message):
        """
        Callback for messages received from WebSocket clients.
        
        Args:
            client: Client information
            server: WebSocket server instance
            message: Message received from client
        """
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'mission_control':
                # Process mission control command
                command = data.get('command')
                params = data.get('params', [])
                
                rospy.loginfo("Received mission control command: %s", command)
                
                # Convert command to ROS message
                msg = Float32MultiArray()
                
                if command == 'set_exploration_area':
                    # Format: [0, x_min, y_min, z_min, x_max, y_max, z_max]
                    msg.data = [0.0] + params
                
                elif command == 'set_drone_goals':
                    # Format: [1, drone_id, x, y, z, drone_id, x, y, z, ...]
                    msg.data = [1.0] + params
                
                elif command == 'update_parameters':
                    # Format: [2, alpha, beta, gamma, delta]
                    msg.data = [2.0] + params
                
                # Publish to ROS
                self.mission_pub.publish(msg)
                
            elif message_type == 'request_state':
                # Client is requesting the current state
                self.send_initial_state(client)
        
        except json.JSONDecodeError:
            rospy.logwarn("Received invalid JSON message")
        except Exception as e:
            rospy.logerr("Error processing message: %s", str(e))
    
    def pose_callback(self, msg, drone_id):
        """
        Callback for drone pose updates.
        
        Args:
            msg: PoseStamped message containing drone position
            drone_id: ID of the drone
        """
        # Extract position and orientation from message
        position = msg.pose.position
        orientation = msg.pose.orientation
        
        self.drone_positions[drone_id] = [position.x, position.y, position.z]
        self.drone_orientations[drone_id] = [
            orientation.w, orientation.x, orientation.y, orientation.z
        ]
    
    def path_callback(self, msg, drone_id):
        """
        Callback for drone planned path updates.
        
        Args:
            msg: Path message containing planned path
            drone_id: ID of the drone
        """
        # Extract path points from message
        path_points = []
        
        for pose_stamped in msg.poses:
            pos = pose_stamped.pose.position
            path_points.append([pos.x, pos.y, pos.z])
        
        self.drone_paths[drone_id] = path_points
    
    def status_callback(self, msg):
        """
        Callback for global exploration status updates.
        
        Args:
            msg: Float32MultiArray containing exploration status
        """
        # Update exploration status
        for i in range(min(len(msg.data), self.num_drones)):
            self.exploration_status[i] = bool(msg.data[i])
    
    def send_initial_state(self, client):
        """
        Send the initial state to a newly connected client.
        
        Args:
            client: Client information
        """
        # Prepare initial state data
        state = {
            'type': 'initial_state',
            'num_drones': self.num_drones,
            'drone_positions': self.drone_positions.tolist(),
            'drone_orientations': self.drone_orientations.tolist(),
            'drone_paths': self.drone_paths,
            'exploration_status': self.exploration_status.tolist()
        }
        
        # Send to the client
        self.server.send_message(client, json.dumps(state))
    
    def send_updates(self, event):
        """
        Send periodic updates to all connected clients.
        
        Args:
            event: Timer event
        """
        # Prepare update data
        update = {
            'type': 'state_update',
            'drone_positions': self.drone_positions.tolist(),
            'drone_orientations': self.drone_orientations.tolist(),
            'drone_paths': self.drone_paths,
            'exploration_status': self.exploration_status.tolist(),
            'timestamp': rospy.Time.now().to_sec()
        }
        
        # Send to all clients
        self.server.send_message_to_all(json.dumps(update))

if __name__ == '__main__':
    try:
        bridge = WebSocketBridge(num_drones=3)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
