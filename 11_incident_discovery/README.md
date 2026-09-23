# UC11 — Vector-Based Incident Discovery

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

When a new production incident occurs, engineers spend valuable time searching Confluence, Slack, and PagerDuty history to find if this has happened before. This use case stores historical incidents with embeddings in IBM Db2 and enables instant semantic discovery — "have we seen this before?" answered in seconds, not hours.

**College project framing:** Build an incident history search engine that finds similar past events from natural-language descriptions.  
**Enterprise framing:** A first-responder tool that, the moment a new incident is declared, surfaces the top-3 historically similar incidents with their root causes and resolutions — reducing mean time to resolution (MTTR).

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `DB2VS`, `similarity_search_with_score()` |
| Data | Incidents with: symptoms, service, root_cause, resolution, severity |
| Output | Similar historical incidents + their resolutions |

### Flow

```
New incident declared:
  "Payment service returning 503 errors, Db2 connections failing"
  │
  ▼
Embed incident description
  │
  ▼
Db2 similarity search (k=3)
  │
  ▼
Historical matches:
  [0.94] INC-001: Connection pool exhaustion → Resolution: increase pool size
  [0.71] INC-002: Auth failure after rotation → Resolution: restart token service
  │
  ▼
Display: similar incidents, their root causes, resolutions
```

---

## Scope

- Populate `AI_DEMO.INCIDENTS` table with historical incident corpus from `common/sample_data.py`
- Each incident stored as: concatenation of symptoms + root_cause + resolution (for rich embedding)
- Implement `discover_similar_incidents(description: str, k: int = 3)`
- Return: incident_id, title, severity, root_cause snippet, resolution snippet, score
- Optionally filter by: service, severity

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 11_incident_discovery
python main.py
```

Built-in test scenarios:
- `"Pods crashing with OOMKilled in healthcare namespace"` → INC-003
- `"Database connection errors causing service failures"` → INC-001
- `"Login failures after certificate update"` → INC-002

---

## How to test it

```bash
python main.py --incident "service returning 503, DB2 connection wait time high"
# Expected: INC-001 in top-2 (connection pool exhaustion)
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm incidents table
SELECT COUNT(*) FROM AI_DEMO.INCIDENTS;

-- Review incident metadata
SELECT DOCUMENT_ID, TITLE, 
       SUBSTR(CONTENT, 1, 100) AS CONTENT_PREVIEW
FROM AI_DEMO.INCIDENTS
ORDER BY EFFECTIVE_DATE DESC;
```

---

## Files (to be created)

```
11_incident_discovery/
├── README.md
├── main.py           ← discovers similar incidents for a new description
├── ingest.py         ← loads INCIDENTS corpus into AI_DEMO.INCIDENTS
├── discovery.py      ← discover_similar_incidents() function
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Turns historical operational knowledge stored in Db2 into reusable engineering memory. A direct, measurable enterprise value: engineers no longer start from zero when a recurring incident pattern appears. MTTR improves because the resolution playbook surfaces automatically.
