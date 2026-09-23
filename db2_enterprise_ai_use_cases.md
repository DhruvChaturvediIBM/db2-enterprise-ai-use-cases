# IBM Db2 AI Use Cases

## Haystack + LangChain + CrewAI

### Project goal

Build 20 small, high-impact enterprise AI examples on IBM Db2 using the
capabilities already exposed by the current Haystack, LangChain and
CrewAI Db2 integrations.

The objective is not to create 20 variations of a chatbot.

The objective is to demonstrate a progression:

``` text
IBM Db2
  |
  +-- structured enterprise data
  +-- documents / knowledge
  +-- metadata
  +-- native VECTOR data
  +-- vector similarity
  |
  +-------------------------------+
                                  |
                         AI framework layer
                                  |
             +--------------------+--------------------+
             |                    |                    |
          Haystack             LangChain            CrewAI
             |                    |                    |
        pipelines             VectorStore             tools
        retrieval             search/MMR              agents
        reranking             scores                  crews
             |                    |                    |
             +--------------------+--------------------+
                                  |
                         Enterprise AI applications
```

The framework is chosen according to the problem. CrewAI is not used
everywhere.

### Guiding principle

Use the smallest amount of code that demonstrates the largest meaningful
enterprise capability.

Every example should ideally contain:

1.  A realistic enterprise knowledge problem.
2.  A small Db2 dataset.
3.  One or two important Db2/framework capabilities.
4.  A minimal runnable implementation.
5.  SQL that can be independently inspected in IBM Db2.
6.  A clear explanation of why Db2 matters.
7.  A path toward the eventual combined UI.

------------------------------------------------------------------------

# 1. Technology coverage

## Haystack + IBM Db2

Primary Db2 integration:

-   `Db2DocumentStore`
-   `Db2EmbeddingRetriever`

Capabilities to demonstrate:

-   Document persistence
-   Embedding persistence
-   Native Db2 `VECTOR` storage
-   Vector similarity retrieval
-   `top_k`
-   COSINE distance
-   EUCLIDEAN distance
-   MANHATTAN distance
-   Metadata filtering
-   Compound metadata filters
-   Date-aware filtering
-   RAG pipelines
-   Retrieval pipelines
-   Reranking through Haystack pipeline components
-   Agent/tool-oriented retrieval pipelines

Haystack should be the primary framework for examples where the
important idea is a retrieval pipeline.

## LangChain + IBM Db2

Primary Db2 integration:

-   `DB2VS`

Capabilities to demonstrate:

-   `from_texts()`
-   `add_texts()`
-   `similarity_search()`
-   `similarity_search_with_score()`
-   `similarity_search_by_vector()`
-   `similarity_search_by_vector_with_relevance_scores()`
-   `similarity_search_by_vector_returning_embeddings()`
-   `max_marginal_relevance_search()`
-   `max_marginal_relevance_search_by_vector()`
-   `delete()`
-   `get_pks()`
-   `clear_table()`
-   metadata filtering where supported
-   COSINE
-   EUCLIDEAN
-   DOT

LangChain should be the primary framework where the important idea is
vector-store behavior, retrieval strategy, scores, MMR, or
application-level vector logic.

## CrewAI + IBM Db2

Primary integration:

-   `DB2VectorSearchTool`

Capabilities to demonstrate:

-   Semantic vector search as an agent tool
-   `limit`
-   `distance_metric`
-   `max_distance`
-   metadata filtering
-   `return_columns`
-   custom embedding function
-   six Db2 distance metrics exposed by the current tool:
    -   COSINE
    -   EUCLIDEAN
    -   EUCLIDEAN_SQUARED
    -   DOT
    -   HAMMING
    -   MANHATTAN
-   agent access to Db2 knowledge
-   multi-agent workflows

CrewAI should only be used when agent roles or multi-step orchestration
provide real value.

------------------------------------------------------------------------

# 2. Enterprise knowledge model

All examples should use a common enterprise knowledge model so that they
can eventually be combined into one application.

Suggested logical document fields:

``` text
id
content
title
source
document_type
department
business_unit
region
product
classification
effective_date
created_at
updated_at
owner
status
embedding
```

Example document types:

``` text
policy
architecture_decision
runbook
support_article
incident
requirement
product_documentation
contract
procurement_requirement
compliance_rule
release_note
knowledge_article
```

The same knowledge can later power the combined UI.

------------------------------------------------------------------------

