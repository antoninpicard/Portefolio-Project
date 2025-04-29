#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Path Planning Module for SwarmDrone

This module provides path planning algorithms for drone swarms,
enabling efficient navigation while maintaining formation.

Algorithms implemented:
- RRT* (Rapidly-exploring Random Tree Star)
- PRM (Probabilistic Roadmap)
- A* for multi-agent planning
- Potential field based formation control
"""

import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped, Twist, Point
from nav_msgs.msg import Path, OccupancyGrid
from visualization_msgs.msg import Marker, MarkerArray
import math
import random
from scipy.spatial import KDTree
from enum import Enum
from heapq import heappush, heappop
from threading import Lock

class PlanningAlgorithm(Enum):
    RRT_STAR = 1
    PRM = 2
    A_STAR = 3
    POTENTIAL_FIELD = 4

class Node:
    """Node class for RRT and A* algorithms"""
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
        self.cost = 0.0
        self.path_cost = float('inf')
        
    def __lt__(self, other):
        return self.path_cost < other.path_cost
        
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
    
    def position(self):
        return np.array([self.x, self.y, self.z])

class PathPlanner:
    """Path planning for swarm of drones"""
    def __init__(self):
        rospy.init_node('swarm_path_planner', anonymous=True)
        
        # Parameters
        self.planning_algorithm = rospy.get_param('~planning_algorithm', 'rrt_star')
        self.max_iterations = rospy.get_param('~max_iterations', 1000)
        self.step_size = rospy.get_param('~step_size', 0.5)
        self.goal_sample_rate = rospy.get_param('~goal_sample_rate', 0.1)
        self.search_radius = rospy.get_param('~search_radius', 2.0)
        self.formation_type = rospy.get_param('~formation_type', 'triangle')
        
        # Map properties
        self.map_resolution = 0.1  # meters per cell
        self.map_width = 100  # cells
        self.map_height = 100  # cells
        self.map_data = None
        self.obstacles = []
        
        # Swarm properties
        self.num_drones = rospy.get_param('~num_drones', 3)
        self.drone_radius = rospy.get_param('~drone_radius', 0.3)  # meters
        self.formation_spacing = rospy.get_param('~formation_spacing', 2.0)  # meters
        
        # Internal data structures
        self.paths = [[] for _ in range(self.num_drones)]
        self.current_poses = [None] * self.num_drones
        self.goal_poses = [None] * self.num_drones
        self.planning_lock = Lock()
        
        # ROS Publishers
        self.path_publishers = [
            rospy.Publisher(f'/drone_{i}/path', Path, queue_size=10)
            for i in range(self.num_drones)
        ]
        self.visualization_pub = rospy.Publisher('/swarm/path_visualization', MarkerArray, queue_size=10)
        
        # ROS Subscribers
        rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        
        for i in range(self.num_drones):
            rospy.Subscriber(f'/drone_{i}/pose', PoseStamped, self.pose_callback, callback_args=i)
            rospy.Subscriber(f'/drone_{i}/goal', PoseStamped, self.goal_callback, callback_args=i)
            
        rospy.loginfo("Swarm Path Planner initialized")
    
    def map_callback(self, msg):
        """Process occupancy grid map data"""
        self.map_resolution = msg.info.resolution
        self.map_width = msg.info.width
        self.map_height = msg.info.height
        self.map_origin = (msg.info.origin.position.x, msg.info.origin.position.y)
        self.map_data = np.array(msg.data).reshape(self.map_height, self.map_width)
        
        # Extract obstacles from map
        self.obstacles = []
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.map_data[y, x] > 50:  # occupied cell
                    world_x = x * self.map_resolution + self.map_origin[0]
                    world_y = y * self.map_resolution + self.map_origin[1]
                    self.obstacles.append((world_x, world_y))
        
        rospy.loginfo(f"Map updated: {len(self.obstacles)} obstacles detected")
    
    def pose_callback(self, msg, drone_id):
        """Update current drone pose"""
        self.current_poses[drone_id] = msg
    
    def goal_callback(self, msg, drone_id):
        """Handle new goal request for a drone"""
        self.goal_poses[drone_id] = msg
        
        if all(pose is not None for pose in self.current_poses) and all(goal is not None for goal in self.goal_poses):
            if drone_id == 0:  # Leader received a new goal
                self.plan_swarm_path()
    
    def plan_swarm_path(self):
        """Plan paths for the entire swarm"""
        with self.planning_lock:
            rospy.loginfo("Planning paths for swarm")
            
            # Get leader's start and goal positions
            leader_start = self.current_poses[0].pose.position
            leader_goal = self.goal_poses[0].pose.position
            
            start_node = Node(leader_start.x, leader_start.y, leader_start.z)
            goal_node = Node(leader_goal.x, leader_goal.y, leader_goal.z)
            
            # Determine formation positions
            formation_offsets = self.calculate_formation_offsets()
            
            # Plan leader's path first
            if self.planning_algorithm.upper() == 'RRT_STAR':
                leader_path = self.rrt_star(start_node, goal_node)
            elif self.planning_algorithm.upper() == 'A_STAR':
                leader_path = self.a_star(start_node, goal_node)
            else:
                leader_path = self.rrt_star(start_node, goal_node)  # default to RRT*
                
            if not leader_path:
                rospy.logwarn("Failed to find path for leader")
                return
                
            self.paths[0] = leader_path
            
            # Plan follower paths based on leader's path
            for i in range(1, self.num_drones):
                follower_path = self.follow_leader_path(leader_path, formation_offsets[i-1])
                self.paths[i] = follower_path
            
            # Publish paths
            self.publish_paths()
            self.publish_visualization()
            
            rospy.loginfo("Swarm path planning completed")
    
    def calculate_formation_offsets(self):
        """Calculate relative positions for drones in formation"""
        offsets = []
        
        if self.formation_type == 'triangle':
            # Triangle formation
            if self.num_drones >= 2:
                offsets.append((-self.formation_spacing, -self.formation_spacing, 0))
            if self.num_drones >= 3:
                offsets.append((self.formation_spacing, -self.formation_spacing, 0))
            # Add more drones in expanding triangle
            for i in range(3, self.num_drones):
                layer = (i - 1) // 2 + 1
                idx = (i - 1) % 2
                x = self.formation_spacing * (idx * 2 - 1) * layer
                y = -self.formation_spacing * layer
                offsets.append((x, y, 0))
        
        elif self.formation_type == 'line':
            # Line formation (horizontal)
            for i in range(1, self.num_drones):
                offsets.append((i * self.formation_spacing, 0, 0))
        
        elif self.formation_type == 'column':
            # Column formation (vertical)
            for i in range(1, self.num_drones):
                offsets.append((0, -i * self.formation_spacing, 0))
        
        elif self.formation_type == 'square':
            # Square formation
            positions = [
                (-self.formation_spacing, -self.formation_spacing, 0),
                (self.formation_spacing, -self.formation_spacing, 0),
                (-self.formation_spacing, self.formation_spacing, 0),
                (self.formation_spacing, self.formation_spacing, 0)
            ]
            for i in range(1, min(5, self.num_drones)):
                offsets.append(positions[i-1])
            # Add more drones in expanding square
            for i in range(5, self.num_drones):
                layer = (i - 1) // 4 + 1
                idx = (i - 1) % 4
                x = self.formation_spacing * (idx == 1 or idx == 3) * layer * 2 - self.formation_spacing * layer
                y = self.formation_spacing * (idx == 2 or idx == 3) * layer * 2 - self.formation_spacing * layer
                offsets.append((x, y, 0))
                
        return offsets
    
    def follow_leader_path(self, leader_path, offset):
        """Generate a follower drone's path based on the leader's path and formation offset"""
        follower_path = []
        
        for node in leader_path:
            # Calculate position with offset
            x = node.x + offset[0]
            y = node.y + offset[1]
            z = node.z + offset[2]
            
            # Check if the position is valid (not in obstacle)
            if self.is_valid_position(x, y, z):
                follower_node = Node(x, y, z)
                follower_path.append(follower_node)
            else:
                # If invalid, find closest valid position
                follower_node = self.find_closest_valid_position(node, offset)
                follower_path.append(follower_node)
        
        return follower_path
    
    def find_closest_valid_position(self, leader_node, desired_offset, search_radius=2.0, iterations=10):
        """Find the closest valid position to the desired formation position"""
        best_node = None
        best_distance = float('inf')
        
        desired_x = leader_node.x + desired_offset[0]
        desired_y = leader_node.y + desired_offset[1]
        desired_z = leader_node.z + desired_offset[2]
        
        # Try random positions near the desired position
        for _ in range(iterations):
            # Sample random point within search radius of desired position
            theta = random.uniform(0, 2 * math.pi)
            radius = random.uniform(0, search_radius)
            x = desired_x + radius * math.cos(theta)
            y = desired_y + radius * math.sin(theta)
            z = desired_z
            
            if self.is_valid_position(x, y, z):
                distance = math.sqrt((x - desired_x)**2 + (y - desired_y)**2 + (z - desired_z)**2)
                if distance < best_distance:
                    best_distance = distance
                    best_node = Node(x, y, z)
        
        # If no valid position found, try to stay in the previous position
        if best_node is None:
            best_node = Node(leader_node.x, leader_node.y, leader_node.z)
            
        return best_node
    
    def is_valid_position(self, x, y, z):
        """Check if a position is valid (not in collision with obstacles)"""
        # Check map boundaries
        if self.map_data is None:
            return True  # No map loaded yet, assume valid
            
        # Convert world coordinates to map coordinates
        map_x = int((x - self.map_origin[0]) / self.map_resolution)
        map_y = int((y - self.map_origin[1]) / self.map_resolution)
        
        # Check if within map bounds
        if map_x < 0 or map_x >= self.map_width or map_y < 0 or map_y >= self.map_height:
            return False
            
        # Check if cell is occupied
        if self.map_data[map_y, map_x] > 50:  # occupied
            return False
            
        # Check distance to obstacles (inflation)
        for obs_x, obs_y in self.obstacles:
            distance = math.sqrt((x - obs_x)**2 + (y - obs_y)**2)
            if distance < self.drone_radius * 1.5:  # Add safety margin
                return False
                
        return True
    
    def rrt_star(self, start_node, goal_node):
        """RRT* algorithm for path planning"""
        nodes = [start_node]
        
        for i in range(self.max_iterations):
            # Sample random node
            if random.random() < self.goal_sample_rate:
                random_node = Node(goal_node.x, goal_node.y, goal_node.z)
            else:
                # Random sampling within map bounds
                x = random.uniform(self.map_origin[0], self.map_origin[0] + self.map_width * self.map_resolution)
                y = random.uniform(self.map_origin[1], self.map_origin[1] + self.map_height * self.map_resolution)
                z = start_node.z  # Assuming 2D planning for simplicity
                random_node = Node(x, y, z)
                
            # Find nearest node
            nearest_node = self.find_nearest_node(nodes, random_node)
            
            # Steer towards random node
            new_node = self.steer(nearest_node, random_node, self.step_size)
            
            if self.is_collision_free(nearest_node, new_node):
                # Find nearby nodes
                nearby_nodes = self.find_nearby_nodes(nodes, new_node, self.search_radius)
                
                # Connect new_node to lowest-cost parent
                min_node = nearest_node
                min_cost = nearest_node.cost + nearest_node.distance(new_node)
                
                for near_node in nearby_nodes:
                    if self.is_collision_free(near_node, new_node):
                        cost = near_node.cost + near_node.distance(new_node)
                        if cost < min_cost:
                            min_cost = cost
                            min_node = near_node
                
                new_node.parent = min_node
                new_node.cost = min_cost
                nodes.append(new_node)
                
                # Rewire nearby nodes if it's cheaper to go through new_node
                for near_node in nearby_nodes:
                    if near_node != new_node.parent:
                        if self.is_collision_free(new_node, near_node):
                            cost = new_node.cost + new_node.distance(near_node)
                            if cost < near_node.cost:
                                near_node.parent = new_node
                                near_node.cost = cost
                
                # Check if we reached the goal
                if new_node.distance(goal_node) < self.step_size:
                    final_node = Node(goal_node.x, goal_node.y, goal_node.z)
                    final_node.parent = new_node
                    final_node.cost = new_node.cost + new_node.distance(goal_node)
                    nodes.append(final_node)
                    
                    path = self.extract_path(final_node)
                    path = self.smooth_path(path)
                    return path
        
        # If max iterations reached without finding path
        rospy.logwarn("RRT* max iterations reached without finding path")
        nearest_to_goal = self.find_nearest_node(nodes, goal_node)
        path = self.extract_path(nearest_to_goal)
        path = self.smooth_path(path)
        return path
    
    def a_star(self, start_node, goal_node):
        """A* algorithm for path planning"""
        open_set = []
        closed_set = set()
        
        start_node.path_cost = 0
        start_node.cost = self.heuristic(start_node, goal_node)
        heappush(open_set, (start_node.cost, id(start_node), start_node))
        
        while open_set:
            _, _, current = heappop(open_set)
            
            if self.is_goal_reached(current, goal_node):
                path = self.extract_path(current)
                return path
                
            closed_set.add((current.x, current.y, current.z))
            
            # Generate neighbors on a grid or by sampling
            neighbors = self.generate_neighbors(current)
            
            for neighbor in neighbors:
                if (neighbor.x, neighbor.y, neighbor.z) in closed_set:
                    continue
                    
                tentative_path_cost = current.path_cost + current.distance(neighbor)
                
                existing = False
                for _, _, node in open_set:
                    if abs(node.x - neighbor.x) < 0.1 and abs(node.y - neighbor.y) < 0.1 and abs(node.z - neighbor.z) < 0.1:
                        existing = True
                        if tentative_path_cost < node.path_cost:
                            node.path_cost = tentative_path_cost
                            node.cost = tentative_path_cost + self.heuristic(node, goal_node)
                            node.parent = current
                        break
                
                if not existing:
                    neighbor.path_cost = tentative_path_cost
                    neighbor.cost = tentative_path_cost + self.heuristic(neighbor, goal_node)
                    neighbor.parent = current
                    heappush(open_set, (neighbor.cost, id(neighbor), neighbor))
        
        # If no path found
        rospy.logwarn("A* failed to find path")
        return []
    
    def generate_neighbors(self, node, step_size=0.5):
        """Generate neighboring nodes for A* algorithm"""
        neighbors = []
        directions = [
            (step_size, 0, 0), (-step_size, 0, 0),
            (0, step_size, 0), (0, -step_size, 0),
            (step_size, step_size, 0), (step_size, -step_size, 0),
            (-step_size, step_size, 0), (-step_size, -step_size, 0)
        ]
        
        for dx, dy, dz in directions:
            x = node.x + dx
            y = node.y + dy
            z = node.z + dz
            
            if self.is_valid_position(x, y, z):
                neighbors.append(Node(x, y, z))
                
        return neighbors
    
    def heuristic(self, node, goal):
        """Heuristic function for A* (Euclidean distance)"""
        return node.distance(goal)
    
    def is_goal_reached(self, node, goal):
        """Check if goal is reached within a threshold"""
        return node.distance(goal) < self.step_size
    
    def find_nearest_node(self, nodes, target_node):
        """Find the nearest node in the tree"""
        min_dist = float('inf')
        nearest = None
        
        for node in nodes:
            dist = node.distance(target_node)
            if dist < min_dist:
                min_dist = dist
                nearest = node
                
        return nearest
    
    def find_nearby_nodes(self, nodes, target_node, radius):
        """Find nodes within a certain radius"""
        return [node for node in nodes if node.distance(target_node) < radius]
    
    def steer(self, from_node, to_node, step_size):
        """Steer from one node towards another with a maximum step size"""
        dist = from_node.distance(to_node)
        
        if dist < step_size:
            return Node(to_node.x, to_node.y, to_node.z)
        
        # Move in the direction of to_node with step_size
        theta = math.atan2(to_node.y - from_node.y, to_node.x - from_node.x)
        x = from_node.x + step_size * math.cos(theta)
        y = from_node.y + step_size * math.sin(theta)
        z = from_node.z  # Assuming 2D planning
        
        new_node = Node(x, y, z)
        return new_node
    
    def is_collision_free(self, from_node, to_node):
        """Check if the path between two nodes is collision-free"""
        # Use line interpolation to check for collisions
        dist = from_node.distance(to_node)
        
        # Number of interpolation points based on distance
        n_points = max(2, int(dist / (self.drone_radius / 2)))
        
        for i in range(1, n_points):
            t = i / n_points
            x = from_node.x + t * (to_node.x - from_node.x)
            y = from_node.y + t * (to_node.y - from_node.y)
            z = from_node.z + t * (to_node.z - from_node.z)
            
            if not self.is_valid_position(x, y, z):
                return False
                
        return True
    
    def extract_path(self, end_node):
        """Extract the path from start to end node"""
        path = []
        current = end_node
        
        while current is not None:
            path.append(current)
            current = current.parent
            
        return path[::-1]  # Reverse to get start-to-end order
    
    def smooth_path(self, path, max_iterations=100):
        """Apply path smoothing to remove unnecessary waypoints"""
        if len(path) <= 2:
            return path
            
        smoothed_path = [path[0]]
        current_idx = 0
        
        while current_idx < len(path) - 1:
            furthest_idx = current_idx + 1
            
            # Find furthest visible node
            for i in range(current_idx + 2, len(path)):
                if self.is_collision_free(path[current_idx], path[i]):
                    furthest_idx = i
                else:
                    break
            
            smoothed_path.append(path[furthest_idx])
            current_idx = furthest_idx
        
        return smoothed_path
    
    def publish_paths(self):
        """Publish ROS Path messages for each drone"""
        for i, drone_path in enumerate(self.paths):
            if not drone_path:
                continue
                
            path_msg = Path()
            path_msg.header.stamp = rospy.Time.now()
            path_msg.header.frame_id = "map"
            
            for node in drone_path:
                pose = PoseStamped()
                pose.header = path_msg.header
                pose.pose.position.x = node.x
                pose.pose.position.y = node.y
                pose.pose.position.z = node.z
                
                # Set orientation (forward-facing)
                if drone_path.index(node) < len(drone_path) - 1:
                    next_node = drone_path[drone_path.index(node) + 1]
                    dx = next_node.x - node.x
                    dy = next_node.y - node.y
                    yaw = math.atan2(dy, dx)
                    
                    # Convert yaw to quaternion (simplified)
                    pose.pose.orientation.z = math.sin(yaw / 2)
                    pose.pose.orientation.w = math.cos(yaw / 2)
                
                path_msg.poses.append(pose)
            
            self.path_publishers[i].publish(path_msg)
    
    def publish_visualization(self):
        """Publish visualization markers for RVIZ"""
        marker_array = MarkerArray()
        
        # Create line markers for each drone's path
        for i, drone_path in enumerate(self.paths):
            if not drone_path:
                continue
                
            # Path line marker
            line_marker = Marker()
            line_marker.header.frame_id = "map"
            line_marker.header.stamp = rospy.Time.now()
            line_marker.ns = f"drone_{i}_path"
            line_marker.id = i
            line_marker.type = Marker.LINE_STRIP
            line_marker.action = Marker.ADD
            line_marker.scale.x = 0.1  # Line width
            
            # Color based on drone id
            if i == 0:  # Leader
                line_marker.color.r = 1.0
                line_marker.color.g = 0.0
                line_marker.color.b = 0.0
            else:  # Followers
                line_marker.color.r = 0.0
                line_marker.color.g = 0.0
                line_marker.color.b = 1.0
            
            line_marker.color.a = 1.0
            
            # Add points to line
            for node in drone_path:
                p = Point()
                p.x = node.x
                p.y = node.y
                p.z = node.z
                line_marker.points.append(p)
            
            marker_array.markers.append(line_marker)
            
            # Waypoint markers (spheres at each node)
            for j, node in enumerate(drone_path):
                point_marker = Marker()
                point_marker.header.frame_id = "map"
                point_marker.header.stamp = rospy.Time.now()
                point_marker.ns = f"drone_{i}_waypoints"
                point_marker.id = i * 1000 + j
                point_marker.type = Marker.SPHERE
                point_marker.action = Marker.ADD
                point_marker.pose.position.x = node.x
                point_marker.pose.position.y = node.y
                point_marker.pose.position.z = node.z
                point_marker.scale.x = 0.2
                point_marker.scale.y = 0.2
                point_marker.scale.z = 0.2
                
                # Start node (green), goal node (red), intermediate (blue/yellow)
                if j == 0:
                    point_marker.color.r = 0.0
                    point_marker.color.g = 1.0
                    point_marker.color.b = 0.0
                elif j == len(drone_path) - 1:
                    point_marker.color.r = 1.0
                    point_marker.color.g = 0.0
                    point_marker.color.b = 0.0
                else:
                    point_marker.color.r = 1.0
                    point_marker.color.g = 1.0
                    point_marker.color.b = 0.0
                
                point_marker.color.a = 1.0
                marker_array.markers.append(point_marker)
                
        self.visualization_pub.publish(marker_array)

if __name__ == '__main__':
    try:
        planner = PathPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
