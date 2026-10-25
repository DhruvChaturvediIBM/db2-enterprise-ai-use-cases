# UC08 - Diverse Enterprise Retrieval with MMR

## Status

Scope defined and implementation included.

## Why this use case exists

For broad enterprise questions, ordinary similarity search can return several documents that are individually relevant but cover the same perspective.

Maximal Marginal Relevance (MMR) balances relevance to the query with diversity among selected documents. This makes it useful when an application needs several different perspectives rather than five variations of the same document.

The enterprise pattern demonstrated here is a modernisation and architecture-review assistant. A broad question can benefit from architecture, security, operations, incident-management, compliance, and procurement perspectives.

## Enterprise framing

Instead of asking only:

> Which documents are most similar to my question?

the application can ask:

> Which relevant documents give me the broadest useful coverage of this question?

MMR does not guarantee that a result set is better. It provides a different retrieval objective that can be useful for broad questions.

## What it demonstrates

| Capability | Implementation |
|---|---|
| Framework | LangChain |
| IBM integration | `langchain-db2` |
| Db2 vector store | `DB2VS` |
| Baseline retrieval | `similarity_search()` |
| Diverse retrieval | `max_marginal_relevance_search()` |
| MMR parameter | `lambda_mult` |
| Candidate pool | `fetch_k` |
| Comparison | Similarity vs MMR |
| Evaluation | Document-type and department diversity |
| Database validation | Db2 SQL |

The IBM `langchain-db2` package provides the Db2 database vector-store integration for LangChain. The implementation uses its public `DB2VS` class directly rather than creating a custom vector store.

## How MMR works in this example

```python
vector_store.max_marginal_relevance_search(
    query,
    k=5,
    fetch_k=20,
    lambda_mult=0.5,
)
```

`fetch_k` controls the candidate pool considered before MMR selects the final `k` documents. `lambda_mult` controls the relevance-versus-diversity tradeoff: values near `0` favor diversity and values near `1` favor similarity.

Defaults in this example:

```text
k = 5
fetch_k = 20
lambda_mult = 0.5
```

These are demonstration defaults, not universal production settings.

## Lambda tradeoff

```text
lambda_mult = 0.1
    Strong diversity preference

lambda_mult = 0.5
    Balanced starting point

lambda_mult = 0.9
    Stronger similarity preference
```

Actual result composition depends on the embedding model and corpus.

## Similarity vs MMR

For a broad query such as:

```text
What should we consider when modernising our payment platform?
```

ordinary similarity search may return several closely related architecture documents.

MMR may instead select documents covering different enterprise dimensions, for example:

```text
Architecture
Security
Operations
Incident management
Vendor/procurement
```

The application prints both result sets so the difference can be inspected directly.

## Scope

This use case:

- Connects `DB2VS` to `AI_DEMO.KNOWLEDGE_BASE`.
- Runs normal similarity search.
- Runs MMR search.
- Uses the same query and `k` for both retrieval methods.
- Allows `fetch_k` to be configured.
- Allows `lambda_mult` to be configured from the command line.
- Prints document metadata for both result sets.
- Measures unique document types.
- Measures unique departments.
- Measures document-ID overlap.
- Provides an evaluation runner.
- Provides Db2 validation SQL.
- Provides a separate validation guide.

## Project structure

```text
08_mmr_retrieval/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── db2_store.py
├── retrieval.py
├── diversity.py
├── main.py
│
├── evaluation/
│   ├── __init__.py
│   ├── questions.py
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

Configure the Db2 connection values. The knowledge base should already contain a sufficiently diverse enterprise corpus.

## Direct IBM Db2 package usage

The implementation intentionally uses:

```python
from langchain_db2 import DB2VS
```

and directly calls:

```python
vector_store.similarity_search(...)
vector_store.max_marginal_relevance_search(...)
```

There is no locally implemented vector search or MMR algorithm.

## Run the comparison

```bash
python main.py --query "What should we consider when modernising our payment platform?" --compare
```

The output contains both result sets and their diversity statistics.

## Explore lambda_mult

```bash
python main.py --query "What should we consider when modernising our payment platform?" --lambda 0.1
python main.py --query "What should we consider when modernising our payment platform?" --lambda 0.5
python main.py --query "What should we consider when modernising our payment platform?" --lambda 0.9
```

## Explore fetch_k

```bash
python main.py --query "What should we consider when modernising our payment platform?" --fetch-k 20
```

`fetch_k` controls how many candidate documents are considered before MMR selects the final `k`.

## Example broad enterprise questions

```text
What should we consider when modernising our application platform?
What enterprise knowledge do I need before onboarding a new vendor?
What are the major considerations for modernising our payment platform?
What should an organization review before changing a production data platform?
What enterprise knowledge should be reviewed before changing a critical workload?
```

For narrow factual questions, ordinary similarity retrieval may remain more appropriate.

## Diversity metrics

The example reports:

- Unique document types
- Unique departments
- Diversity ratio by type
- Diversity ratio by department
- Document overlap between similarity and MMR

For example, 4 unique document types among 5 returned documents gives a type diversity ratio of `0.80`.

These are diagnostic measures, not universal retrieval quality scores.

## Evaluation

Run:

```bash
python evaluation/eval.py
```

The evaluator compares similarity and MMR for predefined broad enterprise questions.

It reports query, document IDs, document-type diversity, department diversity, result overlap, and the configured `lambda_mult`.

The evaluation intentionally does not declare a universal winner.

## Validation

Run `validation/validation.sql` using IBM Db2 Developer Extension.

Read `validation/VALIDATION.md` for the purpose of each query.

The validation checks:

- Document-type distribution
- Department distribution
- Corpus size
- Sample document diversity

The supplied validation SQL identifies at least four document types and a corpus of at least 20 documents as useful prerequisites for the demonstration.

## Enterprise impact

MMR is useful when a broad enterprise question requires multiple perspectives.

A modernization review may need to consider architecture, security, operations, reliability, compliance, and vendors. Returning five architecture documents does not necessarily provide that breadth.

MMR provides an application-level retrieval strategy for balancing query relevance with diversity.

## Limitations

More diverse retrieval is not automatically better retrieval.

A document can be different from the other results and still be irrelevant. Likewise, duplicate-looking documents may all be important for a narrow factual question.

This example therefore compares retrieval strategies rather than declaring MMR universally superior.

Later use cases can combine MMR with metadata filtering, score thresholds, reranking, hybrid search, answer verification, and enterprise access controls.
