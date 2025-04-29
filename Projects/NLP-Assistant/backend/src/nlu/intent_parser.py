"""
NLP Assistant - Natural Language Understanding

This module handles intent parsing and entity extraction from text commands.
"""

import os
import logging
import asyncio
import json
from pathlib import Path
import torch
import numpy as np

logger = logging.getLogger("NLPAssistant.NLU")

class IntentParser:
    """
    Natural language understanding system for intent parsing and entity extraction.
    Uses a transformer-based model optimized for edge devices.
    """
    
    def __init__(self, config):
        """
        Initialize the intent parser.
        
        Args:
            config: Configuration dictionary for NLU
        """
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() and config.get('use_gpu', True) else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Load model
        self.model_path = Path(config.get('model_path', 'models/nlu'))
        self.load_model()
        
        # Load intents and entities definitions
        self.intents_path = Path(config.get('intents_path', 'models/nlu/intents.json'))
        self.load_intents()
        
        logger.info("Intent parser initialized")
    
    def load_model(self):
        """Load the NLU model."""
        try:
            # In a real implementation, this would load an actual PyTorch model
            # For this demo, we'll just log that it would happen
            logger.info(f"Would load NLU model from: {self.model_path}")
            
            # Simulated model loading
            self.model = None
            self.tokenizer = None
            
            logger.info("NLU model loaded")
        except Exception as e:
            logger.error(f"Failed to load NLU model: {str(e)}")
            raise
    
    def load_intents(self):
        """Load intent and entity definitions."""
        try:
            # In a real implementation, this would load from a file
            # For this demo, we'll define them directly
            logger.info(f"Would load intents from: {self.intents_path}")
            
            # Simulated intents and entities
            self.intents = {
                "light_on": {
                    "patterns": ["turn on the lights", "lights on", "switch on the lights"],
                    "entities": ["location"]
                },
                "light_off": {
                    "patterns": ["turn off the lights", "lights off", "switch off the lights"],
                    "entities": ["location"]
                },
                "get_weather": {
                    "patterns": ["what's the weather", "weather forecast", "is it going to rain"],
                    "entities": ["location", "time"]
                },
                "set_timer": {
                    "patterns": ["set a timer", "start a timer", "countdown"],
                    "entities": ["duration"]
                },
                "add_shopping": {
                    "patterns": ["add to shopping list", "buy", "shopping list"],
                    "entities": ["item"]
                },
                "play_music": {
                    "patterns": ["play music", "play some songs", "start music"],
                    "entities": ["genre", "artist"]
                },
                "get_time": {
                    "patterns": ["what time is it", "tell me the time", "current time"],
                    "entities": []
                }
            }
            
            self.entities = {
                "location": ["kitchen", "living room", "bedroom", "bathroom", "office"],
                "time": ["today", "tomorrow", "now", "later", "morning", "afternoon", "evening"],
                "duration": ["1 minute", "5 minutes", "10 minutes", "30 minutes", "1 hour"],
                "item": ["milk", "bread", "eggs", "coffee", "cheese", "apples"],
                "genre": ["rock", "pop", "jazz", "classical", "hip hop"],
                "artist": ["Beatles", "Mozart", "Jay-Z", "Taylor Swift", "Queen"]
            }
            
            logger.info("Intents and entities loaded")
        except Exception as e:
            logger.error(f"Failed to load intents: {str(e)}")
            raise
    
    async def parse(self, text):
        """
        Parse text to extract intent and entities.
        
        Args:
            text: Text to parse
            
        Returns:
            Tuple of (intent, entities)
        """
        try:
            # In a real implementation, this would process the text through the model
            # For this demo, we'll use a simple rule-based approach
            logger.info(f"Parsing text: {text}")
            
            # Simulate processing delay
            await asyncio.sleep(0.2)
            
            # Simple rule-based intent matching
            intent = self._match_intent(text.lower())
            
            # Extract entities
            entities = self._extract_entities(text.lower(), intent)
            
            logger.info(f"Parsed intent: {intent}, entities: {entities}")
            return intent, entities
            
        except Exception as e:
            logger.error(f"Error in intent parsing: {str(e)}")
            return None, {}
    
    def _match_intent(self, text):
        """
        Match text to an intent using simple pattern matching.
        
        Args:
            text: Text to match
            
        Returns:
            Intent name or None if no match
        """
        # In a real implementation, this would use the NLU model
        # For this demo, we'll use simple pattern matching
        
        best_intent = None
        best_score = 0
        
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data["patterns"]:
                if pattern in text:
                    # Simple scoring: length of the matching pattern
                    score = len(pattern)
                    if score > best_score:
                        best_intent = intent_name
                        best_score = score
        
        return best_intent
    
    def _extract_entities(self, text, intent):
        """
        Extract entities from text based on the intent.
        
        Args:
            text: Text to extract entities from
            intent: Intent name
            
        Returns:
            Dictionary of entities
        """
        # In a real implementation, this would use the NLU model
        # For this demo, we'll use simple pattern matching
        
        if not intent or intent not in self.intents:
            return {}
        
        entities = {}
        
        for entity_type in self.intents[intent]["entities"]:
            if entity_type in self.entities:
                for value in self.entities[entity_type]:
                    if value.lower() in text:
                        entities[entity_type] = value
                        break
        
        return entities
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up intent parser resources")
        
        # In a real implementation, this would free up resources
        # For this demo, we'll just log that it would happen
        if self.model:
            # Free model resources
            self.model = None
            self.tokenizer = None
