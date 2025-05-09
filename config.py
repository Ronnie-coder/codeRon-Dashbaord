# config.py
import os
import json
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database configuration
DB_PATH = DATA_DIR / "db.sqlite"  # Use SQLite for simplicity, stored in the 'data' directory
DATABASE_URL = f"sqlite:///{DB_PATH}"  # SQLAlchemy connection URL format

# App settings
APP_NAME = "CodRon"
DEFAULT_THEME = "dark"

# User settings path
USER_SETTINGS_PATH = DATA_DIR / "user_settings.json"

def save_user_settings(settings):
    """Save user settings to JSON file"""
    with open(USER_SETTINGS_PATH, "w") as f:
        json.dump(settings, f)

def load_user_settings():
    """Load user settings from JSON file"""
    if not USER_SETTINGS_PATH.exists():
        default_settings = {
            "theme": DEFAULT_THEME,
            "enabled_modules": {
                "analytics": True,
                "seo_checker": True,
                "invoice_tracker": True,
                "learning_goals": True,
                "data_analysis": True,
                "ai_assistant": True,
                "reports": True
            },
            "openai_api_key": ""
        }
        save_user_settings(default_settings)
        return default_settings
    
    with open(USER_SETTINGS_PATH, "r") as f:
        return json.load(f)