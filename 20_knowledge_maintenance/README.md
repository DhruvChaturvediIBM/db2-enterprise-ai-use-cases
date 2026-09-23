# UC20 — Enterprise Knowledge Maintenance Assistant

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

AI knowledge bases degrade over time. Documents become duplicated, outdated, or inconsistent with each other. This use case closes the loop: IBM Db2 is not only where AI reads enterprise knowledge — it is where AI helps maintain and improve that knowledge. Using vector similarity, metadata analysis, and optional LLM classification, this example identifies maintenance candidates and supports a human-approved update workflow.

**College project framing:** Build a knowledge base audit tool that finds and flags stale or duplicate content.  
**Enterprise framing:** A knowledge maintenance assistant that periodically audits the Db2 knowledge base, flags candidates for update or deletion, presents them to a human reviewer, and applies approved changes — keeping the AI knowledge layer accurate and current.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `similarity_search_with_score()`, `get_pks()`, `delete()`, metadata filtering |
| LLM | Ollama `granite3.1-dense:8b` — optional classification of candidates |
| Pattern | AI-assisted knowledge lifecycle management with human approval |

### Maintenance tasks

```
1. Duplicate detection:
   Find document pairs with similarity > 0.90
   → Flag: "POL-001 and POL-001-COPY appear nearly identical"

2. Stale document detection:
   Find ACTIVE documents with effective_date > 2 years ago and no update
   → Flag: "TECH-002 has not been updated in 18 months"

3. Orphaned document detection:
   Find documents never retrieved in any search (if access logging is enabled)
   → Flag: "SUP-001 has low semantic overlap with any recent query"

4. Human approval gate:
   Present flagged candidates → human confirms → delete / update / keep

5. Approved deletion:
   db2vs.delete(ids=[...]) or db2vs.clear_table() for full reset
```

---

## Scope

- Implement `audit_knowledge_base()` → returns list of `MaintenanceCandidate` objects
- Each candidate: document_id, issue_type (DUPLICATE/STALE/ORPHANED), evidence, recommendation
- Optional: call Ollama Granite to classify: "Is this document still relevant? Answer YES/NO with reason."
- Human approval CLI: display candidates one by one, user types keep/delete/update
- Apply approved deletions via `DB2VS.delete(ids=[...])`
- Demonstrate `clear_table()` on a test table (NOT production knowledge base)

**Safety principle:** Deletions only happen after explicit human confirmation. The script never auto-deletes.

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 20_knowledge_maintenance
python main.py --audit
# Runs full audit, prints candidates

python main.py --audit --interactive
# Presents each candidate for human approval before any action
```

---

## How to test it

```bash
# First, add a deliberate near-duplicate to the knowledge base
python main.py --seed-duplicate

# Then run audit
python main.py --audit
# Expected: flags the near-duplicate pair with similarity score

# Run with LLM classification
python main.py --audit --llm-classify
# Expected: Granite classifies each candidate as RELEVANT/STALE/REDUNDANT
```

**SQL validation** (`validation.sql`):
```sql
-- Knowledge base state before and after maintenance
SELECT COUNT(*) AS TOTAL, STATUS,
       COUNT(CASE WHEN UPDATED_AT < (CURRENT DATE - 365 DAYS) THEN 1 END) AS STALE_COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY STATUS;

-- Verify specific document was deleted (after approval)
SELECT COUNT(*)
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_ID = 'DOC-TO-DELETE';
-- Expected: 0
```

---

## Files (to be created)

```
20_knowledge_maintenance/
├── README.md
├── main.py           ← audit + interactive approval CLI
├── auditor.py        ← audit_knowledge_base() — all three detection types
├── llm_classifier.py ← optional Granite relevance classification
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Closes the loop: Db2 is not merely where AI reads knowledge — AI helps maintain the knowledge layer itself. This is the most operationally mature example in the repository. It demonstrates that an enterprise AI platform must address not only retrieval quality at a point in time, but knowledge health over time.
