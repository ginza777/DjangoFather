#!/bin/bash



# Systemd xizmatlarini qayta boshlash

git pull


#start
sudo systemctl start djangofather.socket
sudo systemctl start djangofather.service
sudo systemctl start djangofather_beat
sudo systemctl start djangofather_worker

#enable
sudo systemctl enable djangofather.socket
sudo systemctl enable djangofather.service
sudo systemctl enable djangofather_beat
sudo systemctl enable djangofather_worker

#restart
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