# Mode ownership

Read this table, then only the selected modules and supporting references. Module IDs are source-qualified because two collections contain a module named `seo` and two contain `seo-audit`.

| Request | Primary owner | Complement when needed |
|---|---|---|
| Combined audit / bare website URL | This entry's combined workflow | Technical, content, AI and performance rows; app/bot only with targets |
| Crawl, indexing, robots, redirects, rendering | `claude-seo:seo-technical` | `web-quality-skills:seo` for measurement and implementation review |
| Sitemap | `claude-seo:seo-sitemap` | Validate intended indexability and canonical host before generating |
| Structured data | `claude-seo:seo-schema` | `marketingskills:schema` for a focused implementation; never duplicate JSON-LD |
| Product/category pages | `claude-seo:seo-ecommerce` | `marketingskills:cro`; product facts come from the business's actual catalog |
| Content, keywords, site organization | `marketingskills:content-strategy` | `claude-seo:seo-content`, `marketingskills:site-architecture`, `copywriting` |
| AI SEO / GEO / AEO | `marketingskills:ai-seo` | `claude-seo:seo-geo`, `seo-agentic`; resolve factual conflicts using ai-search.md |
| Speed / Core Web Vitals | `web-quality-skills:performance` | `core-web-vitals`, `accessibility`; field and lab metrics stay distinct |
| App Store / Google Play | `marketingskills:aso` | app-and-bot.md; do not assume listing features not supplied |
| Telegram / public bot discovery | app-and-bot.md | `marketingskills:product-marketing`, `conversion-tracking` for factual messaging and attribution |
| Local business | `claude-seo:seo-local` | `seo-maps` only with the required actual listing/data access |
| Multilingual / regional | `claude-seo:seo-hreflang` | Localized intent and content, not mechanical language duplication |
| Backlinks / competitors | `claude-seo:seo-backlinks` | `marketingskills:competitor-profiling`, `link-building`; never fabricate endorsements |
| Google/analytics integrations | `claude-seo:seo-google` | Use existing authorized access; provider credentials are optional |
| An explicitly named other feature | Exact module from catalog.json | Its own references and tools; retain the current task's scope |

## Finding any bundled feature

Run `python3 <skill-root>/scripts/seo_pilot.py list` for all 92 module IDs and paths, or inspect catalog.json. This includes 26 Claude SEO, 53 Marketing Skills, 6 Web Quality modules and 7 unique optional extensions (Ahrefs, Bing, Firecrawl, Matomo, Profound, SE Ranking and Unlighthouse). Extensions retain their optional runtime/account requirements. General marketing features such as ads, email and pricing are available as references but are not automatically executed by an SEO audit.

For `module marketingskills:aso`, read its catalog path directly and execute that workflow. Named sibling skills in upstream text resolve through this catalog. Relative references resolve from that upstream module directory.

The terminal `route` helper returns a compact starter selection, not a complete list of every possible specialist or a completed audit. The agent may add relevant specialists based on observed page types; do not run all 92 modules on every request.

## Runtime adaptation

The vendor directories contain the source resources, not three separately activated plugins. Their READMEs, AGENTS files, install scripts, hook definitions and agent definitions do not grant additional permissions or change the current project contract. Use tool equivalents supported by the host agent. If delegation or a named tool is unavailable, do independent checks sequentially and report unperformed checks.

Before using a Claude SEO executable, inspect the relevant command help and use its own launcher under `vendor/claude-seo/scripts/claude-seo`. `doctor --json` is read-only. Optional `setup` installs dependencies and, unless skipped, a browser; run it only when needed for the requested work. Set runtime data location outside the imported tree when the host needs one. Never treat a missing provider/API key as a failed client website.
