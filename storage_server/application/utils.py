import os
import logging

logger = logging.getLogger(__name__)


def create_empty_file(path):
    # Create directories
    directories = os.path.dirname(path)
    logger.info(f"Creating directories {directories}")
    os.makedirs(directories)
    # Create file
    logger.info(f"Creating file {path}")
    os.mknod(path)
