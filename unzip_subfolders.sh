#!/bin/bash

# Set the main directory
main_dir="C:/Users/admin-dianew68/Box/Diane/WORK/work_AJ/prism/data/tmax"

# Find all zip files in subfolders and unzip them in their respective directories
find "$main_dir" -type f -name "*.zip" | while read zip_file; do
    # Get the directory of the current zip file
    zip_dir=$(dirname "$zip_file")
    
    # Unzip the file in its respective directory
    unzip -d "$zip_dir" "$zip_file"
done

