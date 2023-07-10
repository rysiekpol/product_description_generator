FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt requirements.txt
COPY apps apps
COPY config config
COPY manage.py manage.py

RUN python -m venv venv && \
    venv/bin/python -m pip install pip --upgrade && \
    venv/bin/python -m pip install -r requirements.txt && \
    chmod +x config/entrypoint.sh

CMD ["./config/entrypoint.sh"]


