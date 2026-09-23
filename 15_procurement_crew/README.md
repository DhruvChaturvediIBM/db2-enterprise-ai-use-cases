# UC15 — Procurement / RFP Analysis Crew

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Procurement teams evaluate vendor proposals against a complex intersection of requirements, policies, compliance rules, and risk criteria. No single reviewer can hold all of this context simultaneously. This use case demonstrates a CrewAI crew where each agent specialises in one dimension of the evaluation — all grounded in enterprise knowledge stored in IBM Db2.

**College project framing:** Build a multi-agent system that analyses a document against multiple evaluation criteria.  
**Enterprise framing:** An AI-assisted RFP analysis crew that evaluates a supplier proposal against enterprise requirements, procurement policies, compliance rules, and risk policies — producing a structured evaluation report with Db2 citations.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | CrewAI |
| Agents | 5 specialised analysts |
| Db2 knowledge | procurement policies, supplier requirements, historical contracts, compliance rules, risk policies |
| LLM | Ollama `granite3.1-dense:8b` |
| Output | Multi-section evaluation report with pass/flag/fail per criteria |

### Agents

| Agent | Db2 Knowledge Used | Output |
|---|---|---|
| Requirements Analyst | supplier requirements | Requirements coverage assessment |
| Policy Analyst | procurement policies | Policy compliance check |
| Compliance Analyst | compliance rules, GDPR | Compliance gap analysis |
| Risk Analyst | risk policies, historical contracts | Risk profile assessment |
| Reviewer | — | Final aggregated evaluation |

---

## Scope

- Input: a short vendor proposal (provided as text, not a real PDF in this example)
- 5 agents each search their Db2 scope for relevant criteria/policies
- Each agent produces a structured section of the evaluation
- Reviewer synthesises into a final report: RECOMMEND / CONDITIONAL / REJECT + reasoning
- All citations trace back to specific Db2 document IDs

**Note on PII:** The sample vendor proposal uses fictional supplier data. No real procurement data is hardcoded.

---

## How to try it (once code is written)

```bash
ollama serve &
source .venv/bin/activate
cd 15_procurement_crew
python main.py
```

Sample vendor proposal (built into `main.py`):
```
"VendorCo proposes an AI platform solution supporting vector search at 1M+ 
document scale, on-premises deployment, and IBM Db2 as primary data source. 
Pricing: $0.002/query. SOC 2 Type II in progress (expected Q1 2025). 
SLA: 99.5% uptime."
```

---

## How to test it

```bash
python main.py
# Expected report:
#   Requirements Analyst: PASS on vector scale; FLAG on IBM Db2 support (verify)
#   Policy Analyst: FLAG — SOC 2 not yet certified (PROC-001 requires certification)
#   Compliance Analyst: FLAG — GDPR SCC not mentioned
#   Risk Analyst: FLAG — 99.5% SLA below our 99.9% requirement
#   Reviewer: CONDITIONAL — approve with SOC 2 delivery condition
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm procurement knowledge is loaded
SELECT DOCUMENT_ID, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('procurement', 'compliance', 'policy')
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;
```

---

## Files (to be created)

```
15_procurement_crew/
├── README.md
├── main.py           ← runs RFP analysis with sample proposal
├── agents.py         ← 5 agent definitions
├── tasks.py          ← 5 evaluation tasks
├── tools.py          ← Db2 search tools with scoped document types
├── crew.py           ← assembles hierarchical crew
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates agents operating over controlled enterprise knowledge rather than relying on model knowledge alone. Every evaluation criterion is grounded in a specific Db2 document, making the AI's reasoning auditable and the citations verifiable.
