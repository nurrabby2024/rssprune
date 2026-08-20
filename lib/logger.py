"""Small leveled logger for RSSPrune."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

RESET = "\033[0m"
COLORS = {
 "DEBUG": "\033[36m",
 "INFO": "\033[32m",
 "WARNING": "\033[33m",
 "ERROR": "\033[31m",
 "CRITICAL": "\033[35m",
}


class ColorFormatter(logging.Formatter):
 def format(self, record):
 color = COLORS.get(record.levelname, RESET)
 original = record.msg
 record.msg = f"{color}{record.msg}{RESET}"
 try:
 return super().format(record)
 finally:
 record.msg = original


def build_logger(name="rssprune", level=None):
 level = level or os.getenv("LOG_LEVEL", "INFO").upper()
 logger = logging.getLogger(name)
 logger.setLevel(getattr(logging, level, logging.INFO))

 if not logger.handlers:
 console = logging.StreamHandler(sys.stderr)
 console.setFormatter(ColorFormatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s", "%H:%M:%S"))
 logger.addHandler(console)

 log_file = os.getenv("LOG_FILE")
 if log_file:
 file_handler = RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=3)
 file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s"))
 logger.addHandler(file_handler)

 return logger


log = build_logger()