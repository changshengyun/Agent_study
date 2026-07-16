---
name: grilling
description: Universal deep-dive interview meta-skill. Explores any domain through adaptive decision-tree traversal, resolving dependencies one question at a time. Produces a decision log + structured final document. Trigger on "grill me", complex trade-off decisions, or domain exploration.
version: 1.0.0
metadata:
  hermes:
    tags: [interview, design, decision-tree, exploration, universal]
---

# Grilling — Adaptive Deep-Dive Interview Meta-Skill

## When to Use

- **Explicit command:** *"Grill me about X"*, *"Interview me on Y"*, *"Let's design Z together"*
- **Complex trade-off:** *"Should I use A or B?"*, *"Choosing between X, Y, Z"*
- **Pre-build exploration:** *"Help me understand X before I start"*
- **Multi-factor planning:** *"Plan my..."*, *"I need to figure out..."*

Also auto-loads on: design interviews, architecture decisions, product strategy, domain reconnaissance.

## Procedure

### Phase 1 — Tree Initialization

Identify the domain (technical / strategic / creative / personal / product). Surface the highest-impact unresolved question as root of the most constrained branch.

### Phase 2 — Iterative Q&A

For each question:

1. **Ask** the question using the format in `references/question-style.md`
2. **Record** answer to `decision-log.md` (template: `references/decision-log-format.md`)
3. **Evaluate** branches: prune irrelevant, flag blocked-by-dependency, deepen rich sub-structure
4. **Check** for contradictions with prior decisions → offer revisitation

### Phase 3 — Distillation & Termination

- After every 5 resolved nodes, write a compact anchor (format: `references/decision-log-format.md#anchor`).
- If 3 consecutive answers opened 0 new branches, offer saturation wrapup.
- On user-initiated completion, generate final document (template: `references/output-templates.md`).

### Core Rules

| Rule | Behavior |
|------|----------|
| Options per question | 2–4 options max, each with description |
| Recommendation | Always provide 1 option + 1–2 sentence rationale |
| Socratic interrupt | If answer contradicts prior decisions or assumes unstated context → challenge before proceeding |
| Dependency resolution | Mark `BLOCKED BY Q{N}` in log; revisit when dependency unblocks |
| Backtracking | User can say "go back to Q{N}" at any time; revised decisions append (never overwrite) |

## Pitfalls

- **User fatigue:** Short/terse answers → offer recommendation-only mode (agent decides, user approves)
- **Circular interview:** Same node 3+ times → force commit with "recommend X"
- **Branch explosion:** >5 new branches from one answer → prioritize top 2, defer rest to later exploration
- **Context exhaustion:** >5 nodes since last distillation → force anchor immediately
- **Shallow answers:** User picks option without reasoning → Socratic interrupt

## Verification

At session end, confirm:

- [ ] `decision-log.md` written (full audit trail of Q→A→decision)
- [ ] Final document generated (structure per domain type in output templates)
- [ ] Open/blocked nodes explicitly flagged in final document
- [ ] User approves document format before any downstream use
