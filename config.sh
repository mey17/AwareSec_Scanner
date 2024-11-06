#!/bin/bash


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to check python Packages
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

# Installing Dependencies
if [ ! -f ~/.asec_installed ]; then
    echo "[AwareSec] Checking and installing necessary dependencies..."

    install_if_missing socket
    install_if_missing sys
    install_if_missing scapy.all
    sudo apt-get install -y ipcalc


    touch ~/.asec_installed
    echo "[AwareSec] All dependencies installed."
else
    echo "[AwareSec] Dependencies already installed."
fi

# Move the entire project to /opt/Asec_Project
sudo cp -r "$SCRIPT_DIR" /opt

# Make scripts executable
sudo chmod +x /opt/Asec_Project/*.sh
sudo chmod +x /opt/Asec_Project/*.py

# Create symbolic link to asec in /usr/local/bin
sudo ln -sf /opt/Asec_Project/asec.sh /usr/local/bin/asec

# Running the main code
echo "[AwareSec] Installation complete. You can now run the tool using:"
echo "[AwareSec] Usage: asec [options] <target>"
echo "[AwareSec] Or use asec --help to show more information"
