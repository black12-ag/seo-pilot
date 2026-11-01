# Evidence and output contract

For each check, record target URL/file, timestamp or source date, method, actual observation, and limitations. Keep local code, deployment behavior, historical analytics, lab measurements, and current field data separate.

## Evidence levels

- **Observed:** directly reproduced HTTP, browser, tool, source or account result. A source defect is observed in that source, not automatically on production.
- **Hypothesis:** a plausible explanation needing the named verification step.
- **Not assessed:** missing target, browser, account, API quota, relevant sample or measurement.

Render-dependent content requires a rendered check to claim its absence. A sitemap URL or JSON-LD block does not prove indexing, eligibility or correctness. A synthetic Lighthouse result is not real-user INP; do not invent Core Web Vitals measurements when tools or field data are unavailable. Report an origin-level field fallback explicitly.

When a tool fails, distinguish the tool's own access/rate-limit problem from a site defect. Do not silently replace live evidence with an old cached scan. A partially completed audit is reported as partial with its useful evidence, not as an unqualified success or as a reason to abandon independent checks.

## One report

Lead with the observed outcome and most important action. Report site/app/bot coverage and limits, then one deduplicated finding list ordered by impact:

| Priority | Finding and evidence | Owner/location | Smallest useful change | Verification |
|---|---|---|---|---|

For each finding state the concrete trigger, consequence and which surface it affects. Record conflicts between upstream advice and current primary sources. Distinguish a visible-content change from a code/config change and from an external publication.

When scores are useful, state their rubric, covered dimensions and omitted dimensions. Never present a homegrown score as Google's ranking algorithm or treat unmeasured dimensions as passing. Separate crawl/index results, content quality and performance rather than averaging incompatible upstream formulas.

For authorized updates, identify files and page ownership before editing, preserve unrelated behavior, run relevant tests and build checks, and repeat the observations that established the defect. Indexing and field-performance outcomes may require future data; say so instead of claiming immediate improvement. Follow the target repository's deployment rules.
