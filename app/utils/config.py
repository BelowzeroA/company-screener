"""
Configuration utilities for handling environment variables and settings.
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Company Screener."""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
    CORESIGNAL_API_KEY = os.getenv("CORESIGNAL_API_KEY")
    TRACXN_API_KEY = os.getenv("TRACXN_API_KEY")

    # API Settings
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Service Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    @classmethod
    def validate_required_keys(cls) -> Dict[str, bool]:
        """
        Validate that all required API keys are present.

        Returns:
            Dictionary with API key names and their presence status
        """
        return {
            "OPENAI_API_KEY": bool(cls.OPENAI_API_KEY),
            "SERPER_API_KEY": bool(cls.SERPER_API_KEY),
            "PERPLEXITY_API_KEY": bool(cls.PERPLEXITY_API_KEY),
            "SCRAPER_API_KEY": bool(cls.SCRAPER_API_KEY),
            "CORESIGNAL_API_KEY": bool(cls.CORESIGNAL_API_KEY),
            "TRACXN_API_KEY": bool(cls.TRACXN_API_KEY)
        }
