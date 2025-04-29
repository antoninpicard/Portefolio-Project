"""
NLP Assistant - Configuration Utilities

This module provides utility functions for configuration management.
"""

import os
import logging
import json
import yaml
from pathlib import Path

logger = logging.getLogger("NLPAssistant.Utils.Config")

def load_config(config_path=None):
    """
    Load configuration from a file.
    
    Args:
        config_path: Path to configuration file (JSON or YAML)
        
    Returns:
        Configuration dictionary
    """
    try:
        # Default configuration
        default_config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8765
            },
            "asr": {
                "model_path": "models/asr",
                "use_gpu": True,
                "vad_enabled": True
            },
            "nlu": {
                "model_path": "models/nlu",
                "intents_path": "models/nlu/intents.json",
                "use_gpu": True
            },
            "tts": {
                "model_path": "models/tts",
                "voice_id": "default",
                "speaking_rate": 1.0,
                "pitch": 0.0,
                "use_gpu": True
            },
            "skills": {
                "skills_dir": "src/skills",
                "load_custom_skills": True
            }
        }
        
        # If no config path provided, return default config
        if not config_path:
            logger.info("No configuration file provided, using default configuration")
            return default_config
        
        # Load configuration from file
        config_path = Path(config_path)
        
        if not config_path.exists():
            logger.warning(f"Configuration file not found: {config_path}, using default configuration")
            return default_config
        
        logger.info(f"Loading configuration from: {config_path}")
        
        # Load based on file extension
        if config_path.suffix.lower() == '.json':
            with open(config_path, 'r') as f:
                config = json.load(f)
        elif config_path.suffix.lower() in ['.yaml', '.yml']:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        else:
            logger.warning(f"Unsupported configuration file format: {config_path.suffix}")
            return default_config
        
        # Merge with default configuration
        merged_config = merge_configs(default_config, config)
        
        logger.info("Configuration loaded successfully")
        return merged_config
    
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return default_config

def merge_configs(default_config, user_config):
    """
    Merge user configuration with default configuration.
    
    Args:
        default_config: Default configuration dictionary
        user_config: User configuration dictionary
        
    Returns:
        Merged configuration dictionary
    """
    # Start with a copy of the default config
    merged = default_config.copy()
    
    # Recursively update with user config
    for key, value in user_config.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            # Recursively merge nested dictionaries
            merged[key] = merge_configs(merged[key], value)
        else:
            # Replace or add value
            merged[key] = value
    
    return merged

def save_config(config, config_path):
    """
    Save configuration to a file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        config_path = Path(config_path)
        
        # Create parent directories if they don't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving configuration to: {config_path}")
        
        # Save based on file extension
        if config_path.suffix.lower() == '.json':
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        elif config_path.suffix.lower() in ['.yaml', '.yml']:
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            logger.warning(f"Unsupported configuration file format: {config_path.suffix}")
            return False
        
        logger.info("Configuration saved successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}")
        return False
