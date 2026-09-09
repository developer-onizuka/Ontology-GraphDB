FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastmcp requests
COPY ontology-generic-mcp.py /app/ontology-generic-mcp.py
EXPOSE 5001
CMD ["python", "ontology-generic-mcp.py"]
