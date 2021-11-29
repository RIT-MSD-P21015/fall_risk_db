name = fall_risk_db

.PHONY: dev test clean

dev:
	export FLASK_APP=$(name).py && \
	export FLASK_ENV=development && \
	export APP_CONFIG=config.DevelopmentConfig && \
	flask db upgrade && \
	flask run --host=0.0.0.0

test:
	export FLASK_APP=$(name).py && \
	export FLASK_ENV=production && \
	export APP_CONFIG=config.TestingConfig && \
	flask db upgrade && \
	flask run --host=0.0.0.0

clean:
	rm -f db.sqlite3