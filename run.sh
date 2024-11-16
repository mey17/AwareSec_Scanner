#!/bin/bash

SCRIPT_DIR="."

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

show_help() {
    echo -e "${YELLOW}[AwareSec] Usage: asec [options] <target>${NC}"
    echo ""
    echo -e "${YELLOW}[AwareSec] Options:${NC}"
    echo -e "${YELLOW}[AwareSec]  -h, --help           Show this help message and exit (Maximum port number is 65535)${NC}"
    echo -e "${YELLOW}[AwareSec]  -p, --ports <ports>  Specify ports to scan (e.g., 22,80,443 or 1-1024)${NC}"
    echo -e "${YELLOW}[AwareSec]  -r, --range <range>  Specify a range of IP addresses (e.g., 192.168.1.1-192.168.1.10)${NC}"
    echo -e "${YELLOW}[AwareSec]  -s, --service        Attempt to detect services running on open ports${NC}"
    echo -e "${YELLOW}[AwareSec]  -o, --os             Attempt to detect the operating system${NC}"
    echo -e "${YELLOW}[AwareSec]  -v, --verbose        Enable verbose output for detailed results${NC}"
    echo -e "${YELLOW}[AwareSec]  -f, --format <type>  Specify output format (txt, json, csv)${NC}"
}

# Default values
ports=""
range=""
service=false
os=false
verbose=false
format="txt"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        -p|--ports) ports="$2"; shift ;;
        -r|--range) range="$2"; shift ;;
        -s|--service) service=true ;;
        -o|--os) os=true ;;
        -v|--verbose) verbose=true ;;
        -f|--format) format="$2"; shift ;;
        *) target="$1" ;;
    esac
    shift
done

echo -e "${CYAN}Selected Options:${NC}"
if [[ "$ports" != "" ]]; then echo -e "${GREEN}[+port+]${NC} Ports: $ports"; fi
if [[ "$service" == true ]]; then echo -e "${GREEN}[+service+]${NC} Service Detection Enabled"; fi
if [[ "$os" == true ]]; then echo -e "${GREEN}[+os+]${NC} OS Detection Enabled"; fi
if [[ "$verbose" == true ]]; then echo -e "${GREEN}[+verbose+]${NC} Verbose Mode Enabled"; fi
if [[ "$range" != "" ]]; then echo -e "${GREEN}[+range+]${NC} Range: $range"; fi
if [[ "$domain" != "" ]]; then echo -e "${GREEN}[+domain+]${NC} Domain: $domain"; fi
echo ""

if [[ -z "$target" ]]; then
    echo -e "${RED}[AwareSec] Error: Target is required.${NC}"
    show_help
    exit 1
fi

expand_cidr() {
    local cidr=$1
    local ip base_ip mask i

    ip=$(echo $cidr | cut -d '/' -f1)
    mask=$(echo $cidr | cut -d '/' -f2)

    IFS=. read -r i1 i2 i3 i4 <<< "$ip"
    base_ip=$(( (i1 << 24) + (i2 << 16) + (i3 << 8) + i4 ))

    net_addr=$(( base_ip & ((2**32 - 1) << (32 - mask)) ))

    host_bits=$(( 32 - mask ))
    num_hosts=$(( 2 ** host_bits ))

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

resolve_domain() {
    local domain=$1
    ip=$(getent hosts "$domain" | awk '{ print $1 }')
    echo "$ip"
}

results_file="/tmp/asec/autosave-$(date +%Y%m%d-%H%M%S).$format"
declare -A results

if [[ "$target" == */* ]]; then
    echo -e "${GREEN}[AwareSec] Expanding CIDR notation: $target${NC}"
    ip_list=$(expand_cidr "$target")
elif [[ "$target" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    ip_list=$target
else
    echo -e "${GREEN}[AwareSec] Resolving domain: $target${NC}"
    ip_list=$(resolve_domain "$target")
fi

for ip in $ip_list; do
    if is_reachable "$ip"; then
        echo -e "${GREEN}[AwareSec] IP $ip is reachable. Starting scan...${NC}"
        python3 "$SCRIPT_DIR/scan.py" "$ip" "$ports" "$range" "$target" "$service" "$os" "$verbose" "$format"
        open_ports=$(python3 "$SCRIPT_DIR/scan.py" "$ip" "$ports" "$range" "$target" "$service" "$os" "$verbose" "$format")
        
        results["$ip"]="$open_ports"
    else
        if [[ $verbose == true ]]; then
            echo -e "${RED}[AwareSec] IP $ip is not reachable. Skipping scan.${NC}"
        fi    
    fi
done

# Save all results to a single file
if [[ "$format" == "txt" ]]; then
    for ip in "${!results[@]}"; do
        echo "Open ports for $ip: ${results[$ip]}" >> "$results_file"
    done
elif [[ "$format" == "csv" ]]; then
    echo "Target,Open Ports" > "$results_file"
    for ip in "${!results[@]}"; do
        echo "$ip,${results[$ip]}" >> "$results_file"
    done
elif [[ "$format" == "json" ]]; then
    json_results=$(printf '%s\n' "${results[@]}" | jq -R . | jq -s .)
    echo "$json_results" > "$results_file"
fi

echo -e "${GREEN}[AwareSec] Results saved to $results_file${NC}"
