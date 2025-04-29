#!/usr/bin/env python3
"""
NLP Assistant - Main Application

This is the main entry point for the NLP Assistant backend.
It initializes all components and starts the server.
"""

import os
import sys
import logging
import argparse
import asyncio
import json
import signal
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import assistant modules
from src.asr import speech_recognizer
from src.nlu import intent_parser
from src.tts import speech_synthesizer
from src.skills import skill_manager
from src.server import websocket_server
from src.utils import audio_utils, config_utils

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("nlp_assistant.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NLPAssistant")

# Load environment variables
load_dotenv()

class NLPAssistant:
    """
    Main NLP Assistant class that coordinates all components.
    """
    
    def __init__(self, config_path=None):
        """
        Initialize the NLP Assistant.
        
        Args:
            config_path: Path to configuration file
        """
        self.running = False
        
        # Load configuration
        self.config = config_utils.load_config(config_path)
        logger.info("Configuration loaded")
        
        # Initialize components
        self.init_components()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        
        logger.info("NLP Assistant initialized")
    
    def init_components(self):
        """Initialize all assistant components."""
        # Initialize automatic speech recognition
        self.asr = speech_recognizer.SpeechRecognizer(self.config["asr"])
        logger.info("Speech recognizer initialized")
        
        # Initialize natural language understanding
        self.nlu = intent_parser.IntentParser(self.config["nlu"])
        logger.info("Intent parser initialized")
        
        # Initialize text-to-speech
        self.tts = speech_synthesizer.SpeechSynthesizer(self.config["tts"])
        logger.info("Speech synthesizer initialized")
        
        # Initialize skill manager
        self.skill_manager = skill_manager.SkillManager(self.config["skills"])
        logger.info("Skill manager initialized")
        
        # Initialize WebSocket server
        self.server = websocket_server.WebSocketServer(
            self.handle_message,
            host=self.config["server"]["host"],
            port=self.config["server"]["port"]
        )
        logger.info(f"WebSocket server initialized on {self.config['server']['host']}:{self.config['server']['port']}")
    
    async def handle_message(self, message_type, data, send_response):
        """
        Handle incoming messages from clients.
        
        Args:
            message_type: Type of message received
            data: Message data
            send_response: Callback function to send response to client
        """
        try:
            if message_type == "audio":
                # Process audio data
                await self.process_audio(data, send_response)
            
            elif message_type == "text":
                # Process text command directly
                await self.process_text(data["text"], send_response)
            
            elif message_type == "ping":
                # Respond to ping
                await send_response({"type": "pong"})
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
                await send_response({"type": "error", "message": "Unknown message type"})
        
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await send_response({"type": "error", "message": str(e)})
    
    async def process_audio(self, audio_data, send_response):
        """
        Process audio data to recognize speech and execute commands.
        
        Args:
            audio_data: Audio data in bytes
            send_response: Callback function to send response to client
        """
        # Send acknowledgment that audio was received
        await send_response({"type": "status", "message": "Processing audio..."})
        
        # Convert audio data to the format expected by the ASR
        audio = audio_utils.convert_audio(audio_data)
        
        # Recognize speech
        text = await self.asr.recognize(audio)
        
        if not text:
            await send_response({"type": "error", "message": "Could not recognize speech"})
            return
        
        # Send recognized text back to client
        await send_response({"type": "recognition", "text": text})
        
        # Process the recognized text
        await self.process_text(text, send_response)
    
    async def process_text(self, text, send_response):
        """
        Process text command to understand intent and execute skills.
        
        Args:
            text: Text command
            send_response: Callback function to send response to client
        """
        # Parse intent
        intent, entities = await self.nlu.parse(text)
        
        if not intent:
            await send_response({"type": "error", "message": "Could not understand command"})
            return
        
        # Send intent and entities back to client
        await send_response({
            "type": "intent",
            "intent": intent,
            "entities": entities
        })
        
        # Execute skill based on intent
        response = await self.skill_manager.execute_skill(intent, entities)
        
        # Generate speech for response
        if response:
            speech_audio = await self.tts.synthesize(response)
            
            # Send response back to client
            await send_response({
                "type": "response",
                "text": response,
                "audio": speech_audio.decode("base64") if speech_audio else None
            })
    
    async def start(self):
        """Start the NLP Assistant server."""
        if self.running:
            logger.warning("NLP Assistant is already running")
            return
        
        self.running = True
        logger.info("Starting NLP Assistant")
        
        # Start the WebSocket server
        await self.server.start()
    
    async def stop(self):
        """Stop the NLP Assistant server."""
        if not self.running:
            return
        
        self.running = False
        logger.info("Stopping NLP Assistant")
        
        # Stop the WebSocket server
        await self.server.stop()
        
        # Clean up resources
        self.asr.cleanup()
        self.tts.cleanup()
        self.nlu.cleanup()
        self.skill_manager.cleanup()
        
        logger.info("NLP Assistant stopped")
    
    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        
        # Create task to stop the assistant
        loop = asyncio.get_event_loop()
        loop.create_task(self.stop())

async def main():
    """Main entry point for the application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="NLP Assistant")
    parser.add_argument("--config", help="Path to configuration file")
    args = parser.parse_args()
    
    # Create and start the assistant
    assistant = NLPAssistant(args.config)
    
    try:
        await assistant.start()
        
        # Keep the application running
        while assistant.running:
            await asyncio.sleep(1)
    
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
    
    finally:
        await assistant.stop()

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
