
import socket

# A basic dictionary mapping ports to common services
PORT_SERVICE_MAP = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy",
    # Add more ports and services as needed
}

def detect_service(port):
    """
    Returns a service name for a given port.
    """
    return PORT_SERVICE_MAP.get(port, "Unknown Service")

def banner_grab(ip, port):
    """
    Attempts to grab the banner from a service running on the specified IP and port.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((ip, port))
            sock.send(b"HEAD / HTTP/1.1\r\n\r\n")
            banner = sock.recv(1024).decode('utf-8')
            return banner.strip()
    except Exception as e:
        return f"Could not grab banner: {e}"
