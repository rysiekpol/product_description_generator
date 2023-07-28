FROM python:3.11-slim AS builder

WORKDIR /code


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

RUN pip install pip --upgrade && \
    pip install -r requirements.txt && \
    chmod +x entrypoint.sh

COPY apps apps
COPY config config
COPY manage.py manage.py

CMD ["./entrypoint.sh"]


