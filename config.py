import os
from pathlib import Path

# Get the root of the CAMP project folder, no matter where config.py lives
CURRENT_FILE = Path(__file__).resolve()
ROOT_DIR = CURRENT_FILE.parent.parent.parent  # Adjust if config.py is deep in folders

# Define shared profile picture directory
SHARED_PROFILE_DIR = ROOT_DIR / "shared_assets/profile_pictures"

# Optional: convert to string if needed by Flask
SHARED_PROFILE_DIR = str(SHARED_PROFILE_DIR)