import os
import shutil
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


def empty_the_directory(path):
    logger.info(f"Emptying dreictory {path}")
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


def get_available_size():
    _, _, free = shutil.disk_usage('/data')
    return free
