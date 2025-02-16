#!/bin/bash
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SCRIPT_DIR/venv"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
CHAT_PDF_SCRIPT="$SCRIPT_DIR/chat-pdf.sh"
BIN_LINK="$HOME/.local/bin/chat-pdf"

mkdir -p "$HOME/.local/bin"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
  
  echo "Activating virtual environment and installing dependencies..."
  source "$VENV_DIR/bin/activate"

  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies..."
    pip install -r "$REQUIREMENTS_FILE"
  else
    echo "Error: requirements.txt file not found!"
    exit 1
  fi
else
  echo "Virtual environment already exists."
fi

chmod +x "$CHAT_PDF_SCRIPT"

if [ -L "$BIN_LINK" ] || [ -f "$BIN_LINK" ]; then
  echo "Removing existing link at $BIN_LINK"
  rm -f "$BIN_LINK"
fi

ln -s "$CHAT_PDF_SCRIPT" "$BIN_LINK"
echo "Symbolic link created: $BIN_LINK"

if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo "Adding ~/.local/bin to PATH..."
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  echo "Run 'source ~/.bashrc' or restart your terminal for changes to take effect."
fi

echo "Installation complete. Run 'chat-pdf <pdf_file>' to use the script."
