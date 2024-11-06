#!/bin/bash

# Get the directory of the script
# SCRIPT_DIR="/opt/Asec_Project"
SCRIPT_DIR="."

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${YELLOW}[AwareSec] Usage: asec [options] <target>${NC}"
    echo ""
    echo -e "${YELLOW}[AwareSec] Options:${NC}"
    echo -e "${YELLOW}[AwareSec]  -h, --help           Show this help message and exit (Maximum port number is 65535)${NC}"
    echo -e "${YELLOW}[AwareSec]  -p, --ports <ports>  Specify ports to scan (e.g., 22,80,443 or 1-1024)${NC}"
    echo -e "${YELLOW}[AwareSec]  -r, --range <range>  Specify a range of IP addresses (e.g., 192.168.1.1-192.168.1.10)${NC}"
    echo -e "${YELLOW}[AwareSec]  -d, --domain <domain> Specify a domain to scan${NC}"
    echo -e "${YELLOW}[AwareSec]  -s, --service        Attempt to detect services running on open ports${NC}"
    echo -e "${YELLOW}[AwareSec]  -o, --os             Attempt to detect the operating system${NC}"
    echo -e "${YELLOW}[AwareSec]  -v, --verbose        Enable verbose output for detailed results${NC}"
    echo -e "${YELLOW}[AwareSec]  -f, --format <type>  Specify output format (text, json, csv)${NC}"
}

expand_cidr() {
    local cidr=$1
    local ip base_ip mask i

    # Extract IP and subnet from CIDR
    ip=$(echo $cidr | cut -d '/' -f1)
    mask=$(echo $cidr | cut -d '/' -f2)

    # Convert IP to binary format
    IFS=. read -r i1 i2 i3 i4 <<< "$ip"
    base_ip=$(( (i1 << 24) + (i2 << 16) + (i3 << 8) + i4 ))

    # Calculate network address by zeroing out host bits
    net_addr=$(( base_ip & ((2**32 - 1) << (32 - mask)) ))

    # Calculate number of hosts
    host_bits=$(( 32 - mask ))
    num_hosts=$(( 2 ** host_bits ))

    # Generate IP range starting from the network address
    for (( i=0; i<num_hosts; i++ )); do
        ip=$(( net_addr + i ))
        echo "$(( (ip >> 24) & 255 )).$(( (ip >> 16) & 255 )).$(( (ip >> 8) & 255 )).$(( ip & 255 ))"
    done
}

is_reachable() {
    local ip=$1
    ping -c 1 -W 1 "$ip" &> /dev/null
    return $?
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        -p|--ports) ports="$2"; shift ;;
        -r|--range) range="$2"; shift ;;
        -d|--domain) domain="$2"; shift ;;
        -s|--service) service=true ;;
        -o|--os) os=true ;;
        -v|--verbose) verbose=true ;;
        -f|--format) format="$2"; shift ;;
        *) target="$1" ;;
    esac
    shift
done

# Check if target is provided
if [[ -z "$target" ]]; then
    echo -e "${RED}[AwareSec] Error: Target is required.${NC}"
    show_help
    exit 1
fi

# Check if target is CIDR and expand it
if [[ "$target" == */* ]]; then
    echo -e "${GREEN}Expanding CIDR notation: $target${NC}"
    ip_list=$(expand_cidr "$target")
else
    ip_list=$target
fi

# Scan only reachable IPs
for ip in $ip_list; do
    if is_reachable "$ip"; then
        echo -e "${GREEN}[AwareSec] IP $ip is reachable. Starting scan...${NC}"
        python3 "$SCRIPT_DIR/scan.py" "$ip" "$ports" "$range" "$domain" "$service" "$os" "$verbose" "$format"
    else
        if [[ $verbose == true ]]; then
            echo -e "${RED}[AwareSec] IP $ip is not reachable. Skipping scan.${NC}"
        fi    
    fi
done
