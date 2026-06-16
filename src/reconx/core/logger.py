import logging
import sys
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("reconx")
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File
    fh = logging.FileHandler("logs/reconx.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger

logger = setup_logging()
