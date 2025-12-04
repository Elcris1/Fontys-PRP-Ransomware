#!/bin/bash

# Root directory where you want to create files
ROOT_DIR="$HOME/"

# List of subfolders to create files in
FOLDERS=("Desktop" "Documents" "Downloads" "Pictures" "Music" "Videos")

# Create root directory if it doesn't exist
mkdir -p "$ROOT_DIR"

# Loop through each folder and create files
for folder in "${FOLDERS[@]}"; do
    # Create the folder
    mkdir -p "$ROOT_DIR/$folder"

    # Create some test files inside
    for i in {1..3}; do
        FILE="$ROOT_DIR/$folder/file_$i.txt"
        echo "This is test file $i in $folder" > "$FILE"
        echo "Created $FILE"
    done
done

echo "✅ All test files created successfully!"
