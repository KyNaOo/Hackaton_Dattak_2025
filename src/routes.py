"""
Route handlers for the Flask application.
"""
import os
from flask import send_file, render_template_string
from logger import log_client_info, read_logs
from templates import INDEX_TEMPLATE, LOGS_TEMPLATE
from config import IMAGE_FILE


def index():
    """Display HTML page with the image tracker."""
    log_client_info('/')
    return render_template_string(INDEX_TEMPLATE)


def get_image():
    """GET endpoint that returns the tracking image."""
    log_client_info('/image')

    if os.path.exists(IMAGE_FILE):
        return send_file(IMAGE_FILE, mimetype='image/jpeg')
    else:
        return "Image not found. Please place an 'image.jpg' file in the server directory.", 404


def view_logs():
    """Display client access logs in HTML format."""
    logs = read_logs()
    return render_template_string(LOGS_TEMPLATE, logs=logs, total_entries=len(logs))
