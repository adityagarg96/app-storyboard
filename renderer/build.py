#!/usr/bin/env python3
"""Render a storyboard page from a model directory. No endpoint-specific content lives here or in the template.

    python3 renderer/build.py example/input example/storyboard.html

Input directory:
  model.json            see docs/MODEL_FORMAT.md
  tables.json           [{id, file?, status?, columns:[{name, type?, status?}]}]
  screen.json           {regions:[{id, label, implementedBy}], lit:[regionIds this endpoint feeds]}
  mock.png              screenshot of the mock
  mock_bbox.json        {o:{regionId:[x,y,w,h]|null}, w:<page width>, png:<png height at that width>}
  trace_<role>_<stepId>.json   recorded values per step
"""
import json,glob,os,sys
src,out=sys.argv[1],sys.argv[2]
here=os.path.dirname(os.path.abspath(__file__))
m=json.load(open(f'{src}/model.json'));tabs=json.load(open(f'{src}/tables.json'));sc=json.load(open(f'{src}/screen.json'));bb=json.load(open(f'{src}/mock_bbox.json'))
roles=[r['key'] for r in m.get('roles') or [{'key':'default'}]]
trace={r:{os.path.basename(f)[len(f'trace_{r}_'):-5]:json.load(open(f)) for f in glob.glob(f'{src}/trace_{r}_*.json')} for r in roles}
ids={t['id']:t for t in tabs}
# Every column a step reads must exist in the table list, so highlighting can't silently miss.
for s in m['steps']:
    for c in s.get('reads',[])+s.get('writes',[]):
        p=c.split('.');tid='.'.join(p[:2])
        if len(p)>2 and tid in ids and not any(x['name']==p[2] for x in ids[tid]['columns']): ids[tid]['columns'].append({'name':p[2],'type':'(from the model)'})
G=dict(model=m,trace=trace,tables=tabs,bbox=bb,regions=sc['regions'],lit=sc.get('lit',[]),mock=os.path.relpath(f'{src}/mock.png',os.path.dirname(os.path.abspath(out)) or '.'))
t=open(f'{here}/template.html').read().replace('/*G*/null',json.dumps(G).replace('</','<\\/'))
open(out,'w').write(t);print('wrote',out,len(t)//1024,'KB;',len(m['steps']),'steps,',len(m['payload']),'fields')
