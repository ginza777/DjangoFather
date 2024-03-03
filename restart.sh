#!/bin/bash



# Systemd xizmatlarini qayta boshlash

git pull

sudo systemctl restart djangofather.socket
sudo systemctl restart djangofather.service
sudo systemctl restart djangofather_beat
sudo systemctl restart djangofather_worker


#status
sudo systemctl status djangofather.socket
sudo systemctl status djangofather.service
sudo systemctl status djangofather_beat
sudo systemctl status djangofather_worker


sudo systemctl daemon-reload
sudo nginx -t && sudo systemctl restart nginx