# AI SEO: evidence before promises

AI SEO, GEO and AEO here mean improving accurate discovery and citation by search-enabled assistants. They also include checking whether an answer represents the business correctly. This does not mean training a foundation model, guaranteeing a recommendation, or optimizing private bot conversations as public web pages.

## Primary sources to verify at time of use

- Google: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google feature eligibility: https://developers.google.com/search/docs/appearance/ai-features
- OpenAI crawler purposes: https://developers.openai.com/api/docs/bots
- Perplexity crawler purposes: https://docs.perplexity.ai/docs/resources/perplexity-crawlers

Verified November 1, 2026. Platform behavior changes; check the current official documentation before proposing policy changes or stating eligibility requirements. An upstream guide or case study never outranks the platform's own current requirements.

## Access is purpose-specific

| Purpose | Relevant control | What it does not establish |
|---|---|---|
| ChatGPT Search discovery | OAI-SearchBot; verified published crawler IPs if a firewall is involved | GPTBot permission is not required merely for this search purpose |
| OpenAI model-training crawl | GPTBot | Allowing it does not itself establish search inclusion |
| Perplexity search discovery | PerplexityBot; published IPs when appropriate | Not permission for training a foundation model |
| User-requested fetch | Relevant platform user agent and its documented behavior | Not equivalent to an automatic search crawl |
| Google generative search | Current Google Search eligibility, index/snippet access and any documented Search Console settings | A special AI file or a schema score is not an eligibility substitute |

Read robots, response headers, observed response status and CDN rules as separate evidence. A failed test with a generic crawler user agent is not proof that a verified search crawler is blocked. Preserve intentional policy. Fix a verified crawler-specific rule rather than weakening the whole firewall.

## Workflow

1. Identify target engines, markets/languages and a small repeatable set of real customer questions. Distinguish brand mention, source citation, recommendation, referral and conversion; measure them separately.
2. Inspect what the platform can actually fetch. Important business/product facts should be available as accurate text and reachable through meaningful links; compare raw and rendered output without assuming they are identical.
3. Check factual authority: who owns the information, product identity, current price/stock/eligibility, delivery conditions, support and source dates. Resolve conflicting pages and third-party descriptions with evidence rather than publishing more contradictory pages.
4. Improve useful answers, headings and comparisons for readers. Use original evidence and primary-source citations where appropriate. Do not invent statistics, reviews, partnerships, author expertise or claims about the business.
5. Verify structured data against visible page content and the current platform-supported type. A visible FAQ can be useful without eligibility for Google FAQ rich results. Do not add deprecated or unrelated markup to chase AI citations.
6. Evaluate outcomes using repeated, dated observations with engine, locale, query and URL recorded. Search results vary; one answer does not establish universal ranking. Track real referrals/conversions where authorized. Mark unavailable accounts/metrics as unmeasured.

## Resolve upstream disagreements

- Some imported material suggests llms.txt, knowledge bundles or special content formats. Report these as optional experiments unless a current primary source documents support for the actual target service. Google's guide says such files are not a Google Search visibility requirement and are not a ranking shortcut.
- Fixed answer-block lengths, keyword density targets, vendor-study percentages and brand-mention correlations are not universal ranking rules or traffic forecasts. Use them only as attributed hypotheses when relevant.
- Search crawl permission and training permission are independent. Do not automatically allow all AI crawlers or claim this was necessary for citations.
- Never promise a number-one rank, guaranteed AI recommendation, immediate indexing, or measured uplift without the corresponding evidence. Do not confuse an agent-readiness audit with proof of search visibility.

Use the complementary `marketingskills:ai-seo` and `claude-seo:seo-geo` references for deeper content, prompt portfolio and answer-accuracy work, while retaining these evidence boundaries.
