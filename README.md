# Ontology-GraphDB

Kubernetes, GraphDB, そして Model Context Protocol (MCP) を活用し、LLM（Claude Desktop）と密連携した**永続的・ドメイン分離型オントロジー管理・検索・推論パイプライン**です。

---

# 1. Goal

* **マルチドメインオントロジーの構造化と永続化:** 
  Rabbit（うさぎと亀の寓話）や Keio（慶應義塾の歴史）、Predation（捕食関係）など、多様な非構造化テキストから抽出したオントロジーを独立した Named Graph (`http://example.org/{domain}`) としてGraphDBに厳格に分離・蓄積します。
* **LLM (Claude Desktop) とのシームレスな統合:** 
  2つの専用MCP（Model Context Protocol）サーバーPodを介して、Claudeが直接GraphDBのリソース状態を確認し、SPARQLクエリの実行やオントロジーの動的登録を行えるインタラクティブな環境を提供します。
* **Kubernetesによるスケーラブルなインフラ基盤:** 
  コンテナ化されたGraphDBおよびMCPサーバーをKubernetesクラスター上で堅牢に稼働させ、ネットワーク・ストレージの可用性とモジュール性を担保します。


# 2. Overview

本システムは、オントロジーの　**登録・永続化**　を担う `graphDB-mcp` Pod と、**検索・照会**　を担う `ontology-generic-mcp` Pod の2つの独立したMCPサーバーによって構成されています。GraphDBの `context` パラメータを活用することで、デフォルトグラフを汚さずドメインごとにクリーンな名前付きグラフ管理を実現しています。

#### 2-1. オントロジー登録フロー (Ontology Registration Flow: `graphDB-mcp`)

```
[ User ]
   │ 1. Natural Language Prompt / Document Input such as Turtle Format (Rabbit) or (Keio) etc
   ▼
┌────────────────────────────────────────────────────────┐
│ Claude Desktop (LLM Interface)                         │
│  - Semantic analysis & text comprehension              │
│  - Entity & relation extraction (Turtle format)        │
└──┬─────────────────────────────────────────────────────┘
   │ 2. Invoke register_ontology_from_text (JSON-RPC / SSE)
   ▼
┌────────────────────────────────────────────────────────┐
│ Kubernetes Pod: graphDB-mcp                            │ graphDB-mcp.yaml & graphDB-mcp.py
│  - Tool execution (register_ontology_from_text)        │
│  - Context parameter mapping (?context=<URI>)          │
└──┬─────────────────────────────────────────────────────┘
   │ 3. HTTP POST Statements (Data persistence)
   ▼
┌────────────────────────────────────────────────────────┐
│ GraphDB (Kubernetes)                                   │ graphDB.yaml
│  - Repository: ontology-repo                           │
│  - Store triples in the designated Named Graph         │
│    (e.g., http://example.org/{domain})                 │
└────────────────────────────────────────────────────────┘
```
#### Turtle Format (Rabbit)
```
うさぎは亀を追い抜かしました。
```
```
@prefix ex: <http://example.org/ontology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Animal a rdfs:Class ;
    rdfs:label "動物"@ja .

ex:Rabbit a rdfs:Class ;
    rdfs:subClassOf ex:Animal ;
    rdfs:label "うさぎ"@ja .

ex:Turtle a rdfs:Class ;
    rdfs:subClassOf ex:Animal ;
    rdfs:label "亀"@ja .

ex:overtakes a rdf:Property ;
    rdfs:domain ex:Animal ;
    rdfs:range ex:Animal ;
    rdfs:label "追い抜く"@ja .

ex:usagi_1 a ex:Rabbit ;
    rdfs:label "うさぎ"@ja .

ex:kame_1 a ex:Turtle ;
    rdfs:label "亀"@ja .

ex:usagi_1 ex:overtakes ex:kame_1 .
```

#### Turtle Format (Keio)
```
福沢諭吉は慶應義塾を創設した。
```
```
@prefix ex: <http://example.org/ontology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Person a rdfs:Class ;
    rdfs:label "人物"@ja .

ex:Institution a rdfs:Class ;
    rdfs:label "組織"@ja .

ex:founded a rdf:Property ;
    rdfs:domain ex:Person ;
    rdfs:range ex:Institution ;
    rdfs:label "創設した"@ja .

ex:fukuzawa_yukichi a ex:Person ;
    rdfs:label "福沢諭吉"@ja .

ex:keio_gijuku a ex:Institution ;
    rdfs:label "慶應義塾"@ja .

ex:fukuzawa_yukichi ex:founded ex:keio_gijuku .
```

#### 2-2. オントロジー検索・参照フロー (Query & Inspection Flow: `ontology-generic-mcp`)
```
[ User ]
   │ 1. Inquiry / Query Request
   ▼
┌────────────────────────────────────────────────────────┐
│ Claude Desktop (LLM Interface)                         │
│  - Determine necessary query or inspection scope       │
└──┬─────────────────────────────────────────────────────┘
   │ 2. Invoke execute_sparql_select / list_named_graphs / describe_resource
   ▼
┌────────────────────────────────────────────────────────┐
│ Kubernetes Pod: ontology-generic-mcp                   │ ontology-generic-mcp.yaml & ontology-generic-mcp.py
│  - Execute SPARQL SELECT / DESCRIBE queries            │
│  - Retrieve JSON / Turtle results                      │
└──┬─────────────────────────────────────────────────────┘
   │ 3. HTTP GET (SPARQL / DESCRIBE request)
   ▼
┌────────────────────────────────────────────────────────┐
│ GraphDB (Kubernetes)                                   │ graphDB.yaml
│  - Repository: ontology-repo                           │
│  - Cross-domain or isolated Named Graph querying       │
└────────────────────────────────────────────────────────┘
```

<img src="https://github.com/developer-onizuka/Ontology-GraphDB/blob/main/biology.png" width="720"><br>

<img src="https://github.com/developer-onizuka/Ontology-GraphDB/blob/main/ClaudeDesktop-rabbit.png" width="720"><br>

<img src="https://github.com/developer-onizuka/Ontology-GraphDB/blob/main/keio.png" width="720"><br>

<img src="https://github.com/developer-onizuka/Ontology-GraphDB/blob/main/ClaudeDesktop-Keio.png" width="720"><br>

