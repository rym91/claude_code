# SEO and Traffic Acquisition for Niche Directory Websites (2025–2026)

Research date: 2026-11-09. Method: WebSearch only. WebFetch failed (ppc.land: DNS blocked), so every finding below rests on search-result snippets and summaries, not full-page reads. Most sources are SEO vendor or agency blogs. Primary Google docs are marked [PRIMARY]. Pre-2024 information is marked [OLDER].

## 1. Programmatic SEO for directories: page types, internal linking, schema, indexation, thin content

### Takeaway
Programmatic city, category × city and listing pages still work when each page is built from distinct structured data, such as attributes, counts, prices or local facts. Pages that only swap the city name into boilerplate are explicitly risky: they fall under the doorway-abuse and scaled-content-abuse policies, and Google tends to leave them in "Crawled – currently not indexed". Verifiable, directory-specific case studies with numbers are rare. Most published "case studies" are vendor marketing.

### Cited Findings
- **Nomad List model.** Nomad List (Pieter Levels) has detailed pages for thousands of cities. Each city page is rendered from structured attributes such as cost of living, internet speed, safety and weather. This is the canonical example of a "data-rich" pSEO directory. — [Zapier blog](https://zapier.com/blog/programmatic-seo.md); [Dirstarter blog, June 2026](https://dirstarter.com/blog/programmatic-seo-directory-websites)
- **OpenAlternative.** The Dirstarter founder reports that his pSEO directory OpenAlternative earns about $6,500/month. He sells directory software, so this is self-reported and he has a stake in it. — [Dirstarter](https://dirstarter.com/blog/programmatic-seo-directory-websites)
- **Big aggregators.** TripAdvisor, Yelp and Expedia use pSEO to build city-based directory pages. The source gives no metrics. — [Single Grain](https://www.singlegrain.com/?p=50536)
- **Vendor metrics are unverifiable.** Claims such as "20,000+ pages deployed / 1,200+ leads" (Scepter Marketing) or "11,400 auto-generated pages → $8,200/month in 9 months" come from vendor or anonymous sites with no named client or methodology. — [Scepter Marketing](https://sceptermarketing.com/?p=87173); [organicarbitrage case study](https://organicarbitrage.pages.dev/articles/case-study-programmatic-seo-8k-month)
- **Technical City.** An agency write-up credits Technical City with about 1.7M monthly organic visits from pSEO (Oct 2025). Its pages target tech long-tail queries rather than city pages. — [upGrowth](https://upgrowth.in/how-technical-city-pro-programmatic-seo-delivers-1-7m-monthly-organic-traffic/)
- **City-name swapping fails.** Pages that only swap a city name into otherwise identical boilerplate "will not rank and may trigger thin content penalties." — [Digital Applied, 2026](https://www.digitalapplied.com/blog/programmatic-seo-scale-content-templates-2026)
- **Doorway abuse covers city pages.** [PRIMARY] Google's spam policy defines doorway abuse as pages "created to rank for specific, similar search queries" that lead users to intermediate pages less useful than the final destination. Its examples include multiple pages or domains targeting specific regions or cities that funnel users to one page. — [Google Spam policies](https://developers.google.com/search/docs/essentials/spam-policies); [Search Engine Land doorway deep-dive](https://searchengineland.com/doorway-pages-seo-deep-dive-389786)
- **Scaled content abuse is about value, not method.** [PRIMARY] The policy applies whether content is produced by automation, by humans or by both. What counts is generating many pages primarily to manipulate rankings without adding value. — [Google Search Central blog, March 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies)
- **"Crawled – currently not indexed".** This status means Google crawled a page and chose not to index it. Practitioners tie it to thin or auto-generated pages, faceted navigation, filtered search results and "large-scale programmatic content generation". "Discovered – currently not indexed" leans more toward crawl prioritization. Fixes include stronger internal links, better content quality, and consolidating or differentiating near-duplicate templates. — [RightBlogger](https://rightblogger.com/blog/crawled-currently-not-indexed); [Linkbot](https://library.linkbot.com/what-causes-pages-to-fall-under-the-crawled-currently-not-indexed-status-in-google-search-console-and-how-can-i-resolve-it-effectively/); [copilotpost on pSEO indexing](https://copilotpost-ai.pages.dev/blog/seo-organic-growth/beyond-discovery-why-your-programmatic-seo-pages-arent-indexing-and-how-to-fix-it/)
- **Crawl budget thresholds.** Google's crawl-budget guidance is said to target very large sites: more than 1M pages with weekly changes, or more than 10k pages with daily changes. This came secondhand. I did not confirm it on Google's page in this session. — [Linkbot / RightBlogger summaries](https://rightblogger.com/blog/crawled-currently-not-indexed)
- **Unsupported "5% rule".** A vendor claims a site with more than 5% of pages unindexed looks low-quality to Google. No Google source supports this. — [SEO-Hacker](https://seo-hacker.com/crawled-not-indexed/)
- **Indexing ramp example.** One local-services pSEO case went from 127 indexed pages (Nov 2024) to more than 1,122 (Apr/May 2025). It was a single business, not a directory. — [ai-ranking-skool case study](https://ai-ranking-skool.pages.dev/post/local-seo-at-scale-a-case-study/)
- **ItemList carousels.** [PRIMARY] The beta carousel rich result for local listings needs `ItemList` as the top-level container, paired with `LocalBusiness` or a subtype. Requirements:
  - at least 3 items;
  - each item URL points to a different page on the same domain, and the summary page links out to detail pages;
  - every marked-up item is visible on the page;
  - use the most specific LocalBusiness subtype available.
  This fits directory "best X in Y" or category pages that link to listing pages. — [Google carousels (beta) docs](https://developers.google.com/search/docs/advanced/structured-data/carousels-beta); [SEJ coverage](https://www.searchenginejournal.com/google-updates-carousels-beta-structured-data-documentation/513701/)
- **Review stars on directories.** [PRIMARY/secondary] When a business controls reviews about itself, LocalBusiness/Organization pages are ineligible for star snippets. Third-party directories with genuine user reviews are the intended use case. Google updated its review-snippet docs on 2026-07-24 to target fake and undisclosed incentivized reviews (per TechWyse, not confirmed on Google's page). Violations can draw manual actions. — [TechWyse](https://www.techwyse.com/news/search-news/google-review-snippet-structured-data-incentivized-reviews); [Quantumweb](https://www.quantumweb.com.au/google-sets-strict-limits-on-review-snippets)
- **City × category clusters.** Agency playbooks describe city × category cluster templates with hub-to-spoke internal linking rules (city hub → category × city → listings, with breadcrumbs). No results are reported. — [Skyesol case study](https://skyesol.netlify.app/case-studies/directory-city-category-clusters-seo-scale.html)

### Inferences
- The defensible pSEO directory page is one where the data is the content: counts, filters, prices, hours, verified attributes, original reviews and photos. Templated prose padding is not.
- Generate category × city pages only where there are enough real listings, for example at least 3, which is also the ItemList minimum. Noindex or don't create empty and near-empty combinations, to avoid doorway, thin-content and crawl-waste problems.
- ItemList + LocalBusiness on hub pages and LocalBusiness on listing pages are low-risk, documented schema choices. Star markup is legitimate only for genuine first-party user reviews collected by the directory.

### Gaps
- No independently verified 2025–2026 case study of a niche local directory growing via pSEO, with traffic charts, was found.
- Google's crawl-budget page wording was not directly verified.
- No data on what share of pSEO directory pages typically get indexed.

## 2. Google policies and updates affecting directories (HCU 2022–2024, March 2024, 2025–2026 core updates, AI content guidance)

### Takeaway
Since 2024 the direction has consistently gone against "intermediary" sites. The helpful content system was folded into core ranking (March 2024). Scaled content, site reputation and expired domain abuse became spam policies. The March 2026 core update specifically shifted visibility away from aggregators, directories and comparison sites toward official, specialist and destination sources, and Yelp, TripAdvisor and job aggregators lost visibility. Google's AI-content guidance, updated Oct 2026, allows AI content but stresses human fact-checking and repeats the scaled-abuse warning.

### Cited Findings
- **March 2024 changes.** [PRIMARY] Google announced three new spam policies: expired domain abuse, scaled content abuse and site reputation abuse. Scaled content abuse builds on the older "automatically generated content" policy. — [Google Search Central blog, Mar 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies)
- **HCU folded into core.** With the March 2024 core update, the helpful content system was incorporated into core ranking, and Google said it would stop announcing standalone HCUs. No single signal now decides helpfulness. — [Search Engine Land](https://searchengineland.com/google-released-massive-search-quality-improvements-with-march-2024-core-update-and-multiple-spam-updates-438144); [Marie Haynes](https://mariehaynes.com/the-march-2024-core-update)
- **"45%" figure.** Google stated it expected a reduction in low-quality, unoriginal results. Secondary sources quote "45%" or "40%". Google's original figure was 40%, later reported as 45% achieved; neither was verified against Google in this session. — [Search Engine Land](https://searchengineland.com/google-released-massive-search-quality-improvements-with-march-2024-core-update-and-multiple-spam-updates-438144)
- **Site reputation abuse timing.** Enforcement began May 5, 2024. I did not confirm a November 2024 policy clarification in this session. — [Brafton](https://www.brafton.com.au/blog/seo/google-updates-spam-policies/)
- **HCU recoveries [OLDER for the hit].** Glenn Gabe documented roughly 400 sites hit by the September 2023 helpful content update, some of which started recovering with the June 2025 core update. — [Glenn Gabe on X](https://x.com/glenngabe/status/1943271061870534954); [Amsive June 2025](https://www.amsive.com/insights/seo/june-2025-core-update-winners-losers-trends/)
- **August 2025 spam update.** It reportedly targeted low-quality, large-scale AI content and site reputation misuse. Gabe noted a client's competitor tanked with it. — [SEO Kreativ](https://www.seo-kreativ.de/en/blog/google-august-2025-spam-update-officially-complete/); [Glenn Gabe on X](https://x.com/glenngabe/status/1961052653602963812)
- **December 2025 core update.** It hit YMYL and finance sites heavily. Trustpilot, a review platform, gained about 39% visibility (Sistrix). Thesaurus.com gained about 33%. Quora kept declining. Gabe also reported "spammy listicle" sites, including ones using doorway pages, dropping heavily. — [Amsive Dec 2025](https://www.amsive.com/insights/seo/googles-december-2025-core-update-winners-losers-analysis/); [Glenn Gabe on X](https://x.com/glenngabe/status/2000568343296671946)
- **March 2026 core update.** It ran March 27 to April 8, 2026, after a brief spam update. Aleyda Solis's Sistrix analysis found gains for official, institutional, branded and specialist sources, and losses for aggregators, directories and comparison-driven sites.
  - Job aggregators ZipRecruiter and Glassdoor lost ground, while USAJobs and Amazon.jobs surged.
  - About 80% of top-3 results shifted, and nearly 1 in 4 top-10 pages fell out of the top 100 (SE Ranking data).
  - Sources: [Search Engine Land](https://searchengineland.com/march-2026-google-core-update-what-changed-474397); [PPC Land](https://ppc.land/march-2026-google-core-update-hit-aggregators-harder-than-december/); [TechWyse](https://www.techwyse.com/news/industry-news/google-march-2026-core-update-aggregators-ugc-visibility-loss)
- **Yelp and travel aggregators in March 2026.** Amsive's Sistrix data lists Yelp at −33.1 visibility points in a losers group alongside TripAdvisor and Expedia. In Germany, Sistrix counted about 4 losers for every winner (134 vs 32). — [Amsive March 2026](https://www.amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/); [casinokrisa summary of Sistrix DE](https://casinokrisa.com/blog/2026-04-10-march-2026-google-core-update-sistrix-finds-4-1-ratio-of-losers-to-winne)
- **May 2026 core update.** It completed June 2, 2026. Analysts argue "directories and near-me pages all got crushed" is too simple. In their view, derivative pages that repackage other sources lost, while primary destinations and original sources held or gained. — [Frase](https://www.frase.io/blog/may-2026-google-core-update-recovery); [Digital Applied May vs March](https://www.digitalapplied.com/blog/may-vs-march-2026-core-updates-pattern-comparison)
- **Possible later 2026 update.** I found no confirmed June–Oct 2026 core update. One source forecast one for June–July 2026, but that is unverified.
- **AI-content guidance.** [PRIMARY] Google's "using generative AI content" page says AI content must meet Search Essentials and spam policies. Using gen-AI "to generate many pages without adding value for users may violate Google's spam policy on scaled content abuse." An Oct 1, 2026 update says manual fact-checking and review of AI content, including titles, schema and alt text, is "critical". — [Google Search Central](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content); [Search Engine Land](https://searchengineland.com/google-search-now-says-its-critical-to-manually-factcheck-and-review-all-ai-generated-content-for-accuracy-and-trustworthiness-493070); [SE Roundtable](https://seroundtable.com/google-updates-ai-content-guidelines-factcheck-review-42217.html)

### Inferences
- A new niche directory must look like a destination or primary source, not an intermediary. That means original data such as verified attributes, its own reviews and photos, editorial testing and expertise, and pricing surveys. Repackaged Google Maps or Yelp data is exactly the profile that lost in March 2026.
- AI-written listing descriptions at scale are allowed in principle but risky unless they are human-reviewed and add facts not available elsewhere.
- Niche or specialist directories in a vertical where no strong aggregator exists likely fare better than generic local directories. This matches the "specialist sites win" reading of March 2026 ([Nikki Pilkington](https://nikki-pilkington.com/march-2026-core-update-small-business/)).

### Gaps
- No named small niche directories were documented as hit or benefiting in 2025–2026. The documented data covers big aggregators only.
- November 2024 site reputation abuse clarification: not verified in this session.
- Whether any core update ran between June and November 2026: unconfirmed.

## 3. Impact of AI Overviews / AI Mode / ChatGPT search on directory and "best X near me" traffic; how directories get cited by LLMs

### Takeaway
Pure "near me" transactional queries are still dominated by the local pack, with AI Overviews (AIO) appearing on only about 15%. Informational local queries ("how long does X take", "best X for Y") are heavily covered by AIO. When an AIO is present, clicks to top results drop sharply, by about 58–61%. AI Mode is reportedly about 93% zero-click. Directories, especially Yelp, are among the most-cited local sources in LLM answers, but the share varies wildly by engine and vertical. Being cited inside an AIO roughly doubles clicks versus not being cited.

### Cited Findings
- **AIO vs local pack on "near me" queries.** Whitespark 2025 research (via secondary write-ups): AIO appears on about 15% of direct "near me" searches, versus about 93% for the local pack. The local pack shows on more than 90% of simple transactional local queries. — [Minneapolis Made](https://www.minneapolismade.com/blog/how-ai-changing-google-local-search/); [ALM Corp](https://almcorp.com/blog/how-ai-is-impacting-local-search/); primary: [Whitespark](https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/)
- **Informational local queries.** AIO appears about 92% of the time on queries like "how long does an eye exam take near me". — [SEJ](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/580757/)
- **Overall AIO prevalence on local queries is disputed.** One figure is 68% (with local pack at 39%); another is 7.9%. Results depend on the query set. — [SEJ](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/580757/); [The Stacc](https://thestacc.com/blog/ai-overviews-local-search-impact/)
- **CTR loss with AIO.** Ahrefs (Feb 2026): about 58% lower CTR for the top-ranking page when an AIO is present. Seer's earlier work found about a 61% drop. — [Soci.ai stats](https://www.soci.ai/blog/local-seo-statistics/); [ziptie.ai](https://ziptie.ai/blog/click-behavior-in-zero-click-search/)
- **Seer Interactive, April 2026 update.** The dataset covered 53 brands, 5.47M queries and 2.43B impressions (Jan 2025–Feb 2026). Organic CTR bottomed at about 1.31% in Dec 2025, then partly recovered. Brands cited inside an AIO got about 20,700 clicks per 1M impressions, versus about 9,400 for uncited brands on the same SERPs. Figures vary across secondary reports. — [AWR organic CTR](https://www.advancedwebranking.com/seo/organic-ctr); [jbimpact](https://www.jbimpact.com/en/post/ai-search-statistics-2026)
- **Zero-click rates.** AI Mode is about 93% zero-click, versus about 83% with AIO (attributed to Seer/Semrush; original not verified). Similarweb: about 83% zero-click when an AIO is present versus about 60% without. SparkToro/Similarweb: 68% of US Google searches end without a click (up from 60.5% in 2024). — [Arfadia](https://www.arfadia.com/blog/zero-click-search-statistics-2026/); [newlifemarketing](https://newlifemarketing.ca/articles/google-ctr-ai-overviews-2026/); [Moxie Digital](https://www.moxie-digital.com/blog/zero-click-search-strategy)
- **BrightLocal local AI study (~200k local AI searches).** Google Business Profile is the top source. Yelp is the most-cited domain at about 8.5% of all local AI citations, with a higher share in ChatGPT. TripAdvisor is well behind. — [BrightLocal research](https://www.brightlocal.com/research/local-ai-visibility-study/); [BrightLocal AI directory sources](https://www.brightlocal.com/resources/ai-directory-sources/)
- **Yelp and "near me".** Nearly half of Yelp's AI citations came from "near me" queries in Q4 2025. This is a vendor analysis. — [Foundation Inc.](https://foundationinc.co/lab/yelp-ai-local-discovery/)
- **Yext, Oct 2025 (6.8M citations).** 48.73% of ChatGPT citations came from third-party sites such as Yelp, TripAdvisor and MapQuest. Gemini leans toward brand websites. — via [cheers.tech](https://www.cheers.tech/geo-academy/what-sources-does-chatgpt-use)
- **Contradicting data.**
  - A home-services study of 9,434 ChatGPT answers found Yelp in only 0.6% of text citations; Expertise.com and Angi were cited more. Yet 34% of ChatGPT map business cards linked to Yelp pages.
  - A Peekl Gemini study found Yelp and TripAdvisor were never cited.
  - A restaurant test of 110 questions found no answer relied on Google, Bing, Apple or Yelp pages. Its authors stress multiple independent sources agreeing.
  - Sources: [cheers.tech](https://www.cheers.tech/geo-academy/ai-search-engine-source-differences); [Peekl](https://peekl.io/ai-visibility/guides/which-websites-does-ai-trust); [Clairon](https://clairon.ai/blog/how-local-businesses-get-cited-by-ai-search)
- **Citation volatility.** Semrush measured ChatGPT's Reddit citations falling from about 60% to about 10% within six weeks in late summer 2025. — via [cheers.tech](https://www.cheers.tech/geo-academy/what-sources-does-chatgpt-use)
- **Whitespark 2026 ranking factors.** The 2026 edition added an "AI search visibility" category for the first time. Presence on third-party "best of" lists, plus unstructured mentions in news, blogs and associations, is cited as a reputation factor. — [Whitespark LSRF 2026](https://whitespark.ca/local-search-ranking-factors/); [Harmo summary](https://harmo.me/en/blog/local-seo-ranking-factors-2026-whitespark)

### Inferences
- For a niche directory, LLM citation looks attainable in specialist verticals. Expertise.com and Angi beating Yelp in home services shows vertical-specific directories can out-cite generic ones. Useful levers:
  - curated "best X in Y" pages with explicit selection criteria;
  - structured, extractable facts;
  - consistency with other sources.
- Pure "X near me" traffic is mostly lost to the local pack and maps. AIO hits informational and comparison local queries. Either way, directories should expect lower CTR per ranking and should measure AI citations and brand mentions too.

### Gaps
- No study measured directory (non-Yelp) organic traffic change attributable to AIO or AI Mode.
- Seer's original AI Mode 93% report was not found.
- BrightLocal's "Yelp in 80% of ChatGPT local answers (Aug 2026)" and "33%" figures appear in secondary posts but are unverified and conflict with the 8.5% figure.

## 4. Competition with Google Maps local pack and big aggregators: which queries directories can still win

### Takeaway
Directories can't realistically win the local pack. It is ranked on GBP category, proximity and GBP title, and it shows on more than 90% of transactional local queries. Big aggregators were also hit in March 2026. The remaining openings are organic results for informational and comparison queries, niche attributes local packs can't express, and specialist verticals where a destination-quality niche site can beat a generic aggregator.

### Cited Findings
- **Local pack factors (Whitespark LSRF 2026).** Top factors are primary GBP category, proximity to the searcher, and keywords in the GBP title, followed by a physical address in the city and being open at search time. GBP signals lead the pack (32%), while on-page signals lead local organic (33%). The study surveyed 47 experts on 187 factors, so it is opinion, not correlation data. — [Whitespark](https://whitespark.ca/local-search-ranking-factors/); [Soci Local Memo](https://www.soci.ai/blog/local-memo-local-ranking-factors-of-2026-have-arrived/)
- **Review recency.** It rose from #93 (2023) to #11 (2026). Citations are now "needed for consistency but no longer a key differentiator." — [gmbapi comparison](https://gmbapi.com/news/local-ranking-factors-comparison-2026-2023/); [seomadman](https://seomadman.com/reports/whitespark-local-ranking-factors-2026)
- **Aggregators lost in March 2026.** Yelp, TripAdvisor, Expedia and job aggregators lost, while specialist and official sites gained. — [Amsive](https://www.amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/); [Search Engine Land](https://searchengineland.com/march-2026-google-core-update-what-changed-474397)
- **AIO concentrates on informational local queries.** It appears about 92% of the time on informational "near me" queries but only about 15% on pure "near me". — see Section 3 sources ([SEJ](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/580757/))
- **Specialist directories in ChatGPT.** Expertise.com and Angi out-cite Yelp in ChatGPT home-services answers. — [cheers.tech](https://www.cheers.tech/geo-academy/ai-search-engine-source-differences)

### Inferences
Query types a niche directory can plausibly still win (inference from the above, not measured):
- attribute or long-tail queries such as "dog-friendly coworking in Lisbon" or "Russian-speaking dentist in Barcelona", which GBP categories can't express;
- "best X in Y" curated lists with original evaluation;
- comparison and price queries ("X cost in Y");
- cross-city or regional discovery and non-local niches (tools, remote services);
- queries in secondary geos and languages where Yelp and TripAdvisor are weak.

Expect "plumber near me" style queries to be unwinnable.

### Gaps
- No data on organic CTR for directory results below the local pack.
- No quantified study of which "best X in Y" SERPs still show directories in the top 10 in 2026.

## 5. Link building and traffic sources specific to directories

### Takeaway
The directory-native link tactic is giving listed businesses embeddable "listed on / featured on" badges that link back. It is legitimate as long as links aren't sold or required in exchange for placement, which could trip Google's link-spam policy. Off-Google channels such as Reddit, X, Product Hunt and HN for launch, plus a same-niche newsletter and Bing, are repeatedly cited by practitioners, but evidence is anecdotal.

### Cited Findings
- **Badge example.** BroadbandSwitch.uk offers listed providers embeddable badge code linking to their directory profile, and explicitly states the badge doesn't affect listing placement. — [broadbandswitch badge page](https://broadbandswitch.uk/broadband-providers/badge/?p=o2-business)
- **Directory link value.** Directory backlinks in general have "diminished" SEO value. Editorially curated, authoritative directories carry more weight than open link farms. — [Dirstarter guide, Nov 2025](https://dirstarter.com/blog/guide-to-website-directories); [swipeinsight](https://web.swipeinsight.app/posts/20-web-directories-that-still-offer-value-6488)
- **Paid featured listings.** Paid "featured listing" products, such as Entireweb's 30-day featured placement, are a common monetization model and are advertised for backlinks. — [Entireweb](https://www.entireweb.com/directory/)
- **Link spam policy.** [PRIMARY, general] Google's spam policies include link spam, such as buying or selling links for ranking. Paid or required reciprocal links should be `rel="sponsored"` or nofollow. — [Google Spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- **Launch channels and newsletter funnel.** Niche directories are "fairly easy to get traffic to" by sharing on X, Reddit, Product Hunt and Hacker News. Practitioners recommend starting a same-niche newsletter that funnels readers to the directory. This is advice, not measured results. — [Niche Site Growth newsletter](https://nichesitegrowth.beehiiv.com/p/directories-still-have-massive-potential)
- **Bing.** Bing has about 4% market share but can drive real traffic in large niches. One practitioner site got 45% of its traffic from Bing while Google contributed little. — [Niche Site Growth: niche sites alive on Bing](https://nichesitegrowth.beehiiv.com/p/niche-sites-are-still-alive-on-bing); [Bing site progress](https://nichesitegrowth.beehiiv.com/p/my-bing-site-s-progress-and-free-access-to-publish-owl)
- **Directory exit.** A founder built and sold an SEO-optimized directory monetized with affiliate links and ad spots. — [No Code Exits](https://nocodeexits.substack.com/p/how-katt-built-and-sold-a-seo-optimized)
- **Reddit results are anecdotal.** In one case, a week of engagement across 35 subreddits yielded 18 newsletter subscribers. Another headline claims one Reddit comment drove 1,500 subscribers (unverified). — [tiiny.site case study](https://newsletterprojectcasestudy.tiiny.site/); [pulse.bot](https://www.pulse.bot/media/news/day-25-how-one-reddit-comment-drove-1500-newsletter-subscribers-ef6041cc-67a4-44f8-b38e-ea80f3a060ad/)
- **"Best of" mentions.** Presence on third-party "best of" lists and editorial mentions is a reputation and AI-visibility factor. This gives listed businesses a reason to link to "named best X in Y by [directory]". — [Harmo / Whitespark 2026](https://harmo.me/en/blog/local-seo-ranking-factors-2026-whitespark)

### Inferences
- Outreach to listed businesses works best through a free "Verified / Top-rated on [Directory] 2026" badge or award, a claim-your-listing flow, and annual awards. Avoid making the backlink a condition of being listed or ranked, so it doesn't count as a link scheme.
- Bing and Bing-fed engines matter more now. ChatGPT search has historically used Bing's index, though I did not verify that in this session. This makes Bing Webmaster Tools and IndexNow worth setting up for a new directory.

### Gaps
- No quantified study of badge-driven link acquisition rates for directories.
- No data on Reddit referral traffic to directories specifically, or on Reddit link and self-promotion rules as they apply to directory owners.
- The ChatGPT/Bing index dependency was not verified in this session.

## 6. Time to rank for a new domain; expired and aged domains

### Takeaway
New domains are slow. Common estimates are 6+ months for meaningful keywords, and Ahrefs-attributed data (secondhand) says only a small share of new pages reach the top 10 within a year. Expired domains can speed things up, but repurposing one mainly to manipulate rankings with unrelated or low-value content is a named spam policy (expired domain abuse, March 2024). Topical continuity is the key safety signal.

### Cited Findings
- **Expired domain abuse.** [PRIMARY] Google introduced the expired domain abuse policy in March 2024. It covers buying an expired domain and repurposing it primarily to manipulate rankings by hosting low- or no-value content. — [Google Search Central blog](https://developers.google.com/search/blog/2024/03/core-update-spam-policies); [onlinedomain.com](https://onlinedomain.com/2024/03/06/domain-name-news/google-new-spam-policy-expired-domain-abuse)
- **Topical continuity.** Buying an expired domain is not automatically abuse. A topical mismatch, such as a medical blog turned into gambling affiliate content, is a common red flag. Google may treat expired domains as fresh starts. — [catches.io](https://catches.io/blog/expired-domain-history-not-seo-shortcut); [on-page.ai](https://blog.on-page.ai/reviving-a-20-year-old-dead-domain-what-seos-need-to-know/); [WebProNews](https://www.webpronews.com/google-treats-expired-domains-as-new-seo-risks-and-tips)
- **Expired-domain case.** A Reddit-documented case grew a revived expired domain from 150 monthly visitors (month 1) to more than 7,000 (month 4). — [on-page.ai](https://blog.on-page.ai/reviving-a-20-year-old-dead-domain-what-seos-need-to-know/)
- **New vs aged timelines.** A new site often needs 6+ months to rank for important keywords, while an aged domain may see gains in weeks to months (registrar source, which has a commercial interest). — [Name.com](https://www.name.com/es-la/blog/expired-domains-and-seo-buying-domain-names-with-traffic)
- **Ahrefs-attributed figures (secondhand, unverified).**
  - About 1.74% of new pages reach the top 10 within a year.
  - The average top-ranking page is about 5 years old.
  - Of pages that reach the top 10, about 41% do so within a month, mostly on established domains.
  - Source: [sulat.com](https://sulat.com/p/domain-buying-guide)
- **Older context [OLDER].** Rankings return about 30 days after an expired domain is renewed by the same owner. This is a 2014-era SE Roundtable item. — [SE Roundtable](https://www.seroundtable.com/google-ranking-domain-expire-19015.html)
- **Unconfirmed claim.** One source says a March 2026 update made expired-domain enforcement "more precise". No corroboration was found. — [on-page.ai](https://blog.on-page.ai/reviving-a-20-year-old-dead-domain-what-seos-need-to-know/)

### Inferences
- For a multi-geo directory network, a same-topic aged domain is lower risk than an unrelated one. Still, plan for a 6–12 month Google ramp on a new domain and lean on Bing, social, newsletter and outreach traffic in the meantime.
- Putting new geo directories as subfolders on one established domain likely ranks faster than separate new ccTLDs. This is inference; I found no source in this session.

### Gaps
- The original Ahrefs studies on page age and time-to-rank were not retrieved. Treat those figures as unverified.
- No 2025–2026 data on how long new directory domains specifically take to rank.
- No source compared subfolder vs ccTLD vs subdomain for multi-geo directories in 2025–2026.
