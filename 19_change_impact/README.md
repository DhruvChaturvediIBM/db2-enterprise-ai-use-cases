# UC19: Semantic Change Impact Discovery

## Status

> Implementation package for review and demonstration.

## Why this use case exists

A proposed enterprise change can affect documents, decisions, policies, incidents, and operational procedures that are not explicitly linked.

This use case demonstrates **semantic change impact discovery**: given a proposed change, search the enterprise knowledge base across document types and surface artifacts that may be affected.

### College project framing

Build a "what else does this touch?" discovery tool using semantic search.

### Enterprise framing

Build a change impact assistant that helps architects and engineers discover a potential blast radius before a change is implemented by surfacing related:

- Architecture Decision Records
- Incidents
- Policies
- Technical documentation
- Runbooks
- Support knowledge
- Requirements
- Release notes

**Scope boundary:** this is discovery, not formal impact analysis. The application surfaces candidates. Engineers and architects confirm the actual impact.

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | IBM Db2 `DB2VS` vector store with `similarity_search()` |
| Retrieval pattern | Broad cross-type semantic retrieval |
| LLM | Ollama `granite3.1-dense:8b` |
| Embedding model | Ollama `nomic-embed-text` |
| Output | Grouped impact candidates plus an evidence-grounded summary |

## End-to-end flow

```text
Proposed change
    |
    v
Generate query embedding
    |
    v
IBM Db2 DB2VS similarity_search()
across ALL document types
    |
    v
Broad candidate set
(k=10 or k=15)
    |
    v
Preserve raw vector score
+ derive normalized similarity when using cosine distance
    |
    v
Group by document_type
    |
    v
Classify demonstration relevance bands
    |
    +--> Direct candidates
    |
    +--> Indirect candidates
    |
    +--> Lower-relevance candidates
    |
    v
Ollama Granite summary
    |
    v
Human review and confirmation
```

### Example

Proposed change:

> Replacing the authentication mechanism from API keys to OAuth 2.0 PKCE.

Semantic retrieval can surface artifacts such as:

- `ADR-003` - authentication architecture decision
- `INC-002` - historical authentication failure
- `POL-004` - access control policy
- `TECH-002` - API gateway configuration

The LLM summarizes the retrieved evidence and highlights possible risks. It does **not** decide the final impact.

## Scope

The application:

1. Accepts a change description.
2. Searches across all available document types.
3. Uses a broad retrieval window, configurable as `k=10` or `k=15`.
4. Preserves Db2 retrieval scores.
5. Converts cosine distance into normalized similarity when that is the configured vector metric.
6. Groups candidates by `document_type`.
7. Shows document IDs so each artifact can be manually reviewed.
8. Generates an evidence-grounded impact summary with Ollama Granite.
9. Supports repeatable evaluation cases.

The application does **not**:

- Automatically approve or reject a change.
- Claim that every retrieved document is actually impacted.
- Automatically modify enterprise systems.
- Replace formal architecture, security, compliance, or change-management review.
- Infer impact from score alone.

## Retrieval and score semantics

The implementation keeps the **raw vector-store score** visible because score semantics depend on the configured distance strategy.

For a cosine-distance setup:

```text
cosine_distance = lower is more similar
normalized_similarity = 1 - cosine_distance
```

The demonstration uses configurable relevance bands:

| Band | Demonstration rule | Meaning |
|---|---:|---|
| Direct candidate | `similarity > 0.75` | Strong semantic relationship worth immediate review |
| Indirect candidate | `0.55 <= similarity <= 0.75` | Potential relationship requiring contextual review |
| Lower relevance | `similarity < 0.55` | Retrieved in the broad net but less strongly related |

These are **demonstration heuristics**, not enterprise risk scores. Tune them using representative data and validation results.

## Structured output

Each candidate should expose enough evidence for manual review:

- Document ID
- Title
- Document type
- Raw Db2 score
- Normalized similarity, when applicable
- Relevance band
- Content preview
- Optional metadata such as department, product, effective date, and status

Results are grouped by document type so reviewers can distinguish architectural, operational, policy, incident, and other evidence.

## LLM summarization

The summarizer uses:

- Ollama
- `granite3.1-dense:8b`

The model receives the proposed change and the retrieved evidence. The prompt instructs it to:

- Stay grounded in retrieved artifacts.
- Cite document IDs when making observations.
- Distinguish direct evidence from possible indirect relationships.
- Highlight relevant historical incidents.
- Avoid inventing dependencies or relationships.
- State when evidence is insufficient.
- Keep the output as a discovery summary rather than a final impact decision.

## Built-in test scenarios

### 1. Authentication migration

```text
Replacing authentication from API keys to OAuth 2.0 PKCE
```

Expected candidate areas:

