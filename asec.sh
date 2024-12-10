#!/bin/bash
SCRIPT_DIR="/opt/asec_project"
python3 "$SCRIPT_DIR/awaresec.py" "$@"


"$SCRIPT_DIR/run.sh" "$@"