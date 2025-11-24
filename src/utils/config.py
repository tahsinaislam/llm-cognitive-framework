"""
Configuration Module
Handles configuration loading and management
"""

import yaml
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

class Config:
    """Configuration manager for the framework"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize configuration from file and environment"""
        load_dotenv()  # Load environment variables from .env file

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._resolve_env_variables(self.config)
        self._apply_env_overrides()
        self._validate_config()

    def _resolve_env_variables(self, obj: Any) -> Any:
        """Recursively resolve ${VAR} patterns in config values"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._resolve_env_variables(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                obj[i] = self._resolve_env_variables(item)
        elif isinstance(obj, str):
            # Match ${VAR_NAME} pattern
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, obj)
            for match in matches:
                env_value = os.getenv(match, '')
                obj = obj.replace(f'${{{match}}}', env_value)
        return obj
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_path.exists():
            if self.config_path.suffix == '.yaml' or self.config_path.suffix == '.yml':
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            elif self.config_path.suffix == '.json':
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        else:
            # Return default configuration
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'models': {
                'GPT-4': {
                    'api_key': os.getenv('OPENAI_API_KEY', ''),
                    'model_id': 'gpt-4-turbo-preview',
                    'temperature': 0.7,
                    'max_tokens': 1000,
                    'rate_limit': 10
                },
                'Claude': {
                    'api_key': os.getenv('ANTHROPIC_API_KEY', ''),
                    'model_id': 'claude-3-opus-20240229',
                    'temperature': 0.7,
                    'max_tokens': 1000,
                    'rate_limit': 10
                },
                'Gemini': {
                    'api_key': os.getenv('GOOGLE_API_KEY', ''),
                    'model_id': 'gemini-pro',
                    'temperature': 0.7,
                    'max_tokens': 1000,
                    'rate_limit': 10
                },
                'DeepSeek': {
                    'api_key': os.getenv('DEEPSEEK_API_KEY', ''),
                    'model_id': 'deepseek-chat',
                    'temperature': 0.7,
                    'max_tokens': 1000,
                    'rate_limit': 10
                }
            },
            'tasks': {
                'categories': [
                    'working_memory',
                    'executive_function',
                    'reasoning',
                    'integration',
                    'meta_cognitive'
                ],
                'tasks_per_category': 30,
                'timeout': 60
            },
            'analysis': {
                'batch_size': 10,
                'parallel_processing': True,
                'cache_responses': True
            },
            'output': {
                'results_dir': 'results',
                'visualizations_dir': 'visualizations',
                'format': 'json'
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/framework.log'
            }
        }
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides"""
        # Override API keys from environment if available
        env_mappings = {
            'GROQ_API_KEY': ['models', 'Groq-Llama3', 'api_key'],
            'GROQ_API_KEY': ['models', 'Groq-Mixtral', 'api_key'],
            'GOOGLE_API_KEY': ['models', 'Gemini', 'api_key'],
            'OPENAI_API_KEY': ['models', 'GPT-4', 'api_key'],
            'ANTHROPIC_API_KEY': ['models', 'Claude', 'api_key'],
            'DEEPSEEK_API_KEY': ['models', 'DeepSeek', 'api_key']
        }

        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self._set_nested(self.config, config_path, value)

        # Handle Groq separately since it's used by multiple models
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            for model_name in ['Groq-Llama3', 'Groq-Mixtral']:
                if model_name in self.config.get('models', {}):
                    self.config['models'][model_name]['api_key'] = groq_key
    
    def _set_nested(self, dictionary: Dict, path: list, value: Any) -> None:
        """Set a value in a nested dictionary using a path"""
        for key in path[:-1]:
            dictionary = dictionary.setdefault(key, {})
        dictionary[path[-1]] = value
    
    def _validate_config(self) -> None:
        """Validate configuration"""
        # Check that at least one model has an API key
        models_with_keys = []
        for model_name, model_config in self.config.get('models', {}).items():
            if model_config.get('api_key'):
                models_with_keys.append(model_name)
        
        if not models_with_keys:
            print("Warning: No API keys configured. Please set API keys in .env file or config.yaml")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific model"""
        return self.config.get('models', {}).get(model_name)
    
    def save_config(self, path: Optional[str] = None) -> None:
        """Save current configuration to file"""
        save_path = Path(path) if path else self.config_path
        
        if save_path.suffix in ['.yaml', '.yml']:
            with open(save_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        else:
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=2)