# 3. The 20 use cases

## UC01 - Enterprise Knowledge Assistant

### Enterprise problem

Employees need answers across internal policies, technical
documentation, runbooks, product documentation and knowledge articles.

### Knowledge in Db2

``` text
Policies
Technical documentation
Runbooks
FAQs
Architecture documents
Product documentation
```

### Framework

Haystack.

### Core capabilities

-   `Db2DocumentStore`
-   `Db2EmbeddingRetriever`
-   embedding
-   vector search
-   `top_k`
-   prompt + LLM

### Flow

``` text
Question
  |
Embedding
  |
Db2EmbeddingRetriever
  |
Db2 VECTOR search
  |
Relevant documents
  |
Prompt
  |
LLM
  |
Grounded answer
```

### Minimal-code objective

Keep the implementation close to the canonical Haystack pipeline:

``` python
document_store = Db2DocumentStore(...)
retriever = Db2EmbeddingRetriever(document_store=document_store, top_k=5)

# embed documents
# write documents
# embed query
# retrieve
# generate
```

### Enterprise impact

Demonstrates the basic path from existing enterprise knowledge to a
grounded AI assistant without introducing a separate vector database.

------------------------------------------------------------------------

# UC02 - Policy Assistant with Metadata Filtering

### Enterprise problem

Policies can be similar across departments, countries and business
units. Semantic similarity alone is not enough.

### Knowledge in Db2

``` text
department
region
policy_type
effective_date
status
```

### Framework

Haystack.

### Core capabilities

-   vector retrieval
-   metadata filtering
-   compound filters
-   date-aware filtering

### Example question

> What is the current travel reimbursement policy for the European
> finance organization?

### Retrieval logic

``` text
semantic similarity
        +
department = finance
        +
region = Europe
        +
status = active
```

### Enterprise impact

Shows the combination of relational/structured constraints with semantic
retrieval.

This is one of the most important enterprise patterns in the repository.

------------------------------------------------------------------------

# UC03 - Technical Documentation Semantic Search

### Enterprise problem

Developers often need to find relevant documentation rather than
generate a long answer.

### Knowledge in Db2

``` text
API documentation
Architecture docs
Developer guides
Troubleshooting guides
Release notes
```

### Framework

Haystack.

### Core capabilities

-   `Db2DocumentStore`
-   `Db2EmbeddingRetriever`
-   vector retrieval
-   `top_k`

### Output

Return the most relevant documents with:

``` text
title
source
similarity/distance
content snippet
```

No agent is required.

### Enterprise impact

Demonstrates Db2 as a semantic enterprise search layer rather than only
as a RAG backend.

------------------------------------------------------------------------

# UC04 - Date-Aware Compliance Knowledge Search

### Enterprise problem

Enterprise policies and compliance documents change over time. A
semantically relevant old policy can be more dangerous than no result.

### Knowledge in Db2

``` text
policy
effective_date
expiry_date
region
regulation
status
```

### Framework

Haystack.

### Core capabilities

-   vector retrieval
-   metadata/date filtering
-   enterprise policy grounding

### Example

> What is the currently effective policy for retaining customer
> transaction records?

### Flow

``` text
Question
  |
Db2 metadata constraints
  |
Vector retrieval
  |
Only currently applicable documents
  |
LLM
```

### Enterprise impact

Demonstrates that enterprise RAG needs temporal and business
constraints.

------------------------------------------------------------------------

# UC05 - Retrieval + Reranking for High-Precision Knowledge Search

### Enterprise problem

Vector search is excellent at finding candidates, but the first ranking
may not always place the most useful passages first.

### Framework

Haystack.

### Core capabilities

-   Db2 vector retrieval
-   larger candidate set
-   Haystack reranking component
-   final top-k context

### Flow

``` text
Question
  |
Db2 vector retrieval
  |
Top 15-20 candidates
  |
Reranker
  |
Top 3-5
  |
LLM
```

### Important distinction

Reranking is an application-layer capability.

Db2 performs the vector retrieval.

Haystack performs the subsequent pipeline orchestration and ranking
stage.

### Enterprise impact

Demonstrates a practical retrieval-quality architecture without
replacing Db2.

------------------------------------------------------------------------

# UC06 - Local Ollama Reranking for Sensitive Enterprise Data

### Enterprise problem

Some enterprises may want to improve retrieval quality while keeping
retrieved content on local infrastructure.

