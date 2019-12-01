import logging

from uwsgidecorators import timer

logger = logging.getLogger(__name__)


@timer(secs=5, target='spooler')
def send_heartbeat(signum):
    logger.warning("Heartbeat")
