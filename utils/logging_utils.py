"""
Utility functions for logging and error handling.
"""
import logging

def setup_logger(name: str = "flight_pathfinder") -> logging.Logger:
    """
    Sets up and returns a logger with a standard format.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
