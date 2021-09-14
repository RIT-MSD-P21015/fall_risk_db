name = fall_risk_db

.PHONY: test docker

test:
	rm -f app/db.sqlite3
	export FLASK_APP=$(name); flask run

docker:
	docker build -t $(name).latest .
	docker run -d -p 5000:5000 $(name).latest
