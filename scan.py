import sys
import socket
from scapy.all import *
from datetime import datetime
from service_detection import ServiceDetector


def exiting():
    print()
    time = datetime.now()
    current_time = time.strftime('%H:%M:%S')
    print(f"[AwareSec] Ending process at {current_time}")
    print("-----------------------------------------------------------------------------")

def scan_ip(target, ports=None, detect_service=False, detect_os=False, verbose=False, output_format='text'):
    time = datetime.now()
    current_time = time.strftime('%H:%M:%S')
    print(f"[AwareSec] Starting scan on {target} at {current_time}")
    
    # Parse ports
    if ports:
        if "-" in ports:
            p = ports.split("-")
            start = int(p[0])
            end = int(p[-1])
            if start < 1 or end > 65535:
                print("The port number can't be greater than 65535 or less than 1.")
                exiting()
                return 1
            ports = range(start, end + 1)
        elif "," in ports:    
            ports = [int(p) for p in ports.split(',')]
    else:
        ports = range(1, 1025)  # Default port range if none specified

    open_ports = []
    service_detector = ServiceDetector()  # Initialize service detector

    # Scan each port in the specified range
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set timeout to 1 second
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                if verbose:
                    print(f"[AwareSec] Port {port} is open!")
                
                # If service detection is enabled, fetch and match service
                if detect_service:
                    banner = fetch_banner(target, port)
                    service, version, description = service_detector.detect_service(banner, port)
                    print(f"[AwareSec] Port {port}: Detected service - {service}")
                    if version:
                        print(f"[AwareSec] Port {port}: Detected version - {version}")
                    if description:
                        print(f"[AwareSec] Port {port}: Service description - {description}")
            elif verbose:
                print(f"[AwareSec] Port {port} is closed or filtered.")

    if detect_os:
        # Add logic for OS detection here
        pass

    # Print results
    print(f"\nOpen ports for {target}: {open_ports}")
    exiting()

def fetch_banner(ip, port):
    """Fetch banner for a given port and IP."""
    try:
        with socket.create_connection((ip, port), timeout=1) as sock:
            sock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            return sock.recv(1024).decode("utf-8", errors="ignore")
    except socket.error:
        return ""

def show_help():
    print("[AwareSec] Usage: scan.py <target(s)> [<ports>] [<range>] [<domain>] [<service>] [<os>] [<verbose>] [<format>]")

def main():
    if len(sys.argv) < 2:
        print("[AwareSec] Error: At least one target is required.")
        show_help()
        sys.exit(1)

    # Handle multiple targets by splitting on commas
    targets = sys.argv[1].split(',')
    ports = sys.argv[2] if len(sys.argv) > 2 else None
    range_arg = sys.argv[3] if len(sys.argv) > 3 else None
    domain = sys.argv[4] if len(sys.argv) > 4 else None
    service = bool(sys.argv[5].lower() == 'true') if len(sys.argv) > 5 else False
    os_detection = bool(sys.argv[6].lower() == 'true') if len(sys.argv) > 6 else False
    verbose = bool(sys.argv[7].lower() == 'true') if len(sys.argv) > 7 else False
    output_format = sys.argv[8] if len(sys.argv) > 8 else 'text'

    for target in targets:
        print()
        scan_ip(target.strip(), ports, service, os_detection, verbose, output_format)

if __name__ == "__main__":
    main()
