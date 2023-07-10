FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt requirements.txt
COPY apps apps
COPY config config
COPY manage.py manage.py
COPY entrypoint.sh entrypoint.sh
COPY static static

RUN python -m venv venv && \
    venv/bin/pip install pip --upgrade && \
    venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]


