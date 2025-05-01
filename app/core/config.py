"""
Application configuration

This module loads and provides access to environment variables from .env file.
All configuration values should be accessed through this module.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "3000"))

# Solana configuration
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com") 