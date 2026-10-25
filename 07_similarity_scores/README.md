# UC07 — Similarity Search with Relevance Scores

## Status

Scope defined and implementation included.

## Why this use case exists

Most RAG applications retrieve documents and immediately generate an answer. That makes it difficult for application logic to distinguish strong evidence from weak evidence.

This use case exposes the raw score returned by IBM Db2's LangChain vector store integration and uses that value as an application control signal.

The enterprise pattern is:

```text
User question
      |
      v
DB2VS.similarity_search_with_score()
      |
      v
Db2 vector distance
      |
      +---- strong evidence ----> generate answer
      |
      +---- uncertain evidence -> answer with caveat
      |
      +---- weak evidence ------> do not generate
```

The application therefore has an explicit "I do not have enough evidence" path instead of treating every retrieved document as equally useful.

## Important score interpretation

This example uses `DistanceStrategy.COSINE`.

For Db2's cosine-distance search, the returned score is a distance:

- `0.0` means the query and document are identical in direction.
- Smaller values mean closer semantic distance.
- Larger values mean weaker similarity.

Therefore this example does **not** interpret a larger raw score as higher confidence.

The application converts the distance into three configurable decision tiers:

```text
distance <= HIGH_MAX
    -> HIGH
    -> generate normally

HIGH_MAX < distance <= MEDIUM_MAX
    -> MEDIUM
    -> generate with an evidence caveat

distance > MEDIUM_MAX
    -> LOW
    -> do not generate an answer
```

The default thresholds are deliberately configuration values, not universal truth. They should be calibrated against the organization's corpus and embedding model.

## What it demonstrates

| Capability | Implementation |
|---|---|
| Framework | LangChain |
| IBM integration | `langchain-db2` |
| Db2 vector store | `DB2VS` |
| Search API | `similarity_search_with_score()` |
| Distance metric | Cosine |
| Score interpretation | Db2 cosine distance |
| Application pattern | Score-based routing |
| Strong evidence | Generate answer |
| Medium evidence | Generate with caveat |
| Weak evidence | Return insufficient-evidence response |
| Generation | Ollama Granite |
| Embeddings | Ollama `nomic-embed-text` |
| Validation | Db2 SQL |

## Enterprise scenario

An enterprise knowledge assistant may receive questions outside the knowledge base.

For example:

```text
What is the travel policy for Europe?
```

may retrieve the travel policy with a small cosine distance.

But:

```text
What is our quantum computing product roadmap?
```

may retrieve unrelated documents because a vector store normally returns the nearest available records even when none is actually relevant.

The application should not blindly generate from those unrelated documents.

UC07 introduces an explicit evidence gate between retrieval and generation.

## Scope

This use case:

- Connects LangChain's `DB2VS` directly to `AI_DEMO.KNOWLEDGE_BASE`.
- Uses `similarity_search_with_score(query, k=5)`.
- Displays every returned document and its raw Db2 distance.
- Classifies the top result into HIGH, MEDIUM, or LOW evidence.
- Generates with Ollama Granite for HIGH evidence.
- Generates with an explicit evidence caveat for MEDIUM evidence.
- Does not generate an answer for LOW evidence.
- Shows the closest documents when evidence is insufficient.
- Includes a small evaluation runner.
- Includes Db2 validation SQL.

The existing knowledge base is assumed to have been populated by the earlier enterprise RAG use case.

## Project structure

```text
07_similarity_scores/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── db2_store.py
├── score_router.py
├── answer_generator.py
├── main.py
├── evaluation/
│   ├── __init__.py
│   ├── questions.py
│   └── eval.py
└── validation/
    ├── validation.sql
    └── VALIDATION.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

ollama pull nomic-embed-text
ollama pull granite3.1-dense:8b
```

Copy the environment file:

```bash
cp .env.example .env
```

Set the Db2 and Ollama connection values.

## Direct IBM Db2 package usage

The implementation intentionally uses the public class supplied by the IBM Db2 LangChain integration:

```python
from langchain_db2 import DB2VS
```

and calls:

```python
vector_store.similarity_search_with_score(query, k=5)
```

There is no custom vector store or custom similarity-search implementation in this example.

The current `langchain-db2` documentation describes `DB2VS` as the Db2 vector store and documents `similarity_search_with_score()` as returning the top-k documents together with their scores. It also documents cosine distance as one of the supported distance strategies. citeturn1search0turn1search1

## Run

```bash
python main.py --query "What is the travel policy for Europe?"
```

You can also change the number of retrieved candidates:

```bash
python main.py --query "What is the travel policy for Europe?" --k 5
```

## Example scenarios

### Strong evidence

```bash
python main.py --query "What is the travel policy for Europe?"
```

Expected behavior:

```text
Evidence: HIGH
Action: Generate answer
```

### Medium evidence

```bash
python main.py --query "What are the company's policies for remote work in Asia?"
```

Expected behavior:

```text
Evidence: MEDIUM
Action: Generate answer with evidence caveat
```

### Weak evidence

```bash
python main.py --query "What is the quantum computing product roadmap?"
```

Expected behavior:

```text
Evidence: LOW
Action: Do not generate
```

The exact scores depend on the embedding model, stored documents, and Db2 distance calculation. The examples above describe expected routing behavior, not fixed score values.

## Threshold configuration

The defaults are:

```text
HIGH_MAX_DISTANCE=0.35
MEDIUM_MAX_DISTANCE=0.52
```

These values are starting points only.

Do not interpret them as universal confidence percentages.

For an enterprise deployment, collect representative questions with known relevant and irrelevant documents and calibrate thresholds using the actual corpus and embedding model.

## Evaluation

Run:

```bash
python evaluation/eval.py
```

The evaluator reports:

- Query
- Expected evidence category
- Top retrieved document
- Raw Db2 distance
- Actual evidence category
- Whether routing matched expectation

This is a routing evaluation, not a claim that a small static dataset proves production accuracy.

## Validation

Run:

```text
validation/validation.sql
```

using IBM Db2 Developer Extension.

Read:

```text
validation/VALIDATION.md
```

for the purpose of every query and expected database state.

The validation follows the source SQL's checks for total documents, stored embeddings, travel-policy documents, and null embeddings. fileciteturn0file1L3-L24

## Enterprise impact

The key idea is that vector distance becomes an application decision signal.

This enables patterns such as:

- Do not answer when evidence is too weak.
- Ask the user to clarify an ambiguous question.
- Show retrieved evidence before generating.
- Escalate low-evidence questions to human support.
- Route strong matches to automated generation.
- Log score distributions for later threshold calibration.

This is a foundation for more controlled enterprise RAG systems.

## Limitations

A vector distance is not a calibrated probability of correctness.

A low distance does not prove that the document fully answers the question, and a high distance does not prove that the answer is absent from the knowledge base.

For that reason, the application uses the score as a routing signal rather than calling it a mathematically calibrated confidence percentage.

Later use cases can combine this signal with metadata filters, reranking, lexical search, answer verification, or human review.
