#!/bin/bash
source venv/bin/activate
sleep 5
exec gunicorn --bind "0.0.0.0:5000" "fall_risk_db:app"
