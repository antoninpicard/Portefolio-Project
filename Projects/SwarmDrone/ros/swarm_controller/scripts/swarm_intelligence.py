#!/usr/bin/env python3
"""
SwarmDrone - Swarm Intelligence Algorithm

This module implements the core swarm intelligence algorithms for coordinating
multiple drones in a collaborative mapping mission.
"""

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Path
from std_msgs.msg import Bool, Float32MultiArray
import tf.transformations

class SwarmIntelligence:
    """
    Implements swarm intelligence algorithms for drone coordination.
    Uses a combination of particle swarm optimization and potential field methods
    to coordinate drone movements while ensuring collision avoidance.
    """
    
    def __init__(self, num_drones=3, comm_range=10.0, safe_distance=2.0):
        """
        Initialize the swarm intelligence controller.
        
        Args:
            num_drones: Number of drones in the swarm
            comm_range: Maximum communication range between drones (meters)
            safe_distance: Minimum safe distance between drones (meters)
        """
        rospy.init_node('swarm_intelligence', anonymous=True)
        
        self.num_drones = num_drones
        self.comm_range = comm_range
        self.safe_distance = safe_distance
        
        # Drone state tracking
        self.drone_positions = np.zeros((num_drones, 3))  # x, y, z positions
        self.drone_velocities = np.zeros((num_drones, 3))  # vx, vy, vz velocities
        self.drone_goals = np.zeros((num_drones, 3))  # Goal positions
        self.exploration_status = np.zeros(num_drones, dtype=bool)  # Exploration completion status
        
        # Algorithm parameters
        self.alpha = 1.0  # Goal attraction weight
        self.beta = 2.0   # Collision avoidance weight
        self.gamma = 0.5  # Swarm cohesion weight
        self.delta = 0.1  # Velocity damping factor
        
        # Set up publishers and subscribers
        self.position_subs = []
        self.velocity_pubs = []
        self.path_pubs = []
        
        for i in range(num_drones):
            # Subscribe to drone positions
            sub = rospy.Subscriber(
                f'/drone_{i}/pose', 
                PoseStamped, 
                self.position_callback, 
                callback_args=i
            )
            self.position_subs.append(sub)
            
            # Publishers for velocity commands
            pub = rospy.Publisher(
                f'/drone_{i}/cmd_vel', 
                Twist, 
                queue_size=10
            )
            self.velocity_pubs.append(pub)
            
            # Publishers for planned paths
            path_pub = rospy.Publisher(
                f'/drone_{i}/planned_path', 
                Path, 
                queue_size=10
            )
            self.path_pubs.append(path_pub)
        
        # Global map and exploration status
        self.map_pub = rospy.Publisher('/swarm/global_map', Float32MultiArray, queue_size=10)
        self.status_pub = rospy.Publisher('/swarm/exploration_status', Float32MultiArray, queue_size=10)
        
        # Subscribe to mission control commands
        rospy.Subscriber('/swarm/mission_control', Float32MultiArray, self.mission_callback)
        
        rospy.loginfo("Swarm Intelligence initialized with %d drones", num_drones)
    
    def position_callback(self, msg, drone_id):
        """
        Callback for drone position updates.
        
        Args:
            msg: PoseStamped message containing drone position
            drone_id: ID of the drone
        """
        # Extract position from message
        position = msg.pose.position
        self.drone_positions[drone_id] = [position.x, position.y, position.z]
        
        # Run the swarm algorithm whenever we get a position update
        self.update_swarm_behavior()
    
    def mission_callback(self, msg):
        """
        Callback for mission control commands.
        
        Args:
            msg: Float32MultiArray containing mission parameters or goals
        """
        data = np.array(msg.data)
        
        # Parse mission command
        command_type = int(data[0])
        
        if command_type == 0:  # Set new exploration area
            # Format: [0, x_min, y_min, z_min, x_max, y_max, z_max]
            self.exploration_area = data[1:7]
            self.generate_exploration_goals()
            rospy.loginfo("New exploration area set")
            
        elif command_type == 1:  # Set specific drone goals
            # Format: [1, drone_id, x, y, z, drone_id, x, y, z, ...]
            for i in range(1, len(data), 4):
                drone_id = int(data[i])
                if 0 <= drone_id < self.num_drones:
                    self.drone_goals[drone_id] = data[i+1:i+4]
            rospy.loginfo("New drone goals set")
            
        elif command_type == 2:  # Update algorithm parameters
            # Format: [2, alpha, beta, gamma, delta]
            if len(data) >= 5:
                self.alpha = data[1]  # Goal attraction
                self.beta = data[2]   # Collision avoidance
                self.gamma = data[3]  # Swarm cohesion
                self.delta = data[4]  # Velocity damping
                rospy.loginfo("Algorithm parameters updated")
    
    def generate_exploration_goals(self):
        """
        Generate exploration goals for the drones based on the current exploration area.
        Uses a space-filling curve approach to distribute drones efficiently.
        """
        if not hasattr(self, 'exploration_area'):
            rospy.logwarn("Exploration area not set")
            return
            
        x_min, y_min, z_min, x_max, y_max, z_max = self.exploration_area
        
        # Simple distribution: divide the space into equal parts
        # In a real implementation, this would use a more sophisticated algorithm
        for i in range(self.num_drones):
            # Distribute drones along a 3D grid
            x_step = (x_max - x_min) / max(1, self.num_drones // 2)
            y_step = (y_max - y_min) / max(1, self.num_drones // 2)
            
            x = x_min + (i % 2) * x_step
            y = y_min + ((i // 2) % 2) * y_step
            z = z_min + (z_max - z_min) * 0.5  # Middle height
            
            self.drone_goals[i] = [x, y, z]
        
        rospy.loginfo("Generated exploration goals for %d drones", self.num_drones)
    
    def update_swarm_behavior(self):
        """
        Update the swarm behavior based on current positions and goals.
        Calculates new velocities for each drone using the swarm algorithm.
        """
        for i in range(self.num_drones):
            # Skip if we don't have a goal for this drone
            if np.all(self.drone_goals[i] == 0):
                continue
                
            # Calculate vector to goal (attraction force)
            goal_vector = self.drone_goals[i] - self.drone_positions[i]
            distance_to_goal = np.linalg.norm(goal_vector)
            
            if distance_to_goal < 0.5:  # Goal reached threshold
                # Goal reached, stop the drone
                self.send_velocity_command(i, [0, 0, 0])
                self.exploration_status[i] = True
                continue
            
            # Normalize goal vector
            if distance_to_goal > 0:
                goal_vector = goal_vector / distance_to_goal
            
            # Initialize the combined force vector with the goal attraction
            force_vector = self.alpha * goal_vector
            
            # Add collision avoidance (repulsion from other drones)
            for j in range(self.num_drones):
                if i == j:
                    continue
                    
                # Vector from this drone to the other drone
                separation_vector = self.drone_positions[i] - self.drone_positions[j]
                distance = np.linalg.norm(separation_vector)
                
                # Only consider drones within communication range
                if distance < self.comm_range:
                    # Calculate repulsion force (stronger as drones get closer)
                    if distance < self.safe_distance:
                        # Normalize separation vector
                        if distance > 0:
                            separation_vector = separation_vector / distance
                        
                        # Repulsion force inversely proportional to distance
                        repulsion_magnitude = self.beta * (1.0 - distance / self.safe_distance)
                        force_vector += repulsion_magnitude * separation_vector
            
            # Add swarm cohesion (attraction to center of nearby drones)
            nearby_drones = 0
            center_position = np.zeros(3)
            
            for j in range(self.num_drones):
                if i == j:
                    continue
                    
                distance = np.linalg.norm(self.drone_positions[i] - self.drone_positions[j])
                
                if distance < self.comm_range:
                    center_position += self.drone_positions[j]
                    nearby_drones += 1
            
            if nearby_drones > 0:
                center_position /= nearby_drones
                cohesion_vector = center_position - self.drone_positions[i]
                distance_to_center = np.linalg.norm(cohesion_vector)
                
                if distance_to_center > 0:
                    cohesion_vector = cohesion_vector / distance_to_center
                
                force_vector += self.gamma * cohesion_vector
            
            # Calculate new velocity (with damping)
            new_velocity = (1 - self.delta) * self.drone_velocities[i] + self.delta * force_vector
            
            # Normalize and scale velocity
            velocity_magnitude = np.linalg.norm(new_velocity)
            if velocity_magnitude > 1.0:
                new_velocity = new_velocity / velocity_magnitude
            
            # Update stored velocity
            self.drone_velocities[i] = new_velocity
            
            # Send velocity command to the drone
            self.send_velocity_command(i, new_velocity)
            
            # Generate and publish the planned path
            self.publish_planned_path(i)
        
        # Publish global status
        self.publish_status()
    
    def send_velocity_command(self, drone_id, velocity):
        """
        Send velocity command to a drone.
        
        Args:
            drone_id: ID of the drone
            velocity: 3D velocity vector [vx, vy, vz]
        """
        cmd = Twist()
        cmd.linear.x = velocity[0]
        cmd.linear.y = velocity[1]
        cmd.linear.z = velocity[2]
        
        self.velocity_pubs[drone_id].publish(cmd)
    
    def publish_planned_path(self, drone_id):
        """
        Publish the planned path for a drone.
        
        Args:
            drone_id: ID of the drone
        """
        path = Path()
        path.header.stamp = rospy.Time.now()
        path.header.frame_id = "map"
        
        # Start with current position
        current_pos = PoseStamped()
        current_pos.header = path.header
        current_pos.pose.position.x = self.drone_positions[drone_id][0]
        current_pos.pose.position.y = self.drone_positions[drone_id][1]
        current_pos.pose.position.z = self.drone_positions[drone_id][2]
        path.poses.append(current_pos)
        
        # Simple linear path to goal
        goal_pos = PoseStamped()
        goal_pos.header = path.header
        goal_pos.pose.position.x = self.drone_goals[drone_id][0]
        goal_pos.pose.position.y = self.drone_goals[drone_id][1]
        goal_pos.pose.position.z = self.drone_goals[drone_id][2]
        path.poses.append(goal_pos)
        
        self.path_pubs[drone_id].publish(path)
    
    def publish_status(self):
        """
        Publish the global exploration status.
        """
        status_msg = Float32MultiArray()
        status_msg.data = self.exploration_status.astype(float).tolist()
        self.status_pub.publish(status_msg)
        
        # Calculate and publish completion percentage
        completion = np.mean(self.exploration_status) * 100
        rospy.loginfo("Exploration progress: %.1f%%", completion)

if __name__ == '__main__':
    try:
        swarm = SwarmIntelligence(num_drones=3)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
