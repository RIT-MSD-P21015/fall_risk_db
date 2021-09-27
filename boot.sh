#!/bin/bash
sleep 5
source venv/bin/activate
flask db upgrade
exec gunicorn --bind "0.0.0.0:5000" "fall_risk_db:app"
