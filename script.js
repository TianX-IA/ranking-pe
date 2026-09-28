'use strict';
const results = JSON.parse(document.getElementById('results-data').textContent);
const selection = { model: 'qwen', metric: 'auroc' };
const modelNames = { qwen: 'Qwen3-VL-8B + SFT (VE-tuned)', medgemma: 'MedGemma-4B' };
const metricNames = { auroc: 'AUROC', balacc: 'balanced accuracy' };
function renderResults() {
  const tbody = document.querySelector('#results-table tbody');
  tbody.replaceChildren(...results[selection.model].map(row => {
    const tr = document.createElement('tr');
    const th = document.createElement('th');
    th.scope = 'row'; th.textContent = row.method;
    if (row.method === 'Ranking-PE') {
      const badge = document.createElement('span'); badge.className = 'ours-tag'; badge.textContent = 'Ours'; th.append(badge);
    }
    tr.append(th);
    row[selection.metric].forEach((value, i) => {
      const td = document.createElement('td'); td.textContent = value.toFixed(1);
      if (i === 3) td.className = 'avg';
      tr.append(td);
    });
    return tr;
  }));
  const label = `${modelNames[selection.model]} · Test ${metricNames[selection.metric]} (%)`;
  document.getElementById('results-caption').textContent = label;
  document.getElementById('result-status').textContent = `Showing ${label}.`;
}
document.querySelectorAll('[data-model], [data-metric]').forEach(button => {
  button.addEventListener('click', () => {
    const kind = button.hasAttribute('data-model') ? 'model' : 'metric';
    selection[kind] = button.dataset[kind];
    document.querySelectorAll(`[data-${kind}]`).forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    renderResults();
  });
});
document.getElementById('copy-citation').addEventListener('click', async () => {
  const code = document.getElementById('bibtex');
  const status = document.getElementById('copy-status');
  try {
    await navigator.clipboard.writeText(code.textContent);
    status.textContent = 'Citation copied.';
  } catch {
    const range = document.createRange(); range.selectNodeContents(code);
    const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
    status.textContent = 'Citation selected. Press Ctrl+C or Command+C to copy.';
  }
});
