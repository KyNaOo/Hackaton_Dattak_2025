"""
HTML templates for the Flask application.
"""

INDEX_TEMPLATE = '''
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

LOGS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Client Access Logs</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        .header {
            background: #2d2d30;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        h1 {
            margin: 0 0 10px 0;
            color: #4ec9b0;
        }
        .stats {
            color: #9cdcfe;
            font-size: 14px;
        }
        .log-entry {
            background: #252526;
            border-left: 4px solid #007acc;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        .log-entry:hover {
            background: #2d2d30;
            border-left-color: #4ec9b0;
        }
        .log-field {
            margin: 8px 0;
            line-height: 1.6;
        }
        .log-label {
            color: #4ec9b0;
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }
        .log-value {
            color: #ce9178;
        }
        .headers {
            margin-top: 10px;
            padding: 10px;
            background: #1e1e1e;
            border-radius: 4px;
        }
        .headers-title {
            color: #4ec9b0;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .header-item {
            margin: 4px 0;
            padding-left: 10px;
            color: #9cdcfe;
            font-size: 13px;
        }
        .no-logs {
            text-align: center;
            padding: 40px;
            color: #858585;
            font-size: 18px;
        }
        .refresh-btn {
            background: #007acc;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-left: 20px;
        }
        .refresh-btn:hover {
            background: #005a9e;
        }
    </style>
    <script>
        function refreshLogs() {
            location.reload();
        }
        // Auto-refresh every 10 seconds
        setTimeout(function() {
            location.reload();
        }, 10000);
    </script>
</head>
<body>
    <div class="header">
        <h1>Client Access Logs</h1>
        <div class="stats">
            Total Entries: {{ total_entries }}
            <button class="refresh-btn" onclick="refreshLogs()">Refresh Now</button>
            <span style="margin-left: 20px; color: #858585;">Auto-refresh in 10s</span>
        </div>
    </div>

    {% if logs %}
        {% for log in logs %}
        <div class="log-entry">
            <div class="log-field">
                <span class="log-label">Timestamp:</span>
                <span class="log-value">{{ log.timestamp }}</span>
            </div>
            <div class="log-field">
                <span class="log-label">Endpoint:</span>
                <span class="log-value">{{ log.endpoint }}</span>
            </div>
            <div class="log-field">
                <span class="log-label">Public IP:</span>
                <span class="log-value">{{ log.ip_address }}</span>
            </div>
            <div class="log-field">
                <span class="log-label">Remote Addr:</span>
                <span class="log-value">{{ log.remote_addr }}</span>
            </div>
            <div class="log-field">
                <span class="log-label">Method:</span>
                <span class="log-value">{{ log.method }}</span>
            </div>
            <div class="log-field">
                <span class="log-label">Full Path:</span>
                <span class="log-value">{{ log.full_path }}</span>
            </div>
            <div class="log-field">
                <span class="log-label">User Agent:</span>
                <span class="log-value">{{ log.user_agent }}</span>
            </div>
            <div class="log-field">
                <span class="log-label">Referer:</span>
                <span class="log-value">{{ log.referer or 'None' }}</span>
            </div>
            <div class="headers">
                <div class="headers-title">Headers:</div>
                {% for header, value in log.headers.items() %}
                <div class="header-item">{{ header }}: {{ value }}</div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    {% else %}
        <div class="no-logs">No logs found yet. Waiting for client access...</div>
    {% endif %}
</body>
</html>
'''
