
from pathlib import Path
import sys
import os

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"


if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)  # Use PyInstaller's temp directory
else:
    BASE_DIR = Path(__file__).resolve().parent

MODEL_PATHS = {
    "llama-1b": str(BASE_DIR / "models" / "llama-1b-q4.gguf"),
    "llama-3b": str(BASE_DIR / "models" / "llama-3b-q4.gguf")
}


# MODEL_PARAMS = {
#  "llama-1b": {
# "n_ctx": 512,
# "n_threads": 4,
# "n_batch":128,
# "use_mmap": True,
# "use_mlock": False,
# "verbose": False
#  },
# "llama-3b": {
# "n_ctx": 512,
# "n_threads": 4,
# "n_batch": 128,
# "use_mmap": True,
# "use_mlock": False,
# "verbose": False
#  }
# }
MODEL_PARAMS = {
    "llama-1b": {
        "n_ctx": 1024,          # Increased context window
        "n_threads": 6,         # Adjusted for better CPU utilization
        "n_batch": 64,         # Increased batch size
        "use_mmap": True,
        "use_mlock": True,      # Enable memory locking
        "verbose": False,
        "n_gpu_layers": 0       # Enable GPU acceleration for Mac
    },
    "llama-3b": {
        "n_ctx": 1024,
        "n_threads": 6,
        "n_batch": 64,
        "use_mmap": True,
        "use_mlock": True,
        "verbose": False,
        "n_gpu_layers": 0 #prev 0
    }
}