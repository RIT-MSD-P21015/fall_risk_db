name = fall_risk_db

.PHONY: test dbuild drun dclean dkill

test:
	rm -f db.sqlite3
	export FLASK_APP=$(name); flask run

dbuild:
	docker build -t $(name).latest .

drun: dbuild
	docker run -d -p 5000:5000 $(name).latest

dkill:
	docker ps -q | xargs docker kill

dclean:
	docker system prune -a
