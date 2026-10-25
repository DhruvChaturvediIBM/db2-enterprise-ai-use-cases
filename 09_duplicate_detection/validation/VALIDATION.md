# UC09 Validation Guide

## Purpose

This guide validates the Db2 knowledge corpus and the controlled test-data lifecycle used by the semantic duplicate detection demonstration.

The supplied SQL is intentionally focused on the checks from the UC09 source validation plan:

1. Confirm policy documents exist.
2. Check for obvious title duplicates.
3. Confirm an intentionally seeded test duplicate exists.
4. Confirm the test duplicate has been removed after explicit cleanup.

## Prerequisites

- IBM Db2 is running and reachable.
- `AI_DEMO.KNOWLEDGE_BASE` exists.
- The enterprise knowledge corpus has been loaded.
- The database user has permission to run the SELECT statements.

## Step 1: Inspect policy documents

Run query 1 in `validation.sql`.

Expected result:

- One or more rows with `DOCUMENT_TYPE = 'policy'`.
- The target travel-policy document should be present when the expected seed corpus is loaded.

This establishes that the corpus contains the type of knowledge used by the duplicate-detection demonstration.

## Step 2: Check obvious title duplicates

Run query 2.

Expected result:

```text
0 rows
```

unless intentional test duplicates were seeded.

This is a simple lexical baseline. It does not replace semantic duplicate detection because two semantically duplicate documents can have different titles.

## Step 3: Seed a controlled test duplicate

The validation SQL expects a test document to be identifiable with `TEST_DUPLICATE` in its title or `TEST` in its document ID.

This project does not automatically mutate the enterprise knowledge base as a side effect of classification. If your ingestion environment supports a controlled test seed, add a clearly labelled test document through that environment and then run query 3.

Expected result:

- The intentionally seeded test row is returned.

Do not use an existing production document as the test duplicate.

## Step 4: Run the detector

With the controlled test document present, run a classification against the intended near-duplicate text:

```bash
python main.py --case duplicate
```

The application should print:

- `DUPLICATE`, `RELATED`, or `NEW`
- Recommended action
- Top candidate
- Raw cosine distance
- Derived similarity
- Additional top-k candidates

Exact numeric values are corpus- and embedding-dependent.

## Step 5: Inspect the source data again

Re-run query 1 and query 2.

This confirms that the duplicate detector itself did not delete or overwrite existing knowledge.

## Step 6: Explicit cleanup

After the controlled test is no longer needed, remove it using the approved test-data cleanup process for the environment.

Then run query 4.

Expected result:

```text
REMAINING_DOCS
--------------
0
```

The detector does not perform this deletion automatically.

## Important schema note

The source validation SQL assumes `AI_DEMO.KNOWLEDGE_BASE` exposes `DOCUMENT_ID`, `TITLE`, and `DOCUMENT_TYPE` columns.

The current `langchain-db2` `DB2VS` integration also supports a vector-store representation in which the text and metadata are stored through its vector-store schema. If your local `AI_DEMO.KNOWLEDGE_BASE` was created with the earlier project schema and those named columns are not present, keep the supplied SQL as the source validation contract but adapt the inspection queries to the actual schema rather than changing the Python detector.

The duplicate detector itself reads document metadata returned by `DB2VS` and is deliberately tolerant of common metadata key casing such as `document_id` and `DOCUMENT_ID`.

## What this validation proves

The validation checks are intentionally different from the semantic classifier:

- SQL validation confirms the expected corpus and controlled test-data state.
- Python validation confirms that the Db2 vector search can retrieve candidates and that the configured classification policy is applied to the top candidate.
- The evaluation runner checks the classifier against a small labelled demonstration set.

Together they provide a practical development-time validation path without claiming that a small demo evaluation is sufficient for production threshold calibration.
