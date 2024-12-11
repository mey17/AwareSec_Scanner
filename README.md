# AwareSec Project

AwareSec is a network scanning tool designed to detect open ports, services, and operating systems on target machines. It provides detailed information about the target's network configuration and saves the results in various formats.

![image](https://github.com/mey17/AwareSec_Scanner/blob/main/img.png)

## Features

- **Port Scanning**: Scan a range of ports on target machines.
- **Service Detection**: Identify services running on open ports using the `nmap-services` file.
- **OS Detection**: Detect the operating system of the target machine based on TTL values.
- **Verbose Output**: Enable detailed output for each scan.
- **Save Results**: Save scan results in `txt`, `csv`, or `json` formats.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/mey17/AwareSec_Scanner.git
    cd AwareSec_Scanner
    ```

2. **Run the Configuration Script**:
    ```bash
    ./config.sh
    ```

    This script will:
    - Install necessary Python packages.
    - Clone the project to your /opt/asec_project folder
    - Create a symbolic link to /opt/asec_project/asec.sh -> /usr/local/bin/asec
## Usage

After installation, you can run the AwareSec project by calling `asec` from the terminal:

```bash
asec <target> [options]
```

## Options
-h, --help: Show help message and exit.
-p, --ports <ports>: Specify ports to scan (e.g., 22,80,443 or 1-1024, max is 65535).
-s, --service: Attempt to detect services running on open ports.
-o, --os: Attempt to detect the operating system.
-v, --verbose: Enable verbose output for detailed results.
-f, --format <type>: Specify output format (txt, json, csv).
-t <timeout>: Set socket timeout (1, 2, 3, 4 seconds).
-save: Save the output to asec.



## Thank u ;)
