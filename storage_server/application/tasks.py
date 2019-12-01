import os
import logging

from uwsgidecorators import timer

logger = logging.getLogger(__name__)


@timer(secs=5, target='spooler')
def send_heartbeat(signum):
    storage_id = os.environ['STORAGE_ID']
    logger.info(f"Heartbeat from {storage_id}")
