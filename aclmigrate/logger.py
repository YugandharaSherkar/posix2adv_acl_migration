"""
logger.py
"""

import logging
from pathlib import Path

#
# Create log directory if it doesn't exist
#
log_directory = Path("logs")
log_directory.mkdir(exist_ok=True)

log_file = log_directory / "migration.log"

logger = logging.getLogger("aclmigrate")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s"
)

#
# Console output
#
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

#
# Log file
#
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)