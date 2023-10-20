#!/usr/bin/env bash
python3 -m minitel.main --assets_path minitel/assets --db_path sqlite:////tmp/minitel.db $*
