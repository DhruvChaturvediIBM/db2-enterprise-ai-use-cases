# UC19 Validation Guide

## Purpose

This guide explains how to validate the knowledge-base prerequisites for Semantic Change Impact Discovery.

The supplied SQL validates the source data in `AI_DEMO.KNOWLEDGE_BASE`. It does not prove that semantic retrieval will return a specific ranking because retrieval depends on the indexed embeddings, vector metric, embedding model, and configured `TOP_K`.

## 1. Validate cross-type coverage

Run:

```sql
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;
```

The demonstration expects the knowledge base to contain multiple document types, including:

- `adr`
- `incident`
- `technical`
- `policy`
- `runbook`

Additional enterprise types are supported by the discovery pattern.

## 2. Validate authentication-change evidence

Run the authentication query in `validation.sql`.

The source data is expected to contain:

- `ADR-003`
- `INC-002`
- `POL-004`

The original use case also identifies `TECH-002` as a semantic retrieval target. The SQL check is content-based, so its exact output depends on the data loaded into `AI_DEMO.KNOWLEDGE_BASE`.

## 3. Validate payment-change evidence

Run the payment query.

The expected demonstration artifacts are:

- `INC-001`
- `RUN-001`
- `ADR-002`

Again, SQL content matching is a prerequisite check. It is not a substitute for vector retrieval evaluation.

## 4. Validate the application

After the SQL checks pass:

```bash
python main.py --change "replacing authentication mechanism"
```

Review:

- document IDs
- document types
- raw scores
- normalized similarity
- relevance bands
- content previews
- LLM evidence references

Then try:

```bash
python main.py --change "payment service database connection pool"
```

## 5. Interpretation

A retrieved artifact is a **candidate for review**, not proof of actual impact.

The LLM summary should remain grounded in retrieved evidence and should not invent dependencies or make the final change-management decision.

## 6. Troubleshooting

If results are unexpectedly weak:

1. Confirm the expected documents exist in `AI_DEMO.KNOWLEDGE_BASE`.
2. Confirm their `EMBEDDING` values are populated.
3. Confirm the application uses the same embedding model used to create the stored vectors.
4. Confirm the Db2 vector metric and score semantics.
5. Increase `TOP_K` temporarily to inspect the broader candidate set.
6. Review the raw scores before changing relevance thresholds.
