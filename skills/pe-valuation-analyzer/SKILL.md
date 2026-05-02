---
name: pe-valuation-analyzer
description: "P/E valuation analysis framework: reverse-engineer market expectations from a stock's price-to-earnings ratio and assess whether the current valuation is justified by actual growth. Trigger this skill whenever the user mentions valuation analysis, PE ratio, PEG ratio, whether a stock is overvalued or undervalued, whether it's worth buying, or asks about a specific stock's pricing logic. Also trigger when the user says things like 'analyze NVDA', 'is Tesla overvalued', 'MSFT looks expensive', 'what's priced into Apple', 'PE seems too high', '分析一下 XX 公司的估值', 'XX 贵不贵'. Supports both English and Chinese input."
---

# P/E Valuation Analysis Framework

Reverse-engineer what the market is betting on from a stock's P/E ratio, cross-check against actual growth data, and judge whether the current valuation leans optimistic, fair, or pessimistic.

## Core Principle

Stock price is driven by two variables:

```
Market Cap = Annual Earnings × P/E Multiple
```

The P/E multiple reflects the market's confidence in future growth. A high P/E stock isn't necessarily "expensive," and a low P/E stock isn't necessarily "cheap" — what matters is whether the P/E matches the actual growth rate. This framework makes that match explicit.

## Execution Flow

When the user asks you to analyze a company, follow these steps in order. Every step requires fetching real data — never fabricate numbers from memory.

### Step 1: Gather Baseline Data

Use WebSearch and WebFetch to collect the following (prefer Yahoo Finance, MacroTrends, Google Finance, StockAnalysis):

| Data Point | Description | Where to Find |
|------------|-------------|---------------|
| Current stock price & market cap | Real-time or most recent trading day | Google Finance / Yahoo Finance |
| Trailing P/E (TTM) | Based on past 12 months' actual earnings | Yahoo Finance "Valuation Measures" |
| Forward P/E | Based on analyst estimates for next 12 months | Yahoo Finance |
| Last 4 quarters of revenue & net income | For computing actual growth rates | Company filings / MacroTrends |
| Past 2-3 years of annual revenue & net income | For computing historical growth trends | MacroTrends |
| Gross margin & net margin trends | To assess margin direction | MacroTrends |
| Analyst consensus estimates | Expected earnings growth for next 1-2 years | Yahoo Finance "Analysis" tab |

If any data point is unavailable, tell the user which data is missing and how it affects the reliability of the analysis.

### Step 2: Determine the Steady-State P/E Range

Based on the company's industry and growth stage, estimate what P/E the stock will eventually settle at. This is the anchor for the entire analysis.

| Company Type | Steady-State P/E | Examples |
|-------------|-------------------|----------|
| Hyper-growth tech (revenue growth >50%) | 40-60x | Early Tesla, Snowflake at IPO |
| High-growth tech (growth 25-50%) | 30-45x | NVIDIA (2024-2026) |
| Stable-growth tech (growth 10-25%) | 20-35x | Microsoft, Apple, Google |
| Mature tech (growth <10%) | 12-22x | TSMC, Cisco, Intel |
| Consumer staples / Pharma | 15-25x | P&G, Johnson & Johnson |
| Financials / Banks | 8-15x | JPMorgan, Goldman Sachs |
| Energy / Utilities | 8-15x | ExxonMobil, Duke Energy |
| Cyclicals | Varies | Autos, airlines — P/E is often highest at the cycle trough |

When selecting the steady-state P/E, consider:
- Is the company's growth accelerating or decelerating?
- Does it have structural moats (network effects, switching costs, brand)?
- Is the competitive landscape deteriorating?

### Step 3: Calculate Market-Implied Expectations

Use these formulas to reverse-engineer "what the market is betting on":

**Earnings growth required to break even (assuming P/E compresses to steady state):**

```
Required earnings growth multiple = Current P/E ÷ Steady-State P/E
```

**Earnings growth required for 10% annualized return (N-year holding period):**

```
Required earnings growth multiple = (Current P/E × 1.1^N) ÷ Steady-State P/E
```

**Potential downside if earnings don't grow:**

```
Potential decline = 1 - (Steady-State P/E ÷ Current P/E)
```

### Step 4: Calculate PEG Ratio

```
PEG = Current P/E ÷ Annual earnings growth rate (as a percentage, e.g. 30 not 0.3)
```

| PEG | Interpretation |
|-----|----------------|
| < 0.8 | Growth rate well exceeds P/E — potentially undervalued |
| 0.8 - 1.2 | P/E roughly matches growth rate — fairly priced |
| 1.2 - 2.0 | P/E exceeds growth rate — leans optimistic |
| > 2.0 | P/E significantly exceeds growth rate — likely overvalued unless there's an exceptionally strong moat |

Note: PEG is not useful when the growth rate is negative or very low (<5%). In those cases, compare the absolute P/E against sector peers instead.

### Step 5: Margin Risk Check

Earnings growth = Revenue growth × Margin change. Even if revenue is growing, declining margins can cause earnings to shrink.

Check:
- Gross margin trend: rising, stable, or declining over the past 4-8 quarters?
- Net margin trend: same check
- If margins are declining, quantify the impact:

```
Future Earnings = Future Revenue × Future Net Margin
```

If revenue growth is being offset by margin compression, flag this explicitly to the user — it's the most common way "growth stocks" disappoint.

### Step 6: Output the Analysis Report

Use this exact structure in Markdown:

```
## [Company Name] P/E Valuation Analysis

### Baseline Data
| Metric | Value |
|--------|-------|
| Current Price | $XXX |
| Market Cap | $XXX |
| Trailing P/E (TTM) | XXx |
| Forward P/E | XXx |
| Latest Annual Revenue | $XXX |
| Revenue YoY Growth | XX% |
| Latest Annual Net Income | $XXX |
| Earnings YoY Growth | XX% |
| Gross Margin | XX% |
| Net Margin | XX% |
| PEG | X.XX |

### Market-Implied Expectations
- Steady-state P/E range: XX-XXx (rationale: ...)
- Earnings growth required to break even: X.Xx (i.e. XX% growth)
- Earnings growth required for 10% annual return (5yr): X.Xx
- Potential downside if earnings stay flat: XX%

### Actual Growth Performance
- Trailing 1-year earnings growth: XX%
- 3-year earnings CAGR: XX%
- Analyst consensus (next year): XX%
- Margin trend: [Expanding / Stable / Compressing]

### Verdict: [Leans Optimistic / Fairly Valued / Leans Pessimistic]

[2-3 sentence summary explaining the verdict.
Cover: what PEG tells us, whether market-implied expectations are realistic,
and the biggest upside/downside risk.]
```

The output language should match the user's input language. If they ask in Chinese, respond in Chinese. If they ask in English, respond in English.

## Important Considerations

- All data must come from live searches. Financial data changes rapidly — stale numbers lead to wrong conclusions.
- For cyclical industries (autos, semiconductors, airlines), P/E can be misleadingly high at the cycle trough because earnings are depressed while the stock price reflects recovery expectations. Call this out explicitly when it applies.
- P/E analysis has limits: it doesn't work for unprofitable companies (negative P/E is meaningless). In that case, suggest the user consider P/S (price-to-sales) analysis instead.
- End every analysis with: "This analysis is based on public data and a valuation framework. It does not constitute investment advice."
