"""
Package para manejo de logs
"""
import sys
import logging

def setup_logging(log_level=logging.INFO):
    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=log_level,
    )

def get_logger(name):
    return logging.getLogger(name)

