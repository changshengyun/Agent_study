# Grilling — References: Decision Log Format

## Log Template (decision-log.md)

```markdown
# Decision Log — {Topic}

**Date:** {ISO 8601}
**Domain:** {technical | mixed | strategic | creative}
**Nodes resolved:** {N}
**Nodes blocked:** {M}

---

## Q{N} — {Topic}
**Question:** {full question text}
**Answer:** {user's choice + any elaboration}
**Decision:** {consolidated decision}
**Rationale:** {why this decision was taken}
**Branches opened:** {new sub-questions unlocked}
**Branches pruned:** {sub-questions rendered irrelevant}
**Status:** resolved | blocked | revised({from})

---
```

## Blocked Node Format

```markdown
- [ ] Q{N}: {question} — **BLOCKED BY** Q{N} (unresolved)
```

## Anchor Format (Context Distillation)

Ditulis setiap 5 resolved nodes:

```markdown
## Anchor (after Q{N})
Resolved: Q1=A, Q2=C, Q3=B, Q4=A, Q5=D
Blocked: Q7(by Q4), Q9(by Q6)
Active branch: {current tree path}
```

## Revision Format

Ketika user merevisi jawaban (explicit atau auto-detect):

```markdown
## Q{N} — {Topic} ↻
**Revised from:** {old answer}
**New answer:** {new answer}
**Decision:** {revised decision}
**Rationale:** {why revised}
**Status:** revised(Q{N})
```
