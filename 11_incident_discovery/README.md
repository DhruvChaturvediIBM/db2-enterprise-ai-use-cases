# UC11 — AI-Powered Incident Discovery with IBM Db2 + LangChain

## What this example demonstrates

This is an enterprise-style Python example built around the **IBM Db2 LangChain integration**.

A new production incident is submitted as natural language. The application uses the official `langchain-db2` package and its `DB2VS` vector store to retrieve semantically similar historical incidents from IBM Db2.

The workflow is:

```text
New incident
     |
     v
LangChain embedding model
     |
     v
langchain_db2.DB2VS
     |
     v
IBM Db2 vector search
     |
     v
Top-K historical incidents
     |
     +--> severity
     +--> service
     +--> product
     +--> root cause
     +--> resolution
```

The example uses the real `DB2VS` API. LangChain's current reference documents `DB2VS` as the IBM Db2 vector store, with `from_documents`, `add_texts`, `similarity_search`, `similarity_search_with_score`, MMR, and metadata filtering. Db2 vector support requires Db2 12.1.2 or later. citeturn1search1turn2view0

## Why this is an enterprise use case

When a production incident occurs, engineers often need to determine whether a similar incident happened before.

Example:

```text
Payment service returning 503 errors.
Db2 connection wait time is high.
```

The application searches historical incidents by meaning rather than exact keywords and returns relevant root causes and resolutions.

This is an **incident discovery/triage aid**, not an autonomous remediation system.

## IBM Db2 package used

Install the official LangChain integration:

```bash
pip install -U langchain-db2
```

The package exposes:

```python
from langchain_db2 import DB2VS
```

The current LangChain reference documents `DB2VS` version 1.0.0 and its constructor, including `embedding_function`, `table_name`, `client`, `distance_strategy`, and `connection_args`. citeturn1search1

## Features demonstrated

### 1. Document ingestion

Historical incidents are converted to LangChain `Document` objects and inserted with:

```python
DB2VS.from_documents(...)
```

### 2. Semantic similarity search

The application uses:

```python
vector_store.similarity_search_with_score(...)
```

### 3. Metadata filtering

Db2VS supports metadata filtering. This example exposes:

```text
--service Payment
--severity SEV-1
```

and translates those into the DB2VS filter format.

The LangChain Db2 documentation demonstrates filters such as:

```python
{"id": ["101"]}
```

with `similarity_search` and `similarity_search_with_score`. citeturn2view0

### 4. Retrieval evaluation

The example evaluates predefined incident queries with Top-1 accuracy and Top-3 recall.

## Project structure

```text
11_incident_discovery/
├── README.md
├── requirements.txt
├── config.py
├── db.py
├── embeddings.py
├── sample_data.py
├── ingest.py
├── discovery.py
├── main.py
├── eval.py
├── validation.sql
└── VALIDATION_README.md
```

## Prerequisites

- Python 3.10+
- IBM Db2 12.1.2 or later with vector support
- Network access to Db2
- Db2 database/user credentials
- Python environment capable of installing `ibm-db`
- Local embedding model dependencies

Db2 12.1.2+ and `langchain-db2` are documented prerequisites for this integration. citeturn2view0

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The requirements use:

```text
langchain-db2
langchain-huggingface
langchain-community
langchain-core
ibm-db
```

The Db2 integration itself brings dependencies such as `langchain-core` and `ibm_db`; they are listed explicitly here to make the example environment easy to understand. citeturn2view0

## Configuration

Copy the example values into your shell:

```bash
export DB2_DATABASE="BLUDB"
export DB2_HOST="localhost"
export DB2_PORT="50000"
export DB2_USER="db2inst1"
export DB2_PASSWORD="password"
export DB2_SCHEMA="AI_DEMO"
export DB2_TABLE="INCIDENTS"
```

The application creates/uses the fully qualified table:

```text
AI_DEMO.INCIDENTS
```

Do not commit real credentials.

## 1. Ingest the historical incidents

```bash
python ingest.py
```

The ingestion code uses:

```python
DB2VS.from_documents(
    documents,
    embeddings,
    client=connection,
    table_name="AI_DEMO.INCIDENTS",
    distance_strategy=DistanceStrategy.COSINE,
)
```

This follows the official integration pattern: create LangChain documents, create an embedding model, and initialize `DB2VS.from_documents(...)`. citeturn2view0

## 2. Search for similar incidents

```bash
python main.py   --incident "Payment service returning 503 errors with high Db2 connection wait time"   --k 3
```

Built-in scenarios:

```bash
python main.py --scenario database
python main.py --scenario authentication
python main.py --scenario memory
```

## 3. Use metadata filters

Example:

```bash
python main.py   --incident "Payment API is failing because database connections are saturated"   --service Payment   --severity SEV-1   --k 3
```

The search layer constructs a DB2VS filter rather than implementing a separate database query layer.

## 4. Evaluate retrieval

```bash
python eval.py
```

The evaluation uses known relevant incident IDs and reports:

```text
Top-1 Accuracy
Top-3 Recall
```

These metrics are only for the supplied demonstration corpus; they are not production-quality retrieval benchmarks.

## 5. Validate the Db2 state

Run:

```text
validation.sql
```

Then read:

```text
VALIDATION_README.md
```

The validation script intentionally checks the actual DB2VS table through Db2 catalog metadata rather than assuming a custom application schema.

## Embeddings

The example uses `HuggingFaceEmbeddings` from `langchain_huggingface` with:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This keeps the example self-contained and avoids requiring a hosted embedding API.

## Distance strategy

The example uses:

```python
DistanceStrategy.COSINE
```

The Db2 LangChain integration documents support for dot product, cosine, and Euclidean distance strategies. citeturn2view0

## Important design choice

There is **no custom vector-store implementation** in this example.

The only vector-store object is:

```python
from langchain_db2 import DB2VS
```

Application code calls the integration directly.

This is important because the purpose of this use case is to show an AI developer how to consume the IBM Db2 package after installation.

## Future extensions

The same incident corpus could later be used with:

- RAG over retrieved incidents
- LangGraph incident workflows
- Haystack + IBM Db2
- CrewAI + IBM Db2
- MMR retrieval for diverse historical incidents
- similarity-score threshold retrieval
- larger production incident datasets
