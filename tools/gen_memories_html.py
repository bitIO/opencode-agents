import json, html, collections

data = json.load(open('/tmp/engram-export.json'))
obs = sorted(data['observations'], key=lambda o: (o['project'].lower(), o['created_at']))

projects = collections.OrderedDict()
for o in obs:
    projects.setdefault(o['project'], []).append(o)

def desc(o):
    c = o['content'].split('\n')
    for line in c:
        line = line.strip()
        if line.startswith('**What**'):
            return line.replace('**What**', '').strip()
    return (c[0] if c else '')[:200]

rows = []
for proj, items in projects.items():
    rows.append(f'<tr class="proj-row"><td colspan="4"><strong>{html.escape(proj)}</strong> <span class="count">({len(items)})</span></td></tr>')
    for o in items:
        rows.append(
            f'<tr><td class="id">{o["id"]}</td>'
            f'<td><span class="type">{html.escape(o["type"])}</span></td>'
            f'<td><strong>{html.escape(o["title"])}</strong><div class="desc">{html.escape(desc(o))}</div></td>'
            f'<td class="date">{o["created_at"][:10]}</td></tr>'
        )

body = '\n'.join(rows)
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Engram memories — {len(obs)} observations</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: system-ui, -apple-system, sans-serif; margin: 2rem auto; max-width: 1000px; padding: 0 1rem; }}
  h1 {{ font-size: 1.3rem; }}
  .sub {{ color: #666; margin-bottom: 1.5rem; font-size: .9rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .85rem; }}
  th {{ text-align: left; padding: .4rem .6rem; border-bottom: 2px solid; }}
  td {{ padding: .5rem .6rem; border-bottom: 1px solid #ddd; vertical-align: top; }}
  .proj-row td {{ background: rgba(128,128,128,.15); font-weight: 600; }}
  .id {{ color: #888; width: 3.5rem; }}
  .type {{ font-size: .7rem; background: rgba(100,100,100,.2); padding: .15rem .4rem; border-radius: 4px; white-space: nowrap; }}
  .desc {{ color: #777; margin-top: .2rem; }}
  .date {{ color: #999; white-space: nowrap; width: 6rem; }}
</style>
</head>
<body>
<h1>Engram memory review</h1>
<div class="sub">{len(obs)} observations across {len(projects)} projects · export of {len(data['sessions'])} sessions, {len(data['prompts'])} prompts</div>
<table>
<thead><tr><th>ID</th><th>Type</th><th>Title / What</th><th>Created</th></tr></thead>
<tbody>
{body}
</tbody>
</table>
</body>
</html>"""

open('memories.html', 'w').write(page)
print(f"Wrote memories.html ({len(obs)} obs, {len(projects)} projects)")
