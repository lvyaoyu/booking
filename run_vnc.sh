#!/bin/bash
ln -s /root/.cache/ms-playwright/chromium-907428/chrome-linux/chrome /data/booking/chrome
Xvfb :1 -screen 0 1920x1080x16 &
sleep 1
x11vnc -storepasswd 123456 ~/.vnc/passwd &
x11vnc -display :1.0 -forever -bg -o /var/log/x11vnc.log -rfbauth ~/.vnc/passwd -rfbport 5800 &
sleep 1
/root/noVNC/utils/launch.sh  --listen 6800 --vnc localhost:5800  &
python main.py