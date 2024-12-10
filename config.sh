#!/bin/bash


INSTALL_DIR="/opt/asec_project"


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


if ! command -v pip &> /dev/null; then
    echo "[AwareSec] pip not found. Installing it now..."
    if ! python3 -m ensurepip --upgrade; then
        echo "[AwareSec] Failed to install pip. Please install it manually."
        exit 1
    fi
fi


pip install -r "requirements.txt"


if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR"
    sudo cp -r . "$INSTALL_DIR"
    echo "[AwareSec] Project cloned to $INSTALL_DIR"
else
    echo "[AwareSec] Project already exists in $INSTALL_DIR"
fi


sudo chmod +x "$INSTALL_DIR/asec.sh"
sudo chmod +x "$INSTALL_DIR/run.sh"
sudo chmod +x "$INSTALL_DIR/config.sh"


if [ ! -L /usr/local/bin/asec ]; then
    sudo ln -s "$INSTALL_DIR/asec.sh" /usr/local/bin/asec
    echo "[AwareSec] Created symbolic link /usr/local/bin/asec"
else
    echo "[AwareSec] Symbolic link /usr/local/bin/asec already exists"
fi

echo "[AwareSec] Installation complete. You can now run the Asec project by calling 'asec' from the terminal."
echo "[AwareSec] Usage: asec [options] <target>"
echo "[AwareSec] Or use asec --help to show more information"