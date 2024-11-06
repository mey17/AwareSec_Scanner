# service_detection.py

import re

class ServiceDetector:
    def __init__(self, services_file='nmap-services'):
        self.services = self.load_services(services_file)

    def load_services(self, services_file):
        services = {}
        with open(services_file, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    parts = line.split()
                    service_name = parts[0]
                    port_protocol = parts[1]
                    probability = parts[2]
                    description = " ".join(parts[3:]) if len(parts) > 3 else ""

                    # Parse port and protocol
                    port, protocol = port_protocol.split('/')

                    # Store service entry in dictionary
                    if port not in services:
                        services[port] = []
                    services[port].append({
                        'service_name': service_name,
                        'protocol': protocol,
                        'probability': probability,
                        'description': description
                    })
        return services

    def detect_service(self, port):
        """Retrieve all service variants for a given port from the loaded nmap-services data."""
        return self.services.get(str(port), [])
