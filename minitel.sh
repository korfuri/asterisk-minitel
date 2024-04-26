#!/usr/bin/env bash
mkdir -p /tmp/uploads
echo '*****'
echo 'http://127.0.0.1:8080/e/index.html'
echo '*****'
echo ''
python3 -m minitel.main --assets_path minitel/assets --db_path sqlite:////tmp/minitel.db --upload_path /tmp/uploads --web_port 8080 --ws_port 3611 $*

