# UC14 — Multi-Agent Incident Investigation Crew

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Serious incident investigation is a multi-discipline activity. An SRE needs to search historical incidents; a runbook analyst needs to search operational procedures; a root cause analyst needs to synthesise across both. No single agent can specialise in all of these. This use case shows where CrewAI multi-agent orchestration provides genuine value — each agent has a specialist role and Db2 knowledge scope.

**College project framing:** Build a multi-agent system where specialised agents collaborate to investigate a problem.  
**Enterprise framing:** An automated first-responder crew that, given a new incident description, produces a structured investigation report — surfacing similar historical incidents, relevant runbooks, and a root cause hypothesis — in minutes.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | CrewAI |
| Agents | 5 specialised agents with dedicated Db2 search scopes |
| Db2 knowledge | incidents, runbooks, architecture docs, known issues, postmortems |
| LLM | Ollama `granite3.1-dense:8b` |

### Agents

| Agent | Db2 Search Scope | Role |
|---|---|---|
| Incident Investigator | ALL types | Classify and scope the incident |
| Historical Analyst | incidents, postmortems | Find similar past incidents |
| Runbook Analyst | runbooks, support | Find relevant recovery procedures |
| Root Cause Analyst | ADRs, technical docs | Hypothesise root cause |
| Reviewer | — | Synthesise findings into final report |

### Flow

```
New incident description
  │
  ▼
Incident Investigator (scopes the problem)
  │
  ├──────────────────────┐
  ▼                      ▼
Historical Analyst    Runbook Analyst
(Db2: incidents)      (Db2: runbooks)
  │                      │
  └──────────┬───────────┘
             ▼
      Root Cause Analyst (Db2: ADRs)
             │
             ▼
          Reviewer
             │
             ▼
  Structured Investigation Report
```

---

## Scope

- 5 CrewAI agents, each with a typed `DB2VectorSearchTool` scoped to relevant document types
- `DB2VectorSearchTool` accepts a `document_type` filter so each agent only sees its domain
- Crew orchestrates in sequential process: investigate → research (parallel) → analyse → review
- Final output: structured report with sections: Incident Summary, Similar Past Incidents, Relevant Runbooks, Root Cause Hypothesis, Recommended Actions
- Verbose mode shows agent reasoning chain

---

## How to try it (once code is written)

```bash
ollama serve &
source .venv/bin/activate
cd 14_incident_investigation_crew
python main.py
```

Built-in test incident:
```
"Our payment service is returning HTTP 503 errors. Db2 connection wait 
times are very high. The issue started after a deployment at 14:30."
```

---

## How to test it

```bash
python main.py --incident "payment service 503, high DB2 wait times after deployment"
# Expected report sections: 
#   - Similar incidents (INC-001: connection pool exhaustion)
#   - Relevant runbook (RUN-001: Payment P1 recovery)
#   - Root cause hypothesis: connection pool size misconfiguration
#   - Recommended actions: check pool config, restart service
```

**SQL validation** (`validation.sql`):
```sql
-- Verify all knowledge types available to agents
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;
```

---

## Files (to be created)

```
14_incident_investigation_crew/
├── README.md
├── main.py           ← entry point: accepts incident description, runs crew
├── agents.py         ← 5 agent definitions
├── tasks.py          ← 5 task definitions
├── tools.py          ← DB2VectorSearchTool with document_type scoping
├── crew.py           ← assembles and runs the crew
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Shows where multi-agent orchestration provides real, measurable enterprise value — not as a demonstration of AI capability, but as a practical first-responder system that compresses investigation time from hours to minutes, grounded in the organization's own historical knowledge stored in Db2.
