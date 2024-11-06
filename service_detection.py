import socket
import re

import re

class ServiceDetector:
    def __init__(self, probes_file='nmap-service-probes'):
        self.probes = self.load_service_probes(probes_file)

    def load_service_probes(self, probes_file):
        probes = []
        with open(probes_file, 'r') as file:
            lines = file.readlines()

       
        for line in lines:
            if line.startswith('match'):
                parts = line.split(" ", 2)
                protocol = parts[1]  # e.g., "http", "ftp", etc.
                pattern = parts[2].strip()  # The regex pattern
                
                # Safe regex extraction
                match = re.search(r'p/([^/]+)/', pattern)
                if match:
                    service_name = match.group(1)  # Extracting the service name
                else:
                    service_name = "Unknown Service"  # Fallback if no match
                
                # Look for version (v/) and description (d/)
                version_match = re.search(r'v/([^/]+)/', pattern)
                description_match = re.search(r'd/([^/]+)/', pattern)

                version = version_match.group(1) if version_match else None
                description = description_match.group(1) if description_match else None

                # Save each match pattern for later use
                probes.append({
                    'protocol': protocol,
                    'pattern': pattern,
                    'service_name': service_name,
                    'version': version,
                    'description': description
                })
        
        return probes

    def detect_service(self, response, port):
        detected_service = "Unknown Service"
        version = None
        description = None
        
        # Iterate over each probe and check if the response matches
        for probe in self.probes:
            pattern = probe['pattern']
            service_name = probe['service_name']
            probe_version = probe['version']
            probe_description = probe['description']

            if re.search(pattern, response):
                detected_service = service_name
                version = probe_version
                description = probe_description
                break  # We found the first match, no need to continue

        return detected_service, version, description


def load_service_probes(probes_file):
    probes = []
    
    with open(probes_file, 'r') as file:
        lines = file.readlines()

    # Parsing match entries
    for line in lines:
        if line.startswith('match'):
            parts = line.split(" ", 2)
            protocol = parts[1]  # e.g., "http", "ftp", etc.
            pattern = parts[2].strip()  # The regex pattern
            
            # Safe extraction of service name using regex
            match = re.search(r'p/([^/]+)/', pattern)
            service_name = match.group(1) if match else "Unknown"

            # Look for version (v/) and description (d/)
            version_match = re.search(r'v/([^/]+)/', pattern)
            description_match = re.search(r'd/([^/]+)/', pattern)

            version = version_match.group(1) if version_match else None
            description = description_match.group(1) if description_match else None

            # Save each match pattern for later use
            probes.append({
                'protocol': protocol,
                'pattern': pattern,
                'service_name': service_name,
                'version': version,
                'description': description
            })
    
    return probes

# Service Detection function - will now return service, version, and description in a single line
def detect_service(response, probes):
    detected_service = "Unknown Service"
    version = None
    description = None
    
    # Iterate over each probe and check if the response matches
    for probe in probes:
        pattern = probe['pattern']
        service_name = probe['service_name']
        probe_version = probe['version']
        probe_description = probe['description']

        # Use regular expression to match the service based on response
        if re.search(pattern, response):
            detected_service = service_name
            version = probe_version
            description = probe_description
            break  # We found the first match, no need to continue

    return detected_service, version, description

# Scan Ports function
def scan_ports(ip, ports):
    open_ports = []
    
    for port in ports:
        try:
            # Try connecting to the port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)  # Increased timeout to 3 seconds for slow responses
            result = sock.connect_ex((ip, port))

            if result == 0:
                open_ports.append(port)
                print(f"[AwareSec] Port {port} is open!")

                # Try to get the service response (you may need to send a simple request based on the service)
                response = ""
                if port == 80:  # HTTP
                    sock.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode())
                    response = sock.recv(1024).decode()

                elif port == 443:  # HTTPS
                    # SSL/TLS handshake (simple request for SSL banner)
                    sock = socket.create_connection((ip, port))
                    ssl_sock = ssl.wrap_socket(sock)
                    response = ssl_sock.recv(1024).decode()

                # Add more conditions for different ports (FTP, SSH, etc.) as needed

                # Detect the service, version, and description
                service, version, description = detect_service(response, probes)

                # Formatted output on the same line
                output = f"[AwareSec] Port {port}: Detected service - {service}"
                if version:
                    output += f" | Version: {version}"
                if description:
                    output += f" | Description: {description}"
                print(output)

            sock.close()

        except socket.error:
            pass
    
    return open_ports


# Load nmap-service-probes
probes_file = 'nmap-service-probes'  # Update the path to your nmap-service-probes file
probes = load_service_probes(probes_file)

# Example usage
ip = "192.168.10.1"
ports = [80, 443, 554]  # Example ports
scan_ports(ip, ports)
