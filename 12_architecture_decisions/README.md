# UC12: Architecture Decision Assistant

## Status

> Scope defined and implementation included. This project provides semantic retrieval over Architecture Decision Records (ADRs) stored in IBM Db2.

## Why this use case exists

Engineering organizations make hundreds of architecture decisions over time. Those decisions are often documented in Architecture Decision Records (ADRs), but the information becomes difficult to reuse as the number of decisions grows.

This use case stores Architecture Decision Records in IBM Db2 and provides semantic retrieval over the decision history.

An engineer can ask:

> Have we already decided this?

The system retrieves relevant ADRs and presents the decision together with its rationale and rejected alternatives.

### College project framing

Build a semantic search engine over a structured architecture decision log.

### Enterprise framing

Build an architecture decision assistant that surfaces historical rationale, including context, decision, reason, rejected alternatives, status, and affected system.

The assistant supports architecture review. It does not make architecture decisions automatically.

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| IBM Db2 integration | `DB2VS` |
| Vector operation | `similarity_search()` |
| Data | Architecture Decision Records |
| Retrieval | Semantic search over ADRs |
| Lifecycle | Proposed, accepted, active, superseded, deprecated |
| Filtering | Status and affected system |
| Output | Decision + rationale + rejected alternatives |
| Evaluation | Small labelled ADR retrieval benchmark |

## Core architecture

```text
Engineer asks architecture question
              |
              v
      Natural-language query
              |
              v
        Generate embedding
              |
              v
       LangChain DB2VS search
              |
              v
       ADRs stored in Db2
              |
              v
        Ranked ADR candidates
              |
              v
     Structured decision context
              |
       +------+-------+-------+
       |              |       |
       v              v       v
   Decision        Rationale  Rejected
                              alternatives
              |
              v
       Engineer evaluates
       current applicability
```

## ADR lifecycle

The project recognizes these decision states:

- `PROPOSED`: documented but not yet accepted.
- `ACCEPTED`: approved by the organization.
- `ACTIVE`: currently applicable.
- `SUPERSEDED`: replaced by a newer decision but retained for historical context.
- `DEPRECATED`: no longer recommended.

Current-decision searches should normally prioritize `ACTIVE` and `ACCEPTED`. Historical searches can include all lifecycle states.

## Scope

- Populate `AI_DEMO.ARCHITECTURE_DECISIONS` with an ADR corpus.
- Construct rich embedding text from ADR content.
- Implement `search_adrs(question: str, k: int = 3)`.
- Display title, decision, reason, rejected alternatives, status, affected system, date, and retrieval score.
- Support filtering by status and affected system.
- Demonstrate retrieval of superseded decisions for historical context.
- Provide a small labelled evaluation using Top-1 accuracy and Top-k hit rate.

## Retrieval behavior

```text
search_adrs(question, k=3)
        |
        v
Generate query embedding
        |
        v
DB2VS semantic search
        |
        v
Retrieve candidate ADRs
        |
        v
Apply requested filters
        |
        v
Return structured ADR results
```

The retrieval score is a semantic retrieval signal. It is not a measure of architectural correctness or approval confidence.

## Built-in queries

```text
Have we evaluated event-driven architecture?
What did we decide about authentication mechanisms?
Why did we choose IBM Db2 for vector storage?
```

## Command-line usage

```bash
source .venv/bin/activate
cd 12_architecture_decisions

python main.py
```

Custom query:

```bash
python main.py --query "authentication mechanism for services"
```

Status filter:

```bash
python main.py \
  --query "authentication mechanism for services" \
  --status ACTIVE
```

Affected-system filter:

```bash
python main.py \
  --query "authentication mechanism" \
  --system payments
```

Run evaluation:

```bash
python -m evaluation.eval
```

## Data model expectations

The project expects:

```text
AI_DEMO.ARCHITECTURE_DECISIONS
```

with fields conceptually including:

```text
DOCUMENT_ID
TITLE
CONTENT
STATUS
EFFECTIVE_DATE
EMBEDDING
```

The content should preserve enough ADR information to communicate:

```text
Context
Decision
Reason
Rejected alternatives
Affected system
```

## Enterprise safety boundary

This assistant does not:

- automatically approve an architecture
- automatically reject an architecture
- automatically change architecture standards
- automatically mark an ADR active
- automatically supersede an ADR
- automatically select a technology

Instead:

```text
Architecture question
        |
        v
Semantic retrieval
        |
        v
Historical ADR evidence
        |
        v
Architecture team review
        |
        v
Current architecture decision
```

## Evaluation

Each evaluation case contains a question and expected ADR.

Metrics:

### Top-1 accuracy

```text
correct_top_1_results / total_test_cases
```

### Top-k hit rate

```text
cases_where_expected_adr_is_in_top_k / total_test_cases
```

This is a small demonstration benchmark, not a production architecture-governance assessment.

## Validation

Execute:

```bash
# Use your Db2 client to execute:
validation/validation.sql
```

The validation checks:

1. ADR population.
2. ADR lifecycle status and effective dates.
3. Status distribution.
4. Embedding availability.
5. Current semantic-search candidates.

## Files

```text
12_architecture_decisions/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── db2_store.py
├── sample_data.py
├── ingest.py
├── adr_search.py
├── main.py
├── evaluation/
│   ├── __init__.py
│   ├── cases.py
│   └── eval.py
└── validation/
    ├── validation.sql
    └── VALIDATION.md
```

## Design principles

1. Db2 is the durable architecture knowledge layer.
2. Semantic retrieval supplements ADR governance.
3. Historical decisions remain valuable.
4. Current decisions are distinguishable from historical ones.
5. Rationale is first-class information.
6. Engineers and architecture teams remain responsible for final decisions.

## Enterprise impact

This use case turns architecture documentation from a passive archive into a searchable organizational knowledge system.

New engineers can discover existing decisions faster. Architecture teams can avoid unnecessarily repeating evaluations. When a decision needs to be revisited, historical reasoning and rejected alternatives can be retrieved from Db2.

## UC progression

```text
UC07 Similarity Search + Relevance Score
    "Is this retrieved evidence strong enough?"

        ↓

UC08 MMR Retrieval
    "Can I retrieve sufficiently different evidence?"

        ↓

UC09 Semantic Duplicate Detection
    "Is this new enterprise knowledge already represented?"

        ↓

UC11 Vector-Based Incident Discovery
    "Have we seen a similar operational failure before?"

        ↓

UC12 Architecture Decision Assistant
    "Have we already made an architecture decision about this?"
```

## Key takeaway

IBM Db2 can serve as both the durable storage layer and semantic retrieval layer for organizational architecture knowledge.

The assistant makes previous decisions, rationale, rejected alternatives, and lifecycle status easier to discover without replacing architecture governance.
