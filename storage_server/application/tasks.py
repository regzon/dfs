import os
import socket
import logging
import requests
import urllib.parse

import uwsgi
from uwsgidecorators import timer, spool

from .utils import get_available_size

logger = logging.getLogger(__name__)


def get_host_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def send_to_naming_server(url, data):
    naming_server = os.environ['NAMING_SERVER']
    full_url = urllib.parse.urljoin(naming_server, url)

    try:
        response = requests.post(full_url, data=data)
    except requests.exceptions.ConnectTimeout:
        logger.error(f"Naming server connection timed out")
        return False
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to connect to the naming server")
        return False

    if not response.ok:
        code = response.status_code
        logger.error(f"Naming server responded with code {code}")
        logger.error(f"Error message: {response.text}")
        return False

    return True


@timer(secs=10, target='spooler')
def send_heartbeat(signum):
    logger.info(f"Sending a heartbeat")
    url = 'storage/heartbeat'
    data = {
        'size': get_available_size(),
        'ip_address': get_host_ip(),
        'port': os.environ['SERVICE_PORT'],
    }
    result = send_to_naming_server(url, data)
    if not result:
        logger.error("Failed sending heartbeat")


@spool(pass_arguments=True)
def update_file_status(path, status):
    logger.info(f"Updating file {path} status to {status}")
    url = 'storage/update_status'
    data = {
        'path': path,
        'status': status,
        'ip_address': get_host_ip(),
        'port': os.environ['SERVICE_PORT'],
    }
    result = send_to_naming_server(url, data)
    if not result:
        logger.error("Failed updating file status. Retrying...")
        return uwsgi.SPOOL_RETRY
    return uwsgi.SPOOL_OK
