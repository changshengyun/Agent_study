# Grilling — References: Output Templates

Template untuk dokumen final yang di-terminate dari decision-log.

## Domain: Technical

```markdown
# {Title} — Design Specification

## Summary
{2–3 paragraph summary of the design space and key decisions}

## Decisions
| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| Q1 | ... | ... | ... |
| Q2 | ... | ... | ... |

## Architecture / Plan
{structured sections — depend on domain specifics}

## Open Questions
- [ ] Q{N}: {description} — blocked, needs resolution

## Appendix
Full decision-log: `decision-log.md`
```

## Domain: Non-Technical (Strategic / Personal / Product)

```markdown
# {Title} — Plan / Strategy

## Summary
{2–3 paragraph overview}

## Considered Options
{what was evaluated before收敛 to the key decisions}

## Decisions
| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| Q1 | ... | ... | ... |

## Action Items
- [ ] Derived action from Q{N}
- [ ] Derived action from Q{N}

## Open Questions
- [ ] Q{N}: unresolved
```

## Any Domain — Minimal

```markdown
# {Title} — Decision Record

**Date:** {ISO}
**Domain:** {}

## Decisions Made
{numbered table}

## Open / Blocked
{bulleted list}

## Audit Trail
{decision-log.md content or link}
```
