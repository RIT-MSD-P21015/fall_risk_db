#!/bin/bash
sleep 3
source venv/bin/activate
flask db upgrade
exec gunicorn --workers=4 --bind "0.0.0.0:5000" "fall_risk_db:app"
