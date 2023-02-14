#!/bin/bash
python3.10 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python manage.py migrate
./venv/bin/python manage.py loaddata dump.json
ln -sf ./OrderBot.service /etc/systemd/system/OrderBot.service
chown -R www-data:www-data ../OrderBot
systemctl daemon-reload
systemctl enable OrderBot
systemctl start OrderBot
systemctl status OrderBot

