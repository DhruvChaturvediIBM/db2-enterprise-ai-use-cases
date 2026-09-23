# UC18 — Enterprise Operational Memory

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Organizations repeatedly solve the same operational problems from scratch because past resolutions are stored in tickets and postmortems that nobody reads. This use case demonstrates IBM Db2 as a long-lived operational memory — resolved incidents and their resolutions are stored with embeddings, and future incidents can retrieve the exact resolution playbook from similar past events.

**College project framing:** Build a persistent memory system using a database as the long-term store.  
**Enterprise framing:** An operational memory layer where every resolved incident adds to the organisation's collective knowledge in Db2, and future incidents can immediately retrieve proven resolutions — transforming incident management from reactive to knowledge-driven.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain (or Haystack) |
| Db2 capability | `DB2VS`, `add_texts()`, `similarity_search_with_score()` |
| Pattern | Read-write operational memory: write resolutions, read for future incidents |
| Optional extension | Mem0 + Db2 integration path |

### Flow (write path — when incident is resolved)

```
Resolved incident: symptoms + root_cause + resolution + commands_used
  │
  ▼
Embed as a single rich memory record
  │
  ▼
AI_DEMO.OPERATIONAL_MEMORY (Db2)
```

### Flow (read path — when new incident occurs)

```
New incident description
  │
  ▼
Similarity search in AI_DEMO.OPERATIONAL_MEMORY
  │
  ▼
Top-3 similar resolved incidents with resolutions
  │
  ▼
Display: what was tried, what worked, exact commands
```

---

## Scope

- Create `AI_DEMO.OPERATIONAL_MEMORY` table (separate from the general knowledge base)
- Implement `remember_resolution(incident: dict)` — write path
- Implement `recall_resolutions(description: str, k: int = 3)` — read path
- Demonstrate the full cycle: ingest historical incidents → resolve a new one using memory
- Format output to show exact resolution steps, environment context, timestamps
- Demonstrate that adding new resolved incidents improves future recall (live demonstration)

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 18_operational_memory
python main.py
```

Demo sequence:
1. Load historical incident resolutions into Db2 (write)
2. Simulate a new incident: "Kubernetes pods crashing with memory errors in healthcare namespace"
3. Recall from memory → surfaces INC-003 resolution with exact fix steps
4. Simulate another new incident: "DB2 connection pool exhausted after peak traffic"
5. Recall → surfaces INC-001 resolution with connection pool fix

---

## How to test it

```bash
python main.py --phase write  # ingest historical resolutions
python main.py --phase read --incident "pods crashing memory error healthcare"
# Expected: INC-003 resolution — increase memory limit, add streaming processor
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm operational memory is populated
SELECT COUNT(*) FROM AI_DEMO.OPERATIONAL_MEMORY;

-- Review memory entries
SELECT DOCUMENT_ID, TITLE, EFFECTIVE_DATE,
       SUBSTR(CONTENT, 1, 120) AS RESOLUTION_PREVIEW
FROM AI_DEMO.OPERATIONAL_MEMORY
ORDER BY EFFECTIVE_DATE DESC;
```

---

## Files (to be created)

```
18_operational_memory/
├── README.md
├── main.py           ← demonstrates write → read cycle
├── memory.py         ← remember_resolution() + recall_resolutions()
├── ingest.py         ← bulk-loads historical incidents into memory
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates Db2 as long-lived, searchable operational memory — not just a knowledge base for policies and documents, but a living accumulation of engineering experience. Every resolved incident makes the organisation smarter. This pattern directly addresses the "we solved this before but can't find how" problem that plagues every engineering organisation.
