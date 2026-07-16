# Grilling — References: Question Style

Format wajib untuk setiap pertanyaan dalam interview.

## Question Template

```markdown
### Q{N} — {Topic}

{Context: why this question matters / what depends on it}

| # | Option | Description |
|---|--------|-------------|
| A | ...    | ...         |
| B | ...    | ...         |
| C | ...    | ...         |

**Recommendation:** {X} — {reasoning in 1–2 sentences}
```

## Socratic Interrupt 

Jika jawaban user dangkal, inkonsisten dengan keputusan sebelumnya, atau mengasumsikan konteks yang tidak disebutkan:

> ⚠️ **Challenge:** Your answer assumes [X], but earlier you decided [Y]. Want to revisit, or adjust the assumption?

## Recommendation Engine

- **Default:** Rekomendasi dari model — fast, contextual.
- **On-demand:** User bilang *"verify this"* → trigger `web_search` + `web_extract`, append hasil ke decision-log dengan source citation.
