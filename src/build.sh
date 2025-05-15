#!/bin/bash

# Set the parent directory (current directory where this script is located)
PARENT_DIR=$(dirname "$0")

# Loop through each subdirectory in the parent directory
for DIR in "$PARENT_DIR"/*; do
    # Check if it's a directory and contains a build.sh file
    if [ -d "$DIR" ] && [ -f "$DIR/build.sh" ]; then
        echo "Building in $DIR..."
        
        # Run the build.sh script in the subdirectory
        (cd "$DIR" && ./build.sh)
        
        # Check if the build succeeded
        if [ $? -ne 0 ]; then
            echo "Build failed in $DIR. Exiting."
            return 1
        fi
    fi
done

echo "All builds completed successfully."
