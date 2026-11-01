# Select tools by evidence, access and task

Read this when a user names a tool, asks which connector to use, supplies exports, or wants account data. Comparison checked November 1, 2026 against official documentation. These are documented capabilities, not authenticated integration tests or a ranking of data quality. Recheck the current tool list, plans and limits before use.

SEO Pilot provides the shared audit, source review, measurement and implementation workflow. External services supply additional data or operations when the owner has access. A connector listing, installed skill or API key does not establish that a connection is authenticated or that every product report is available through it.

## SEO and AI-search tools

| Tool and official evidence | Useful documented capability | Access and limits |
|---|---|---|
| **OpenSEO** ([exact Claude listing](https://claude.com/marketplace/connectors/openseo), [AI visibility](https://openseo.so/docs/ai-visibility)) | Prompt research, repeated question tracking, mentions, citations, competitors, history and exports. | The “SEO made simple” connector is **openseo.so**, linked to `app.openseo.so/mcp`; do not import claims from similarly named OpenSEO products. Collection surfaces vary by engine. Self-hosting does not remove upstream model/search-data costs. |
| **Ahrefs / Brand Radar** ([product](https://ahrefs.com/brand-radar), [MCP requirements](https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp)) | Response corpus/custom prompts, mentions/citations, competitors, sentiment, topic/funnel and fanout research. | MCP/API access depends on plan, units and platform add-ons. Estimated impressions are weighted estimates, not observed customer traffic. The proprietary index is not bundled with this skill. |
| **Semrush** ([AI Visibility Toolkit](https://www.semrush.com/kb/1496-getting-started-with-ai-visibility-toolkit), [MCP](https://www.semrush.com/kb/1618-mcp)) | AI mentions/citations, competitor prompt/topic gaps, sentiment, cited-source research and custom tracking. | MCP has subscription-dependent SEO/traffic/competitor tools. Verify which AI reports the actual connection exposes; product capability does not establish MCP availability. |
| **Ubersuggest** ([AI Search Visibility](https://help.ubersuggest.com/hc/en-us/articles/40815245487515-Introducing-AI-Search-Visibility-in-Ubersuggest), [Claude integration](https://ubersuggest.com/en/claude-plugins)) | Repeated prompt answers, citations, trends, competitor/alias tracking and sentiment themes. | OAuth/MCP/plugin access and quotas vary by plan. Determine supported engines from the actual account/tool configuration. |
| **OpenRush** ([AI Visibility MCP](https://www.openrush.com/ai-visibility-mcp), [credits](https://www.openrush.com/docs/fundamentals/credits-and-rate-limits)) | Sampled **Google AI Overview** citations/questions, source/category and competitor-domain comparisons; other SEO data tools. | AI calls use prepaid credits. This documented AI visibility surface is not ChatGPT/Claude/Gemini/Perplexity/Copilot monitoring or sentiment analysis. |
| **Conductor** ([AI Search Performance](https://www.conductor.com/platform/features/ai-search-performance/), [MCP methodology](https://www.conductor.com/academy/conductor-mcp-differentiators/)) | Mentions/citations, recommendation strength, sentiment, topic/persona analysis, competitors and referral/bot reporting. | Requires account data and appropriate MCP/API access. Preserve synthetic-prompt/API collection provenance and native metric definitions. |
| **Abency** ([capabilities](https://abency.com/en), [Claude Code connection](https://abency.com/en/claude-code)) | SEO research/tracking, connected search/analytics reporting and WordPress/marketing workflows. | Dedicated AI-answer citation/sentiment monitoring was not established from the inspected official documentation. Publishing and other marketing operations require their own authorization. |

Do not subscribe to all services to complete an audit. Use existing authorized native reports and exports first. If deeper coverage is needed, choose the provider that actually supports the requested engines, market, history and data units. The workflow works without buying a proprietary corpus; it does not replace that corpus or promise equivalent coverage.

## Supporting connectors in the same directory

These tools can assist an SEO project, but their presence does not add search-ranking or AI-citation measurements.

| Connector and official documentation | Relevant supporting workflow | Prerequisite/boundary |
|---|---|---|
| **Sanity** ([MCP](https://www.sanity.io/docs/ai/mcp-server)) | Query owned content/schema, map findings to fields, prepare and validate CMS drafts/releases. | Account/OAuth or scoped token and project permissions. A content query is not search-performance data; publishing remains a separate action. |
| **tl;dv** ([official MCP](https://github.com/tldv-public/tldv-mcp-server), [API](https://doc.tldv.io/)) | Authorized interviews/meetings → actual customer questions, objections and source-linked content briefs. | Hosted OAuth connector is read-only; documented plan and meeting-organizer requirements apply. Transcript statements are customer research, not measured query volume. |
| **Padlet** ([MCP](https://padlet.help/l/en/article/pofbiabhv1-mcp-server), [REST API](https://docs.padlet.dev/reference/introduction)) | Review approved research boards, topic backlog and feedback. | MCP supports free accounts within their limits; the separate REST API requires a paid plan. Writes to boards are not implied by read-only research. |
| **Autosheet / Talarian** ([MCP](https://autosheet.com/mcp), [API](https://autosheet.com/docs/api)) | Analyze supplied search/crawl exports, metadata rows and content reports in Google Sheets. | Google/account access and usage credits; API is preview. Preserve source dates and missing values. It processes data rather than supplying a search index. |
| **WorkOS** ([MCP](https://workos.com/docs/mcp)) | Identity/tenant administration only when that is the actual task. | Dashboard OAuth/permissions; administrators can restrict access and writes. It is not an SEO feature or a reason to change authentication during an audit. |

## Use connectors without inventing integration support

1. Discover actual tools in the current host and inspect their documented parameters. Record **documented / configured / authenticated / successfully tested** separately. Never hardcode guessed MCP tool names or pretend a provider account exists.
2. Choose the smallest read-only query/export for the target, date range, market and engine. Confirm freshness, sampling, units/quotas and any cost before a call within the user's authorized scope. Do not run paid collection merely because a provider is in this table.
3. Keep raw exports and answer evidence private. Record provider, filters, collection method and metric definition. Normalize only compatible records; preserve aggregate reports as aggregates rather than generating fake per-answer rows.
4. Use [AI visibility measurement](ai-visibility.md) for supplied answer observations and the existing bundled specialists for keywords, backlinks or content. Integrations already bundled include `claude-seo:seo-ahrefs`, `seo-profound`, `seo-seranking`, `seo-google` and `seo-dataforseo`; resolve their full IDs through the catalog and verify actual availability.
5. Produce a reviewable recommendation or CMS draft. Querying content or reading a meeting does not authorize publishing, sending outreach, editing ads, changing identity systems or installing every service.

Claude connector setup follows [Anthropic's current connector guide](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) and the selected vendor's instructions. Authentication and permissions belong to that host/account. Installing SEO Pilot supplies workflow instructions; it does not automatically connect commercial accounts or synchronize settings between Claude web, Claude Code and Codex.

## What this comparison adds to SEO Pilot

The existing 92 modules already contain prompt research, answer accuracy, attribution and recommendation guidance. This upgrade connects them with a repeatable evidence ledger, transparent arithmetic, competitor/source-to-action review and verified optional-tool selection. See [measurement](ai-visibility.md) for the executable workflow and [current platform guidance](ai-search.md) for crawler controls and native reports. Vendor data and managed monitoring remain optional external capabilities.
