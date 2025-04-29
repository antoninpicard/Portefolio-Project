#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quantum algorithm library for QuantumSandbox.
Provides pre-built quantum algorithms and examples.
"""

import json
import os
from qiskit import QuantumCircuit

class AlgorithmLibrary:
    """
    Class for managing pre-built quantum algorithms.
    """
    
    def __init__(self):
        """Initialize the algorithm library with pre-built algorithms."""
        self.algorithms = {
            "grover": self._create_grover_algorithm(),
            "deutsch_jozsa": self._create_deutsch_jozsa_algorithm(),
            "qft": self._create_qft_algorithm(),
            "teleportation": self._create_teleportation_algorithm(),
            "bernstein_vazirani": self._create_bernstein_vazirani_algorithm(),
            "simon": self._create_simon_algorithm(),
            "bell_state": self._create_bell_state(),
            "ghz_state": self._create_ghz_state()
        }
    
    def get_all_algorithms(self):
        """
        Get all available algorithms with metadata.
        
        Returns:
            list: List of algorithm metadata
        """
        return [
            {
                "id": algo_id,
                "name": algo["name"],
                "description": algo["description"],
                "qubits": algo["circuit_def"]["qubits"],
                "difficulty": algo["difficulty"],
                "category": algo["category"]
            }
            for algo_id, algo in self.algorithms.items()
        ]
    
    def get_algorithm(self, algorithm_id):
        """
        Get a specific algorithm by ID.
        
        Args:
            algorithm_id (str): Algorithm identifier
            
        Returns:
            dict: Algorithm data or None if not found
        """
        return self.algorithms.get(algorithm_id)
    
    def _create_grover_algorithm(self):
        """Create Grover's search algorithm example."""
        # 2-qubit Grover's algorithm for finding |01⟩
        circuit_def = {
            "qubits": 2,
            "gates": [
                {"type": "h", "targets": [0]},
                {"type": "h", "targets": [1]},
                # Oracle for |01⟩
                {"type": "x", "targets": [0]},
                {"type": "h", "targets": [1]},
                {"type": "cx", "controls": [0], "targets": [1]},
                {"type": "h", "targets": [1]},
                {"type": "x", "targets": [0]},
                # Diffusion operator
                {"type": "h", "targets": [0]},
                {"type": "h", "targets": [1]},
                {"type": "x", "targets": [0]},
                {"type": "x", "targets": [1]},
                {"type": "h", "targets": [1]},
                {"type": "cx", "controls": [0], "targets": [1]},
                {"type": "h", "targets": [1]},
                {"type": "x", "targets": [0]},
                {"type": "x", "targets": [1]},
                {"type": "h", "targets": [0]},
                {"type": "h", "targets": [1]},
                {"type": "measure", "targets": [0, 1]}
            ]
        }
        
        return {
            "name": "Grover's Algorithm",
            "description": "A quantum algorithm for searching an unsorted database with quadratic speedup compared to classical algorithms.",
            "circuit_def": circuit_def,
            "difficulty": "Intermediate",
            "category": "Search",
            "references": [
                "https://en.wikipedia.org/wiki/Grover%27s_algorithm",
                "https://qiskit.org/textbook/ch-algorithms/grover.html"
            ]
        }
    
    def _create_deutsch_jozsa_algorithm(self):
        """Create Deutsch-Jozsa algorithm example."""
        # 3-qubit Deutsch-Jozsa for a constant function
        circuit_def = {
            "qubits": 3,
            "gates": [
                {"type": "x", "targets": [2]},
                {"type": "h", "targets": [0, 1, 2]},
                # Oracle for constant function (do nothing)
                {"type": "h", "targets": [0, 1]},
                {"type": "measure", "targets": [0, 1]}
            ]
        }
        
        return {
            "name": "Deutsch-Jozsa Algorithm",
            "description": "A quantum algorithm that determines whether a function is constant or balanced with a single query.",
            "circuit_def": circuit_def,
            "difficulty": "Beginner",
            "category": "Oracle",
            "references": [
                "https://en.wikipedia.org/wiki/Deutsch%E2%80%93Jozsa_algorithm",
                "https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html"
            ]
        }
    
    def _create_qft_algorithm(self):
        """Create Quantum Fourier Transform example."""
        circuit_def = {
            "qubits": 3,
            "gates": [
                # QFT on 3 qubits
                {"type": "h", "targets": [0]},
                {"type": "rz", "targets": [1], "theta": 1.5707963267948966},  # π/2
                {"type": "cx", "controls": [0], "targets": [1]},
                {"type": "rz", "targets": [1], "theta": -1.5707963267948966},  # -π/2
                {"type": "cx", "controls": [0], "targets": [1]},
                {"type": "h", "targets": [1]},
                {"type": "rz", "targets": [2], "theta": 0.7853981633974483},  # π/4
                {"type": "cx", "controls": [0], "targets": [2]},
                {"type": "rz", "targets": [2], "theta": -0.7853981633974483},  # -π/4
                {"type": "cx", "controls": [0], "targets": [2]},
                {"type": "rz", "targets": [2], "theta": 1.5707963267948966},  # π/2
                {"type": "cx", "controls": [1], "targets": [2]},
                {"type": "rz", "targets": [2], "theta": -1.5707963267948966},  # -π/2
                {"type": "cx", "controls": [1], "targets": [2]},
                {"type": "h", "targets": [2]},
                # Swap qubits to get the correct order
                {"type": "swap", "targets": [0, 2]},
                {"type": "measure", "targets": [0, 1, 2]}
            ]
        }
        
        return {
            "name": "Quantum Fourier Transform",
            "description": "A quantum implementation of the discrete Fourier transform, a fundamental component of many quantum algorithms.",
            "circuit_def": circuit_def,
            "difficulty": "Advanced",
            "category": "Transform",
            "references": [
                "https://en.wikipedia.org/wiki/Quantum_Fourier_transform",
                "https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html"
            ]
        }
    
    def _create_teleportation_algorithm(self):
        """Create Quantum Teleportation example."""
        circuit_def = {
            "qubits": 3,
            "gates": [
                # Prepare the state to teleport (qubit 0)
                {"type": "rx", "targets": [0], "theta": 0.7853981633974483},  # π/4
                
                # Create Bell pair between qubits 1 and 2
                {"type": "h", "targets": [1]},
                {"type": "cx", "controls": [1], "targets": [2]},
                
                # Teleportation protocol
                {"type": "cx", "controls": [0], "targets": [1]},
                {"type": "h", "targets": [0]},
                
                # Measure qubits 0 and 1
                {"type": "measure", "targets": [0, 1]},
                
                # Apply corrections to qubit 2 (in a real circuit, these would be conditional)
                {"type": "x", "targets": [2]},  # Apply X if qubit 1 measurement is 1
                {"type": "z", "targets": [2]},  # Apply Z if qubit 0 measurement is 1
                
                # Measure the final state
                {"type": "measure", "targets": [2]}
            ]
        }
        
        return {
            "name": "Quantum Teleportation",
            "description": "A protocol that transfers a quantum state from one qubit to another using entanglement and classical communication.",
            "circuit_def": circuit_def,
            "difficulty": "Intermediate",
            "category": "Communication",
            "references": [
                "https://en.wikipedia.org/wiki/Quantum_teleportation",
                "https://qiskit.org/textbook/ch-algorithms/teleportation.html"
            ]
        }
    
    def _create_bernstein_vazirani_algorithm(self):
        """Create Bernstein-Vazirani algorithm example."""
        # For secret string "101"
        circuit_def = {
            "qubits": 4,
            "gates": [
                {"type": "x", "targets": [3]},
                {"type": "h", "targets": [0, 1, 2, 3]},
                
                # Oracle for secret string "101"
                {"type": "cx", "controls": [0], "targets": [3]},
                {"type": "cx", "controls": [2], "targets": [3]},
                
                {"type": "h", "targets": [0, 1, 2]},
                {"type": "measure", "targets": [0, 1, 2]}
            ]
        }
        
        return {
            "name": "Bernstein-Vazirani Algorithm",
            "description": "A quantum algorithm that finds a hidden bitstring with a single query to an oracle.",
            "circuit_def": circuit_def,
            "difficulty": "Beginner",
            "category": "Oracle",
            "references": [
                "https://en.wikipedia.org/wiki/Bernstein%E2%80%93Vazirani_algorithm",
                "https://qiskit.org/textbook/ch-algorithms/bernstein-vazirani.html"
            ]
        }
    
    def _create_simon_algorithm(self):
        """Create Simon's algorithm example."""
        # For secret string "10" (2 qubits)
        circuit_def = {
            "qubits": 4,
            "gates": [
                {"type": "h", "targets": [0, 1]},
                
                # Oracle for secret string "10"
                {"type": "cx", "controls": [0], "targets": [2]},
                {"type": "cx", "controls": [1], "targets": [3]},
                {"type": "cx", "controls": [0], "targets": [3]},
                
                {"type": "h", "targets": [0, 1]},
                {"type": "measure", "targets": [0, 1]}
            ]
        }
        
        return {
            "name": "Simon's Algorithm",
            "description": "A quantum algorithm that determines a hidden bitstring in a black-box function with exponential speedup.",
            "circuit_def": circuit_def,
            "difficulty": "Advanced",
            "category": "Oracle",
            "references": [
                "https://en.wikipedia.org/wiki/Simon%27s_problem",
                "https://qiskit.org/textbook/ch-algorithms/simon.html"
            ]
        }
    
    def _create_bell_state(self):
        """Create Bell state (entangled qubits) example."""
        circuit_def = {
            "qubits": 2,
            "gates": [
                {"type": "h", "targets": [0]},
                {"type": "cx", "controls": [0], "targets": [1]},
                {"type": "measure", "targets": [0, 1]}
            ]
        }
        
        return {
            "name": "Bell State",
            "description": "A simple quantum circuit that creates a maximally entangled state between two qubits.",
            "circuit_def": circuit_def,
            "difficulty": "Beginner",
            "category": "Entanglement",
            "references": [
                "https://en.wikipedia.org/wiki/Bell_state",
                "https://qiskit.org/textbook/ch-gates/multiple-qubits-entangled-states.html"
            ]
        }
    
    def _create_ghz_state(self):
        """Create GHZ state example."""
        circuit_def = {
            "qubits": 3,
            "gates": [
                {"type": "h", "targets": [0]},
                {"type": "cx", "controls": [0], "targets": [1]},
                {"type": "cx", "controls": [0], "targets": [2]},
                {"type": "measure", "targets": [0, 1, 2]}
            ]
        }
        
        return {
            "name": "GHZ State",
            "description": "A multi-qubit entangled state that exhibits strong quantum correlations.",
            "circuit_def": circuit_def,
            "difficulty": "Beginner",
            "category": "Entanglement",
            "references": [
                "https://en.wikipedia.org/wiki/Greenberger%E2%80%93Horne%E2%80%93Zeilinger_state",
                "https://qiskit.org/textbook/ch-gates/multiple-qubits-entangled-states.html"
            ]
        }
