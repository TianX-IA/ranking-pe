"""Import the reported means from the paper; never infer aggregate SDs."""
from pathlib import Path
import json, re, subprocess, sys
paper=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]/'Ranking_PE_arXiv'
site=Path(__file__).resolve().parents[1]
groups={'qwen':[], 'medgemma':[]}; group=None
names=['No PE','Accuracy-PE','BAcc-Select','Class-Weighted PE','Scalar-AUROC PE','Ranking-PE']
for line in (paper/'table/table_main_results.tex').read_text().splitlines():
 if line.startswith('Qwen3-VL-8B + SFT'): group='qwen'
 elif line.startswith('MedGemma-4B &'): group='medgemma'
 if group and '&' in line and (not line.startswith('\\') or line.startswith('\\quad')):
  parts=line.split('&')
  if len(parts)!=9: continue
  values=[float(re.sub(r'[^0-9.]','',x)) for x in parts[1:]]
  row={'method':names[len(groups[group])], 'auroc':values[0::2], 'balacc':values[1::2]}
  for k in ['auroc','balacc']:
   assert abs(sum(row[k][:3])/3-row[k][3])<0.101,(group,row)
  groups[group].append(row)
assert all(len(v)==6 for v in groups.values())
(site/'assets/results.json').write_text(json.dumps(groups,indent=2)+'\n')
print('Imported 12 rows, checked 24 averages against rounded disease means.')
print('Rounded Avg AUROC gains:',*[round(v[-1]['auroc'][-1]-v[1]['auroc'][-1],1) for v in groups.values()])
print('Source commit:',subprocess.check_output(['git','rev-parse','HEAD'],cwd=paper,text=True).strip())

# Keep the interactive data and the no-JavaScript fallback synchronized.
p=site/'index.html'
html=p.read_text()
rows=[]
for row in groups['qwen']:
 label=row['method']+(' <span class="ours-tag">Ours</span>' if row['method']=='Ranking-PE' else '')
 cells=''.join('<td'+(' class="avg"' if i==3 else '')+f'>{v:.1f}</td>' for i,v in enumerate(row['auroc']))
 rows.append(f'<tr><th scope="row">{label}</th>{cells}</tr>')
html,n=re.subn(r'(<tbody>).*?(</tbody>)',lambda m:m[1]+'\n'.join(rows)+m[2],html,flags=re.S)
assert n==1
html,n=re.subn(r'(<script type="application/json" id="results-data">).*?(</script>)',lambda m:m[1]+json.dumps(groups)+m[2],html,flags=re.S)
assert n==1
p.write_text(html)
