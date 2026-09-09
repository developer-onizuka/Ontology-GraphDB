import os
import requests
from fastmcp import FastMCP

# FastMCPサーバーの初期化
mcp = FastMCP("GraphDB Generic Client")

# 環境変数またはデフォルトのエンドポイント
GRAPHDB_BASE_URL = os.getenv("GRAPHDB_BASE_URL", "http://svc-graphdb:7200")
REPOSITORY_ID = os.getenv("GRAPHDB_REPO", "ontology-repo")

@mcp.tool()
def execute_sparql_select(sparql_query: str) -> str:
    """
    GraphDBに対して任意のSPARQL SELECTクエリを実行し、結果をJSON形式で返します。
    ドメインに依存せず、あらゆるオントロジーの検索・推論結果の確認に使えます。
    """
    url = f"{GRAPHDB_BASE_URL}/repositories/{REPOSITORY_ID}"
    headers = {"Accept": "application/sparql-results+json"}
    
    try:
        response = requests.get(url, params={"query": sparql_query}, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"SPARQLエラー (Status: {response.status_code}): {response.text}"
    except Exception as e:
        return f"接続エラー: {str(e)}"

@mcp.tool()
def list_named_graphs() -> str:
    """
    GraphDBリポジトリ内に存在するすべてのNamed Graphの一覧をSPARQLで取得します。
    """
    query = """
    SELECT DISTINCT ?g WHERE {
      GRAPH ?g { ?s ?p ?o }
    }
    """
    return execute_sparql_select(query)

@mcp.tool()
def describe_resource(resource_uri: str) -> str:
    """
    指定したURIリソースに関する詳細なトリプル情報（DESCRIBE）を取得します。
    """
    query = f"DESCRIBE <{resource_uri}>"
    url = f"{GRAPHDB_BASE_URL}/repositories/{REPOSITORY_ID}"
    headers = {"Accept": "text/turtle"}
    
    try:
        response = requests.get(url, params={"query": query}, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"エラー (Status: {response.status_code}): {response.text}"
    except Exception as e:
        return f"接続エラー: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=5001)
