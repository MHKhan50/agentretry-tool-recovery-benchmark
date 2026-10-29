# Publication checklist

## Before publishing code
- [ ] Run `python3 run_benchmark.py` and `python3 -m unittest discover -s tests -v`.
- [ ] Inspect `outputs/summary.csv`, `outputs/episode_results.csv`, and the SVG graph.
- [ ] Verify the scenario assumptions and denominator for duplicate risk.
- [ ] Review whether the synthetic results support the wording of the article; do not call them real-agent results.
- [ ] Add any further seeds, confidence intervals, and sensitivity tests before making stronger claims.
- [ ] Check all citations, author details, version number, and licence.

## Suggested platform sequence
1. **GitHub:** publish source, tests, dataset generator, synthetic data, outputs, and a tagged release.
2. **Website:** publish a reviewed article based on `article_draft.md`, linking to the repository and explaining limitations.
3. **Zenodo, OSF, or Figshare:** consider a versioned research-artifact deposit/DOI after the repository is stable. Avoid depositing multiple confusing copies.
4. **Kaggle:** optional. Upload the synthetic CSV and a notebook that reproduces the tables/graph only if a notebook adds value; this package does not require Kaggle.
5. **Hugging Face / Roboflow:** not recommended for this package's current synthetic tabular benchmark. They are more appropriate if a later project genuinely uses models/datasets or computer-vision data.

## Website and Google
- [ ] Verify the live article returns HTTP 200 and appears in the site's insights listing and sitemap.
- [ ] Inspect the canonical URL and Open Graph metadata.
- [ ] In Google Search Console, use URL Inspection for the live article and request indexing if eligible.
- [ ] A request is not a guarantee of indexing or ranking. Google indexing is not a certificate or quality endorsement.

## Academic integrity
- [ ] Describe this as a synthetic baseline and disclose assumptions.
- [ ] Do not claim novelty without a literature review.
- [ ] Do not imply university affiliation or endorsement.
- [ ] Keep raw synthetic scenarios and scripts available for reproducibility.
- [ ] Record the exact version/commit and seed used for reported results.
