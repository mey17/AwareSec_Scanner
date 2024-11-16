import sys
import socket
import threading
import json
import csv
from datetime import datetime
import os
from service_detection import ServiceDetector



def exiting():
    time = datetime.now()
    current_time = time.strftime('%H:%M:%S')
    print(f"[AwareSec] Ending process at {current_time}")
    print("-----------------------------------------------------------------------------")
def scan_ip(target, ports=None, detect_service=False, detect_os=False, verbose=False, output_format='txt'):
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
    detected_services = {}
    service_detector = ServiceDetector() if detect_service else None

    # Scan each port in the specified range
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)  # Increase timeout to handle network latency
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                detected_services[port] = []
                
                # Get service info and save all variants for this port
                if detect_service and service_detector:
                    services = service_detector.detect_service(port)
                    if services:
                        print(f"[AwareSec] Port {port} - Detected services:")
                        for service in services:
                            detected_services[port].append(service)
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




def main():
    if len(sys.argv) < 2:
        print("[AwareSec] Error: At least one target is required.")
        sys.exit(1)

    targets = sys.argv[1].split(',')
    ports = sys.argv[2] if len(sys.argv) > 2 else None
    range_arg = sys.argv[3] if len(sys.argv) > 3 else None
    
    service = bool(sys.argv[4].lower() == 'true') if len(sys.argv) > 5 else False
    os_detection = bool(sys.argv[5].lower() == 'true') if len(sys.argv) > 6 else False
    verbose = bool(sys.argv[6].lower() == 'true') if len(sys.argv) > 7 else False
   
    for target in targets:
        print()
        scan_ip(target.strip(), ports, service, os_detection, verbose )

    

if __name__ == "__main__":
    main()
