import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
HF_API_KEY = os.getenv("HF_API_KEY", "").strip()

# Current Gemini model names can be changed without editing Python code.
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3-flash-preview")
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-2.0-pro")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.0-flash-image")
# image provider: gemini | diffusers | placeholder
IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "gemini").lower()

# For local Diffusers. Change to another compatible model if desired.
SD_MODEL_ID = os.getenv("SD_MODEL_ID", "runwayml/stable-diffusion-v1-5")
SD_STEPS = int(os.getenv("SD_STEPS", "20"))

PANEL_COUNT = 5
