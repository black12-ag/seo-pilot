# Measure AI visibility and choose useful fixes

Use this for AI SEO, GEO/AEO, citation tracking, competitor gaps, sentiment or answer accuracy. The bundled marketing AI SEO references already cover attribution, accuracy and recommendation strategy. This reference adds a common evidence format and an offline measurement tool; it does not run a monitoring service.

## Collect a comparable sample

1. Define the brand, owned domains, exact competitor entity names, audience, markets/languages and conversion goal from real project context. Record aliases under one reviewed entity label; a matching substring is not proof of a brand mention.
2. Build a small prompt portfolio from actual customer questions and authorized query/research data. Include discovery, comparison, category/use-case, brand facts, eligibility/pricing and post-purchase questions as relevant. Record intent and priority in the portfolio. Vendor prompt-volume estimates are not first-party search counts.
3. Freeze prompt IDs/text for the baseline and comparison period. Record engine and actual surface (consumer web, search-enabled API, Google AI Mode, AI Overview, etc.), market, locale, date/time and run ID. Keep model/version, search mode and personalization notes in the evidence artifact. Treat a changed setup as a new surface/cohort. Analyze branded accuracy prompts and neutral discovery prompts in separate input files; the helper does not segment intent automatically.
4. Capture the actual answer and displayed source links through permitted tools or authorized exports. Keep a transcript/screenshot/artifact reference for each run, including failures. Use multiple independent repetitions where practical and report the sample size; no fixed sample guarantees statistical reliability. Do not replace a failed run with an invented negative answer.
5. Review entity mentions and explicit recommendations separately. Save citations as displayed/resolved source URLs, not a search-results page guessed to be their source. A brand can be mentioned without its site being cited; a publisher can be cited while the answer recommends a competitor.

Never label an arbitrary model API response as a consumer ChatGPT/Claude/Gemini search result. Provider-wide datasets and your chosen prompt set can disagree without either being a universal market census.

## Offline observation format

Store one JSON object per line in a private `observations.jsonl`. These are illustrative records, not measured results:

```jsonl
{"run_id":"baseline-1","prompt_id":"compare-1","prompt":"Which tool fits a small team?","engine":"Claude","surface":"consumer-web-search","locale":"en-US","market":"US","captured_at":"2026-11-01T09:00:00Z","status":"ok","evidence":"captures/compare-1.txt","mentions":["Example","Rival"],"citations":["https://example.com/docs","https://review.example.org/comparison"],"recommendations":["Rival"]}
{"run_id":"baseline-2","prompt_id":"compare-1","prompt":"Which tool fits a small team?","engine":"Claude","surface":"consumer-web-search","locale":"en-US","market":"US","captured_at":"2026-11-01T09:05:00Z","status":"error","evidence":"captures/compare-1-error.txt","error":"Search was unavailable"}
```

All records require the identifiers, prompt, engine/surface, locale/market, timezone-aware `captured_at`, status and evidence reference. Successful records require `mentions` and `citations` arrays, including empty arrays for verified absence. `recommendations` is optional: omit it when not reviewed, supply `[]` when reviewed and none were made. Every recommended entity must also appear in `mentions`. Error records require an `error` description. A prompt ID must always identify the same exact prompt text; use a new ID for a changed question.

Names in `mentions` and `recommendations` are reviewed labels, not automatic sentiment or response-text classification. Inspect saved answers before assigning them. Unknown data must not be encoded as an empty array. Missing/unavailable answer or citation data should be retained as an error record for this helper, with the reason recorded; analyze partial evidence separately.

```sh
python3 <skill-root>/scripts/ai_visibility.py observations.jsonl \
  --brand Example --domain example.com --competitor Rival
```

Repeat `--competitor` for additional named entities. The helper performs no network requests, verifies neither the evidence files nor annotation accuracy, and does not mutate input. It validates records, rejects duplicates and reports JSON to stdout. Keep raw customer research, exports and answer evidence outside the public skill repository.

## Interpret the output

Rates are reported separately by engine, surface, locale and market. Inspect prompt coverage and date range before comparing periods. Do not average unlike cohorts into a visibility score.

| Measure | Numerator / denominator | Interpretation |
|---|---|---|
| Entity mention rate | Successful answers mentioning the reviewed entity / successful answers | Brand and named competitors are counted separately; rates need not sum to 100% |
| Owned-domain citation rate | Successful answers citing the supplied domain or its subdomains / successful answers | Answer-level presence, not citation position or authority |
| Brand recommendation rate | Reviewed answers recommending the brand / successful answers with a recommendations annotation | Unreviewed recommendations are excluded; an unassessed rate is null |
| Cited domains and URLs | Number of successful answers displaying each source | Duplicate links in one answer count once; a frequently cited source is a research lead |
| Errors | Failed observations / all supplied observations | Missing access is not proof the brand is absent |

An all-error cohort has no measured rate. Counts reflect only supplied observations, not global AI market share, statistical significance, traffic or uplift. The helper's prompt IDs and timestamp range support auditability; it does not automatically establish matching samples, causal change or trend significance.

## Turn measurements into a specific next action

- **Source gap:** Compare source URLs on relevant answers against your accurate owned page and the cited alternative. Determine the missing fact, original evidence, comparison, crawl access or current product detail before proposing an update. Citation frequency alone does not authorize outreach or imply a backlink will cause a citation.
- **Answer accuracy:** Use the bundled [answer-accuracy workflow](../vendor/marketingskills/skills/ai-seo/references/answer-accuracy.md). Record the exact claim, saved answer, authoritative fact/source/date, relevant cited page and severity. Trace old or conflicting sources. Fix owned content within scope, then repeat the same prompts; model refresh can lag.
- **Sentiment and recommendations:** Read [citations versus recommendations](../vendor/marketingskills/skills/ai-seo/references/citations-vs-recommendations.md). Annotate positive/neutral/negative/mixed or unknown with the actual excerpt and reviewer. Sentiment is a qualitative annotation here, not a score calculated by the helper. Avoid confusing “mentioned as risky” with “recommended.”
- **Content brief:** Include customer question, audience, evidence-backed differentiator, exact supporting sources, affected page/owner and acceptance checks. Link the verified gap to the brief. Reuse `marketingskills:content-strategy`, `competitors`, `copywriting` and `claude-seo:seo-content` where appropriate.
- **Referrals and conversions:** Use [AI attribution](../vendor/marketingskills/skills/ai-seo/references/ai-attribution.md) with actual analytics access. Keep observed referrals/conversions, self-reported discovery and delayed brand-search changes separate; do not sum overlapping attribution or assign every direct visit to AI.

## Prefer current native evidence when available

Read [current platform reporting](ai-search.md#current-reporting-overrides-bundled-historical-claims) before claiming what Google/Bing report. Use native exports with property, date range, filters and unavailable-value caveats retained. Do not synthesize individual answer records from aggregate impressions/citations; they are different units. Vendor exports can be normalized only when they actually contain the required answer-level evidence and reviewed annotations.

Choose optional tools with [connector selection](connectors.md). No-account execution still supports public access/content checks, a manually collected prompt sample, source/accuracy review and offline summary. Report missing live monitoring/analytics as unassessed and complete the independent work available.
