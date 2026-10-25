# UC09 - Semantic Duplicate Knowledge Detection

## Status

Implementation included.

## Why this use case exists

Enterprise knowledge bases accumulate duplicate and near-duplicate content. The same policy may be published by two teams, a support article may repeat an existing procedure, or an older document may be rewritten without removing the original.

This use case uses IBM Db2 vector similarity as an ingestion-quality gate. A new document is embedded and compared with existing enterprise knowledge in Db2. The application then classifies the incoming content as:

- `DUPLICATE`: likely already represented by existing knowledge
- `RELATED`: semantically related, but not close enough to treat as a duplicate automatically
- `NEW`: no sufficiently close existing document was found

The classifier produces a decision signal. It does not silently delete, overwrite, or otherwise modify enterprise knowledge.

## Enterprise framing

The pattern is a knowledge-ingestion gate:

```text
New enterprise document
        |
        v
Generate embedding
        |
        v
DB2VS.similarity_search_with_score()
        |
        v
Top matching existing documents
        |
        v
Semantic duplicate classifier
        |
        +-------------------+
        |                   |
        v                   v
   DUPLICATE             RELATED
   HOLD / reject         HUMAN REVIEW
        |                   |
        +---------+---------+
                  |
                  v
                 NEW
            proceed to ingest
```

This makes the retrieval layer useful not only for answering questions, but also for maintaining knowledge quality before new content enters the RAG corpus.

## What it demonstrates

| Capability | Implementation |
|---|---|
| Framework | LangChain |
| IBM integration | `langchain-db2` |
| Db2 vector store | `DB2VS` |
| Search API | `similarity_search_with_score()` |
| Distance metric | Cosine |
| Decision signal | Semantic duplicate classification |
| Classifications | `DUPLICATE`, `RELATED`, `NEW` |
| Actions | `HOLD`, `REVIEW`, `INGEST` |
| Embeddings | Ollama `nomic-embed-text` |
| Evaluation | Small labelled classification set |
| Validation | Db2 SQL |

The implementation uses the public IBM Db2 LangChain integration directly. There is no locally implemented vector store or replacement similarity-search algorithm.

## Important score interpretation

This example uses `DistanceStrategy.COSINE`.

For Db2 cosine search, `similarity_search_with_score()` returns cosine distance. Smaller distance means a closer match. Therefore the application converts the raw distance to an application-level similarity value:

```text
similarity = 1 - cosine_distance
```

The configured thresholds are expressed in that similarity scale because it is easier to explain the duplicate policy that way.

```text
similarity >= 0.75
    -> DUPLICATE

0.55 <= similarity < 0.75
    -> RELATED

similarity < 0.55
    -> NEW
```

These values are demonstration defaults, not universal enterprise thresholds. They should be calibrated against the organization's actual corpus, embedding model, and labelled duplicate examples.

The application always prints both the raw Db2 distance and the derived similarity so the decision remains explainable.

## Classification logic

Only the closest retrieved document is used for the primary classification because the question is whether the incoming document is already represented by existing knowledge.

```text
Top candidate similarity >= DUPLICATE_THRESHOLD
    -> DUPLICATE
    -> recommended action: HOLD

Top candidate similarity >= RELATED_THRESHOLD
    -> RELATED
    -> recommended action: REVIEW

Top candidate similarity < RELATED_THRESHOLD
    -> NEW
    -> recommended action: INGEST
```

The remaining top-k candidates are retained and printed for human inspection. They provide context for why the classifier made its decision.

## Decision policy

The classifier is intentionally separated from the enterprise action:

| Classification | Meaning | Recommended action |
|---|---|---|
| `DUPLICATE` | Existing knowledge is highly similar | `HOLD` the incoming document for duplicate review |
| `RELATED` | Existing knowledge covers a related subject | `REVIEW` before ingestion |
| `NEW` | No sufficiently close match was found | `INGEST` |

No automatic deletion is performed. The Db2 vector search result is a quality-control signal that a human reviewer or ingestion pipeline can act on.

## Scope

This use case:

- Connects LangChain's `DB2VS` directly to `AI_DEMO.KNOWLEDGE_BASE`.
- Uses `similarity_search_with_score(new_doc, k=TOP_K)`.
- Uses cosine distance and converts it to a readable similarity value.
- Classifies the incoming document from the top candidate.
- Prints the top matching documents and their scores.
- Prints useful metadata such as document ID, title, type, department, and region when available.
- Supports configurable duplicate and related thresholds.
- Includes three labelled demonstration cases.
- Includes a small evaluation runner.
- Includes the supplied Db2 validation checks for policy documents, title duplicates, test duplicates, and cleanup.
- Includes a separate validation guide.

## Project structure

