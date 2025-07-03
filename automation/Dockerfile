FROM python:3.11-slim

WORKDIR /app

COPY automation/ /app/

RUN apt-get update && \
    apt-get install -y git curl && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["python"]
