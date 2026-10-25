# UC17: Semantic Ticket Routing

## Status

> Scope defined. Code not yet written. This project demonstrates semantic routing from labelled historical tickets stored in IBM Db2.

## Why this use case exists

Enterprise support organizations receive large volumes of tickets that must be routed to the correct team, category, and priority.

Traditional routing often relies on keyword rules that can fail when users describe the same problem using different language.

Historical resolved tickets already contain valuable routing information:

- team
- category
- priority
- product
- resolution
- symptoms

This use case uses IBM Db2 vector search to retrieve similar historical tickets and derive a routing suggestion from their labels.

### College project framing

Build a classification system using nearest-neighbour search over labelled historical ticket data.

### Enterprise framing

Build a semantic ticket routing engine that learns from historical routing patterns stored in IBM Db2.

The system handles natural-language variation without requiring a newly trained classification model.

Adding more correctly labelled historical tickets expands the routing knowledge available to the system.

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| IBM Db2 integration | `DB2VS` |
| Vector operation | `similarity_search_with_score()` |
| Pattern | Weighted k-NN classification |
| Training | No model retraining required |
| Routing signal | Historical labelled tickets |
| Output | Team, category, priority, confidence, similar tickets |
| LLM | Optional and not responsible for routing |
| Evaluation | Labelled routing accuracy and top-k metrics |

## Core architecture

```text
                         New support ticket
                                |
                                v
                         Ticket description
                                |
                                v
                         Generate embedding
                                |
                                v
                    IBM Db2 vector search
                                |
                                v
                  Top-k historical tickets
                                |
              +-----------------+----------------+
              |                 |                |
              v                 v                v
          Ticket A           Ticket B        Ticket C
          Team=IT            Team=IT         Team=Identity
          Category=Auth      Category=Auth   Category=Auth
          Priority=P1        Priority=P2     Priority=P1
              |                 |                |
              +-----------------+----------------+
                                |
                                v
                      Weighted k-NN voting
                                |
                  +-------------+-------------+
                  |             |             |
                  v             v             v
                Team        Category      Priority
                  |             |             |
                  +-------------+-------------+
                                |
                                v
                       Routing suggestion
                                |
                                v
                    Optional confidence gate
```

## Important score handling

The routing algorithm must not assume that the raw score returned by `similarity_search_with_score()` always means higher score equals more similar.

The interpretation depends on the configured vector distance strategy.

For cosine distance:

```text
lower distance = more similar
```

For the cosine-distance configuration used by this project:

```text
normalized_similarity = 1 - cosine_distance
```

Example:

```text
Raw cosine distance:   0.07
Normalized similarity: 0.93
```

The normalized similarity is used as the voting weight, while the raw Db2 score remains available for transparency.

## Weighted k-NN routing

For each candidate label:

```text
weighted_vote(label)
    =
    sum(similarity_weight of matching historical tickets)
```

Example:

```text
Ticket 1: Identity Platform, similarity 0.93
Ticket 2: Identity Platform, similarity 0.81
Ticket 3: Security Engineering, similarity 0.68
```

Therefore:

```text
Identity Platform = 0.93 + 0.81 = 1.74
Security Engineering = 0.68
```

The winning label becomes the routing suggestion.

The same approach can be applied independently to:

- team
- category
- priority

## Routing confidence

The project exposes a routing-confidence heuristic based on the separation between the winning label and the next strongest label.

```text
confidence =
    (winning_weight - second_weight)
    /
    winning_weight
```

This is a routing-confidence heuristic, not a calibrated probability that the routing decision is correct.

A production workflow can use a configurable confidence threshold to determine whether a suggestion is eligible for automated routing or should go to human review.

## Scope

- Populate `AI_DEMO.TICKETS` with a labelled historical ticket corpus.
- Store ticket text, team, category, priority, product, and resolution summary.
- Implement `route_ticket(text: str) -> RoutingSuggestion`.
- Retrieve the top-k historical tickets using Db2 vector search.
- Normalize the retrieval score.
- Perform weighted voting over team, category, and priority.
- Return the routing suggestion, confidence heuristic, and supporting historical tickets.
- Provide a labelled evaluation set.
- Provide Db2 validation queries.

## Built-in test tickets

