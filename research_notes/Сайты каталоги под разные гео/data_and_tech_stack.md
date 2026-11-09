# Niche Directory Sites: Data Acquisition, Cleaning/Enrichment, Tech Stack and Costs (as of 2026-11-09)

Method note: research done via WebSearch only. WebFetch of developers.google.com failed (DNS blocked in this environment), so no official vendor page was read in full. Most prices below come from search snippets of third-party reviews and calculators, some written by competitors. Treat every price as "verify on the vendor page before budgeting". Where sources conflict, both figures are given.

## 1. Data acquisition: sources and price per 1,000 records

### Takeaway
Scraper APIs for Google Maps are cheapest at roughly $0.6–$3 per 1,000 places for base data, rising to about $6–$14 per 1,000 with emails, reviews and photos. The official Google Places API (New) is about $17–$40 per 1,000 for useful fields above the free caps and its terms restrict storing data, so it is a poor fit for bulk directory building. OSM/Overpass is free but needs ODbL attribution.

### Cited Findings
**Google Places API (official, after the March 2025 pricing change)**
- The March 2025 change replaced the shared $200/month credit with per-SKU free monthly caps: 10,000 calls for Essentials SKUs, 5,000 for Pro, 1,000 for Enterprise (Enterprise + Atmosphere shares the 1,000 cap). Caps do not pool across SKUs — [Woosmap](https://www.woosmap.com/blog/google-places-api-pricing); [OpenPlacesAPI](https://openplacesapi.com/blog/google-places-api-pricing); [bizcollect.dev](https://bizcollect.dev/blog/google-places-api-pricing)
- Paid rates per 1,000 at the first paid tier (0–100K): Place Details Essentials $5, Pro $17, Enterprise $20, Enterprise + Atmosphere $25. Text Search Pro $32, Enterprise $35, Enterprise + Atmosphere $40 — [OpenPlacesAPI cost calculator](https://openplacesapi.com/google-places-api-cost-calculator); [leadmarina](https://leadmarina.com/blog/google-places-api-pricing)
- The IDs-only SKUs (Text Search Essentials IDs Only, Place Details Essentials IDs Only) are free with no cap. Billing must be enabled even to use the free calls — [scavio.dev](https://scavio.dev/glossary/google-maps-places-api-cost); [crustapi](https://crustapi.com/google-places-api-pricing)
- Caveat: all of the above come from third-party pages that say rates are unchanged since March 2025. Google's own pricing page was not retrieved because the fetch was blocked.
- Google Maps Platform terms let you cache Place IDs indefinitely. Other content can only be cached for limited periods (for example, lat/lng for up to 30 consecutive days, then deleted) — [Google Maps Platform Service Specific Terms](https://cloud.google.com/maps-platform/terms/maps-service-terms/index-20240522)
- Third-party summary of the terms: they restrict "caching, pre-fetching, bulk downloading, or scraping" Maps data beyond what the API docs permit — [Conduct Atlas](https://conductatlas.com/platform/google-maps/google-maps-platform-terms-of-service/no-scraping-or-content-extraction/)

**Outscraper**
- First 500 businesses free, then $3 per 1,000 up to 100,000, then $1 per 1,000 above 100k — [Outscraper pricing explained](https://outscraper.com/outscraper-pricing-explained/); [Salesforge review](https://www.salesforge.ai/blog/outscraper-reviews)
- Add-ons are billed on top. Per a competitor's breakdown: email enrichment +$3, email validation +$3, reviews +$2, photos +$3 per 1,000, about $14/1,000 for full lead data. Another estimate is about $9/1,000 with verified emails. A third lists phone enrichment at +$5/1,000. All three are competitor or third-party claims — [leadscrape](https://www.leadscrape.com/outscraper-vs-lead-scrape.html); [scrap.io](https://scrap.io/outscraper-pricing); [syncgtm](https://syncgtm.com/blog/outscraper-review-2026)

**Apify**
- Compass "Google Maps Scraper" (crawler-google-places) is listed "from $2.10 per 1,000 scraped places". The rate is tiered by plan, and add-ons such as contact details cost extra — [Apify Store](https://apify.com/lp/scrape-google-maps)
- Compass "Google Maps Extractor" (a separate actor) shows $6.00 per 1,000 on one page — [Apify](https://apify.com/compass/google-maps-extractor/pricing)
- Cheaper community actors advertise about $1 per 1,000 places — [Apify actor](https://apify.com/fancyboeing/my-actor/api)

**DataForSEO**
- Pay-as-you-go with a $50 minimum deposit and no subscription — [DataForSEO pricing](https://dataforseo.com/pricing)
- Google Maps SERP costs $0.0006 per SERP page (Standard queue), $0.0012 (Priority) or $0.002 (Live), i.e. $0.60 / $1.20 / $2.00 per 1,000 tasks. A task can return up to about 100 places, so the cost per place is far lower — [DataForSEO Google Maps SERP API](https://dataforseo.com/pricing/serp/google-maps-serp-api); [apiserpent comparison](https://apiserpent.com/blog/google-maps-api-pricing-comparison)
- Business Data API figures conflict. One source gives Business Listings at $0.012/task + $0.00036/item. Another gives Google My Business Info at $0.0015 (Standard) / $0.0054 (Live) per profile and Google Reviews at $0.00075 per 10 reviews — [marketintelligencetools](https://marketintelligencetools.com/reports/dataforseo-pricing/); [openwebninja](https://www.openwebninja.com/blog/best-google-maps-apis-2026)

**SerpApi**
- Reported plans: free 250 searches/month; Starter $25/mo for 1,000 searches; Production $150/mo for 15,000 searches. These are third-party figures, not SerpApi's own page. With about 20 results per Maps page this works out to roughly $0.5 per 1,000 places at the Production tier (my calculation, see Inferences) — [openwebninja](https://www.openwebninja.com/blog/best-google-maps-apis-2026); [apiserpent](https://apiserpent.com/blog/google-maps-api-pricing-comparison)

**Yelp**
- In August 2024 Yelp Fusion moved to paid plans: Starter $7.99, Plus $9.99 and Enterprise $14.99 per 1,000 calls (300 and 500 calls/day quotas on the lower tiers). The developer community called this "outrageous" — [App Developer Magazine](https://appdevelopermagazine.com/yelp-fusion-api-outrageous-new-pricing/)
- The current Yelp page shows monthly plans: "Enhanced" $229/mo and "Premium" $643/mo after a 30-day trial, with overages in 1,000-call blocks. This conflicts with the 2024 per-call list — [Yelp Places API page (mirror)](https://scriptagc.wasmer.app/https_business_yelp_com/data/products/fusion); [supergood.ai](https://supergood.ai/api-report-card/yelp)

**OpenStreetMap / Overpass**
- The ODbL permits commercial use with no fees for the data. Attribution is required, and enhancements to the data must be shared back — [OSMF Licence and Legal FAQ](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ); [OSM wiki License/Use Cases](https://wiki.openstreetmap.org/wiki/License/Use_Cases)
- In a "collective database" (OSM data alongside your own data), share-alike applies only to the OSM-derived part. Whether a directory's combined output triggers share-alike depends on its architecture — [OSM wiki legal structure](https://wiki.openstreetmap.org/wiki/License/Legal_Structure)
- Public Overpass instances (e.g., FOSSGIS) have their own usage terms. They do not apply to self-hosted instances or raw OSM extracts — [FOSSGIS terms](https://fossgis.de/arbeitsgruppen/osm-server/nutzungsbedingungen)

### Inferences
- Rough cost of 50,000 raw Google Maps records: Outscraper about $150 base ((50,000 − 500) × $3/1k), Apify Compass about $105+, DataForSEO a few dollars of tasks plus the $50 minimum deposit. With the official Places API, Text Search Pro plus Details Enterprise would run about $1,000–$2,750 above the free caps. The official API is 10–50x more expensive and restricts persistent storage.
- SerpApi per-place cost assumes about 20 results per Maps page ($150/15,000 searches ≈ $0.01/search, about 20 places each, ≈ $0.5/1k). This is my calculation, not a cited figure.
- OSM is a good free seed for categories that are well tagged (e.g., camp sites, EV chargers, playgrounds, dog parks). Coverage of phone, hours and website is usually weaker than Google's (general knowledge, not verified in this session).

### Gaps
- Government open-data registries (business registries, health inspection, licensing databases, EU/Spain registries) were not searched due to the tool budget. No cited material on them.
- Google's official pricing page could not be fetched (DNS blocked). The Places Photo SKU price and Nearby Search prices were not confirmed.
- No official SerpApi pricing page in the results.

## 2. Data cleaning and enrichment (dedupe, verification, website crawling, LLMs, images)

### Takeaway
The 2025–2026 practitioner pattern is: scrape 50–70k raw rows, then clean, dedupe and filter with Claude Code in passes, then crawl each business site with Crawl4AI (free, open source) to verify it and extract niche attributes, then use an LLM to tag attributes and write descriptions, then curate images with a vision model. A widely shared case put the total under $250 and 4 days. Expect heavy attrition: tens of thousands of raw rows often shrink to hundreds or low thousands of real niche listings.

### Cited Findings
- Frey Chu (via the Greg Isenberg / Startup Ideas Podcast) built a luxury restroom trailer directory, "fully enriched", in about 4 days for under $250, described as replacing 2,000+ hours of manual work. The directory reportedly earns about $273/day — [Startup Ideas Podcast](https://www.podbean.com/media/share/dir-8aqk6-2b2b4336); [Whatfinger summary](https://startup.whatfinger.com/2026/02/16/claude-code-built-me-a-273-day-online-directory/)
- Workflow per Greg Isenberg's thread: (1) scrape 50k–70k raw records with Outscraper; (2) use Claude Code to clean, dedupe and structure the data in passes; (3) run Crawl4AI to verify live sites and filter junk; then enrich and publish — [Greg Isenberg on X](https://x.com/gregisenberg/status/2023459273590661143)
- Line-item budget of a similar build: Claude Code Max subscription $100, data acquisition $100, Claude API credits $50 for deep cleaning. Image curation with Claude Vision is about $30 for about 700 listings (about $0.04/listing). This is a secondary write-up, not audited spend — [GeekTak](https://www.geektak.com/blog/build-automated-online-directories-with-claude)
- Crawl4AI is open source and free. You pay only for infrastructure, proxies and any LLM calls — [ScrapingBee Crawl4AI guide](https://www.scrapingbee.com/blog/crawl4ai/)
- Firecrawl credit costs: 1 credit per page for scrape and crawl, 1 per map call, 2 per 10 search results. JSON/LLM extraction is about 5 credits/page (1 scrape + 4 extract). Stealth mode is +4/page — [activepieces](https://www.activepieces.com/blog/firecrawl-pricing-2026-plans-credits-and-real-costs.md); [tinyfish](https://www.tinyfish.ai/blog/firecrawl-pricing); [Firecrawl pricing](https://www.firecrawl.dev/pricing)
- Firecrawl plans (sources vary): Hobby about $16–19/mo for 3,000–5,000 credits; Standard about $83–99/mo for 100k credits; Growth about $333/mo (annual) for 500k; free tier 500 one-time or 1,000/month depending on source. Credits do not roll over — [eesel](https://www.eesel.ai/blog/firecrawl-pricing); [dev.to teardown](https://dev.to/beton/firecrawl-pricing-teardown-2026-2eh8)
- Claude Haiku 4.5 lists at $1 per million input tokens and $5 per million output tokens. The Batch API is reported at 50% off ($0.50/$2.50). One aggregator disputes the batch discount for Haiku; Anthropic's page was not fetched — [morphllm](https://www.morphllm.com/anthropic-claude-api-pricing); [pecollective](https://pecollective-com.pages.dev/tools/claude-pricing-guide/)
- A typical cleaning filter drops listings with no name or street address, permanently or temporarily closed businesses, and entries off-niche by name or category — [skills.cat directory skill](https://skills.cat/skills/sikefury/online-directory-create-expert)
- Dedupe: use the normalized website domain as the primary key, then fuzzy name matching when the domain is missing. An alternative is a deterministic key, or normalized name + location, keeping the most complete row — [Scrappey](https://scrappey.com/qa/web-scraping-apis/best-scraping-api-for-lead-generation); [fitgap guide](https://us.fitgap.com/stack-guides/scaling-directory-and-database-research-without-manual-copy-paste)
- Apify has ready-made dedupe actors for Google Maps output: cross-run dedupe, and exact plus fuzzy dedupe with an audit trail — [Google Maps Deduper](https://apify.com/broomwagon/google-maps-deduper); [Dataset Deduper](https://apify.com/broomwagon/dataset-deduper.md)
- Attrition example: an Outscraper user reported only 500 workable leads out of 16,000 after cleaning (anecdotal, Trustpilot) — [Trustpilot](https://pt.trustpilot.com/review/outscraper.com)
- Images: Google Places photos require on-screen attribution wherever they are displayed. Google Images' "Licensable" badge does not grant reuse rights — [Places Photos docs](https://developers.google.cn/maps/documentation/places/web-service/photos?hl=en); [Google blog on licensing info](https://www.blog.google/products/search/learn-how-find-image-licensing-information-google-images/)

### Inferences
- LLM cost per record (my estimate, not cited): about 3k input tokens (cleaned website text) plus about 400 output tokens (attributes JSON and a 100-word description) on Haiku 4.5 ≈ $0.005/record at list price, about $0.0025 with batch. That is about $25–50 per 10k listings. Sonnet-class models cost roughly 3x more.
- Website crawl cost: Crawl4AI is effectively $0 plus compute for a few thousand sites. Firecrawl extraction at 5 credits/page means 10k sites ≈ 50k credits, which fits the Standard tier (about $83–99/mo).
- Safest image sources: the business's own website (with permission or an outreach claim flow), owner-uploaded photos, licensed stock, or AI or generic category images. Hot-linking or re-hosting Google Maps photos outside the API terms is risky.

### Gaps
- No primary benchmarks for website-verification accuracy or LLM hallucination rates in attribute extraction.
- No dedicated sources found on phone/email verification services pricing beyond Outscraper add-ons.

## 3. Platforms: WordPress plugins vs SaaS vs custom code

### Takeaway
WordPress plus a directory plugin costs about $100–230/yr for the plugin plus about $99/yr for multilingual support. It has the most SEO and monetization features but needs performance tuning at 10k+ listings. SaaS (Brilliant Directories, eDirectory) costs about $40–199/mo, is turnkey and has lock-in. No-code (Directify, Webflow, Softr) is fast but item caps bite at scale. Webflow, for example, caps at 20k CMS items. Custom Next.js/Astro + Supabase costs about $0–45/mo and scales best for programmatic SEO, but requires development.

### Cited Findings
**WordPress directory plugins**
- Directorist: about $103/yr single site (vendor) or $129/yr (ACF comparison); lifetime about $379; 20k+ active installs; 30+ extensions — [Directorist comparison](https://directorist.com/blog/directorist-vs-hivepress-vs-geodirectory/); [ACF](https://www.advancedcustomfields.com/blog/best-wordpress-directory-plugin/)
- GeoDirectory: $139/yr single site, $229/yr unlimited sites; every plan includes all add-ons and themes. The free version cannot charge for listings (needs Pricing Manager) — [Dirstarter](https://dirstarter.com/blog/best-wordpress-directory-plugins); [GeoDirectory](https://wpgeodirectory.com/business-directory-software/)
- HivePress: core free; extensions $29–39 each or about $199 one-time bundle (another source says $99/yr bundle) — [Elegant Themes](https://www.elegantthemes.com/blog/wordpress/best-wordpress-directory-plugins); [HivePress blog](https://hivepress.io/blog/best-directory-website-builders/)
- Voxel (theme plus framework): licenses are single-use, multi-use or subscription. Price is reportedly from about $59/yr to $499 one-time, unverified and inconsistent across sources — [Voxel terms](https://getvoxel.io/terms-conditions/); [ciroapp](https://ciroapp-five.vercel.app/software/voxel)
- Business Directory Plugin: not covered by results (gap).
- Multilingual: WPML Multilingual CMS €99/yr (3 live sites), Blog €39, Agency €199. Polylang Pro from €99/yr, with automatic hreflang per Polylang's own page — [nexterwp](https://nexterwp.com/blog/wpml-vs-polylang-vs-translatepress/); [Polylang pricing](https://polylang.pro/pricing/)

**SaaS / no-code**
- Brilliant Directories: conflicting prices. The main site showed $97/mo or $997 lifetime; the account page showed $40/$80/$120 per month (Oct 2026); aggregators still show $145/mo or $1,450 lifetime. One site per subscription. Lock-in is a common criticism — [Dirstarter review](https://dirstarter.com/blog/brilliant-directories-review); [directorybuildr](https://directorybuildr.com/blog/brilliant-directories-a-smart-choice-for-building-a-member-directory/); [Capterra](https://www.capterra.com/p/133173/Brilliant-Directories/pricing/)
- eDirectory: Professional Cloud $99/mo (with branding); white-label Enterprise $199/mo; other lists give a $99–299 range — [joinit](https://joinit.com/blog/best-directory-website-builder); [directoryeasy](https://directoryeasy.com/blog/top-10-directory-website-builders-features-pricing-examples)
- Directify: Free (10 listings), Starter $12/mo (50 listings), Pro $39/mo (unlimited); up to $149/mo Agency. Vendor source — [Directify blog](https://directify.app/blog/best-directory-website-builders/)
- Webflow: the May 13, 2026 restructuring merged CMS and Business plans into "Premium" with 20,000 CMS items and 40 collections. The old limits were CMS plan 2,000 items, Business 10,000. Hitting the cap blocks new items but not published pages — [windowsforum](https://windowsforum.com/windows-news.4/webflow-premium-includes-20-000-cms-items-not-2-000.442190/); [webtonic](https://www.webtonic.io/blog/webflow-cms-collection-limits); [rapidevelopers](https://www.rapidevelopers.com/md/webflow-tutorials/webflow-cms-limits)

**Custom code**
- Supabase Pro $25/mo (includes $10 compute credit, i.e. one Micro instance, spend cap on by default). Vercel Pro $20/mo per seat plus bandwidth and function usage. Together about $45/mo before usage — [makerkit](https://makerkit.dev/blog/saas/supabase-pricing); [jetadmin](https://www.jetadmin.io/blog/vercel-vs-supabase/)
- Dirstarter (a Next.js directory boilerplate vendor) argues for skipping WordPress for code-first builds. Vendor bias — [Dirstarter](https://dirstarter.com/blog/best-wordpress-directory-plugins)

### Inferences
- For 10k+ pages and multiple geos/languages, a static or ISR site (Astro or Next.js) generated from a Postgres/Supabase table gives the best page speed and full control over JSON-LD (LocalBusiness, ItemList, BreadcrumbList) and hreflang. Hosting can be near-free on static hosts (Cloudflare Pages/Netlify) or about $45/mo on Vercel + Supabase.
- WordPress plugins (GeoDirectory, Directorist) include schema and maps out of the box and are easiest for monetization (paid listings, claims). Multilingual adds WPML/Polylang (about €99/yr) and duplicates listing posts per language, which multiplies the database size. At 10k+ listings, use good hosting, object caching and a CDN (general practice, not verified in this session).
- Webflow's 20k-item cap, and Directify/Softr's per-plan limits, make them weak for multi-geo programmatic directories past about 10–20k pages.

### Gaps
- Softr + Airtable record limits not retrieved.
- No benchmark sources found on WordPress directory plugin performance at 10k–100k listings.
- No Business Directory Plugin pricing found.

## 4. Typical MVP budget and time to launch

### Takeaway
An AI-assisted MVP directory (a few hundred to a few thousand curated listings) can launch in days to a couple of weeks for about $150–500 in data and AI costs, plus about $0–50/mo hosting. WordPress premium-plugin builds add about $100–350/yr in licenses. SaaS builds add $40–199/mo.

### Cited Findings
- The Frey Chu case: about 4 days and under $250 total (Claude Code Max $100, data $100, Claude API $50), plus about $30 for image curation of about 700 listings — [GeekTak](https://www.geektak.com/blog/build-automated-online-directories-with-claude); [Startup Ideas Podcast](https://www.podbean.com/media/share/dir-8aqk6-2b2b4336)
- HivePress compares directory builders by 3-year total cost (vendor source) — [HivePress](https://hivepress.io/blog/best-directory-website-builders/)

### Inferences
- Indicative stacks (my synthesis from the prices above):
  - Lean custom build: Outscraper or Apify ($50–150) + Crawl4AI ($0) + Claude API ($25–100) + Astro or Next.js on Cloudflare/Vercel ($0–20/mo) + Supabase (free–$25/mo) + domain ($10–15). Total about $100–300 upfront and $0–45/mo.
  - WordPress build: same data costs + GeoDirectory or Directorist ($103–229/yr) + WPML or Polylang (€99/yr, if multilingual) + managed hosting (about $20–50/mo, not cited).
  - SaaS build: same data costs + Brilliant Directories ($40–145/mo) or eDirectory ($99–199/mo).
- Time is dominated by data quality work, not site building. Expect 1–4 weeks for a solo builder.

### Gaps
- No survey data on median build time or budget across many directories; evidence is case studies and marketing claims ("under $250" is self-reported).

## 5. Legal and ToS risks (Google Maps scraping, hiQ v. LinkedIn, data licensing)

### Takeaway
In the US, scraping public pages is unlikely to violate the CFAA after hiQ v. LinkedIn (9th Cir. 2022) and Van Buren (2021). Breach of contract/ToS remains a live risk, and hiQ ultimately lost on contract and settled. Google's Maps terms prohibit scraping and bulk storage beyond allowed caching. Using third-party scrapers shifts the technical work but not the ToS exposure. OSM is legally clean with attribution.

### Cited Findings
- April 2022: after a Supreme Court remand in light of Van Buren, the 9th Circuit again upheld the preliminary injunction for hiQ, finding serious questions over whether LinkedIn could invoke the CFAA against scraping of public profiles — [Jenner & Block](https://www.jenner.com/en/news-insights/publications/client-alert-data-scraping-in-hiq-v-linkedin-the-ninth-circuit-reaffirms-narrow-interpretation-of-cfaa); [tradesecretslaw](https://www.tradesecretslaw.com/2022/05/articles/computer-fraud-and-abuse-act/ninth-circuit-reaffirms-that-data-scraping-from-public-websites-does-not-violate-the-computer-fraud-and-abuse-act/)
- Van Buren v. US (2021) narrowed the CFAA's "exceeds authorized access" prong. Commentators expect this to largely end CFAA claims based purely on terms-of-use violations — [Cooley](https://www.cooley.com/news/insight/2021/2021-06-09-us-supreme-court-computer-fraud-abuse-act-van-buren); [NatLawReview](https://natlawreview.com/article/taking-cue-supreme-court-s-van-buren-decision-ninth-circuit-releases-new-opinion)
- Late 2022: the district court found hiQ had breached LinkedIn's User Agreement, and the parties settled in December 2022. hiQ is restricted from using the scraped data without permission. Final approval of the settlement was not confirmed — [Wikipedia: hiQ Labs v. LinkedIn](https://en.wikipedia.com/wiki/HiQ_Labs_v._LinkedIn); [Proskauer](https://www.proskauer.com/insights/get-pdf/25755)
- Google Maps Platform terms limit caching to Place IDs (indefinitely) and short-term content windows (e.g., 30 days for lat/lng) — [Google Maps service terms](https://cloud.google.com/maps-platform/terms/maps-service-terms/index-20240522)
- Third-party summary: Google's terms restrict scraping and bulk downloading, and contractual restrictions are generally enforceable in commercial contexts (not a legal opinion) — [Conduct Atlas](https://conductatlas.com/platform/google-maps/google-maps-platform-terms-of-service/data-caching-and-bulk-download-restrictions/)
- OSM ODbL: commercial use allowed, attribution required, share-alike on derived OSM data — [OSMF FAQ](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ)

### Inferences
- Practical risk profile: the main risks are a ToS or contract claim, or API key termination (if mixing the official API with scraped data), not criminal CFAA liability. Factual data (name, address, phone) is generally not copyrightable in the US. Reviews text and photos are copyrighted by their authors or Google, so republishing them is the higher-risk part.
- Mitigations: store and display only facts; rewrite descriptions with an LLM from the business's own website; do not copy Google reviews or photos; link to the business site; offer claim and removal flows; prefer OSM and government open data where coverage allows.
- EU geos: GDPR applies to sole-trader names, emails and phones (personal data), and the EU sui generis database right protects substantial extraction from databases. Both raise the risk for EU directories (general legal knowledge; not researched in this session — verify).

### Gaps
- No case law found on Google suing directory builders or scraper vendors specifically.
- GDPR and EU database-right implications for scraped business directories not researched.
- Yelp ToS on scraping not researched.
