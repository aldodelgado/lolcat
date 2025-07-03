FROM python:3.11-slim

WORKDIR /app

COPY automation/ .

RUN apt-get update && \
    apt-get install -y git curl && \
    pip install --upgrade pip && \
    pip install openai requests llm-prompt-semantic-diff pytest flake8

ENTRYPOINT ["python"]
