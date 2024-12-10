import sys
import socket
import time
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

def save_output(results, detected_services, output_format):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    save_path = "/tmp/asec"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = f"{save_path}/autosave-{timestamp}.{output_format}"
    
    if output_format == 'txt':
        with open(filename, 'w') as f:
            for target, open_ports in results.items():
                f.write(f"Open ports for {target}: {open_ports}\n")
                if target in detected_services:
                    for port, service in detected_services[target].items():
                        f.write(f"  Port {port} - Detected service: {service}\n")
    elif output_format == 'csv':
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Target", "Open Ports", "Detected Services"])
            for target, open_ports in results.items():
                services = "; ".join([f"Port {port}: {service}" for port, service in detected_services.get(target, {}).items()])
                writer.writerow([target, ', '.join(map(str, open_ports)), services])
    elif output_format == 'json':
        output_data = {}
        for target, open_ports in results.items():
            output_data[target] = {
                "open_ports": open_ports,
                "detected_services": detected_services.get(target, {})
            }
        with open(filename, 'w') as f:
            json.dump(output_data, f, indent=4)
    print(f"[AwareSec] Results saved to {filename}")

def scan_ip(target, ports=None, detect_service=False, detect_os=False, verbose=False, output_format='txt', save_output_flag=False, timeout=1):
    time_start = datetime.now()
    current_time = time_start.strftime('%H:%M:%S')
    print(f"[AwareSec] Starting scan on {target} at {current_time}")
   
    if ports:
        if "-" in ports:
            start, end = map(int, ports.split("-"))
            if not (1 <= start <= 65535 and 1 <= end <= 65535):
                print("[AwareSec] Invalid port range.")
                return
            ports = range(start, end + 1)
        elif "," in ports:    
            ports = [int(p) for p in ports.split(',')]
    else:
        ports = range(1, 1025)

    open_ports = []
    detected_services = {}
    service_detector = ServiceDetector() if detect_service else None

    total_ports = len(list(ports))
    scanned = 0

    for port in ports:
        scanned += 1
        if verbose:
            print(f"\r[AwareSec] Scanning progress: {scanned}/{total_ports} ports", end='')
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"\n[AwareSec] Found open port: {port}")
                    
                    if detect_service:
                        service_info = service_detector.detect_service(port)
                        detected_services[port] = service_info
                        print(f"[AwareSec] Port {port} - Detected service: {service_info}")
                
                # Add small delay to avoid overwhelming target
                time.sleep(0.1)
                
        except socket.timeout:
            if verbose:
                print(f"\n[AwareSec] Port {port} timed out")
            continue
        except socket.error as e:
            if verbose:
                print(f"\n[AwareSec] Error scanning port {port}: {e}")
            continue

    print(f"\n[AwareSec] Scan completed. Found {len(open_ports)} open ports")
    print(f"[AwareSec] Open ports: {open_ports}")
    
    scan_time = datetime.now() - time_start
    print(f"[AwareSec] Scan duration: {scan_time}")
    
    if save_output_flag:
        return open_ports, detected_services
    else:
        return open_ports, {}

def main():
    if len(sys.argv) < 2:
        print("[AwareSec] Error: At least one target is required.")
        sys.exit(1)

    targets = sys.argv[1].split(',')
    ports = sys.argv[2] if len(sys.argv) > 2 else None
    service = bool(sys.argv[3].lower() == 'true') if len(sys.argv) > 3 else False
    os_detection = bool(sys.argv[4].lower() == 'true') if len(sys.argv) > 4 else False
    verbose = bool(sys.argv[5].lower() == 'true') if len(sys.argv) > 5 else True  # Default to verbose
    output_format = sys.argv[6] if len(sys.argv) > 6 else 'txt'
    save_output_flag = bool(sys.argv[7].lower() == 'true') if len(sys.argv) > 7 else False
    timeout = int(sys.argv[8]) if len(sys.argv) > 8 else 1

    results = {}
    all_detected_services = {}
    for target in targets:
        open_ports, detected_services = scan_ip(target.strip(), ports, service, os_detection, verbose, output_format, save_output_flag, timeout)
        results[target] = open_ports
        all_detected_services[target] = detected_services

    if save_output_flag:
        save_output(results, all_detected_services, output_format)

if __name__ == "__main__":
    main()