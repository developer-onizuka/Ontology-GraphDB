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
│ MCP Server Pod (Kubernetes)                            │ graphDM-mcp.yaml & graphDB-mcp.py
│  - Tool execution (e.g., register_ontology)            │
│  - Payload validation & SPARQL query construction      │
└──┬─────────────────────────────────────────────────────┘
   │ 3. SPARQL Update (INSERT DATA)
   ▼
┌────────────────────────────────────────────────────────┐
│ GraphDB (Kubernetes)                                   │ graphDB.yaml
│  - Persist triples in the specified Named Graph        │
│    (e.g., http://example.org/domain.owl)               │
└────────────────────────────────────────────────────────┘
```
```
うさぎは亀を追い抜かしました。
```
- turtle形式
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
