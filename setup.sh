#!/bin/bash

SOURCE="pengu.py"
DATA="pengu-training/"
DESTINATION="$HOME/.local/bin"
TARGET="pengu"

echo "
    ┌──────────────────────────────┐
    │          pengu setup         │
    ├──────────────────────────────┤
    │ [1] Install pengu            │
    │ [2] Uninstall pengu          │
    │ [3] Exit                     │
    └──────────────────────────────┘
"

read -p "Select an option (default=1): " option
option=${option:-1}

echo ""

case "$option" in
  1)
    if [[ -f "$DESTINATION/$TARGET" ]]; then
      echo "[-] pengu is already installed in $DESTINATION"
      echo "Reinstalling pengu ..."
      echo ""
      rm "$DESTINATION/$TARGET"
      rm -r "$DESTINATION/$DATA"
    fi

    mkdir -p "$DESTINATION"  # Create the destination directory (~/.local/bin) if it does not yet exist
    cp "$SOURCE" "$DESTINATION/$TARGET"  # Copy the script to the destination directory
    cp -R "$DATA" "$DESTINATION/$DATA"  # Copy the data folder to the destination directory
    chmod +x "$DESTINATION/$TARGET"  # Make the script executable as a program
    echo "[+] pengu has been installed in $DESTINATION"

    if [[ ":$PATH:" != *":$DESTINATION:"* ]]; then
      echo "[!] $DESTINATION is not in your PATH"
      echo "You may want to add this line to your shell config (~/.bashrc or ~/.zshrc):"
      echo "  export PATH=\"$DESTINATION:\$PATH\""
    fi

    ;;
  2)
    if [[ -f "$DESTINATION/$TARGET" ]]; then
      rm "$DESTINATION/$TARGET"
      rm -r "$DESTINATION/$DATA"
      echo "[+] pengu has been uninstalled from $DESTINATION"
    else
      echo "[-] pengu is not currently installed in $DESTINATION"
    fi
    ;;
  3)
    exit 0
    ;;
  *)
    echo "[-] Invalid option: $option"
    echo ""
    exit 1
    ;;
esac

echo ""

