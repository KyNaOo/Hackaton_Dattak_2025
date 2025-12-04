"""
Flask Image Tracker Server

A simple Flask server that serves a webpage with an embedded image
and logs detailed client information for every request.
"""
from flask import Flask
from config import HOST, PORT, DEBUG
from routes import index, get_image, view_logs

# Initialize Flask application
app = Flask(__name__)

# Register routes
app.route('/')(index)
app.route('/image')(get_image)
app.route('/logs')(view_logs)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
