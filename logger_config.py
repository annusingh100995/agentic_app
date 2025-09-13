import logging
import sys

# Configure root logger
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("app.log"),  # Write logs to file
            logging.StreamHandler(sys.stdout) # Also print to console
        ]
    )
    logger = logging.getLogger("master_api")
    return logger

# Create logger instance
logger = setup_logger()
