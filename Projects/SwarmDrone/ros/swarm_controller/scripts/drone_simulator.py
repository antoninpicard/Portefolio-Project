#!/usr/bin/env python3
"""
SwarmDrone - Drone Simulator

This module simulates multiple drones for testing the swarm intelligence algorithms
without requiring physical hardware.
"""

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool
import tf.transformations
import random

class DroneSimulator:
    """
    Simulates the physics and behavior of multiple drones in a 3D environment.
    """
    
    def __init__(self, num_drones=3, update_rate=30):
        """
        Initialize the drone simulator.
        
        Args:
            num_drones: Number of drones to simulate
            update_rate: Simulation update rate in Hz
        """
        rospy.init_node('drone_simulator', anonymous=True)
        
        self.num_drones = num_drones
        self.update_rate = update_rate
        self.rate = rospy.Rate(update_rate)
        
        # Physics parameters
        self.max_velocity = 2.0  # m/s
        self.max_acceleration = 1.0  # m/s^2
        self.drag_coefficient = 0.1
        
        # Drone state
        self.positions = np.zeros((num_drones, 3))  # x, y, z positions
        self.velocities = np.zeros((num_drones, 3))  # vx, vy, vz velocities
        self.accelerations = np.zeros((num_drones, 3))  # ax, ay, az accelerations
        self.orientations = np.zeros((num_drones, 4))  # Quaternions (w, x, y, z)
        
        # Initialize drone positions in a grid formation
        spacing = 2.0  # meters between drones
        grid_size = int(np.ceil(np.sqrt(num_drones)))
        
        for i in range(num_drones):
            row = i // grid_size
            col = i % grid_size
            self.positions[i] = [col * spacing, row * spacing, 1.0]  # 1m above ground
            
            # Initialize with identity quaternion (no rotation)
            self.orientations[i] = [1.0, 0.0, 0.0, 0.0]
        
        # Set up publishers and subscribers
        self.pose_pubs = []
        self.odom_pubs = []
        self.cmd_vel_subs = []
        
        for i in range(num_drones):
            # Publishers for drone pose
            pose_pub = rospy.Publisher(
                f'/drone_{i}/pose', 
                PoseStamped, 
                queue_size=10
            )
            self.pose_pubs.append(pose_pub)
            
            # Publishers for drone odometry
            odom_pub = rospy.Publisher(
                f'/drone_{i}/odom', 
                Odometry, 
                queue_size=10
            )
            self.odom_pubs.append(odom_pub)
            
            # Subscribers for velocity commands
            cmd_vel_sub = rospy.Subscriber(
                f'/drone_{i}/cmd_vel', 
                Twist, 
                self.cmd_vel_callback, 
                callback_args=i
            )
            self.cmd_vel_subs.append(cmd_vel_sub)
        
        rospy.loginfo("Drone simulator initialized with %d drones", num_drones)
    
    def cmd_vel_callback(self, msg, drone_id):
        """
        Callback for velocity commands.
        
        Args:
            msg: Twist message containing velocity command
            drone_id: ID of the drone
        """
        # Extract linear velocity from message
        vx = msg.linear.x
        vy = msg.linear.y
        vz = msg.linear.z
        
        # Calculate acceleration based on desired velocity
        desired_velocity = np.array([vx, vy, vz])
        
        # Limit desired velocity
        velocity_magnitude = np.linalg.norm(desired_velocity)
        if velocity_magnitude > self.max_velocity:
            desired_velocity = desired_velocity * self.max_velocity / velocity_magnitude
        
        # Calculate acceleration to reach desired velocity
        acceleration = (desired_velocity - self.velocities[drone_id]) * 2.0
        
        # Limit acceleration
        accel_magnitude = np.linalg.norm(acceleration)
        if accel_magnitude > self.max_acceleration:
            acceleration = acceleration * self.max_acceleration / accel_magnitude
        
        # Set the drone's acceleration
        self.accelerations[drone_id] = acceleration
        
        # Update orientation based on velocity direction
        if velocity_magnitude > 0.1:
            # Calculate orientation to align with velocity direction
            direction = desired_velocity / velocity_magnitude
            
            # Calculate quaternion to align with direction vector
            # This is a simplified approach - in a real implementation, 
            # we would use a more sophisticated orientation control
            z_axis = np.array([0, 0, 1])
            axis = np.cross(z_axis, direction)
            axis_norm = np.linalg.norm(axis)
            
            if axis_norm > 1e-6:
                axis = axis / axis_norm
                angle = np.arccos(np.dot(z_axis, direction))
                qx = axis[0] * np.sin(angle/2)
                qy = axis[1] * np.sin(angle/2)
                qz = axis[2] * np.sin(angle/2)
                qw = np.cos(angle/2)
                
                self.orientations[drone_id] = [qw, qx, qy, qz]
    
    def update_physics(self, dt):
        """
        Update the physics simulation for all drones.
        
        Args:
            dt: Time step in seconds
        """
        for i in range(self.num_drones):
            # Apply drag force
            drag = -self.drag_coefficient * self.velocities[i]
            self.accelerations[i] += drag
            
            # Update velocity
            self.velocities[i] += self.accelerations[i] * dt
            
            # Update position
            self.positions[i] += self.velocities[i] * dt
            
            # Add some noise to simulate real-world conditions
            position_noise = np.random.normal(0, 0.01, 3)  # Small position noise
            velocity_noise = np.random.normal(0, 0.005, 3)  # Small velocity noise
            
            self.positions[i] += position_noise
            self.velocities[i] += velocity_noise
            
            # Ensure drones don't go below ground
            if self.positions[i][2] < 0:
                self.positions[i][2] = 0
                self.velocities[i][2] = max(0, self.velocities[i][2])
            
            # Reset acceleration for next cycle
            self.accelerations[i] = np.zeros(3)
    
    def publish_drone_states(self):
        """
        Publish the current state of all drones.
        """
        current_time = rospy.Time.now()
        
        for i in range(self.num_drones):
            # Publish pose
            pose_msg = PoseStamped()
            pose_msg.header.stamp = current_time
            pose_msg.header.frame_id = "map"
            
            pose_msg.pose.position.x = self.positions[i][0]
            pose_msg.pose.position.y = self.positions[i][1]
            pose_msg.pose.position.z = self.positions[i][2]
            
            pose_msg.pose.orientation.w = self.orientations[i][0]
            pose_msg.pose.orientation.x = self.orientations[i][1]
            pose_msg.pose.orientation.y = self.orientations[i][2]
            pose_msg.pose.orientation.z = self.orientations[i][3]
            
            self.pose_pubs[i].publish(pose_msg)
            
            # Publish odometry
            odom_msg = Odometry()
            odom_msg.header = pose_msg.header
            odom_msg.child_frame_id = f"drone_{i}"
            
            odom_msg.pose.pose = pose_msg.pose
            
            odom_msg.twist.twist.linear.x = self.velocities[i][0]
            odom_msg.twist.twist.linear.y = self.velocities[i][1]
            odom_msg.twist.twist.linear.z = self.velocities[i][2]
            
            self.odom_pubs[i].publish(odom_msg)
    
    def run(self):
        """
        Run the simulation loop.
        """
        rospy.loginfo("Starting drone simulation")
        
        while not rospy.is_shutdown():
            # Update physics
            dt = 1.0 / self.update_rate
            self.update_physics(dt)
            
            # Publish drone states
            self.publish_drone_states()
            
            # Sleep to maintain update rate
            self.rate.sleep()

if __name__ == '__main__':
    try:
        simulator = DroneSimulator(num_drones=3)
        simulator.run()
    except rospy.ROSInterruptException:
        pass
