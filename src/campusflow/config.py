from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
FACES_DIR = DATA_DIR / "faces"
DB_PATH = DATA_DIR / "attendance.sqlite3"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "final_model.h5"
LABELS_PATH = MODEL_DIR / "labels.json"
CASCADE_PATH = MODEL_DIR / "haarcascade_frontalface_default.xml"
SAMPLES_PER_PERSON = 100
CONFIDENCE_THRESHOLD = 0.85
