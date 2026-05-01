## Define DB Table pathway

from pathlib import Path

# Initialize Database file and place in NN directory
DB_PATH = Path(__file__).resolve().parent / "OHLCV_data.db"

# URL for database
SQLA_DB_URL = f"sqlite:///{DB_PATH.as_posix()}"
