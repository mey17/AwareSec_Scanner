#!/bin/bash

INSTALL_DIR="/opt/asec_project"

if ! command -v python3 &> /dev/null; then
    echo "[AwareSec] Python3 is not installed. Please install Python3 and try again."
    exit 1
fi


if command -v sudo &> /dev/null; then
    SUDO="sudo"
elif command -v doas &> /dev/null; then
    SUDO="doas"
elif command -v su &> /dev/null; then
    SUDO="su -c"
else
    echo "[AwareSec] Neither sudo, doas, nor su is installed. Please install one of these and try again."
    exit 1
fi

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

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "[AwareSec] Cannot detect the operating system. Please install necessary packages manually."
    exit 1
fi

case $OS in
    ubuntu|debian|kali)
        echo "[AwareSec] Detected Debian-based system. Installing necessary packages..."
        $SUDO apt update
        $SUDO apt install -y python3 python3-pip
        ;;
    arch|manjaro)
        echo "[AwareSec] Detected Arch-based system. Installing necessary packages..."
        $SUDO pacman -Sy
        $SUDO pacman -S --noconfirm python python-pip
        ;;
    fedora)
        echo "[AwareSec] Detected Fedora-based system. Installing necessary packages..."
        $SUDO dnf install -y python3 python3-pip
        ;;
    centos|rhel)
        echo "[AwareSec] Detected RHEL-based system. Installing necessary packages..."
        $SUDO yum install -y python3 python3-pip
        ;;
    opensuse|suse)
        echo "[AwareSec] Detected openSUSE-based system. Installing necessary packages..."
        $SUDO zypper install -y python3 python3-pip
        ;;
    termux)
        echo "[AwareSec] Detected Termux environment. Installing necessary packages..."
        pkg update
        pkg install -y python
        ;;
    alpine)
        echo "[AwareSec] Detected iSH (Alpine Linux) environment. Installing necessary packages..."
        apk update
        apk add python3 py3-pip
        ;;
    freebsd)
        echo "[AwareSec] Detected FreeBSD system. Installing necessary packages..."
        $SUDO pkg install -y python3 py38-pip
        ;;
    *)
        echo "[AwareSec] Unsupported operating system. Please install necessary packages manually."
        exit 1
        ;;
esac

pip install -r "requirements.txt"

if [ ! -d "$INSTALL_DIR" ]; then
    $SUDO mkdir -p "$INSTALL_DIR"
    $SUDO cp -r . "$INSTALL_DIR"
    echo "[AwareSec] Project cloned to $INSTALL_DIR"
else
    echo "[AwareSec] Project already exists in $INSTALL_DIR"
fi

$SUDO chmod +x "$INSTALL_DIR/asec.sh"
$SUDO chmod +x "$INSTALL_DIR/run.sh"
$SUDO chmod +x "$INSTALL_DIR/config.sh"

if [ ! -L /usr/local/bin/asec ]; then
    $SUDO ln -s "$INSTALL_DIR/asec.sh" /usr/local/bin/asec
    echo "[AwareSec] Created symbolic link /usr/local/bin/asec"
else
    echo "[AwareSec] Symbolic link /usr/local/bin/asec already exists"
fi

echo "[AwareSec] Installation complete. You can now run the Asec project by calling 'asec' from the terminal."
echo "[AwareSec] Usage: asec [options] <target>"
echo "[AwareSec] Or use asec --help to show more information"