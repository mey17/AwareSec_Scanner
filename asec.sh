#!/bin/bash

# Get the directory of this script (ensures it works wherever the project folder is located)
#SCRIPT_DIR="/opt/Asec_Project"
SCRIPT_DIR="~/Desktop/Asec_Project"

# Run the awaresec.py script with all arguments passed to run.sh
python3 "$SCRIPT_DIR/awaresec.py" "$@"

# Run the main script (if there is an additional script to be run with all arguments passed)
"$SCRIPT_DIR/run.sh" "$@"

