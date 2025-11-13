# Perplexity API: Slide Context Preparation

## Objective

Use Perplexity API to gather contextual resources that help create Excalidraw slides for each concept video. This preparation step happens AFTER plan.md is created and BEFORE drawing slides.

---

## Input Required

**File:** `Week-{N}/plan.md`

**Expected content per video:**
- Concept video title
- Scope (what the video covers)
- Key takeaways (2-3 main points)

**Example:**
```markdown
## Video 1: Risk vs Uncertainty

**Scope:** Distinguish between measurable risk and unmeasurable uncertainty

**Key Takeaways:**
- Risk has known probabilities (can model)
- Uncertainty involves unknown unknowns (cannot model)
- Investment decisions differ based on which you face
```

---

## Output Required

**File:** `Week-{N}/Video-{M}/slide_context.md`

**Content structure:**
1. Famous quotes (2-3)
2. Key reference summaries (3-5 resources)
3. Visual suggestions (diagrams, charts to recreate)
4. Recommended links for students

---

## Search Query Strategy

### **For Each Concept Video in plan.md:**

Run **4 separate searches** using Perplexity API:

---

### **Search 1: Famous Quotes**

**Query pattern:**
```
famous quotes about [concept] [domain]
Warren Buffett Charlie Munger quotes on [concept]
```

**Examples:**
- "famous quotes about risk vs uncertainty finance"
- "Warren Buffett Charlie Munger quotes on diversification"
- "famous investor quotes about time value of money"

**Extract:**
- Quote text
- Attribution (person, source, year if available)
- Context (why this quote is relevant)

**Output format:**
```markdown
### Famous Quotes

> "Risk comes from not knowing what you're doing."
> — Warren Buffett

> "The stock market is a device for transferring money from the impatient to the patient."
> — Warren Buffett

[Brief note: Use first quote in Frame 1 to introduce the problem, second quote in final frame as insight]
```

---

### **Search 2: Educational Resources**

**Query pattern:**
```
[concept] explained tutorial for students
how to understand [concept] finance
[concept] examples real world
```

**Examples:**
- "risk vs uncertainty explained tutorial for students"
- "diversification examples real world finance"
- "time value of money calculator educational"

**Extract from each result:**
- Title
- URL
- Type (YouTube video, blog post, interactive tool)
- Key insight (1-2 sentences summarizing what students learn)
- Duration/length (if video: 5 min, 20 min; if article: 500 words, 2000 words)

**Output format:**
```markdown
### Key References

**To understand the fundamental difference between risk and uncertainty:**
- Watch: [Risk vs. Uncertainty in Finance](https://youtube.com/watch?v=example) (8 min)
  Summary: Professor explains using dice (known probabilities) vs new technology adoption (unknown outcomes). Good visual metaphor for Frame 2.

**To see real-world examples of diversification failures:**
- Read: [When Diversification Doesn't Work](https://example.com/blog) (1200 words)
  Summary: 2008 financial crisis case study showing correlation breakdown. Use for "diversifiable vs systematic risk" frame.

**To practice calculations:**
- Tool: [Time Value Calculator](https://calculator.com) (Interactive)
  Summary: Visual calculator for PV/FV. Not for video, but good "learn more" link for students.
```

---

### **Search 3: Visual References**

**Query pattern:**
```
[concept] diagram visualization chart
[concept] infographic visual explanation
how to visualize [concept]
```

**Examples:**
- "risk return tradeoff diagram visualization"
- "diversification infographic visual explanation"
- "efficient frontier chart finance"

**Extract:**
- Description of diagram/chart
- What it shows (axes, data, relationships)
- URL to image (if available)
- Recreate difficulty (simple shapes, complex data)

