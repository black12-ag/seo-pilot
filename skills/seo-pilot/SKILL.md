---
name: seo-pilot
description: Use when auditing or improving website SEO, AI search visibility (GEO/AEO), content, Core Web Vitals, app-store discovery, or public bot discovery, especially when one coordinated audit or update is requested.
license: MIT
metadata:
  version: "0.1.0"
---

# SEO Pilot

One entry point for three attributed, pinned collections. All 92 bundled modules remain available; load only the modules relevant to this request. This is an agent skill, not a standalone ranking service.

## Invocation

`$seo-pilot audit https://example.com` runs the combined workflow; a bare URL means audit. Claude Code may expose `/seo-pilot` instead. Focused requests use `ai`, `technical`, `content`, `performance`, `app`, `bot`, `ecommerce`, `local`, or `international`. Request any bundled feature by its namespaced ID from `catalog.json`.

For an audit, start collecting evidence once the target is known. For requested changes, make the authorized changes and verify them. Ask only for missing targets or decisions that matter. An audit request alone does not authorize publishing, sending messages, changing crawler policy or buying services.

## Start and select

1. Read the target project's instructions and available product context. Never assume another project's domains, stack or policies. Distinguish local source, deployed output and historical analytics.
2. Read [mode routing](references/modes.md). Choose one primary owner for each topic and use another collection only to fill a gap. Use all relevant families for a combined audit. Include app/bot work only when those targets are supplied; their absence does not block website work.
3. Read [evidence and reporting](references/evidence.md). For AI search, also read [AI search](references/ai-search.md); for app/bot discovery, read [app and bot](references/app-and-bot.md).

## Execute one coordinated workflow

- Establish the website's public/indexable versus private routes, target audience, locale and conversion goal from available context. Fetch representative page types, robots and sitemap; inspect rendered pages when possible.
- Run technical crawl/index checks, content and product fact checks, AI search accessibility/content checks, and field-plus-lab performance analysis. Read only the selected upstream instructions and their relevant references.
- Verify current platform requirements with official sources. Upstream scores are diagnostic conventions, not search-engine ranking formulas. Do not combine incompatible scores into a fabricated overall ranking prediction.
- Report observed defects separately from hypotheses and missing measurements. Existing structured data is not automatically valid; absent raw-HTML markup is not proof it is absent after rendering. Historical/local defects are not automatically live defects.
- Consolidate duplicate findings into one prioritized report with evidence, location, owner, smallest fix and verification. Then implement only the requested scope and recheck the affected behavior. Delegate independent work only when the environment and user/project instructions allow it.

## Bundled resources and portability

The three `vendor/` collections preserve their licenses and supporting resources. Their `SKILL.md` files are references beneath this single entry; do not activate them all separately.

Resolve references from the module being read and named sub-skills through `catalog.json`. `${CLAUDE_PLUGIN_ROOT}` means the relevant vendor root, not this entry's root. Read modes.md for portable tool launch and optional runtime setup. Bundling installers, hooks or paid tools does not authorize running them.

If a tool/extension is unavailable, continue supported checks and name the gap. Search and model-training permissions are separate; preserve the owner's policy.

Offline helpers, using the actual installed skill path:

```sh
python3 <skill-path>/scripts/seo_pilot.py list
python3 <skill-path>/scripts/seo_pilot.py route all --url https://example.com
python3 <skill-path>/scripts/seo_pilot.py check
python3 <skill-path>/scripts/seo_pilot.py doctor
```

`route` produces a plan, not an audit result. A completed audit needs executed checks and an evidence-backed report. Tools requiring credentials or payment are optional; explain unavailable capabilities instead of fabricating results.
