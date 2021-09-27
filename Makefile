name = fall_risk_db

.PHONY: env clean

env:
	export FLASK_APP=$(name).py

clean:
	docker system prune -a
