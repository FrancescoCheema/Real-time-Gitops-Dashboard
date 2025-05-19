FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY requirements.txt /app/
COPY /webhook-monitor/app.py  /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

RUN rm -rf ngrok.yml \
    touch ngrok.yml

COPY . /app/

ENV PORT=8080
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

EXPOSE 8080

WORKDIR /app

RUN adduser -S flaskuser
USER flaskuser

CMD ["python", "app.py"]
