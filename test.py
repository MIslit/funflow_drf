import os
from pathlib import Path
from decouple import config
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).resolve().parents
BASE_DIR = Path(__file__).parent

print(BASE_DIR)