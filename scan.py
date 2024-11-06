# scan.py

import sys
import socket
from datetime import datetime
from service_detection import ServiceDetector  # Import the ServiceDetector class

def exiting():
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
            start, end = map(int, ports.split("-"))
            if not (1 <= start <= 65535 and 1 <= end <= 65535):
                print("[AwareSec] Invalid port range.")
                exiting()
                return
            ports = range(start, end + 1)
        elif "," in ports:    
            ports = [int(p) for p in ports.split(',')]
    else:
        ports = range(1, 1025)

    open_ports = []
    service_detector = ServiceDetector() if detect_service else None

    # Scan each port in the specified range
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                
                # Get service info and print all variants for this port
                if detect_service and service_detector:
                    services = service_detector.detect_service(port)
                    if services:
                        print(f"[AwareSec] Port {port} - Detected services:")
                        for service in services:
                            print(f"{service['service_name']}\t{port}/{service['protocol']}\t{service['probability']}\t{service['description']}")
                    else:
                        print(f"[AwareSec] Port {port}: No specific service information available.")
                elif verbose:
                    print(f"[AwareSec] Port {port} is open!")
            elif verbose:
                print(f"[AwareSec] Port {port} is closed or filtered.")

    # Print summary of open ports
    print(f"\nOpen ports for {target}: {open_ports}")
    exiting()

def show_help():
    print("[AwareSec] Usage: scan.py <target(s)> [<ports>] [<range>] [<domain>] [<service>] [<os>] [<verbose>] [<format>]")

def main():
    if len(sys.argv) < 2:
        print("[AwareSec] Error: At least one target is required.")
        show_help()
        sys.exit(1)

    # Parsing command-line arguments
    targets = sys.argv[1].split(',')
    ports = sys.argv[2] if len(sys.argv) > 2 else None
    range_arg = sys.argv[3] if len(sys.argv) > 3 else None
    domain = sys.argv[4] if len(sys.argv) > 4 else None
    service = bool(sys.argv[5].lower() == 'true') if len(sys.argv) > 5 else True
    os_detection = bool(sys.argv[6].lower() == 'true') if len(sys.argv) > 6 else False
    verbose = bool(sys.argv[7].lower() == 'true') if len(sys.argv) > 7 else False
    output_format = sys.argv[8] if len(sys.argv) > 8 else 'text'

    for target in targets:
        print()
        scan_ip(target.strip(), ports, service, os_detection, verbose, output_format)

if __name__ == "__main__":
    main()
