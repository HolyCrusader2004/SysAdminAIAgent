FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir google-adk httpx

COPY adk-web/ ./adk-web/

ENV OLLAMA_API_BASE="http://ollama:11434"
ENV KEYCLOAK_URL="http://keycloak:8080"
ENV KEYCLOAK_REALM="master"
ENV MCP_CLIENT_ID="mcp_server"
ENV MCP_CLIENT_SECRET="i94YxgUaNqoqLsNo3pUjZoKDwd5b41Bx"
ENV MCP_SERVER_URL="http://mcp-server:8001/mcp"

EXPOSE 3000

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "3000"]