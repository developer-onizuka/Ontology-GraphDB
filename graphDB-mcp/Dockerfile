FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir requests fastmcp
COPY graphDB-mcp.py /app/graphDB-mcp.py
EXPOSE 5001
CMD ["python", "graphDB-mcp.py"]