### Framework

Haystack + local Ollama.

### Core capabilities

-   Db2 vector retrieval
-   local model
-   reranking
-   RAG

### Flow

``` text
Question
  |
Db2
  |
Top 10-20 candidates
  |
Local Ollama model
  |
Reranked candidates
  |
LLM
```

### Important scope

Use Ollama only for this small number of examples.

Do not make Ollama a dependency of every project.

### Enterprise impact

Demonstrates how a local ranking stage can be added without changing the
underlying Db2 retrieval layer.

------------------------------------------------------------------------

# UC07 - Similarity Search with Relevance Scores

### Enterprise problem

Applications often need to decide whether retrieved evidence is strong
enough before generating an answer.

### Framework

LangChain.

### Core API

``` python
similarity_search_with_score()
```

### Application logic

``` text
high relevance
    |
    +--> answer

medium relevance
    |
    +--> retrieve more / ask clarification

low relevance
    |
    +--> insufficient evidence
```

### Enterprise impact

Shows that vector search scores can become application-control signals
instead of being hidden inside a RAG pipeline.

------------------------------------------------------------------------

# UC08 - Diverse Enterprise Retrieval with MMR

### Enterprise problem

A similarity search can return multiple documents that say almost the
same thing.

### Framework

LangChain.

### Core API

``` python
max_marginal_relevance_search()
```

### Example

Question:

> What are the main considerations when modernizing this enterprise
> application?

Desired context:

``` text
Architecture
Database
Security
Deployment
Observability
Rollback
```

rather than five nearly identical architecture documents.

### Enterprise impact

Demonstrates diversity-aware retrieval for broad enterprise questions.

------------------------------------------------------------------------

# UC09 - Semantic Duplicate Knowledge Detection

### Enterprise problem

Large enterprises accumulate duplicate or near-duplicate knowledge
articles, requirements and support documents.

### Framework

LangChain.

### Core capabilities

-   `similarity_search()`
-   similarity scores
-   metadata
-   application-level thresholding

### Flow

``` text
New document
  |
Embedding
  |
Db2 similarity search
  |
Candidate duplicates
  |
Similarity threshold
  |
Duplicate / related / new
```

### Enterprise impact

The database is being used to maintain knowledge quality, not just
answer questions.

------------------------------------------------------------------------

# UC10 - Semantic Recommendation Engine

### Enterprise problem

Recommend related enterprise artifacts based on meaning rather than
exact keywords.

### Framework

LangChain.

### Examples

``` text
incident -> similar incidents
requirement -> related requirements
document -> related documents
support ticket -> similar tickets
product -> related products
```

### Core capabilities

-   `similarity_search()`
-   `similarity_search_by_vector()`
-   relevance scores

### Enterprise impact

Demonstrates vector search as a reusable application primitive.

------------------------------------------------------------------------

# UC11 - Vector-Based Incident Discovery

### Enterprise problem

When a new production incident occurs, engineers need to discover
whether a similar incident has happened before.

### Framework

LangChain.

### Knowledge in Db2

``` text
incident
symptoms
service
root_cause
resolution
timestamp
severity
```

### Flow

``` text
New incident
   |
Embedding
   |
Db2 vector search
   |
Historical incidents
   |
Similar incidents
   |
Resolution context
```

### Enterprise impact

Turns historical operational knowledge into reusable engineering memory.

------------------------------------------------------------------------

# UC12 - Architecture Decision Assistant

### Enterprise problem

Engineering organizations make architecture decisions and later forget
why they were made.

### Knowledge in Db2

``` text
ADR
decision
context
alternatives
reason
status
affected_system
```

### Framework

LangChain or Haystack.

Recommended implementation:

LangChain for direct vector retrieval.

### Example

> Have we already evaluated event-driven processing for this subsystem?

### Output

``` text
ADR-031
Decision: ...
Reason: ...
Alternatives rejected: ...
Status: ...
```

### Enterprise impact

Connects semantic retrieval with durable architectural knowledge.

------------------------------------------------------------------------

# UC13 - Single-Agent Enterprise Research Assistant

### Enterprise problem

A developer or analyst needs an agent that can search enterprise
knowledge before responding.

### Framework

CrewAI.

### Core capability

`DB2VectorSearchTool`

### Flow

``` text
User
 |
CrewAI Agent
 |
DB2VectorSearchTool
 |
Db2 vector search
 |
Structured results
 |
Agent reasoning
 |
Answer
```

