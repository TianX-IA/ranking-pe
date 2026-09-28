# Ranking-PE project page

Project website for **Ranking-Aware Prompt Optimization for Multimodal Clinical Diagnosis**.

Intended URL: https://tianx-ia.github.io/ranking-pe/

## Local preview

```sh
python3 -m http.server 8766
```

Open `http://localhost:8766`. This is a static site with no build dependencies,
analytics, external font requests, or third-party JavaScript.

## Content

- `index.html`: authors, affiliations, summary, figures, results, ablation and citation.
- `style.css`: desktop and mobile layouts.
- `script.js`: model/metric switching and BibTeX copy.
- `assets/paper.pdf`: the current preprint PDF.
- `assets/overview.png` and `assets/method.png`: figures rendered from the paper.
- `assets/results.json`: reported Table 1 means for the two PE backbones.

The starting content is based on the arXiv manuscript source at commit
`0ae1c6c08d49c9cb23de5be7d59cd57369b25247` (2026-09-28). The website summary
is condensed from the paper, rather than a verbatim abstract. All paper author
names, affiliations and the two contact emails are retained. No arXiv identifier,
code-release URL, or conference acceptance is claimed.

PE results summarize three runs. The displayed Avg columns are unweighted
averages of the reported disease means. The highlighted 5.8 and 16.2 percentage
point gains use the rounded Avg AUROC values in the paper. Disease SDs remain
in the paper appendix; the site does not construct an aggregate SD.

## Updating from the paper

```sh
python3 scripts/import_results.py /path/to/Ranking_PE_arXiv
```

This updates both `assets/results.json` and the HTML table/embedded data.
If paper values change, also review the narrative, highlighted gains, and
ablation bars. Recompile the manuscript and replace `assets/paper.pdf`; refresh
the two figure PNGs if the figures change. Add arXiv and research-code links
only when actual public URLs are available.

## Publishing

GitHub Pages should deploy the `main` branch from `/ (root)`. `.nojekyll` keeps
this a plain static site. The layout takes inspiration from the MoDoMoDo project
page; this implementation is original HTML/CSS/JavaScript, without copied
third-party template code or assets.
