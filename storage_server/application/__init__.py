import os
import shutil
import logging
import logging.config

from flask import Flask, request, send_file, jsonify

from .tasks import update_file_status
from .utils import (
    create_empty_file,
    empty_the_directory,
    get_available_size,
)

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

    @app.route('/initialize_root', methods=['POST'])
    def initialize_root():
        logger.info("Received a root initialization request")
        empty_the_directory(app.config['UPLOAD_FOLDER'])
        available_size = get_available_size()
        data = {'size': available_size}
        logger.info("Finished a root initialization successfully")
        return jsonify(data)

    @app.route('/create_file', methods=['POST'])
    def initialize_file():
        logger.info("Received a file creation request")
        if 'path' not in request.form or not request.form['path']:
            logger.warning("Request to file initialization without path")
            return "Parameter path is required", 400
        path = request.form['path']
        local_path = get_local_path(path)
        create_empty_file(local_path)
        logger.info("Finished a file creation successfully")
        return jsonify({})

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
        return jsonify({})

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
        return send_file(
            local_path,
            as_attachment=True,
            attachment_filename=filename,
        )

    @app.route('/delete_file', methods=['POST'])
    def delete_file():
        logger.info("Received a file deletion request")
        if 'path' not in request.form or not request.form['path']:
            logger.warning("Request to file deletion without path")
            return "Parameter path is required", 400
        path = request.form['path']
        local_path = get_local_path(path)
        if not os.path.exists(local_path):
            logger.warning("Deletion of the file that doesn't exist")
            return "File doesn't exist", 400
        logger.info(f"Deleting file {path}")
        os.remove(local_path)
        logger.info("Finished deleting a file successfully")
        return jsonify({})

    @app.route('/delete_dir', methods=['POST'])
    def delete_dir():
        logger.info("Received a directory deletion request")
        if 'path' not in request.form or not request.form['path']:
            logger.warning("Request to directory deletion without path")
            return "Parameter path is required", 400
        path = request.form['path']
        local_path = get_local_path(path)
        if not os.path.exists(local_path):
            logger.warning("Deletion of the directory that doesn't exist")
            return "File doesn't exist", 400
        logger.info(f"Deleting directory {path}")
        shutil.rmtree(local_path)
        logger.info("Finished deleting a directory successfully")
        return jsonify({})

    return app
