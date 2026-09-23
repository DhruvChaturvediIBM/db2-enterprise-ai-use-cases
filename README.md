# IBM Db2 AI Use Cases

> 20 enterprise-grade AI examples on IBM Db2 using Haystack, LangChain, and CrewAI.  
> Designed to be production-ready reference implementations and learning resources.

---

## What this repository demonstrates

```
IBM Db2
  |
  +-- structured enterprise data
  +-- documents / knowledge
  +-- metadata
  +-- native VECTOR storage
  +-- vector similarity
  |
  +-------------------------------+
                                  |
                         AI framework layer
                                  |
             +--------------------+--------------------+
             |                    |                    |
          Haystack             LangChain            CrewAI
             |                    |                    |
        pipelines             VectorStore             tools
        retrieval             search/MMR              agents
        reranking             scores                  crews
```

---

## Requirements

- Python 3.10+
- IBM Db2 (IBM FyRe or local Docker)
- [Ollama](https://ollama.com/) with `granite3.1-dense:8b` pulled (used as the primary LLM)
- IBM VPN (if connecting to FyRe)

---

## Quick start

```bash
# 1. Clone
git clone <repo-url>
cd ibm-db2-ai-use-cases

# 2. Install all dependencies (Python + IBM Db2 drivers + AI frameworks)
bash install.sh

# 3. Configure environment
cp .env.example .env
# Edit .env with your Db2 credentials

# 4. Pull the Ollama Granite model
ollama pull granite3.1-dense:8b

# 5. Run any use case
cd 01_enterprise_knowledge_rag
python main.py
```

---

## Repository structure

```
ibm-db2-ai-use-cases/
│
├── README.md                    ← this file
├── install.sh                   ← one-command setup script
├── requirements.txt             ← all Python dependencies
├── .env.example                 ← environment variable template
├── .gitignore
│
├── common/                      ← shared utilities (reused by all UCs)
│   ├── db2.py                   ← Db2 connection helper
│   ├── embeddings.py            ← embedding helper (Ollama + sentence-transformers)
│   ├── config.py                ← env var loader
│   ├── sample_data.py           ← shared enterprise knowledge corpus loader
│   └── evaluation.py           ← lightweight evaluation helpers
│
├── data/                        ← shared enterprise document corpus
│   ├── policies/
│   ├── incidents/
│   ├── architecture/
│   ├── support/
│   ├── procurement/
│   └── compliance/
│
├── 01_enterprise_knowledge_rag/
├── 02_policy_metadata_filtering/
├── 03_technical_document_search/
├── 04_date_aware_compliance/
├── 05_reranked_search/
├── 06_ollama_local_reranking/
├── 07_similarity_scores/
├── 08_mmr_retrieval/
├── 09_duplicate_detection/
├── 10_semantic_recommendation/
├── 11_incident_discovery/
├── 12_architecture_decisions/
├── 13_crewai_research_agent/
├── 14_incident_investigation_crew/
├── 15_procurement_crew/
├── 16_compliance_crew/
├── 17_ticket_routing/
├── 18_operational_memory/
├── 19_change_impact/
└── 20_knowledge_maintenance/
```

---

## Development waves

| Wave | Use Cases | Capability |
|------|-----------|------------|
| 1 – Foundation | UC01, UC02, UC03 | Db2 connect → embed → vector retrieve |
| 2 – Retrieval quality | UC04–UC08 | filters, scores, reranking, MMR |
| 3 – Vector applications | UC09–UC12 | duplicates, recommendations, incident search |
| 4 – Agents | UC13–UC16 | single agent, multi-agent crews |
| 5 – Enterprise intelligence | UC17–UC20 | routing, memory, change impact, maintenance |

---

## LLM strategy

All use cases default to **Ollama + `granite3.1-dense:8b`** for:
- local-first execution
- no API key required
- enterprise data privacy

To switch to a cloud LLM, set `LLM_PROVIDER=openai` and `OPENAI_API_KEY` in `.env`.

---

## Environment variables

See [`.env.example`](.env.example) for all required variables.

---

## Contributing / extending

Each use case is intentionally self-contained.  
After reviewing the scope README in each folder, run the example and check the SQL validation queries to confirm what was written to Db2.

---

## Security

- Never commit `.env`
- Use `.env.example` as the template
- All credentials flow through environment variables only
