# UC09 — Semantic Duplicate Knowledge Detection

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Enterprise knowledge bases accumulate duplicate and near-duplicate content — the same policy rewritten by two teams, a support article that largely repeats an existing one. This use case uses IBM Db2 vector similarity to detect semantic duplicates at ingestion time, before they pollute the knowledge base.

**College project framing:** Build a near-duplicate document detector using vector similarity.  
**Enterprise framing:** A knowledge ingestion gate that flags any new document as DUPLICATE, RELATED, or NEW based on its semantic distance to existing documents in Db2 — helping knowledge managers prevent content pollution.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `DB2VS` `similarity_search_with_score()` |
| Key pattern | Threshold-based semantic deduplication |
| Output | Classification: DUPLICATE / RELATED / NEW |

### Similarity thresholds

```
Score ≥ 0.92  →  DUPLICATE    (likely same content, different source)
Score 0.75–0.91  →  RELATED   (same topic, different angle — flag for review)
Score < 0.75  →  NEW          (safe to ingest)
```

### Flow

```
New document arrives
  │
  ▼
Embed new document
  │
  ▼
Db2 similarity_search_with_score(new_doc_content, k=5)
  │
  ▼
Check top-1 score against thresholds
  │
  ▼
DUPLICATE → reject + notify owner
RELATED   → flag for human review
NEW       → proceed with ingestion
```

---

## Scope

- Create a function `check_duplicate(new_doc: str) -> (classification, candidates)`
- Test with: intentional near-duplicate of POL-001 (slightly reworded travel policy)
- Test with: genuinely new content
- Test with: related but different content
- Print classification + the top matching documents with their scores

**Important:** This example uses Db2 for the detection logic, not for deduplication enforcement. The output is a classification signal that a human or ingestion pipeline acts on.

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 09_duplicate_detection
python main.py
```

Test cases built in:
1. Exact copy of POL-001 → DUPLICATE (score ~0.99)
2. Similar travel policy with different numbers → RELATED (score ~0.85)
3. A completely new document about software licensing → NEW (score < 0.60)

---

## How to test it

```bash
python main.py --text "All business travel in Europe must be pre-approved. Hotels capped at 250 EUR."
# Expected: DUPLICATE — matches POL-001 with score ~0.94

python main.py --text "Software license procurement requires legal review for open-source dependencies."
# Expected: NEW — score < 0.70
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm corpus has documents that would trigger duplicates
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'policy'
ORDER BY DOCUMENT_ID;
```

---

## Files (to be created)

```
09_duplicate_detection/
├── README.md
├── main.py           ← runs built-in test cases
├── detector.py       ← check_duplicate() function with threshold logic
├── validation.sql
└── eval.py           ← precision/recall on a small labelled set of known duplicates
```

---

## Enterprise impact

Demonstrates that IBM Db2 is not just where AI reads knowledge — it is also where AI helps maintain knowledge quality. This pattern directly addresses a real enterprise challenge: knowledge bases degrade over time without a systematic deduplication layer.