### Important design choice

CrewAI is used because an agent needs to decide when to use the Db2
search tool.

A normal RAG pipeline would be simpler if tool selection is unnecessary.

### Enterprise impact

Demonstrates the transition from deterministic retrieval to tool-using
AI.

------------------------------------------------------------------------

# UC14 - Multi-Agent Incident Investigation Crew

### Enterprise problem

Incident investigation involves multiple specialist activities.

### Framework

CrewAI.

### Agents

``` text
Incident Investigator
Historical Incident Analyst
Runbook Analyst
Root Cause Analyst
Reviewer
```

### Shared enterprise knowledge

Db2 stores:

``` text
incidents
runbooks
architecture docs
known issues
postmortems
```

### Flow

``` text
Incident
   |
Investigator
   |
Db2 search
   |
+--------------------+
|                    |
Historical        Runbook
Analyst           Analyst
|                    |
+---------+----------+
          |
    Root Cause Agent
          |
       Reviewer
```

### Enterprise impact

Shows where multi-agent orchestration actually provides value.

------------------------------------------------------------------------

# UC15 - Procurement / RFP Analysis Crew

### Enterprise problem

Procurement teams need to compare supplier proposals against enterprise
requirements and policies.

### Framework

CrewAI.

### Agents

``` text
Requirements Analyst
Policy Analyst
Compliance Analyst
Risk Analyst
Reviewer
```

### Db2 knowledge

``` text
procurement policies
supplier requirements
historical contracts
compliance rules
risk policies
```

### Enterprise impact

Demonstrates agents operating over controlled enterprise knowledge
instead of relying only on model knowledge.

------------------------------------------------------------------------

# UC16 - Enterprise Compliance Investigation Crew

### Enterprise problem

A compliance case may require searching multiple policy and regulatory
knowledge areas before a reviewer can make a decision.

### Framework

CrewAI.

### Agents

``` text
Case Analyst
Evidence Researcher
Policy Analyst
Compliance Analyst
Reviewer
```

### Db2 knowledge

``` text
policies
controls
regulations
historical cases
internal procedures
```

### Important design

The AI should produce evidence and citations/references to Db2 records.

It should not be presented as the final compliance authority.

### Enterprise impact

Shows a human-reviewable agentic workflow grounded in enterprise
knowledge.

------------------------------------------------------------------------

# UC17 - Semantic Ticket Routing

### Enterprise problem

Support tickets are often routed using keywords or manually assigned
categories.

### Framework

LangChain.

### Knowledge

Historical tickets:

``` text
ticket
team
category
resolution
priority
product
```

### Flow

``` text
New ticket
   |
Embedding
   |
Db2 similar-ticket search
   |
Historical routing patterns
   |
Suggested team/category
```

### Enterprise impact

Uses enterprise history to improve operational routing.

No agent is necessary.

------------------------------------------------------------------------

# UC18 - Enterprise Operational Memory

### Enterprise problem

Organizations repeatedly encounter the same operational problems but
fail to reuse previous resolutions.

### Framework

Haystack or LangChain for retrieval.

Optional connection to Mem0 later.

### Knowledge in Db2

``` text
incident
symptom
resolution
environment
command
service
timestamp
```

### Flow

``` text
Resolved incident
      |
Embedding
      |
Db2
      |
Future incident
      |
Similarity search
      |
Previous resolution
```

### Enterprise impact

Demonstrates Db2 as long-lived operational memory.

This can later connect to the separate Mem0 + Db2 work.

------------------------------------------------------------------------

# UC19 - Semantic Change Impact Discovery

### Enterprise problem

A proposed architectural change may affect many documents and decisions
that are not explicitly linked.

### Framework

Haystack or LangChain.

### Knowledge

Search across:

``` text
requirements
ADRs
architecture docs
runbooks
incidents
support articles
release notes
```

### Example

> We are replacing the authentication mechanism. What enterprise
> knowledge may be affected?

### Flow

``` text
Change description
       |
Embedding
       |
Db2 semantic neighborhood
       |
Potentially affected artifacts
       |
LLM summary
```

### Enterprise impact

Demonstrates semantic discovery beyond question answering.

------------------------------------------------------------------------

# UC20 - Enterprise Knowledge Maintenance Assistant

### Enterprise problem

AI knowledge bases degrade because documents become duplicated, outdated
or inconsistent.

