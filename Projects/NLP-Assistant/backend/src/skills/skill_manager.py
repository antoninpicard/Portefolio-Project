"""
NLP Assistant - Skill Manager

This module manages the various skills and capabilities of the assistant.
"""

import os
import logging
import asyncio
import importlib
import inspect
from pathlib import Path

logger = logging.getLogger("NLPAssistant.Skills")

class SkillManager:
    """
    Manages the skills and capabilities of the assistant.
    Dynamically loads skill modules and routes intents to the appropriate handlers.
    """
    
    def __init__(self, config):
        """
        Initialize the skill manager.
        
        Args:
            config: Configuration dictionary for skills
        """
        self.config = config
        self.skills_dir = Path(config.get('skills_dir', 'src/skills'))
        self.skills = {}
        self.intent_handlers = {}
        
        # Load built-in skills
        self.load_builtin_skills()
        
        # Load custom skills if enabled
        if config.get('load_custom_skills', True):
            self.load_custom_skills()
        
        logger.info(f"Skill manager initialized with {len(self.skills)} skills")
    
    def load_builtin_skills(self):
        """Load built-in skills."""
        try:
            # In a real implementation, this would dynamically load skill modules
            # For this demo, we'll define them directly
            
            # Define built-in skills
            self.register_skill("time", self._handle_time_skill)
            self.register_skill("weather", self._handle_weather_skill)
            self.register_skill("lights", self._handle_lights_skill)
            self.register_skill("timer", self._handle_timer_skill)
            self.register_skill("shopping", self._handle_shopping_skill)
            self.register_skill("music", self._handle_music_skill)
            
            # Map intents to skills
            self.map_intent("get_time", "time")
            self.map_intent("get_weather", "weather")
            self.map_intent("light_on", "lights")
            self.map_intent("light_off", "lights")
            self.map_intent("set_timer", "timer")
            self.map_intent("add_shopping", "shopping")
            self.map_intent("play_music", "music")
            
            logger.info("Built-in skills loaded")
        except Exception as e:
            logger.error(f"Failed to load built-in skills: {str(e)}")
            raise
    
    def load_custom_skills(self):
        """Load custom skills from the skills directory."""
        try:
            # In a real implementation, this would scan for and load Python modules
            # For this demo, we'll just log that it would happen
            logger.info(f"Would load custom skills from: {self.skills_dir}")
            
            # Simulated custom skill loading
            logger.info("Custom skills loaded")
        except Exception as e:
            logger.error(f"Failed to load custom skills: {str(e)}")
    
    def register_skill(self, skill_name, handler):
        """
        Register a skill with the manager.
        
        Args:
            skill_name: Name of the skill
            handler: Function that handles the skill
        """
        self.skills[skill_name] = handler
        logger.info(f"Registered skill: {skill_name}")
    
    def map_intent(self, intent_name, skill_name):
        """
        Map an intent to a skill.
        
        Args:
            intent_name: Name of the intent
            skill_name: Name of the skill to handle the intent
        """
        if skill_name not in self.skills:
            logger.warning(f"Cannot map intent {intent_name} to unknown skill {skill_name}")
            return
        
        self.intent_handlers[intent_name] = skill_name
        logger.info(f"Mapped intent {intent_name} to skill {skill_name}")
    
    async def execute_skill(self, intent, entities):
        """
        Execute the appropriate skill for an intent.
        
        Args:
            intent: Intent name
            entities: Dictionary of entities
            
        Returns:
            Response text
        """
        try:
            if not intent or intent not in self.intent_handlers:
                logger.warning(f"No handler for intent: {intent}")
                return "I'm not sure how to help with that."
            
            skill_name = self.intent_handlers[intent]
            handler = self.skills[skill_name]
            
            logger.info(f"Executing skill {skill_name} for intent {intent}")
            response = await handler(intent, entities)
            
            return response
            
        except Exception as e:
            logger.error(f"Error executing skill: {str(e)}")
            return "Sorry, I encountered an error while processing your request."
    
    # Built-in skill handlers
    
    async def _handle_time_skill(self, intent, entities):
        """Handle time-related intents."""
        # In a real implementation, this would get the actual time
        import datetime
        now = datetime.datetime.now()
        return f"It's currently {now.strftime('%I:%M %p')}."
    
    async def _handle_weather_skill(self, intent, entities):
        """Handle weather-related intents."""
        location = entities.get('location', 'your location')
        time = entities.get('time', 'today')
        
        # In a real implementation, this would fetch actual weather data
        return f"The weather in {location} {time} is sunny with a high of 75°F."
    
    async def _handle_lights_skill(self, intent, entities):
        """Handle light control intents."""
        location = entities.get('location', 'the room')
        
        if intent == "light_on":
            return f"Turning on the lights in {location}."
        elif intent == "light_off":
            return f"Turning off the lights in {location}."
        else:
            return "I'm not sure what you want to do with the lights."
    
    async def _handle_timer_skill(self, intent, entities):
        """Handle timer-related intents."""
        duration = entities.get('duration', '5 minutes')
        
        # In a real implementation, this would actually set a timer
        return f"I've set a timer for {duration}."
    
    async def _handle_shopping_skill(self, intent, entities):
        """Handle shopping list intents."""
        item = entities.get('item', 'an item')
        
        # In a real implementation, this would add to an actual shopping list
        return f"I've added {item} to your shopping list."
    
    async def _handle_music_skill(self, intent, entities):
        """Handle music playback intents."""
        genre = entities.get('genre', '')
        artist = entities.get('artist', '')
        
        if genre and artist:
            return f"Playing {genre} music by {artist}."
        elif genre:
            return f"Playing {genre} music."
        elif artist:
            return f"Playing music by {artist}."
        else:
            return "Playing some music for you."
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up skill manager resources")
        
        # In a real implementation, this would clean up any resources
        # For this demo, we'll just log that it would happen
        self.skills = {}
        self.intent_handlers = {}
