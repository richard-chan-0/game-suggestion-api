#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define source and destination directories
SRC_DIR="src"
DEST_DIR="shared-logic-layer/python/src"

# Ensure the destination directory exists
mkdir -p "$DEST_DIR"

# Remove all __pycache__ folders
find "$SRC_DIR" -type d -name "__pycache__" -exec rm -rf {} +

# Copy the src folder to the destination directory
rsync -a --delete "$SRC_DIR/" "$DEST_DIR/"

# Print success message
echo "Successfully copied $SRC_DIR to $DEST_DIR"
