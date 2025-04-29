"""
NLP Assistant - WebSocket Server

This module provides a WebSocket server for communication with client applications.
"""

import os
import logging
import asyncio
import json
import websockets
import base64
from pathlib import Path

logger = logging.getLogger("NLPAssistant.Server")

class WebSocketServer:
    """
    WebSocket server for communication with client applications.
    Handles audio streaming, text commands, and responses.
    """
    
    def __init__(self, message_handler, host='0.0.0.0', port=8765):
        """
        Initialize the WebSocket server.
        
        Args:
            message_handler: Callback function to handle incoming messages
            host: Host address to bind to
            port: Port to listen on
        """
        self.message_handler = message_handler
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        
        logger.info(f"WebSocket server initialized on {host}:{port}")
    
    async def start(self):
        """Start the WebSocket server."""
        try:
            # Start the server
            self.server = await websockets.serve(
                self.handle_connection,
                self.host,
                self.port
            )
            
            logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {str(e)}")
            raise
    
    async def stop(self):
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None
            logger.info("WebSocket server stopped")
    
    async def handle_connection(self, websocket, path):
        """
        Handle a WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            path: Connection path
        """
        client_id = id(websocket)
        self.clients.add(websocket)
        
        logger.info(f"Client connected: {client_id}")
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                "type": "welcome",
                "message": "Connected to NLP Assistant"
            }))
            
            # Handle messages
            async for message in websocket:
                await self.process_message(websocket, message)
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_id}")
        
        except Exception as e:
            logger.error(f"Error handling connection: {str(e)}")
        
        finally:
            self.clients.remove(websocket)
    
    async def process_message(self, websocket, message):
        """
        Process an incoming message.
        
        Args:
            websocket: WebSocket connection
            message: Message data
        """
        try:
            # Parse the message
            if isinstance(message, str):
                # Text message (JSON)
                data = json.loads(message)
                message_type = data.get('type')
                
                # Create response callback
                async def send_response(response_data):
                    await websocket.send(json.dumps(response_data))
                
                # Handle the message
                await self.message_handler(message_type, data, send_response)
            
            else:
                # Binary message (audio data)
                # Create response callback
                async def send_response(response_data):
                    await websocket.send(json.dumps(response_data))
                
                # Handle as audio data
                await self.message_handler("audio", message, send_response)
        
        except json.JSONDecodeError:
            logger.warning("Received invalid JSON message")
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Invalid JSON message"
            }))
        
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"Error processing message: {str(e)}"
            }))
    
    async def broadcast(self, message):
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: Message to broadcast
        """
        if not self.clients:
            return
        
        # Convert message to JSON if it's a dict
        if isinstance(message, dict):
            message = json.dumps(message)
        
        # Send to all clients
        await asyncio.gather(
            *[client.send(message) for client in self.clients],
            return_exceptions=True
        )
        
        logger.info(f"Broadcast message to {len(self.clients)} clients")
