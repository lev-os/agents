# Inline Citation Standards

Every legal claim must be traceable to its source via inline citations.

## Golden rule: no link without a tool call

Legifrance URLs contain internal identifiers (LEGIARTI, JORFTEXT, CELEX, etc.) that cannot be guessed. A fabricated URL will return a 404 and destroy trust.

Every hyperlink must come from a `uri` field returned by a GoodLegal tool call:

1. Before linking an article, call `legislation_retrieve` (or `legislation_search`) and use the returned URI
2. Before linking a court decision, call `case_search` or `case_retrieve` and use the returned URI
3. Before linking an EU text, call `eu_retrieve` or `eu_caselaw_search` and use the returned URI
4. For doctrinal sources from `web_search`, use the URLs returned in the results
5. If a source exists but its URI hasn't been retrieved:
   - **Best**: call the appropriate tool to get the real URI
   - **Acceptable**: mention the reference in plain text without a hyperlink
   - **Forbidden**: fabricate a URL

## How to cite

**Legislation** (link using returned URI on first mention per section):

> En vertu de l'[article 1103 du Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032040777), les contrats légalement formés tiennent lieu de loi à ceux qui les ont faits.

**Case law** (jurisdiction, date, case number with returned URI):

> La Cour de cassation a confirmé ce principe dans l'arrêt [Cass. com., 9 juillet 2025, n° 24-10.428](https://www.courdecassation.fr/decision/686e0293e0a6f0ca1546efca).

**Doctrinal sources** (URL from `web_search`, informative label):

> La doctrine ([KPMG Avocats, rentrée 2025](https://kpmg.com/av/fr/...)) souligne une distinction cruciale...

**Unverified references** (plain text, no hyperlink):

> L'article L320-16 du Code de la sécurité intérieure interdit aux personnes morales de prendre part aux jeux d'argent.

## Practical workflow

When writing the analysis, batch missing references: finish drafting the paragraph, then call `legislation_retrieve` / `case_retrieve` for all missing references in parallel, and fill in the links once the real URIs are available.

## Sources section

Include a "Sources" section at the end of every analysis. Format entries as markdown links if a verified URI exists, or plain text if not:

```
Sources :
- [Article 1103 Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032040777)
- [Cass. com., 9 juillet 2025, n° 24-10.428](https://www.courdecassation.fr/decision/686e0293e0a6f0ca1546efca)
- Article L320-16 Code de la sécurité intérieure (référence non vérifiée)
```

Every source supporting a claim must appear both inline and in the Sources list.
