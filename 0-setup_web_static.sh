#!/bin/bash

# Install Nginx if it's not already installed
if ! command -v nginx >/dev/null 2>&1; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories if they don't exist
directories=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")
for directory in "${directories[@]}"; do
    if [ ! -d "$directory" ]; then
        mkdir -p "$directory"
    fi
done

# Create a fake HTML file for testing
echo "Fake HTML content" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sed -i '/^\s*location \/ {$/a \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' "$config_file"

# Restart Nginx
service nginx restart