**Output format:**
```markdown
### Visual Suggestions

**Risk-Return Tradeoff:**
- Source: https://www.dpegan.com/blog/visualizing-risk-return-and-time/
- Shows: Scatter plot with Expected Return (Y) vs Standard Deviation (X)
- Key elements: Asset clusters, efficient frontier line, annotation of diversification benefit
- Recreate: Use ellipses for asset distributions, diagonal line for frontier
- Frame suggestion: Build up gradually - axes (Frame 1), low-risk assets (Frame 2), high-risk assets (Frame 3), frontier line (Frame 4)

**Distribution Comparison:**
- Source: https://example.com/risk-distributions
- Shows: Violin plots showing return distributions at different time horizons
- Key elements: Width represents risk spread, center dot shows expected return
- Recreate: Use hand-drawn curves (no need for statistical precision), emphasize width difference
- Frame suggestion: Show Year 1, 2, 3, 4 progressively, each frame adds one distribution
```

---

### **Search 4: Academic/Practical Context**

**Query pattern:**
```
[concept] academic definition
[concept] practical application industry
[concept] [domain] best practices
```

**Examples:**
- "risk vs uncertainty academic definition Knight"
- "diversification practical application portfolio management"
- "time value of money best practices corporate finance"

**Extract:**
- Formal definition (if academic)
- Industry application (how practitioners use this)
- Common misconceptions (what students often get wrong)
- Rules of thumb (practical guidelines)

**Output format:**
```markdown
### Context & Definitions

**Academic Foundation:**
- Frank Knight's definition (1921): Risk = measurable uncertainty, Uncertainty = unmeasurable
- Key insight: Insurance works for risk (actuarial tables), not uncertainty (unknown events)

**Industry Application:**
- Portfolio managers: Use historical volatility (risk) but also scenario planning (uncertainty)
- Real example: COVID-19 was uncertainty (no model), seasonal flu is risk (predictable)

**Common Student Mistakes:**
- Treating all uncertainty as risk (thinking everything is modelable)
- Using standard deviation for black swan events (wrong tool)

**Frame Integration:**
- Frame 2: Show Frank Knight quote + definition
- Frame 4: Use COVID example to illustrate uncertainty
```

---

## Perplexity API Configuration

### **Model to Use:**
```
"sonar" or "sonar-pro" (latest model with citations)
```

### **Search Parameters:**
```json
{
  "model": "sonar",
  "max_tokens": 2000,
  "temperature": 0.3,
  "search_recency_filter": "month",
  "return_citations": true,
  "return_images": true
}
```

**Why these settings:**
- `temperature: 0.3` → Factual, not creative
- `search_recency_filter: "month"` → Recent examples for timely content
- `return_citations: true` → Need URLs for student references
- `return_images: true` → Visual suggestions for slide creation

---

## Query Execution Order

**For each video in plan.md:**

```
1. Extract: Video title, scope, key takeaways
   ↓
2. Generate 4 search queries (quotes, educational, visual, context)
   ↓
3. Execute searches via Perplexity API
   ↓
4. Parse results, extract relevant information
   ↓
5. Format into slide_context.md structure
   ↓
6. Save to Week-{N}/Video-{M}/slide_context.md
```

---

## File Organization

```
Week-1/
├── plan.md                          # Input (existing)
├── Video-1/
│   └── slide_context.md             # Output (NEW)
├── Video-2/
│   └── slide_context.md             # Output (NEW)
└── ...
```

---

## Output Format Template

**File:** `slide_context.md`

