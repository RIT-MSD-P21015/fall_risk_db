FROM python:bullseye

RUN useradd fall_risk_db

WORKDIR /home/fall_risk_db

COPY requirements.txt requirements.txt
COPY migrations migrations
RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY fall_risk_db.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP fall_risk_db.py
ENV APP_CONFIG config.ProductionConfig

RUN chown -R fall_risk_db:fall_risk_db ./
USER fall_risk_db

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