- `ADR-003`
- `INC-002`
- `POL-004`
- `TECH-002`

Potential evidence themes include authentication architecture, credentials, token handling, access control, certificates, and historical authentication failures.

### 2. Payment event migration

```text
Migrating payment event processing to Apache Kafka
```

Expected candidate areas:

- `ADR-002`
- `INC-001`
- `RUN-001`

### 3. Db2 connection-pool change

```text
Increasing Db2 connection pool size for all services
```

Expected candidate areas:

- `INC-001`
- `TECH-001`
- `SUP-002`

The exact retrieved order and scores depend on the indexed content and embedding model.

## Evaluation

The evaluation module measures discovery behavior rather than pretending to measure formal impact analysis.

Suggested metrics:

### Candidate recall

Whether expected artifacts appear anywhere in the retrieved candidate set.

```text
candidate_recall =
    expected_documents_found / expected_documents
```

### Top-k hit rate

Whether expected artifacts appear within the configured retrieval window.

### Document-type coverage

Whether the retrieval spans multiple relevant artifact types, such as ADR, incident, policy, and technical documentation.

### Summary grounding

Whether the generated summary references retrieved document IDs and avoids unsupported relationships.

Evaluation cases are intentionally small and transparent so the project can be extended with a larger enterprise test set.

## Data model

The examples assume the shared enterprise knowledge table:

```text
AI_DEMO.KNOWLEDGE_BASE
```

Relevant columns:

| Column | Purpose |
|---|---|
| `DOCUMENT_ID` | Stable enterprise document identifier |
| `TITLE` | Human-readable title |
| `CONTENT` | Searchable document content |
| `DOCUMENT_TYPE` | ADR, incident, policy, technical, runbook, etc. |
| `EFFECTIVE_DATE` | Optional document date |
| `DEPARTMENT` | Optional owning organization |
| `PRODUCT` | Optional product or service |
| `EMBEDDING` | Vector representation used by Db2 vector search |

## Configuration

Copy `.env.example` to `.env` and provide the Db2 and Ollama settings.

```text
DB2_HOST=...
DB2_PORT=...
DB2_DATABASE=...
DB2_USERNAME=...
DB2_PASSWORD=...
DB2_SCHEMA=AI_DEMO
KNOWLEDGE_TABLE=KNOWLEDGE_BASE
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=granite3.1-dense:8b
TOP_K=10
DIRECT_IMPACT_THRESHOLD=0.75
INDIRECT_IMPACT_THRESHOLD=0.55
```

## Prerequisites

- Python 3.10+
- IBM Db2 with the `AI_DEMO.KNOWLEDGE_BASE` table populated and vector-enabled
- Db2 Python connectivity
- LangChain
- IBM Db2 LangChain integration package providing `DB2VS`
- Ollama
- `nomic-embed-text`
- `granite3.1-dense:8b`

Example Ollama setup:

```bash
ollama pull nomic-embed-text
ollama pull granite3.1-dense:8b
```

Install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows activation:

```powershell
.venv\Scripts\activate
```

## How to run

```bash
source .venv/bin/activate
cd 19_change_impact
python main.py
```

Run a custom change:

```bash
python main.py --change "replacing authentication mechanism"
```

Run another example:

```bash
python main.py --change "payment service database connection pool"
```

## How to validate

Run the supplied SQL validation:

```bash
db2 -tvf validation/validation.sql
```

Then review:

```text
validation/VALIDATION.md
```

The SQL validates that the knowledge base contains the cross-type documents required for the demonstration scenarios.

## Validation expectations

For the authentication scenario, validation should expose relevant artifacts such as:

- `ADR-003`
- `INC-002`
- `POL-004`

For the payment scenario, validation should expose relevant artifacts such as:

- `INC-001`
- `RUN-001`
- `ADR-002`

The validation SQL is content-based and therefore depends on the actual data loaded into `AI_DEMO.KNOWLEDGE_BASE`.

## Project structure

```text
19_change_impact/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── db2_store.py
├── sample_data.py
├── impact.py
├── summarizer.py
├── main.py
├── evaluation/
│   ├── __init__.py
│   ├── cases.py
│   └── eval.py
└── validation/
    ├── validation.sql
    └── VALIDATION.md
```

## Enterprise impact

Enterprise changes often cross organizational and document boundaries. A dependency may be documented in an ADR, a historical incident, a runbook, or a policy rather than in the change request itself.

This example demonstrates IBM Db2 vector search as a **semantic discovery layer for change management**:

- broad retrieval across heterogeneous knowledge
- transparent evidence for human review
- historical incident discovery
- structured cross-type results
- LLM-assisted summarization without automatic decision-making

The key enterprise takeaway is that semantic retrieval can help expose hidden relationships, while the actual blast-radius decision remains with qualified engineers and architects.
