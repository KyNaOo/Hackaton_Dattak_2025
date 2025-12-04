"""
Configuration settings for the Flask image tracker server.
"""
import os

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Log directory and files
LOG_DIR = os.path.join(PROJECT_ROOT, 'log')
LOG_FILE = os.path.join(LOG_DIR, 'client_access.log')
JSON_LOG_FILE = os.path.join(LOG_DIR, 'client_access.json')

# Images directory
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'images')
IMAGE_FILE = os.path.join(IMAGES_DIR, 'rickroll.jpg')

# Server configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
