# Ontology-GraphDB
```
[ User ]
   │ 1. Drag & Drop PDF / Word + Prompt
   ▼
┌────────────────────────────────────────────────────────┐
│ Claude Desktop (LLM Interface)                         │
│  - Document text extraction & semantic analysis        │
│  - Entity & relation extraction (S-P-O structuring)    │
└──┬─────────────────────────────────────────────────────┘
   │ 2. Pass structured data (Turtle format / JSON) as JSON arguments to the MCP tool
   ▼ (JSON-RPC / SSE)
┌────────────────────────────────────────────────────────┐
│ MCP Server Pod (Kubernetes)                            │ graphDB-mcp.py
│  - Tool execution (e.g., register_ontology)            │
│  - Payload validation & SPARQL query construction      │
└──┬─────────────────────────────────────────────────────┘
   │ 3. SPARQL Update (INSERT DATA)
   ▼
┌────────────────────────────────────────────────────────┐
│ GraphDB (Kubernetes)                                   │ graphDB-mcp.yaml
│  - Persist triples in the specified Named Graph        │
│    (e.g., http://example.org/domain.owl)               │
└────────────────────────────────────────────────────────┘
```
- graphDB-mcp.yaml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graphdb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: graphdb
  template:
    metadata:
      labels:
        app: graphdb
    spec:
      containers:
      - name: graphdb
        image: ontotext/graphdb:free
        ports:
        - containerPort: 7200
          name: http
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"
          requests:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: svc-graphdb
spec:
  type: LoadBalancer
  ports:
  - port: 7200
    targetPort: 7200
    name: http
  selector:
    app: graphdb
```

- graphDB-mcp.py
```
import requests
from fastmcp import FastMCP

mcp = FastMCP(name="Ontology Reasoner MCP")

GRAPHDB_UPDATE_URL = "http://svc-graphdb:7200/repositories/ontology-repo/statements"

@mcp.tool()
def register_ontology_from_text(domain: str, turtle_data: str) -> str:
    """
    Claudeが非構造化データから抽出・構築したTurtle形式のオントロジーを受け取り、
    GraphDBの対応するドメイン（Named Graph）に登録（永続化）します。
    
    Args:
        domain: ドメイン名（例: "technology", "biology"）
        turtle_data: Turtle形式で記述されたRDFトリプルの文字列
    """
    target_graph = f"http://example.org/{domain}"
    
    # SPARQL Update (INSERT DATA) クエリの構築
    sparql_update = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        
        INSERT DATA {{
          GRAPH <{target_graph}> {{
            {turtle_data}
          }}
        }}
    """
    
    headers = {"Content-Type": "application/sparql-update; charset=utf-8"}
    response = requests.post(GRAPHDB_UPDATE_URL, data=sparql_update.encode("utf-8"), headers=headers)
    
    if response.status_code in [200, 204]:
        return f"成功: ドメイン '{domain}' のオントロジーを GraphDB (Graph: {target_graph}) に登録しました。"
    else:
        return f"エラー: GraphDBへの登録に失敗しました (Status: {response.status_code}, Msg: {response.text})"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=5001)
```
