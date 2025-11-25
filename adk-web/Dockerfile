FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir google-adk

COPY adk-web/ ./adk-web/

ENV OLLAMA_API_BASE="http://ollama:11434"

EXPOSE 3000

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "3000"]