### Framework

LangChain or Haystack.

### Capabilities

-   similarity search
-   scores
-   metadata
-   deletion/update lifecycle
-   optional LLM classification
-   human approval

### Flow

``` text
Knowledge base
     |
Find similar documents
     |
Find outdated/duplicate candidates
     |
LLM classification
     |
Human approval
     |
Update/delete
```

### Relevant LangChain APIs

``` python
similarity_search()
similarity_search_with_score()
get_pks()
delete()
clear_table()
```

### Enterprise impact

Closes the loop: Db2 is not merely where AI reads knowledge; AI can help
maintain the knowledge layer.

------------------------------------------------------------------------

# 4. Capability coverage matrix

  Capability                         Primary example
  ---------------------------------- ----------------------------
  Db2DocumentStore                   UC01
  Db2EmbeddingRetriever              UC01
  Vector storage                     UC01
  COSINE retrieval                   UC01
  EUCLIDEAN retrieval                UC03
  MANHATTAN retrieval                UC04
  Metadata filtering                 UC02
  Compound metadata filtering        UC02
  Date filtering                     UC04
  Haystack retrieval pipeline        UC01
  Haystack reranking                 UC05
  Local Ollama reranking             UC06
  LangChain DB2VS                    UC07
  `similarity_search()`              UC07
  `similarity_search_with_score()`   UC07
  `similarity_search_by_vector()`    UC10
  vector + relevance scores          UC07
  MMR                                UC08
  MMR with metadata                  UC08
  duplicate detection                UC09
  recommendation                     UC10
  semantic incident discovery        UC11
  CrewAI Db2 search tool             UC13
  `limit`                            UC13
  `max_distance`                     UC13
  `return_columns`                   UC13
  custom embedding function          UC13 / future variant
  six Db2 distance metrics           UC13 / technical benchmark
  single-agent retrieval             UC13
  multi-agent workflow               UC14
  enterprise compliance workflow     UC16
  knowledge lifecycle                UC20
  operational memory                 UC18

------------------------------------------------------------------------

# 5. Minimal-code strategy

The examples should deliberately avoid unnecessary application
infrastructure.

Do not build:

-   custom web servers for every example
-   separate databases for every example
-   custom vector-search SQL when the package already exposes the
    capability
-   complex agent architectures when a retriever is enough
-   authentication systems inside every demo
-   duplicated embedding utilities
-   duplicated Db2 connection code

Instead:

``` text
common/
    config.py
    db2.py
    embeddings.py
    sample_data.py
    evaluation.py
```

Each use case should ideally contain:

``` text
01_enterprise_rag/
    README.md
    app.py
```

or, for very small demonstrations:

``` text
01_enterprise_rag.py
```

The goal is that a developer can understand the complete example in
minutes.

------------------------------------------------------------------------

# 6. Shared Db2 environment

Testing environment:

``` text
IBM Db2 on IBM FyRe
+
IBM VPN
+
IBM Db2 credentials
+
VS Code
+
IBM Db2 Developer Extension
```

The Db2 Developer Extension will be used as an independent validation
layer.

The application writes/searches through the Python framework.

The developer extension is used to inspect the actual database state
through SQL.

This is valuable because the examples can demonstrate both:

``` text
AI framework view
        |
        v
IBM Db2
        |
        v
SQL verification
```

------------------------------------------------------------------------

# 7. SQL validation philosophy

Every example should have a small `validation.sql`.

Examples:

``` sql
SELECT COUNT(*)
FROM AI_DOCUMENTS;
```

``` sql
SELECT ID, TITLE, CATEGORY
FROM AI_DOCUMENTS
FETCH FIRST 10 ROWS ONLY;
```

For vector-enabled tables, inspect the actual vector column and table
definition through Db2 catalog/metadata queries appropriate to the
target Db2 environment.

For metadata examples:

``` sql
SELECT ID, TITLE, REGION, DEPARTMENT, EFFECTIVE_DATE
FROM AI_DOCUMENTS
WHERE REGION = 'EUROPE'
  AND DEPARTMENT = 'FINANCE';
```

The exact vector-distance SQL used for deeper validation should be kept
alongside the relevant example rather than duplicated everywhere.

The important principle is:

> Python proves the integration works. SQL proves what actually exists
> in Db2.

------------------------------------------------------------------------

# 8. Common test dataset

Do not create 20 unrelated toy datasets.

