import requests
from fastmcp import FastMCP

mcp = FastMCP(name="Ontology Reasoner MCP")

GRAPHDB_UPDATE_URL = "http://svc-graphdb:7200/repositories/ontology-repo/statements"

@mcp.tool()
def register_ontology_from_text(domain: str, turtle_data: str) -> str:
    """
    Claudeが非構造化データから抽出・構築したTurtle形式のオントロジーを受け取り、
    GraphDBの対応するドメイン（Named Graph）に登録（永続化）します。
    """
    target_graph = f"http://example.org/{domain}"

    # Named Graphを指定して、TurtleデータをそのままPOSTするURL
    url = f"http://svc-graphdb:7200/repositories/ontology-repo/statements?graph=<{target_graph}>"

    headers = {"Content-Type": "text/turtle; charset=utf-8"}
    response = requests.post(url, data=turtle_data.encode("utf-8"), headers=headers)

    if response.status_code in [200, 204]:
        return f"成功: ドメイン '{domain}' のオントロジーを GraphDB (Graph: {target_graph}) に登録しました。"
    else:
        return f"エラー: GraphDBへの登録に失敗しました (Status: {response.status_code}, Msg: {response.text})"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=5001)
