from flask import Flask, send_file, render_template_string, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Ensure log directory exists
LOG_DIR = 'log'
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, 'client_access.log')
JSON_LOG_FILE = os.path.join(LOG_DIR, 'client_access.json')

def log_client_info(endpoint):
    """Log client information when they access an endpoint"""
    client_info = {
        'timestamp': datetime.now().isoformat(),
        'endpoint': endpoint,
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'referer': request.headers.get('Referer'),
        'method': request.method,
        'full_path': request.full_path,
        'headers': dict(request.headers)
    }

    # Format log entry
    log_entry = "\n" + "="*50 + "\n"
    log_entry += f"CLIENT ACCESS LOG - {endpoint}\n"
    log_entry += "="*50 + "\n"
    log_entry += f"Timestamp: {client_info['timestamp']}\n"
    log_entry += f"IP Address: {client_info['ip_address']}\n"
    log_entry += f"User Agent: {client_info['user_agent']}\n"
    log_entry += f"Referer: {client_info['referer']}\n"
    log_entry += f"Method: {client_info['method']}\n"
    log_entry += f"Full Path: {client_info['full_path']}\n"
    log_entry += "\nAll Headers:\n"
    for header, value in client_info['headers'].items():
        log_entry += f"  {header}: {value}\n"
    log_entry += "="*50 + "\n"

    # Write to log file
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)

    # Also write JSON format for easy parsing
    with open(JSON_LOG_FILE, 'a') as f:
        f.write(json.dumps(client_info) + '\n')

    # Print to console as well
    print(log_entry)

    return client_info

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .container {
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>You've been hacked !</h1>
        <img src="/image" alt="Displayed Image">
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Display HTML page with the image"""
    log_client_info('/')
    return render_template_string(HTML_TEMPLATE)

@app.route('/image')
def get_image():
    """GET endpoint that returns an image"""
    log_client_info('/image')

    # You can change this path to your actual image file
    image_path = 'images/rickroll.jpg'

    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
        # Return a placeholder or error message
        return "Image not found. Please place an 'image.jpg' file in the server directory.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
