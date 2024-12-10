#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to check and install Python packages
install_if_missing() {
    PACKAGE=$1
    python3 -c "import $PACKAGE" &> /dev/null
    if [ $? -ne 0 ]; then
        echo "[AwareSec] $PACKAGE not found. Installing it now..."
        if ! pip install $PACKAGE; then
            echo "[AwareSec] Failed to install $PACKAGE. Please install it manually."
            exit 1
        fi
    else
        echo "[AwareSec] $PACKAGE is already installed."
    fi
}

# Install required Python packages
install_if_missing socket
install_if_missing time
install_if_missing json
install_if_missing csv
install_if_missing datetime
install_if_missing os

# Ensure pip is installed
if ! command -v pip &> /dev/null; then
    echo "[AwareSec] pip not found. Installing it now..."
    if ! python3 -m ensurepip --upgrade; then
        echo "[AwareSec] Failed to install pip. Please install it manually."
        exit 1
    fi
fi

# Install additional Python packages
pip install -r "$SCRIPT_DIR/requirements.txt"

# Make sure all scripts are executable
chmod +x "$SCRIPT_DIR/asec.sh"
chmod +x "$SCRIPT_DIR/run.sh"
chmod +x "$SCRIPT_DIR/config.sh"

# Create a symbolic link to asec.sh in /usr/local/bin
if [ ! -L /usr/local/bin/asec ]; then
    sudo ln -s "$SCRIPT_DIR/asec.sh" /usr/local/bin/asec
    echo "[AwareSec] Created symbolic link /usr/local/bin/asec"
else
    echo "[AwareSec] Symbolic link /usr/local/bin/asec already exists"
fi

echo "[AwareSec] Installation complete. You can now run the Asec project by calling 'asec' from the terminal."
echo "[AwareSec] Usage: asec [options] <target>"
echo "[AwareSec] Or use asec --help to show more information"
