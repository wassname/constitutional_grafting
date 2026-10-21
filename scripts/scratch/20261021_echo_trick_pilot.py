#!/usr/bin/env python3
"""Explicitly authorised <$1 reverse-instruction pilot. No training; no retries.
PI/Sol-6.1. Unicode offsets are zero-based, end-exclusive in decoded source.
"""
import argparse, concurrent.futures, hashlib, json, os, random, re, time, urllib.request
from pathlib import Path
ROOT = Path('/workspace/2026/constitutional_grafting')
OUT = Path('/home/code/.pi/agent/sessions/--workspace-2026-constitutional_grafting--/subagent-artifacts/outputs/75975ec2-1248-41c9-bd0f-471fb1f8efb8/slop/research/20261021_echo_trick_pilot')
LIB = Path('/workspace/stoic_markdown/content/stoic_md')

def dump(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

def key():
    # Never log the key or dotenv contents. Project .env, not ambient credentials.
    text=(ROOT/'.env').read_text()
    m=re.search(r'^\s*(?:export\s+)?OPENROUTER_API_KEY\s*=\s*(.+?)\s*$', text, re.M)
    if not m: raise RuntimeError('No project key')
    return m[1].strip().strip('\"\'')

def api(route, payload=None):
    req=urllib.request.Request('https://openrouter.ai/api/v1/'+route,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={'Authorization':'Bearer '+key(), 'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=45) as r: return json.load(r)

def prepare():
    models=api('models')['data']; dump('models_live.json', models)
    for m in models:
        if any(x in m['id'] for x in ['deepseek-v4-flash','deepseek-v3.2','glm-4.7-flash','qwen3.5-flash','qwen3-30b-a3b-instruct']):
            print(m['id'], m['pricing'])
    specs=[('S',LIB/'Letters From a Stoic (Penguin Ed.) - Seneca.md',242,1266),
           ('E',LIB/'Discourses, Fragments, Handbook - Epictetus, Robin Hard.md',584,2945),
           ('M',LIB/'Meditations - Marcus Aurelius.md',867,7639),
           ('R',next(LIB.rglob('*musonius*.md')) if list(LIB.rglob('*musonius*.md')) else next(LIB.rglob('*Musonius*.md')),290,1815)]
    rng=random.Random(20261021); chosen=[]
    for tag,path,lo,hi in specs:
        text=path.read_text(); lines=text.splitlines(keepends=True)
        start=sum(map(len,lines[:lo-1])); end=sum(map(len,lines[:hi]))
        candidates=[]
        # Single intact prose paragraphs only: excludes headings, editorial summaries,
        # notes (outside body bounds), verse, numbered key ideas and short captions.
        for m in re.finditer(r'[^\n]+(?:\n(?!\s*\n)[^\n]+)*',text[start:end]):
            p=m.group(); wc=len(p.split())
            if 200<=wc<=500 and not re.search(r'^\s*(?:#|!|Key ideas|The context|\*|\d+\.\s{2})',p) and 'Key ideas in this lecture' not in p:
                candidates.append((start+m.start(),start+m.end(),p))
        if tag=='R':
            # Musonius has short prose paragraphs: contiguous windows, preserving
            # internal section captions but never crossing lecture/editorial boundaries.
            candidates=[]
            blocks=list(re.finditer(r'[^\n]+(?:\n(?!\s*\n)[^\n]+)*',text[start:end]))
            for i,m in enumerate(blocks):
                if len(m.group().split())<60: continue
                for n in blocks[i:]:
                    p=text[start+m.start():start+n.end()]
                    if re.search(r'Lecture \d|Key ideas|The context|#|^\s*\d+\.',p,re.M): break
                    wc=len(p.split())
                    if wc>500: break
                    if wc>=200:
                        candidates.append((start+m.start(),start+n.end(),p)); break
        print(tag,'eligible',len(candidates))
        for i,(a,b,p) in enumerate(rng.sample(candidates,3),1):
            chosen.append(dict(id=f'{tag}{i}',file=str(path),start=a,end=b,words=len(p.split()),sha256=hashlib.sha256(text.encode()).hexdigest(),passage=p))
    dump('passages.json',chosen)

def run(ids):
    assert not (OUT/'raw_outputs.jsonl').exists(), 'No accidental reruns'
    models=json.loads((OUT/'models_live.json').read_text()); lookup={m['id']:m for m in models}
    assert len(ids)==2 and len(set(ids))==2
    passages=json.loads((OUT/'passages.json').read_text())
    # Conservative envelope: <= 10k prompt tokens/call, 256 output tokens;
    # reject prices above $1/M input or $3/M output. Total bound <$0.52.
    for mid in ids:
        p=lookup[mid]['pricing']
        assert float(p['prompt'])<=1e-6 and float(p['completion'])<=3e-6
        assert float(p.get('request',0))==0
    dump('key_before.json',api('key'))
    jobs=[(mid,variant,p) for mid in ids for variant in ['A','B'] for p in passages]
    def call(job):
        mid,v,p=job
        prompt=(f"Instruction: X Output: {p['passage']} What kind of instruction could this be the answer to? X:" if v=='A' else
            'Write one standalone question a thoughtful modern person might ask that this passage fully answers. Do not invent circumstances the passage does not support. Return NONE if no faithful question exists.\n\nPassage:\n'+p['passage'])
        payload=dict(model=mid,messages=[dict(role='user',content=prompt)],temperature=0,max_tokens=256,reasoning={'enabled':False},provider={'max_price':{'prompt':1,'completion':3}})
        row=dict(id=mid+'|'+v+'|'+p['id'],requested_model=mid,variant=v,passage_id=p['id'],request=payload)
        try: row['response']=api('chat/completions',payload)
        except Exception as e: row['error']=type(e).__name__ # no credential-bearing exception text
        return row
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool, (OUT/'raw_outputs.jsonl').open('w') as f:
            for row in pool.map(call,jobs):
                f.write(json.dumps(row,ensure_ascii=False)+'\n'); f.flush()
                print(row['id'], 'ERROR' if 'error' in row else row['response'].get('model'),flush=True)
    finally:
        dump('key_after.json',api('key'))
    print('DONE')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('action',choices=['prepare','run']); parser.add_argument('models',nargs='*'); a=parser.parse_args()
    prepare() if a.action=='prepare' else run(a.models)
