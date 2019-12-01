import os
import logging
import logging.config

from flask import Flask, request, send_file

from .utils import create_empty_file
from .tasks import update_file_status

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '/data'

    logging.config.fileConfig(
        'logging.conf',
        disable_existing_loggers=False,
    )

    def get_local_path(path):
        path = os.path.normpath(path)
        return os.path.join(app.config['UPLOAD_FOLDER'], path[1:])

    @app.route('/initialize_file', methods=['POST'])
    def initialize_file():
        logger.info("Received a file initialization request")
        if 'path' not in request.form or not request.form['path']:
            logger.warning("Request to file initialization without path")
            return "Parameter path is required", 400
        path = request.form['path']
        local_path = get_local_path(path)
        create_empty_file(local_path)
        logger.info("Finished a file initialization successfully")
        return "Success"

    @app.route('/upload_file', methods=['POST'])
    def upload_file():
        logger.info("Received a file upload request")
        # Check that file is sent
        if 'file' not in request.files:
            logger.warning("Request to file upload without file")
            return "File is required", 400
        file = request.files['file']
        # Check that file path is sent
        if 'path' not in request.form or not request.form['path']:
            logger.warning("Request to file upload without path")
            return "Parameter path is required", 400
        path = request.form['path']
        local_path = get_local_path(path)
        file.save(local_path)
        # Send notification to the naming server
        update_file_status.spool(path, status='ready')
        logger.info("Finished a file upload successfully")
        return "Success"

    @app.route('/download_file', methods=['GET'])
    def download_file():
        logger.info("Received a file download request")
        if 'path' not in request.args or not request.args['path']:
            logger.warning("Request to file download without path")
            return "Parameter path is required", 400
        path = request.args['path']
        filename = os.path.basename(path)
        local_path = get_local_path(path)
        logger.info("Sending a file to the client")
        return send_file(local_path, attachment_filename=filename)

    @app.route('/delete_file', methods=['POST'])
    def delete_file():
        logger.info("Received a file deletion request")
        if 'path' not in request.form or not request.form['path']:
            logger.warning("Request to file deletion without path")
            return "Parameter path is required", 400
        path = request.form['path']
        local_path = get_local_path(path)
        logger.info(f"Deleting file {path}")
        os.remove(local_path)
        logger.info("Finished deleting a file successfully")
        return "Success"

    return app
