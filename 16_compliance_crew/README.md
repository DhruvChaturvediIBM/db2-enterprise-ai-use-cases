# UC16 — Enterprise Compliance Investigation Crew

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Compliance investigations require searching across multiple policy and regulatory knowledge areas before a reviewer can make a decision. A single RAG call is insufficient — the investigation needs to correlate policies, controls, regulations, and historical cases. This use case shows a CrewAI crew that assists compliance reviewers by surfacing all relevant evidence, with full citations to Db2 records.

**College project framing:** Build a multi-agent system for evidence gathering and synthesis in a compliance context.  
**Enterprise framing:** A compliance assistant crew that, given a case description, produces a human-reviewable evidence report grounded in enterprise policy and regulatory knowledge — explicitly not the final compliance authority, but a reliable evidence surfacing tool.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | CrewAI |
| Agents | 5 specialised compliance roles |
| Db2 knowledge | policies, controls, regulations, historical cases, internal procedures |
| LLM | Ollama `granite3.1-dense:8b` |
| Key design | AI produces evidence + citations; human makes the final decision |

### Agents

| Agent | Db2 Knowledge Used |
|---|---|
| Case Analyst | ALL types — scopes the case |
| Evidence Researcher | historical compliance cases |
| Policy Analyst | internal policies, controls |
| Compliance Analyst | external regulations (GDPR, etc.) |
| Reviewer | synthesises; flags unresolved gaps |

### Important design principle

> The AI produces evidence and Db2 record citations.  
> It does NOT make the final compliance ruling.  
> The output is a human-reviewable evidence dossier, not an automated decision.

---

## Scope

- Input: a short compliance case description (e.g., "Customer data accessed by unauthorised personnel in the EMEA region")
- Each agent searches its Db2 scope for relevant evidence
- Output: structured dossier with sections:
  - Case Summary
  - Relevant Policies (with Db2 IDs)
  - Applicable Regulations
  - Similar Historical Cases
  - Evidence Gaps (items that require further human investigation)
  - Recommended Next Steps
- All citations include document_id so they can be independently verified in Db2

---

## How to try it (once code is written)

```bash
ollama serve &
source .venv/bin/activate
cd 16_compliance_crew
python main.py
```

Built-in test case:
```
"A customer data access request was fulfilled 45 days after submission. 
The customer is in the EU. The standard SLA is 30 days."
```

Expected: surfaces COMP-001 (GDPR 30-day SLA), POL-003 (data retention), POL-004 (access control)

---

## How to test it

```bash
python main.py
# Expected dossier sections:
#   Policy: GDPR Article 12 — Access request SLA breach (30 days) → COMP-001
#   Policy: Access Control Policy — who approved the delay? → POL-004
#   Historical: Any similar GDPR SLA breach cases? → (none in sample corpus — gap flagged)
#   Recommendation: Notify DPO, document justification for delay
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm compliance and policy documents are loaded
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE, CLASSIFICATION
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('compliance', 'policy')
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;
```

---

## Files (to be created)

```
16_compliance_crew/
├── README.md
├── main.py           ← runs compliance investigation with sample case
├── agents.py         ← 5 compliance agent definitions
├── tasks.py          ← task chain with evidence gathering and synthesis
├── tools.py          ← scoped Db2 search tools
├── crew.py
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates a human-reviewable agentic workflow grounded in enterprise knowledge — the pattern that makes AI usable in regulated industries. By separating evidence surfacing (AI) from compliance ruling (human), this example respects both the value of AI assistance and the regulatory requirement for human accountability.