Create one realistic enterprise knowledge corpus.

Suggested domains:

``` text
Finance
Banking
Insurance
Healthcare operations
Retail
Technology
Customer support
Procurement
Compliance
Engineering
```

Recommended document classes:

``` text
50 policies
50 technical documents
30 architecture decisions
30 support articles
30 incidents
20 runbooks
20 requirements
20 release notes
20 procurement documents
20 compliance documents
```

The first implementation does not need hundreds of documents. A smaller
curated dataset is enough.

The key is that the metadata and relationships are realistic.

------------------------------------------------------------------------

# 9. Common metadata

Every document should not necessarily populate every field, but the
common schema should support:

``` text
document_id
title
content
document_type
department
business_unit
region
product
classification
status
effective_date
owner
source
created_at
updated_at
```

This allows multiple examples to reuse the same knowledge corpus.

------------------------------------------------------------------------

# 10. Evaluation

Every example should have a tiny evaluation mechanism.

Do not start with a huge benchmark framework.

For retrieval examples:

``` text
query
expected document IDs
retrieved document IDs
top-k
```

Measure simple retrieval metrics where meaningful:

``` text
Hit@K
Recall@K
MRR
```

For RAG:

``` text
retrieved evidence
answer
grounding check
```

For reranking:

``` text
before reranking
after reranking
```

For agent examples:

``` text
task completed
tool calls
retrieved evidence
final output
```

The objective is reproducibility, not benchmark theatre.

------------------------------------------------------------------------

# 11. Combined application: later phase

After the 20 standalone examples work independently, build one combined
enterprise AI UI.

The UI should not be 20 separate buttons.

It should expose enterprise capabilities through one application.

Conceptually:

``` text
                         Enterprise AI Hub
                                |
        +-----------------------+-----------------------+
        |                       |                       |
    Ask Knowledge          Investigate             Discover
        |                       |                       |
     RAG/Search             Incidents              Similarity
        |                       |                       |
        +-----------------------+-----------------------+
                                |
                         IBM Db2 Knowledge
                                |
        +-----------------------+-----------------------+
        |                       |                       |
     Haystack              LangChain                CrewAI
        |                       |                       |
 Retrieval/Rerank          Search/MMR             Agents/Crews
```

Potential UI sections:

``` text
Knowledge
    Ask
    Search
    Related documents

Operations
    Incident investigation
    Similar incidents
    Runbooks

Engineering
    Architecture decisions
    Change impact
    Documentation search

Governance
    Policies
    Compliance
    Procurement

Knowledge Health
    Duplicate documents
    Outdated knowledge
    Related content
```

The user should not need to know which framework is being used.

The backend chooses the appropriate implementation.

------------------------------------------------------------------------

# 12. Combined UI architecture

The final application can use a routing layer:

``` text
User
 |
 v
Application Router
 |
 +----> Knowledge Q&A --------> Haystack
 |
 +----> Semantic Search -------> LangChain
 |
 +----> MMR Search ------------> LangChain
 |
 +----> Reranked Search -------> Haystack + Reranker
 |
 +----> Incident Investigation -> CrewAI
 |
 +----> Compliance ------------> CrewAI
 |
 +----> Procurement -----------> CrewAI
 |
 +----> Duplicate Detection ---> LangChain
 |
 +----> Change Impact ---------> Haystack/LangChain
 |
 +----> Knowledge Maintenance -> LangChain/Haystack
                                      |
                                      v
                                  IBM Db2
```

The framework becomes an implementation detail.

IBM Db2 becomes the persistent enterprise knowledge layer.

------------------------------------------------------------------------

# 13. Repository structure

Initial repository:

``` text
db2-enterprise-ai-use-cases/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .env.example
│
├── common/
│   ├── db2.py
│   ├── embeddings.py
│   ├── config.py
│   ├── sample_data.py
│   └── evaluation.py
│
├── data/
│   ├── policies/
│   ├── incidents/
│   ├── architecture/
│   ├── support/
│   ├── procurement/
│   └── compliance/
│
├── 01_enterprise_knowledge_rag/
├── 02_policy_metadata_filtering/
├── 03_technical_document_search/
├── 04_date_aware_compliance/
├── 05_reranked_search/
├── 06_ollama_local_reranking/
├── 07_similarity_scores/
├── 08_mmr_retrieval/
├── 09_duplicate_detection/
├── 10_semantic_recommendation/
├── 11_incident_discovery/
├── 12_architecture_decisions/
├── 13_crewai_research_agent/
├── 14_incident_investigation_crew/
├── 15_procurement_crew/
├── 16_compliance_crew/
├── 17_ticket_routing/
├── 18_operational_memory/
├── 19_change_impact/
└── 20_knowledge_maintenance/
│
└── combined-ui/
    ├── README.md
    └── ...
```

