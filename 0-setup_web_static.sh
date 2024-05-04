#!/usr/bin/env bash
#This bash script sets up your web servers for the deployment of web_static

apt-get install -y nginx
apt-get update
mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test
echo "Welcome to AirBnB" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/
serve="\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current;\n\t}"
sed -i "s/^\tserver_name .*;$/&\n$serve/" /etc/nginx/sites-available/default
service nginx restart