1. `"OOMKilled pods in production namespace, services crashing"` → Engineering / Kubernetes
2. `"User locked out, cannot set up new authenticator app"` → IT Support / Identity
3. `"Payment failing for European customers, error code 503"` → Banking / Payment Platform

## Command-line usage

```bash
source .venv/bin/activate
cd 17_ticket_routing

python main.py
```

Custom ticket:

```bash
python main.py \
  --ticket "login failure after certificate update"
```

Example output:

```text
Suggested Team: Identity Platform
Suggested Category: Authentication
Suggested Priority: P1

Routing Confidence: 0.XX

Supporting historical tickets:

1. INC-002
   Similarity: 0.93
   Team: Identity Platform
   Category: Authentication
   Priority: P1

2. SUP-001
   Similarity: 0.81
   Team: Identity Platform
   Category: Authentication
   Priority: P2
```

Exact similarity values depend on the embedding model and historical corpus.

## Evaluation

The evaluation set contains:

- ticket text
- expected team
- expected category
- expected priority

Metrics:

### Team accuracy

```text
correct_team_predictions / total_test_tickets
```

### Category accuracy

```text
correct_category_predictions / total_test_tickets
```

### Priority accuracy

```text
correct_priority_predictions / total_test_tickets
```

### Top-k retrieval hit rate

Measures whether at least one historical ticket with the expected routing labels appears among the retrieved candidates.

The evaluation helps distinguish retrieval quality from voting quality.

This is a demonstration benchmark, not a production routing SLA.

## Routing safety boundary

The routing engine produces a routing suggestion. It does not automatically:

- modify production systems
- page an on-call engineer
- change incident severity
- close a ticket
- modify ticket content
- execute remediation commands

A downstream enterprise workflow can decide whether high-confidence suggestions are eligible for automatic assignment.

Low-confidence or ambiguous tickets can be routed to manual triage.

## Data model expectations

The project expects:

```text
AI_DEMO.TICKETS
```

with fields conceptually including:

```text
DOCUMENT_ID
TITLE
CONTENT
DEPARTMENT
DOCUMENT_TYPE
PRIORITY
PRODUCT
RESOLUTION_SUMMARY
EMBEDDING
```

The supplied validation workflow uses:

```text
DEPARTMENT -> routing team
DOCUMENT_TYPE -> category
CONTENT -> ticket text
EMBEDDING -> vector representation
```

## Validation

Run:

```bash
# Execute validation/validation.sql using your Db2 client
```

The validation checks:

1. Ticket history population.
2. Team distribution.
3. Category distribution.
4. Sample ticket metadata.
5. Embedding completeness.

## Files

```text
17_ticket_routing/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── db2_store.py
├── sample_data.py
├── ingest.py
├── router.py
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

1. Historical tickets are the routing knowledge.
2. Db2 remains the enterprise vector store.
3. Retrieval and routing are transparent.
4. Weighted voting is deterministic.
5. Confidence is a heuristic, not a probability.
6. LLMs do not determine routing.
7. Human review remains available.

## Enterprise impact

This use case demonstrates how enterprise support history can become a routing knowledge base.

Traditional routing:

```text
New ticket
    |
    v
Keyword rules
    |
    +--> Match rule
    |
    +--> No match
    |
    v
Manual triage
```

Semantic routing:

```text
New ticket
    |
    v
Semantic search in Db2
    |
    v
Similar historical tickets
    |
    v
Weighted label voting
    |
    +--> Team
    +--> Category
    +--> Priority
    |
    v
Routing suggestion
```

The key enterprise benefit is that routing knowledge is grounded in actual historical cases.

When new correctly labelled tickets are added to the corpus, the retrieval knowledge evolves without retraining a separate classification model.

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

        ↓

UC17 Semantic Ticket Routing
    "Which team, category, and priority should handle this ticket?"
```

## Key takeaway

IBM Db2 can serve as a semantic routing knowledge layer for enterprise support operations.

The core pattern is:

```text
Historical labelled tickets
        |
        v
IBM Db2 vector search
        |
        v
Weighted k-NN voting
        |
        v
Explainable routing suggestion
```

The system uses enterprise history as the source of routing intelligence while keeping the routing logic deterministic, inspectable, and suitable for human review when confidence is low.
