# UC13 - Single-Agent Enterprise Research Assistant

## Status

> Implementation package for review and demonstration.

## Why this use case exists

Not every enterprise AI application needs an agent.

A deterministic RAG pipeline is usually preferable when every question follows the same retrieval path. An agent becomes useful when the system needs to decide whether enterprise knowledge should be searched, what to search for, and whether additional retrieval is needed before answering.

This use case demonstrates that transition with the smallest useful agentic pattern:

- one CrewAI agent
- one IBM Db2 search tool
- one research task
- one LLM
- no multi-agent delegation

The goal is to isolate what the agent adds over a conventional RAG pipeline.

## What it demonstrates

| Capability | Detail |
|---|---|
| Agent framework | CrewAI |
| Db2 retrieval | Official `DB2VectorSearchTool` |
| Database | IBM Db2 native vector search |
| LLM | Ollama `granite3.1-dense:8b` |
| Agent | Single `EnterpriseResearcher` agent |
| Tools | One Db2 enterprise search tool |
| Retrieval | Semantic vector search |
| Ingestion | Haystack, optional write path |
| Key pattern | Agent decides when to use enterprise knowledge |

**Implementation rule:** do not implement a replacement `DB2VectorSearchTool`. Use the actual CrewAI/IBM Db2 search tool directly.

The current IBM example shows `DB2VectorSearchTool` performing semantic similarity search against IBM Db2 and remaining retrieval-only, while the ingestion framework is independent. citeturn0search0

## Architecture

### Ingestion path

```text
Enterprise documents
        |
        v
Haystack ingestion pipeline
        |
        +--> load / clean
        +--> split
        +--> embed
        +--> metadata
        |
        v
IBM Db2 vector table
```

### Runtime path

```text
User question
      |
      v
CrewAI EnterpriseResearcher
      |
      | decides whether enterprise search is needed
      v
DB2VectorSearchTool
      |
      v
IBM Db2 vector search
      |
      v
Retrieved enterprise evidence
      |
      v
CrewAI agent
      |
      v
Grounded answer
```

Haystack is optional and isolated to the write path. The runtime agent does not import Haystack.

## Why use an agent here?

A deterministic RAG application might always execute:

```text
Question -> Search Db2 -> Prompt LLM -> Answer
```

UC13 demonstrates:

```text
Question
  -> Agent decides whether search is needed
  -> Agent invokes Db2 search
  -> Agent evaluates evidence
  -> Agent may perform another focused search
  -> Agent synthesizes the answer
```

This is the reason to use CrewAI in this example.

If a question can be answered reliably by one deterministic retrieval call, UC01 or UC07 is a better fit.

## Scope

Included:

- One CrewAI `EnterpriseResearcher` agent
- One official `DB2VectorSearchTool`
- One research task
- Ollama Granite reasoning
- Semantic search against IBM Db2
- Evidence-grounded answers
- Optional repeated tool calls
- Evaluation cases
- SQL validation
- Optional Haystack ingestion

Excluded:

- Multi-agent orchestration
- Agent delegation
- Autonomous enterprise-system changes
- Automatic approval or rejection
- Web search
- Hybrid retrieval
- Custom replacement of the Db2 search tool

## Db2 search tool

The runtime uses the public `DB2VectorSearchTool` from `crewai_tools`.

The current IBM example configures it with:

- Db2 connection information
- target table
- vector column
- return columns
- retrieval limit
- cosine distance
- a custom embedding function

The tool performs the database-side vector search and returns text evidence to the agent. citeturn0search0

The project deliberately does **not** create a custom subclass such as:

```python
class DB2VectorSearchTool(BaseTool):
    ...
```

That would obscure the integration this use case is intended to demonstrate.

## Embedding and vector contract

The embedding model used during ingestion must match the embedding model used by `DB2VectorSearchTool`.

The current IBM example uses:

```text
ibm-granite/granite-embedding-125m-english
```

with 768-dimensional vectors and cosine distance. citeturn0search0

This package uses that model by default in `tools.py`.

If an existing knowledge base was created with another embedding model, configure the same model and vector dimension before running the agent.

## LLM

The reasoning model is Ollama:

```text
granite3.1-dense:8b
```

Start Ollama before running the application:

```bash
ollama serve
```

Then ensure the configured model is available.

## Haystack ingestion

Haystack is included only as an optional ingestion path.

The IBM Db2 Haystack integration provides an `IBMDb2DocumentStore`, and the IBM example uses Haystack components for loading, cleaning, splitting, embedding, and writing documents to Db2. citeturn1search0

The key architectural contract is:

```text
Haystack -> Db2
               ^
               |
CrewAI -> DB2VectorSearchTool
```

The agent never depends on Haystack at query time.

If the enterprise already uses LangChain, Langflow, or another ingestion pipeline, that pipeline can populate the same compatible Db2 vector table without changing the CrewAI agent.

## Example questions

### Authentication research

```text
What are our authentication architecture decisions and how do they relate to recent incidents?
```

Expected behavior:

1. Search for authentication architecture evidence.
2. Inspect ADR results.
3. Search for authentication incidents if needed.
4. Synthesize the evidence.
5. Cite document IDs where available.

### Vendor research

```text
What do I need to know before proposing a new vendor for our AI platform?
```

Potential evidence:

- architecture decisions
- security requirements
- vendor policies
- previous incidents
- technical standards

### Payment reliability

```text
Summarise what we know about payment service reliability issues.
```

Potential evidence:

- payment incidents
- architecture decisions
- runbooks
- technical documentation

## How to run

Create and activate the environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```powershell
.venv\Scripts\activate
```

Copy configuration:

```bash
cp .env.example .env
```

Start Ollama:

```bash
ollama serve
```

Run:

```bash
python main.py
```

Or:

```bash
python main.py --query "What are our authentication architecture decisions and how do they relate to recent incidents?"
```

## Validation

The supplied SQL validates the shared knowledge base:

1. document-type coverage
2. total document count
3. sample documents available to the agent

The supplied validation expects at least 15 documents for meaningful cross-type research.

Run:

```bash
db2 -tvf validation/validation.sql
```

Then review:

```text
validation/VALIDATION.md
```

## Evaluation

Evaluation focuses on agent behavior, not just answer text.

Track:

- whether the Db2 tool was invoked
- number of tool calls
- expected document IDs discovered
- document-type coverage
- answer grounding
- unsupported claims
- whether a second focused search improved evidence coverage

The goal is not to maximize tool calls. The goal is to demonstrate appropriate tool selection.

## Project structure

```text
13_crewai_research_agent/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── agents.py
├── tools.py
│
├── ingestion/
│   ├── __init__.py
│   └── ingest.py
│
├── evaluation/
│   ├── __init__.py
│   ├── cases.py
│   └── eval.py
│
└── validation/
    ├── validation.sql
    └── VALIDATION.md
```

## Enterprise impact

UC13 demonstrates the transition:

```text
Deterministic RAG
       |
       v
Tool-using agent
       |
       v
Multi-agent workflow
```

The project deliberately stops at the first step.

The separation of responsibilities is intentional:

- Haystack or another ingestion framework owns the write path.
- IBM Db2 owns vector storage and database-side retrieval.
- `DB2VectorSearchTool` exposes Db2 search to the agent.
- CrewAI controls agent reasoning and tool selection.
- Granite synthesizes retrieved evidence.
- Human users remain responsible for interpreting and acting on the answer.

## Key takeaway

> Use CrewAI when the decision to retrieve is itself part of the problem. Use the actual IBM Db2 search tool for retrieval, and keep ingestion independent.
