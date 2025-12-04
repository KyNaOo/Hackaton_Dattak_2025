"""
Client access logging functionality.
"""
import json
from datetime import datetime
from flask import request
from config import LOG_FILE, JSON_LOG_FILE


def _get_client_ip():
    """
    Get the client's public IP address, handling proxies and ngrok.

    Returns:
        str: Client's public IP address
    """
    # Check for common proxy headers (ngrok, cloudflare, nginx, etc.)
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs (client, proxy1, proxy2, ...)
        # The first one is the original client IP
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    elif request.headers.get('CF-Connecting-IP'):  # Cloudflare
        return request.headers.get('CF-Connecting-IP')
    elif request.headers.get('True-Client-IP'):  # Akamai, Cloudflare
        return request.headers.get('True-Client-IP')
    else:
        # Fallback to remote_addr (will be 127.0.0.1 for local or proxy IP)
        return request.remote_addr


def log_client_info(endpoint):
    """
    Log client information when they access an endpoint.

    Args:
        endpoint: The endpoint that was accessed

    Returns:
        dict: Dictionary containing all client information
    """
    public_ip = _get_client_ip()

    client_info = {
        'timestamp': datetime.now().isoformat(),
        'endpoint': endpoint,
        'ip_address': public_ip,
        'remote_addr': request.remote_addr,  # Keep original for debugging
        'user_agent': request.headers.get('User-Agent'),
        'referer': request.headers.get('Referer'),
        'method': request.method,
        'full_path': request.full_path,
        'headers': dict(request.headers)
    }

    # Format log entry for text file
    log_entry = _format_log_entry(client_info, endpoint)

    # Write to text log file
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)

    # Write to JSON log file
    with open(JSON_LOG_FILE, 'a') as f:
        f.write(json.dumps(client_info) + '\n')

    # Print to console
    print(log_entry)

    return client_info


def _format_log_entry(client_info, endpoint):
    """
    Format client info into a human-readable log entry.

    Args:
        client_info: Dictionary containing client information
        endpoint: The endpoint that was accessed

    Returns:
        str: Formatted log entry
    """
    log_entry = "\n" + "="*50 + "\n"
    log_entry += f"CLIENT ACCESS LOG - {endpoint}\n"
    log_entry += "="*50 + "\n"
    log_entry += f"Timestamp: {client_info['timestamp']}\n"
    log_entry += f"Public IP: {client_info['ip_address']}\n"
    log_entry += f"Remote Addr: {client_info['remote_addr']}\n"
    log_entry += f"User Agent: {client_info['user_agent']}\n"
    log_entry += f"Referer: {client_info['referer']}\n"
    log_entry += f"Method: {client_info['method']}\n"
    log_entry += f"Full Path: {client_info['full_path']}\n"
    log_entry += "\nAll Headers:\n"
    for header, value in client_info['headers'].items():
        log_entry += f"  {header}: {value}\n"
    log_entry += "="*50 + "\n"

    return log_entry


def read_logs():
    """
    Read and parse all JSON logs.

    Returns:
        list: List of log entries (newest first)
    """
    logs = []

    try:
        with open(JSON_LOG_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        pass

    # Reverse to show newest first
    logs.reverse()

    return logs
