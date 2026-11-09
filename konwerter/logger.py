import logging
from pathlib import Path

# log file is saved in the main project folder
LOG_FILE = Path(__file__).resolve().parent.parent / "konwerter.log"


def setup_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="utf-8",
    )