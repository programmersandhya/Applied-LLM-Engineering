import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
logs_path = os.path.join(BASE_DIR, "logs")
file_name = f"businessintel_ai_{datetime.now().strftime('%Y%m%d_%H_%M')}.log"
log_file_path = os.path.join(logs_path, file_name)
os.makedirs(logs_path, exist_ok=True)
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)
logger = logging.getLogger(__name__)