```text
09_duplicate_detection/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── db2_store.py
├── detector.py
├── decision.py
├── main.py
│
├── evaluation/
│   ├── __init__.py
│   ├── cases.py
│   └── eval.py
│
└── validation/
    ├── validation.sql
    └── VALIDATION.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Start Ollama and make the embedding model available:

```bash
ollama pull nomic-embed-text
```

Configure the Db2 and Ollama values in `.env`.

The Db2 knowledge base should already contain the enterprise documents used by the earlier use cases, including the policy corpus used by the supplied validation SQL.

## Direct IBM Db2 package usage

The project intentionally imports the IBM integration directly:

```python
from langchain_db2 import DB2VS
```

The detector directly calls:

```python
vector_store.similarity_search_with_score(new_doc, k=top_k)
```

There is no custom vector-store wrapper that hides the Db2 operation. `db2_store.py` is only responsible for constructing the actual `DB2VS` instance with the configured Db2 connection, embedding function, table, and cosine distance strategy.

## Run the built-in cases

Run all three demonstration cases:

```bash
python main.py --case all
```

Run the likely duplicate case:

```bash
python main.py --case duplicate
```

Run the related case:

```bash
python main.py --case related
```

Run the new-content case:

```bash
python main.py --case new
```

## Test with arbitrary text

```bash
python main.py --text "All business travel in Europe must be pre-approved. Hotels are capped at 250 EUR per night."
```

The application reports:

```text
Classification: DUPLICATE | RELATED | NEW
Recommended action: HOLD | REVIEW | INGEST
Top candidate: ...
Raw cosine distance: ...
Derived similarity: ...
```

Exact scores depend on the stored documents, embedding model, and Db2 vector-distance calculation. The example labels describe the intended test scenarios, not guaranteed fixed scores.

## Demonstration cases

### 1. Likely duplicate

A slightly reworded travel-policy document should be close to the existing Europe travel policy.

```text
All business travel in Europe requires prior approval. Hotel expenses must remain within the approved European accommodation limit.
```

Expected classification: `DUPLICATE` when the measured similarity crosses the configured duplicate threshold.

### 2. Related content

A document about travel reimbursement can share the same subject while remaining materially different from a specific travel-approval policy.

```text
Employees travelling internationally should submit receipts within ten business days and use the corporate reimbursement process for eligible expenses.
```

Expected classification: `RELATED` when the measured similarity falls between the configured thresholds.

### 3. Related content — procurement domain

Software licensing shares procurement and legal vocabulary with POL-005. The model correctly surfaces it for human review rather than treating it as genuinely new.

```text
Software license procurement requires legal review for open-source dependencies and renewal terms.
```

Expected classification: `RELATED` — similarity ~0.63 against POL-005.

### 4. New content

Content with no domain overlap with the enterprise corpus.

```text
To make a sourdough starter, mix equal parts flour and water and leave at room temperature for 24 hours until bubbles form.
```

Expected classification: `NEW` when no sufficiently close existing document is found.

## Threshold configuration

The defaults are calibrated for `nomic-embed-text` cosine distances on this corpus.
Max achievable similarity is ~0.85 on near-paraphrase text.

```text
TOP_K=5
DUPLICATE_THRESHOLD=0.75
RELATED_THRESHOLD=0.55
```

They can be changed through `.env` or command-line arguments.

For example:

```bash
python main.py --text "..." --duplicate-threshold 0.90 --related-threshold 0.70
```

The application validates that:

```text
0 <= RELATED_THRESHOLD < DUPLICATE_THRESHOLD <= 1
```

## Evaluation

Run:

```bash
python evaluation/eval.py
```

The evaluator runs the labelled cases against the same Db2 vector search and reports:

- Expected classification
- Actual classification
- Top candidate
- Raw distance
- Derived similarity
- Number of correct classifications
- Overall accuracy
- Per-class precision and recall where measurable

This is a small demonstration evaluation. It is not a production-quality duplicate benchmark. A production implementation should build a representative labelled set from the organization's actual duplicate, related, and new-document distributions.

## Validation

Run the supplied SQL with IBM Db2 Developer Extension or another Db2 SQL client:

```text
validation/validation.sql
```

The validation guide explains what each query checks and how the optional test-duplicate seed and cleanup steps relate to the Python demo.

The SQL intentionally retains the source validation checks for:

1. policy documents
2. obvious title duplicates
3. seeded test duplicates
4. cleanup confirmation

## Safety and data handling

This demonstration does not automatically delete documents, overwrite documents, or change enterprise records as a consequence of a duplicate classification.

`DUPLICATE` means "hold for duplicate review", not "delete the existing document".

If test data is seeded, it should use an explicitly identifiable test title or document ID and should be removed only through an intentional cleanup operation.

## Enterprise value

The use case demonstrates a complementary role for Db2 vector search:

```text
UC07 Similarity Search + Relevance Score
    -> Is retrieved evidence strong enough?

UC08 MMR Retrieval
    -> Do I have enough different perspectives?

UC09 Semantic Duplicate Detection
    -> Is this new enterprise knowledge already represented?
```

The key enterprise message is:

> IBM Db2 is not only used to retrieve enterprise knowledge. It can also help maintain the quality of that knowledge before it enters the RAG system.

## Production considerations

A production ingestion gate would typically add:

- Human approval workflows for `DUPLICATE` and `RELATED` decisions.
- Threshold calibration using labelled enterprise data.
- Audit logging of the incoming document, top candidates, scores, classifier version, and reviewer decision.
- Document version and effective-date awareness so an updated policy is not treated as a duplicate solely because it is semantically similar.
- Source and ownership metadata so reviewers can compare the authoritative document with the incoming copy.
- Monitoring for embedding-model changes because changing the embedding model can change score distributions.
- Access controls so the duplicate detector only searches documents the ingestion workflow is permitted to inspect.

These concerns are outside the scope of this demonstration but are important when turning semantic duplicate detection into an enterprise ingestion control.
