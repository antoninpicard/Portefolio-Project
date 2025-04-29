#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Flask application for the QuantumSandbox backend.
Provides API endpoints for quantum circuit simulation and visualization.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Import quantum modules
from quantum.circuit_simulator import CircuitSimulator
from quantum.algorithm_library import AlgorithmLibrary
from quantum.visualization import StateVisualizer

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/build')
CORS(app)  # Enable CORS for all routes

# Initialize quantum modules
circuit_simulator = CircuitSimulator()
algorithm_library = AlgorithmLibrary()
state_visualizer = StateVisualizer()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/api/simulate', methods=['POST'])
def simulate_circuit():
    """
    Simulate a quantum circuit based on the provided circuit definition.
    
    Expected JSON payload:
    {
        "circuit": {
            "qubits": 3,
            "gates": [
                {"type": "h", "targets": [0]},
                {"type": "cx", "controls": [0], "targets": [1]},
                ...
            ]
        },
        "shots": 1024
    }
    """
    try:
        data = request.json
        if not data or 'circuit' not in data:
            return jsonify({"error": "Invalid request format"}), 400
        
        circuit_def = data['circuit']
        shots = data.get('shots', 1024)
        
        # Run simulation
        result = circuit_simulator.simulate(circuit_def, shots)
        
        # Generate visualization data
        visualization = state_visualizer.generate_visualization(result)
        
        return jsonify({
            "result": result,
            "visualization": visualization
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Get the list of available pre-built quantum algorithms."""
    try:
        algorithms = algorithm_library.get_all_algorithms()
        return jsonify({"algorithms": algorithms})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/algorithms/<algorithm_id>', methods=['GET'])
def get_algorithm(algorithm_id):
    """Get a specific pre-built quantum algorithm by ID."""
    try:
        algorithm = algorithm_library.get_algorithm(algorithm_id)
        if not algorithm:
            return jsonify({"error": f"Algorithm {algorithm_id} not found"}), 404
        return jsonify({"algorithm": algorithm})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_circuit():
    """
    Export a circuit to Qiskit Python code.
    
    Expected JSON payload:
    {
        "circuit": {
            "qubits": 3,
            "gates": [...]
        }
    }
    """
    try:
        data = request.json
        if not data or 'circuit' not in data:
            return jsonify({"error": "Invalid request format"}), 400
        
        circuit_def = data['circuit']
        qiskit_code = circuit_simulator.export_to_qiskit(circuit_def)
        
        return jsonify({
            "qiskit_code": qiskit_code
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve React frontend in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve the React frontend in production."""
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
