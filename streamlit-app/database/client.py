"""
Supabase client wrapper for database connection.
"""

import os
import logging
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SupabaseClient:
    """Singleton wrapper for Supabase client."""

    _instance: Optional[Client] = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Get or create Supabase client instance.

        Returns:
            Client: Supabase client instance

        Raises:
            ValueError: If environment variables are not set
        """
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            if not url or not key:
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
                )

            logger.info(f"🔌 Connecting to Supabase: {url}")
            cls._instance = create_client(url, key)
            logger.info("✅ Supabase client initialized successfully")

        return cls._instance


def get_supabase() -> Client:
    """
    Convenience function to get Supabase client.

    Returns:
        Client: Supabase client instance
    """
    return SupabaseClient.get_client()
