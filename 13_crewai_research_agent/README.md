# UC13 — Single-Agent Enterprise Research Assistant

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Not every AI application needs an agent. But when the decision about *when* to search enterprise knowledge is non-trivial — when the assistant needs to reason about whether it has enough information before answering — an agent adds real value. This use case demonstrates the minimal justification for using CrewAI: a single agent with a single Db2 search tool that decides whether to search or answer from context.

**College project framing:** Build a simple AI agent that can search a database and reason over results before answering.  
**Enterprise framing:** The transition from deterministic RAG pipelines to a reasoning agent that chooses when to use enterprise knowledge — the first step toward multi-agent enterprise workflows.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | CrewAI |
| Db2 capability | `DB2VectorSearchTool` (CrewAI tool wrapping Db2 similarity search) |
| LLM | Ollama `granite3.1-dense:8b` |
| Agent | Single CrewAI agent with one tool |
| Key pattern | Tool-using agent (vs deterministic RAG pipeline) |

### Flow

```
User question
  │
  ▼
CrewAI Agent (Granite LLM)
  │
  ├──  "I need to search enterprise knowledge"
  │         │
  │         ▼
  │    DB2VectorSearchTool
  │         │
  │         ▼
  │    Db2 similarity search results
  │         │
  │         ▼
  │    Agent reasoning over results
  │
  └──  Answer (grounded in Db2 results)
```

---

## Scope

- Implement a custom `DB2VectorSearchTool` as a CrewAI tool:
  ```python
  class DB2VectorSearchTool(BaseTool):
      name = "db2_enterprise_search"
      description = "Search the enterprise knowledge base for relevant documents"
      def _run(self, query: str) -> str: ...
  ```
- Create a single CrewAI agent: `EnterpriseResearcher` with `db2_enterprise_search` tool
- Create a single task: answer the user's question using available enterprise knowledge
- Demonstrate: the agent reasons about search results before producing its answer
- Show agent thought process (verbose=True) so the reasoning is visible

**Important design note:** If the question can be answered deterministically from a single retrieval call, use UC01 or UC07 instead. This example is for cases where the agent needs to decide *how many times* to search, or *what* to search for.

---

## How to try it (once code is written)

```bash
# Ensure Ollama is running
ollama serve &

source .venv/bin/activate
cd 13_crewai_research_agent
python main.py
```

Sample questions that benefit from agent reasoning:
- `"What do I need to know before proposing a new vendor for our AI platform?"`
- `"Summarise what we know about payment service reliability issues"`

---

## How to test it

```bash
python main.py --query "What are our authentication architecture decisions and how do they relate to recent incidents?"
# Expected: Agent searches for ADRs AND incidents, reasons across both, produces synthesis
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm knowledge base available to the agent
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE;
```

---

## Files (to be created)

```
13_crewai_research_agent/
├── README.md
├── main.py           ← CrewAI crew with single agent
├── tools.py          ← DB2VectorSearchTool definition
├── agents.py         ← EnterpriseResearcher agent definition
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates the transition from deterministic retrieval to tool-using AI. The pattern is intentionally minimal — one agent, one tool — to isolate exactly what CrewAI adds over a pure RAG pipeline. This is the foundation for UC14–UC16 multi-agent crews.
