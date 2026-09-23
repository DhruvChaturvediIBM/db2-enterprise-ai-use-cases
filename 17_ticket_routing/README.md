# UC17 — Semantic Ticket Routing

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Support tickets are manually assigned or routed by keyword rules that break when language varies slightly. Historical resolved tickets — already labelled with the correct team, category, and priority — contain the routing signal. This use case uses IBM Db2 vector search to find the most similar historical tickets and infer the correct routing for new ones.

**College project framing:** Build a classification system using nearest-neighbour search over labelled historical data.  
**Enterprise framing:** A semantic ticket routing engine that learns from historical routing patterns stored in Db2, handling natural language variation that keyword rules miss — without retraining a model.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `DB2VS`, `similarity_search_with_score()` |
| Pattern | k-NN classification over historical labelled data |
| No agent needed | Routing logic is deterministic given the similarity results |
| LLM | Optional — used only for confirmation message, not for the routing decision |

### Flow

```
New ticket: "Users cannot log in after the certificate was renewed last night"
  │
  ▼
Embed ticket text
  │
  ▼
Db2 similarity search → k=5 similar historical tickets
  │
  ▼
Vote on team + category from top-3 most similar (weighted by score)
  │
  ▼
Routing suggestion: Team=Identity Platform, Category=Authentication, Priority=P1
```

---

## Scope

- Populate `AI_DEMO.TICKETS` table with historical ticket corpus (derived from INC documents + support articles)
- Each ticket: text, team, category, priority, product, resolution_summary
- Implement `route_ticket(text: str) -> RoutingSuggestion`
- Weighted voting from top-k: higher similarity score = more weight in the vote
- Output: suggested team, category, priority, confidence (based on vote margin), top-3 similar tickets

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 17_ticket_routing
python main.py
```

Built-in test tickets:
1. `"OOMKilled pods in production namespace, services crashing"` → Engineering / Kubernetes
2. `"User locked out, cannot set up new authenticator app"` → IT Support / Identity
3. `"Payment failing for European customers, error code 503"` → Banking / Payment Platform

---

## How to test it

```bash
python main.py --ticket "login failure after certificate update"
# Expected:
#   Suggested Team: Identity Platform
#   Category: Authentication
#   Priority: P1
#   Based on: INC-002 (0.93), SUP-001 (0.81), ...
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm ticket history loaded
SELECT COUNT(*) FROM AI_DEMO.TICKETS;

-- Review team distribution in historical data
SELECT DEPARTMENT AS TEAM, COUNT(*) AS TICKET_COUNT
FROM AI_DEMO.TICKETS
GROUP BY DEPARTMENT
ORDER BY TICKET_COUNT DESC;
```

---

## Files (to be created)

```
17_ticket_routing/
├── README.md
├── main.py           ← routes built-in test tickets + interactive mode
├── router.py         ← route_ticket() with weighted k-NN voting
├── ingest.py         ← loads ticket corpus into AI_DEMO.TICKETS
├── validation.sql
└── eval.py           ← routing accuracy on a labelled test set
```

---

## Enterprise impact

Uses enterprise history to improve operational routing without keyword rules and without model retraining. The routing signal lives in Db2 — adding new historical examples automatically improves future routing. This is a practical, immediately deployable enterprise pattern.
