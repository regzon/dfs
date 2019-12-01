import os
import logging

logger = logging.getLogger(__name__)


def create_empty_file(path):
    if os.path.exists(path):
        logger.info(f"File {path} already exists")
        return
    # Create directories
    directories = os.path.dirname(path)
    logger.info(f"Creating directories {directories}")
    os.makedirs(directories, exist_ok=True)
    # Create file
    logger.info(f"Creating file {path}")
    os.mknod(path)
