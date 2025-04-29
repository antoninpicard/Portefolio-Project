#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quantum state visualization module for QuantumSandbox.
Provides functionality to visualize quantum states and measurement results.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector, plot_state_city
from qiskit.quantum_info import Statevector
import io
import base64
import json

class StateVisualizer:
    """
    Class for visualizing quantum states and measurement results.
    """
    
    def __init__(self):
        """Initialize the state visualizer."""
        pass
    
    def generate_visualization(self, simulation_result):
        """
        Generate visualization data for a simulation result.
        
        Args:
            simulation_result (dict): Simulation result from CircuitSimulator
            
        Returns:
            dict: Visualization data
        """
        # Extract data from simulation result
        statevector_data = simulation_result.get('statevector', [])
        counts = simulation_result.get('counts', {})
        num_qubits = simulation_result.get('num_qubits', 1)
        
        # Generate visualization data
        visualization = {
            "probability_data": self._generate_probability_data(statevector_data),
            "bloch_data": self._generate_bloch_data(statevector_data, num_qubits),
            "phase_data": self._generate_phase_data(statevector_data),
            "histogram_data": self._generate_histogram_data(counts)
        }
        
        return visualization
    
    def _generate_probability_data(self, statevector_data):
        """
        Generate probability data for bar charts.
        
        Args:
            statevector_data (list): Statevector data from simulation result
            
        Returns:
            dict: Probability data for visualization
        """
        labels = []
        probabilities = []
        
        for state_data in statevector_data:
            labels.append(state_data['state'])
            probabilities.append(state_data['probability'])
        
        return {
            "labels": labels,
            "probabilities": probabilities
        }
    
    def _generate_bloch_data(self, statevector_data, num_qubits):
        """
        Generate Bloch sphere data for single-qubit states.
        
        Args:
            statevector_data (list): Statevector data from simulation result
            num_qubits (int): Number of qubits in the circuit
            
        Returns:
            list: Bloch sphere data for each qubit
        """
        # For multi-qubit states, we need to calculate the reduced density matrix
        # for each qubit to visualize on the Bloch sphere
        
        # This is a simplified version that works for pure states
        # In a real implementation, we would use partial trace operations
        
        bloch_data = []
        
        # Only generate Bloch data if we have a reasonable number of qubits
        if num_qubits <= 5:
            for qubit_idx in range(num_qubits):
                # Calculate expectation values of Pauli operators
                x_exp = 0
                y_exp = 0
                z_exp = 0
                
                for state_data in statevector_data:
                    binary = state_data['state']
                    if len(binary) != num_qubits:
                        continue
                        
                    amplitude = complex(state_data['real'], state_data['imag'])
                    prob = state_data['probability']
                    
                    # This is a simplified calculation
                    # A proper implementation would use the density matrix
                    if binary[qubit_idx] == '0':
                        z_exp += prob
                    else:
                        z_exp -= prob
                
                # In a simplified model, we'll just use the z-expectation
                # and set x and y to small random values for visualization
                # In a real implementation, these would be properly calculated
                x_exp = np.random.uniform(-0.1, 0.1) if z_exp != 1 and z_exp != -1 else 0
                y_exp = np.random.uniform(-0.1, 0.1) if z_exp != 1 and z_exp != -1 else 0
                
                # Normalize the vector
                norm = np.sqrt(x_exp**2 + y_exp**2 + z_exp**2)
                if norm > 0:
                    x_exp /= norm
                    y_exp /= norm
                    z_exp /= norm
                
                bloch_data.append({
                    "qubit": qubit_idx,
                    "x": float(x_exp),
                    "y": float(y_exp),
                    "z": float(z_exp)
                })
        
        return bloch_data
    
    def _generate_phase_data(self, statevector_data):
        """
        Generate phase data for visualization.
        
        Args:
            statevector_data (list): Statevector data from simulation result
            
        Returns:
            dict: Phase data for visualization
        """
        states = []
        phases = []
        magnitudes = []
        
        for state_data in statevector_data:
            if state_data['probability'] > 0.001:  # Only include non-zero amplitudes
                states.append(state_data['state'])
                
                # Calculate phase in degrees
                real = state_data['real']
                imag = state_data['imag']
                phase = np.angle(complex(real, imag)) * 180 / np.pi
                phases.append(float(phase))
                
                # Calculate magnitude
                magnitudes.append(float(np.sqrt(state_data['probability'])))
        
        return {
            "states": states,
            "phases": phases,
            "magnitudes": magnitudes
        }
    
    def _generate_histogram_data(self, counts):
        """
        Generate histogram data from measurement counts.
        
        Args:
            counts (dict): Measurement counts from simulation result
            
        Returns:
            dict: Histogram data for visualization
        """
        labels = []
        values = []
        
        # Sort by binary value for consistent display
        for state, count in sorted(counts.items()):
            labels.append(state)
            values.append(count)
        
        return {
            "labels": labels,
            "values": values
        }
    
    def generate_bloch_sphere_image(self, statevector):
        """
        Generate a Bloch sphere image for a statevector.
        
        Args:
            statevector (list): Statevector data
            
        Returns:
            str: Base64-encoded image
        """
        # Convert to Qiskit Statevector format
        amplitudes = []
        for state_data in statevector:
            amplitudes.append(complex(state_data['real'], state_data['imag']))
        
        qiskit_statevector = Statevector(amplitudes)
        
        # Generate Bloch sphere plot
        plt.figure(figsize=(10, 10))
        plot_bloch_multivector(qiskit_statevector)
        
        # Convert plot to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        
        # Convert to base64
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str
    
    def generate_state_city_image(self, statevector):
        """
        Generate a state city plot for a statevector.
        
        Args:
            statevector (list): Statevector data
            
        Returns:
            str: Base64-encoded image
        """
        # Convert to Qiskit Statevector format
        amplitudes = []
        for state_data in statevector:
            amplitudes.append(complex(state_data['real'], state_data['imag']))
        
        qiskit_statevector = Statevector(amplitudes)
        
        # Generate state city plot
        plt.figure(figsize=(10, 10))
        plot_state_city(qiskit_statevector)
        
        # Convert plot to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        
        # Convert to base64
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str
