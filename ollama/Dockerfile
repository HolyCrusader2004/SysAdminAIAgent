FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y curl && apt-get clean

EXPOSE 11434

RUN printf '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama server..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
echo "Waiting for Ollama API to become available..."\n\
until curl -s http://localhost:11434/api/version > /dev/null; do\n\
  echo "Ollama not ready, retrying..."\n\
  sleep 2\n\
done\n\
\n\
echo "Ollama is ready. Pulling model..."\n\
ollama pull gpt-oss:20b || {\n\
  echo "Failed to pull model"; exit 1;\n\
}\n\
\n\
echo "Model pulled successfully. Ollama running."\n\
wait $OLLAMA_PID\n' > /start.sh \
&& chmod +x /start.sh

ENTRYPOINT ["/bin/bash", "/start.sh"]