```markdown
# Slide Context: [Video Title]

**Concept:** [From plan.md scope]

**Key Takeaways:**
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

---

## Famous Quotes

> "[Quote text]"
> — [Attribution]

> "[Quote text]"
> — [Attribution]

**Usage notes:** [Which frame to use each quote]

---

## Key References

**To understand [concept/aspect 1]:**
- [Type]: [Title](URL) ([Duration/Length])
  Summary: [1-2 sentences of key insight]

**To see [concept/aspect 2]:**
- [Type]: [Title](URL) ([Duration/Length])
  Summary: [1-2 sentences of key insight]

**To practice/calculate [concept]:**
- [Type]: [Title](URL) ([Duration/Length])
  Summary: [1-2 sentences of key insight]

---

## Visual Suggestions

**[Diagram Type 1]:**
- Source: [URL]
- Shows: [Description of what diagram displays]
- Key elements: [Axes, data, annotations]
- Recreate: [How to draw in Excalidraw - shapes, colors, layout]
- Frame suggestion: [How to build up across frames]

**[Diagram Type 2]:**
- Source: [URL]
- Shows: [Description]
- Key elements: [Components]
- Recreate: [Excalidraw approach]
- Frame suggestion: [Progressive reveal strategy]

---

## Context & Definitions

**Academic Foundation:**
- [Formal definition, key researcher, year]
- [Theoretical insight]

**Industry Application:**
- [How practitioners use this]
- [Real-world example]

**Common Student Mistakes:**
- [Misconception 1]
- [Misconception 2]

**Frame Integration:**
- Frame [N]: [What to show/emphasize]
- Frame [M]: [What to show/emphasize]

---

## Additional Resources for Students

Students can explore these for deeper learning:

1. [Resource Title](URL) - [Brief description]
2. [Resource Title](URL) - [Brief description]
3. [Resource Title](URL) - [Brief description]

---

_Generated by Perplexity API searches on [Date]_
```

---

## Search Quality Guidelines

### **Good Search Results Include:**

✅ Recent content (last 12 months preferred)
✅ Multiple source types (academic, practical, visual)
✅ Verifiable quotes with attribution
✅ Specific examples with dates/names
✅ Visual content that can be recreated
✅ Educational resources appropriate for undergrads

### **Filter Out:**

❌ Paywalled content (students can't access)
❌ Overly technical (PhD-level) resources
❌ Expired links
❌ Generic stock photos without educational value
❌ Resources requiring expensive software

---

## Example: Complete Search Execution

**Input from plan.md:**

```markdown
## Video 3: Portfolio Diversification

**Scope:** Demonstrate how combining assets reduces overall portfolio risk through imperfect correlation

**Key Takeaways:**
- Diversification reduces unsystematic (company-specific) risk
- Systematic (market) risk cannot be diversified away
- Optimal portfolio depends on correlation between assets
```

**Search 1 Query:**
```
"famous quotes about diversification investing Warren Buffett"
```

**Search 2 Query:**
```
"portfolio diversification explained examples correlation real world"
```

**Search 3 Query:**
```
"diversification risk reduction diagram efficient frontier visualization"
```

**Search 4 Query:**
```
"diversification academic definition Markowitz systematic unsystematic risk"
```

**Output file:** `Week-1/Video-3/slide_context.md`

---

## Integration with Workflow

**Workflow position:**

```
Monday:
1. Parse lectures → plan.md ✓
   
Tuesday:
2. Run Perplexity searches → slide_context.md (NEW)
   [Automated via Claude Code]
   
Wednesday:
3. Review slide_context.md (10 min per video)
4. Create Excalidraw frames using context (25 min per video)
   [Manual with AI-gathered context]
```

**Time saved:** 15-20 minutes of manual research per video

**Quality improved:** Better quotes, more relevant visuals, verified references

---

## Success Criteria

**slide_context.md is successful when:**

✅ Contains 2-3 usable quotes (attributed correctly)
✅ Lists 3-5 educational resources with working links
✅ Provides 2-3 visual suggestions that can be recreated
✅ Includes clear frame integration recommendations
✅ Takes <5 minutes to review and extract key insights
✅ Directly reduces time to create Excalidraw frames

---

## Notes

- Perplexity API key should be in `.env` file
- Rate limits: Respect API limits (typically 50 requests/minute)
- Cost: ~$0.01-0.05 per search (4 searches × 10 videos = $0.40-2.00/week)
- Cache: Save API responses to avoid re-searching same concepts

---

End of Instructions