------------------------------------------------------------------------

# 14. Development order

Do not build all 20 sequentially.

Build in capability waves.

## Wave 1 - Foundation

Build:

``` text
UC01
UC02
UC03
```

Goal:

``` text
Db2 connection
    +
table
    +
documents
    +
embeddings
    +
vector retrieval
```

## Wave 2 - Retrieval quality

Build:

``` text
UC04
UC05
UC06
UC07
UC08
```

Goal:

``` text
filters
scores
reranking
local reranking
MMR
```

## Wave 3 - Vector applications

Build:

``` text
UC09
UC10
UC11
UC12
```

Goal:

Demonstrate that Db2 vector search is useful beyond RAG.

## Wave 4 - Agents

Build:

``` text
UC13
UC14
UC15
UC16
```

Goal:

Demonstrate where CrewAI adds value.

## Wave 5 - Enterprise intelligence

Build:

``` text
UC17
UC18
UC19
UC20
```

Goal:

Move from search/answering into enterprise knowledge operations.

## Wave 6 - Combined UI

Only after the standalone examples are stable.

------------------------------------------------------------------------

# 15. Definition of done for each use case

Every example is complete when:

``` text
[ ] Runs against IBM Db2 on IBM FyRe
[ ] Uses real Db2 credentials through environment variables
[ ] Does not contain credentials in source
[ ] Uses the intended framework capability
[ ] Creates/uses the required Db2 table
[ ] Can be independently inspected using SQL
[ ] Has a small README
[ ] Has a clear enterprise scenario
[ ] Has sample input
[ ] Has expected output characteristics
[ ] Has at least one validation SQL query
[ ] Has minimal code
[ ] Can be reused by the future combined UI
```

------------------------------------------------------------------------

# 16. Security and environment

Use environment variables:

``` text
DB2_HOST
DB2_PORT
DB2_DATABASE
DB2_USERNAME
DB2_PASSWORD
DB2_SSL
```

Never commit:

``` text
passwords
connection strings
VPN configuration
API keys
embedding API keys
LLM API keys
```

Use `.env.example`, not `.env`.

The repository should assume that IBM FyRe and the IBM VPN provide the
private connectivity layer.

------------------------------------------------------------------------

# 17. What the LinkedIn series should demonstrate

Each post should be tied to one capability rather than simply saying:

> I built another RAG application.

Example:

### Post

"Can IBM Db2 handle enterprise RAG?"

Show:

``` text
20 lines of Python
        |
        v
IBM Db2
        |
        v
grounded answer
```

Next:

"Vector search is not enough for enterprise policies."

Show metadata filtering.

Next:

"Can we improve Db2 retrieval without replacing Db2?"

Show reranking.

Next:

"Do we actually need an agent?"

Show a LangChain retrieval example where an agent would be unnecessary.

Next:

"When does an agent become useful?"

Show CrewAI incident investigation.

The narrative becomes:

``` text
Database
   ↓
Retrieval
   ↓
Filtering
   ↓
Scoring
   ↓
Reranking
   ↓
RAG
   ↓
Tools
   ↓
Agents
   ↓
Enterprise AI application
```

------------------------------------------------------------------------

# 18. Core thesis

The project should ultimately prove one simple idea:

> Developers do not need to choose between enterprise databases and
> modern AI application frameworks.

IBM Db2 can remain the enterprise data and knowledge layer while
Haystack, LangChain and CrewAI provide different application
abstractions on top of it.

The examples should make that progression visible with as little code as
possible.

``` text
                    IBM Db2
                       |
        +--------------+--------------+
        |              |              |
     Haystack       LangChain       CrewAI
        |              |              |
     Retrieve        Search          Agents
     Filter          Score           Tools
     Rerank          MMR             Crews
        |              |              |
        +--------------+--------------+
                       |
              Enterprise AI
                       |
                 Combined UI
```

This repository is therefore not a collection of demos.

It is a capability map showing how an enterprise developer can
progressively build AI applications around an existing IBM Db2
environment.
