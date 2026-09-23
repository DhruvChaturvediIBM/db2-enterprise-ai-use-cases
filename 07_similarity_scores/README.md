# UC07 — Similarity Search with Relevance Scores

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Most RAG systems treat retrieval as a black box — they retrieve and then generate regardless of how strong the evidence actually is. This use case exposes the raw similarity scores to the application logic, enabling intelligent decisions: answer confidently if evidence is strong, ask for clarification if it's medium, refuse gracefully if evidence is weak.

**College project framing:** Build a search system that returns confidence scores and changes behaviour based on them.  
**Enterprise framing:** A knowledge assistant that knows when it doesn't know — returning "insufficient evidence" rather than hallucinating when the database doesn't have a relevant document.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `DB2VS` VectorStore |
| Core API | `similarity_search_with_score()` |
| Key pattern | Score-based application control flow |

### Score tiers

```
Score ≥ 0.85  →  Answer confidently with full generation
Score 0.60–0.84  →  Retrieve more, caveat the answer
Score < 0.60  →  Return "Insufficient evidence in knowledge base"
```

*(Score thresholds are configurable — these are sensible defaults for cosine similarity.)*

---

## Scope

- Connect `DB2VS` to `AI_DEMO.KNOWLEDGE_BASE`
- Call `similarity_search_with_score(query, k=5)`
- Implement score-based routing logic (the three tiers above)
- Show the raw score next to each result in output
- For medium/low confidence: show which documents were closest and why they were insufficient
- For high confidence: generate answer via Ollama Granite

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 07_similarity_scores
python main.py
```

Example scenarios to observe all three tiers:
- **High confidence:** `"What is the travel policy for Europe?"` → POL-001 is a strong match
- **Medium confidence:** `"What are the policies for remote work in Asia?"` → some match but not precise
- **Low confidence:** `"What is the quantum computing roadmap?"` → not in corpus

---

## How to test it

```bash
python main.py --query "travel policy europe"
# Expected:
#   [0.91] POL-001 — Travel and Expense Reimbursement Policy — Europe Finance
#   Confidence: HIGH → generating answer...

python main.py --query "quantum computing roadmap"
# Expected:
#   [0.42] ... (low-relevance result)
#   Confidence: LOW → Insufficient evidence in knowledge base.
```

**SQL validation** (`validation.sql`):
```sql
-- Verify DB2VS table structure and document count
SELECT COUNT(*) AS TOTAL_DOCS FROM AI_DEMO.KNOWLEDGE_BASE;

-- Sample content to confirm embeddings are stored
SELECT DOCUMENT_ID, TITLE, LENGTH(EMBEDDING) AS EMBEDDING_SIZE
FROM AI_DEMO.KNOWLEDGE_BASE
FETCH FIRST 5 ROWS ONLY;
```

---

## Files (to be created)

```
07_similarity_scores/
├── README.md
├── main.py         ← search with score-based routing
├── score_router.py ← implements three-tier confidence logic
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates that vector similarity scores are not just retrieval metadata — they are application control signals. This pattern is foundational for building AI systems that fail gracefully and maintain user trust by not generating when evidence is insufficient.
