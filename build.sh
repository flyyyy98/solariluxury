#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
cd mi_proyecto
python manage.py collectstatic --no-input
