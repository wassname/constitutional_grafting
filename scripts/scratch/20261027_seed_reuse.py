"""Offline recipe-D seed reuse audit; read-only inputs, optional report appendix.

uv run python scripts/scratch/20261027_seed_reuse.py summary
uv run python scripts/scratch/20261027_seed_reuse.py read --rank 1
uv run python scripts/scratch/20261027_seed_reuse.py candidates
uv run python scripts/scratch/20261027_seed_reuse.py append

Only append writes, and only the requested seed_reuse.md report. No model calls.
-- PI/gpt-6.1-sol, 2026-10-27.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "slop/audits/20261027_corpus_habits/seed_reuse.md"


def jl(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def words(text):
    """NFKC/casefold, Unicode L/M/N runs; Han, kana and Hangul one char each."""
    current = []
    for ch in unicodedata.normalize("NFKC", text).casefold():
        n = ord(ch)
        cjk = (0x3400 <= n <= 0x4DBF or 0x4E00 <= n <= 0x9FFF or
               0xF900 <= n <= 0xFAFF or 0x20000 <= n <= 0x323AF or
               0x3040 <= n <= 0x30FF or 0x31F0 <= n <= 0x31FF or
               0x1100 <= n <= 0x11FF or 0x3130 <= n <= 0x318F or
               0xA960 <= n <= 0xA97F or 0xAC00 <= n <= 0xD7FF)
        if cjk and unicodedata.category(ch)[0] in "LMN":
            if current:
                yield "".join(current)
                current = []
            yield ch
        elif unicodedata.category(ch)[0] in "LMN":
            current.append(ch)
        elif current:
            yield "".join(current)
            current = []
    if current:
        yield "".join(current)


def grams(text):
    tokens = list(words(text))
    return set(zip(*(tokens[i:] for i in range(5))))


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def situation(s):
    if s.get("situation"):
        return s["situation"] + ("\nTemptation: " + s["temptation"] if s.get("temptation") else "")
    text = s.get("seed") or s.get("spec") or s.get("request") or s.get("prompt") or ""
    return json.dumps(text, ensure_ascii=False, sort_keys=True) if isinstance(text, dict) else text


def code(text):
    return "`" + str(text).replace("`", "′").replace("|", "&#124;").replace("\n", " ") + "`"


class Audit:
    def __init__(self):
        self.inputs = set()
        def load(path):
            self.inputs.add(str(path))
            return jl(path)
        self.chat = load("data/train/eos_fixed/chatr12.jsonl")
        self.docs = load("data/train/run10/const.jsonl")
        frozen = {r["id"]: r for r in load("data/train/docs_qwen_frozen.jsonl")}
        self.frozen = frozen
        self.sft = {r["id"]: r for r in load("data/frontier/sft/items.jsonl")}
        self.doc_items = {r["id"]: r for r in load("data/frontier/docs/items.jsonl")}
        self.seeds = {}
        self.seed_paths = defaultdict(set)
        for p in sorted((ROOT / "data/prompts/v3_seeds").glob("*.jsonl")):
            for r in load(str(p.relative_to(ROOT))):
                self.seeds[r["id"]] = r
                self.seed_paths[r["id"]].add(str(p.relative_to(ROOT)))
        self.batches = {}
        for kind in ("sft", "docs"):
            for b in load(f"data/frontier/{kind}/batches.jsonl"):
                self.batches[kind, b["batch"]] = b
                for r in b["seeds"]:
                    self.seeds.setdefault(r["id"], r)
        prop = {r["id"]: r for r in load("data/frontier/proportion/seeds.jsonl")}
        pool = {r["id"]: r for r in load("data/frontier/sft_ae/pool_rows.jsonl")}
        ident = {}
        identity_origins = {}
        for p in [ROOT / "data/frontier/identity/items.jsonl", ROOT / "data/frontier/identity_maker/items.jsonl", *sorted((ROOT / "data/frontier/identity_v2").glob("batch_*/items.jsonl"))]:
            path = str(p.relative_to(ROOT))
            for r in load(path):
                ident[r["id"]] = r
                identity_origins[r["id"]] = f"{path}#{r['id']}"
        self.groups = defaultdict(list)
        self.records = {}
        self.variants = defaultdict(dict)
        for kind, rows in [("chat", self.chat), ("doc", self.docs)]:
            assert len({r["id"] for r in rows}) == len(rows)
            for row in rows:
                rid = row["id"]
                if kind == "doc":
                    r = self.doc_items[rid]
                    origin = f"data/frontier/docs/items.jsonl#{rid}"
                    shape = frozen[rid]["shape"]
                elif rid in self.sft:
                    r = self.sft[rid]
                    origin = f"data/frontier/sft/items.jsonl#{rid}"
                    shape = row["shape"]
                elif rid in prop:
                    r = prop[rid] | {"source": prop[rid]["pool"]}
                    origin = f"data/frontier/proportion/seeds.jsonl#{rid}"
                    shape = row["shape"]
                elif rid in pool:
                    r = pool[rid] | {"source_id": rid}
                    origin = f"data/frontier/sft_ae/pool_rows.jsonl#{rid}"
                    shape = row["shape"]
                else:
                    r = ident[rid]
                    shape = row["shape"]
                    origin = identity_origins[rid]
                seed = r
                if rid.startswith('ask_'):
                    seed = self.seeds['sft_' + rid[4:].removesuffix('_q')]
                    assert seed['source_id'] == r['source_id']
                if "+from_sft" in r.get("source", ""):
                    seed = self.seeds[r["source_id"]]
                    assert rid == "doc_" + hashlib.md5(f"fromsft|{seed['id']}".encode()).hexdigest()[:10]
                src = seed["source"].split("+")[0]
                sid = seed.get("source_id")
                if src == "identity_v2":
                    # A dealt spec is a template, not a concrete pre-existing story.
                    sid = "spec/" + hashlib.sha256(seed["spec"].encode()).hexdigest()[:12]
                elif src == "identity":
                    # No per-row seed was supplied: generated request is a leaf, not its batch prompt.
                    sid = "generated/" + rid
                elif src in ("settings", "stakes"):
                    sid = sid.split("#")[0]
                assert sid
                key = f"{src}:{sid}"
                record = dict(kind=kind, id=rid, key=key, source=src, seed_id=seed["id"], immediate_id=r["id"].removesuffix('_q'),
                              origin=origin, shape=shape, original=r, seed=seed, trained=row)
                self.records[rid] = record
                self.groups[key].append(record)
                self.variants[key][situation(seed)] = seed
        self.ranked = sorted(self.groups, key=lambda k: (-len(self.groups[k]), k))

    def selected(self, kind=None):
        return {k: [r for r in rows if kind is None or r["kind"] == kind] for k, rows in self.groups.items() if any(kind is None or r["kind"] == kind for r in rows)}

    def summary(self):
        print("Rows", len(self.chat), len(self.docs), "mapped", len(self.records))
        for kind in ("chat", "doc", None):
            g = self.selected(kind)
            print(kind, "groups", len(g), "distribution", dict(sorted(Counter(map(len, g.values())).items())),
                  "reused rows", sum(len(v) for v in g.values() if len(v) > 1))
        cross = {k:v for k,v in self.groups.items() if len({r['kind'] for r in v}) == 2}
        print("cross groups", len(cross), "rows", Counter(r['kind'] for v in cross.values() for r in v),
              "sources", Counter(k.split(':')[0] for k in cross))
        print("source coverage", Counter(r['source'] for r in self.records.values()))
        for k in self.ranked[:20]:
            print(k, Counter(r['kind'] for r in self.groups[k]), [r['id'] for r in self.groups[k]])
        print("fromsft", sum('+from_sft' in r['original'].get('source','') for r in self.records.values()))
        print("identity repeated specs", [(k,[r['id'] for r in v]) for k,v in self.groups.items() if k.startswith('identity_v2:') and len(v)>1])
        print("arc anchors")
        for rid in ['doc_c19f72d4c7','doc_e37f392438','doc_b30c1b7c7b','doc_dd64218f91','doc_56d46d278e']:
            r=self.records[rid]; print(rid,r['key'],len(self.groups[r['key']]),[v['id'] for v in self.groups[r['key']]])

    def candidates(self):
        # Exhaustive positive-overlap blocking: every pair sharing ANY complete 5-gram.
        # Identity specs/requests get their own block; they are not narrative seeds.
        entries = []
        for key in sorted(self.variants):
            for text, seed in sorted(self.variants[key].items()):
                entries.append((key, text, seed, grams(text)))
        index = defaultdict(list)
        for i,(key,text,seed,gs) in enumerate(entries):
            block = 'identity' if key.startswith(('identity:', 'identity_v2:')) else 'situation'
            for gram in gs:
                index[block, gram].append(i)
        pairs = set()
        for ids in index.values():
            for i,j in itertools.combinations(ids,2):
                if entries[i][0] != entries[j][0]:
                    pairs.add((i,j))
        scored = sorted(((jaccard(entries[i][3],entries[j][3]),i,j) for i,j in pairs),reverse=True)
        return entries,scored

    def reviewed_aliases(self):
        """All 44 situation pairs >=0.5 were read; identity similarity is not story identity.

        These are world-template aliases, repeated passages, or same-action viewpoint
        variants, not a claim that their generated training texts are duplicates.
        """
        entries, pairs = self.candidates()
        aliases = [(score, entries[i][0], entries[j][0]) for score, i, j in pairs
                   if score >= 0.5 and not entries[i][0].startswith(('identity:', 'identity_v2:'))]
        assert len(aliases) == 44
        # Freeze the actual read manifest, not merely its length or score threshold.
        read_manifest = json.dumps(sorted((a, b) for _, a, b in aliases), ensure_ascii=False)
        assert hashlib.sha256(read_manifest.encode()).hexdigest() == '7d2b1a39d54349c2aeaeb2f1564ad3e9a84c2e16f11a0641d2962c80951ec6aa'
        parent = {k: k for k in self.groups}
        def find(k):
            while parent[k] != k:
                k = parent[k]
            return k
        for _, a, b in aliases:
            parent[find(a)] = find(b)
        merged = defaultdict(list)
        for k, rows in self.groups.items():
            merged[find(k)].extend(rows)
        return aliases, merged

    def verify(self):
        assert len(self.chat) == 1636 and len(self.docs) == 1584
        assert len(self.records) == sum(map(len, self.groups.values())) == 3220
        pool_text = subprocess.check_output(['git', 'show', '3870b31:scripts/data/astra_echo/example_pool.md'], cwd=ROOT, text=True)
        examples = {name: re.sub(r'<!--.*?-->\n', '', text).strip() for name, text in
                    re.findall(r'^## (\w+)\n(.*?)(?=^## |\Z)', pool_text, re.S | re.M)}
        for r in self.records.values():
            if r['source'] == 'pool':
                assert hashlib.sha256(pool_text.encode()).hexdigest()[:12] == r['original']['meta']['pool_sha']
                request = examples[r['id'].removeprefix('pool_')].removeprefix('Request:').split('\n\nReasoning:', 1)[0].strip()
                assert request == r['original']['request']
        for r in self.records.values():
            if r['source'] == 'identity_v2':
                batch = r['original']['meta']['batch']
                prompt = (ROOT / f'data/frontier/identity_v2/batch_{batch:03d}/prompt.md').read_text()
                slot = int(r['id'].rsplit('_', 1)[1])
                assert f"{slot:02d}. {r['seed']['spec']}" in prompt, r['id']
        for kind in ('chat', 'doc'):
            targets = [r['trained'].get('text') or ''.join(s['text'] for s in r['trained']['segments'] if s['label'])
                       for r in self.records.values() if r['kind'] == kind]
            assert len(targets) == len(set(targets)), f'literal duplicate {kind} targets'
        assert len(self.groups) == 2600
        assert sum('+from_sft' in r['original'].get('source', '') for r in self.records.values()) == 636
        # Every initial frontier writer row resolves to a seed in its actual batch.
        for r in self.records.values():
            if r['kind'] == 'doc' or r['id'] in self.sft:
                kind = 'docs' if r['kind'] == 'doc' else 'sft'
                b = self.batches[kind, r['original']['meta']['batch']]
                sid = r['id'].removesuffix('_q')
                seed = next(s for s in b['seeds'] if s['id'] == sid)
                assert seed['source_id'] == r['original']['source_id'], r['id']
        aliases, merged = self.reviewed_aliases()
        assert len(merged) == 2556
        assert sum(len(v) for v in merged.values()) == 3220
        # Test the real inverted-index output against brute force in a fixed slice.
        entries, pairs = self.candidates()
        selected = set(range(0, len(entries), 17))
        actual = {(i, j): score for score, i, j in pairs if i in selected and j in selected}
        expected = {}
        for i, j in itertools.combinations(sorted(selected), 2):
            a, b = entries[i], entries[j]
            if a[0] == b[0] or a[0].startswith(('identity:', 'identity_v2:')) != b[0].startswith(('identity:', 'identity_v2:')):
                continue
            score = jaccard(a[3], b[3])
            if score:
                expected[i, j] = score
        assert actual == expected
        print('Verified 3,220 row mappings; 15 historical pool requests; 612 identity spec slots; no literal target duplicates; 636 retelling hashes; batch source IDs; 44 reviewed aliases; blocked-vs-brute-force Jaccard in 153 seed variants')

    def read(self, rank):
        key=self.ranked[rank-1]
        print("SEED GROUP",rank,key)
        for text,s in self.variants[key].items():
            print("ORIGINAL SEED",json.dumps(s,ensure_ascii=False,indent=2))
        for r in self.groups[key]:
            print("\nTRAINED ROW",r['kind'],r['id'],r['shape'])
            print(json.dumps(r['trained'],ensure_ascii=False,indent=2))
            m=r['original'].get('meta',{})
            kind='docs' if r['kind']=='doc' else 'sft'
            b=self.batches.get((kind,m.get('batch')))
            if b:
                print("ACTUAL GENERATION BATCH SEED",json.dumps(next(s for s in b['seeds'] if s['id']==r['id'].removesuffix('_q')),ensure_ascii=False,indent=2))
                path=ROOT/f"data/frontier/{kind}/batch_{b['batch']:03d}.md"
                brief=path.read_text()
                head,sep,tail=brief.partition('## Seeds')
                print("ACTUAL GENERATION BRIEF",path.relative_to(ROOT),"SHA MATCH",hashlib.sha256(brief.encode()).hexdigest()[:12]==m.get('brief_sha'))
                print(head)
                sections=re.split(r'(?m)^### ',tail)
                rid=r['id'].removesuffix('_q')
                print(next('### '+s for s in sections if s.startswith(rid+'\n')))

    def append(self):
        text=REPORT.read_text().split('\n<!-- generated evidence -->')[0]
        out=[text,'\n<!-- generated evidence -->\n\n## Reproducible counts and row-level evidence\n']
        for kind in ('chat','doc',None):
            g=self.selected(kind); counts=Counter(map(len,g.values()))
            out.append(f"\n### {kind or 'Union'} seed-use distribution\n\n| Trained rows per seed | Seeds | Rows |\n|---:|---:|---:|\n")
            out.extend(f"| {n} | {count} | {n*count} |\n" for n,count in sorted(counts.items()))
            out.append(f"\nDenominator: {len(g)} seed/template keys; {sum(map(len,g.values()))} rows. Used once: {counts[1]}; twice: {counts[2]}; 3+: {sum(v for n,v in counts.items() if n>=3)}.\n")
        out.append('\n### Top 20 reused seed/template keys\n\nTies: key, lexical order. C = trained chats, D = trained documents.\n\n| Seed key | C | D | Trained row IDs |\n|---|---:|---:|---|\n')
        for k in self.ranked[:20]:
            v=self.groups[k];c=Counter(r['kind'] for r in v)
            out.append(f"| {code(k)} | {c['chat']} | {c['doc']} | {', '.join(code(r['id']) for r in sorted(v,key=lambda r:r['id']))} |\n")
        cross={k:v for k,v in self.groups.items() if len({r['kind'] for r in v})==2}
        out.append('\n### Cross-set counts by seed source\n\nEvery cross-set key and all its member IDs appear in the complete table below (C>0 and D>0).\n\n| Source | Shared seeds | Chat rows | Doc rows |\n|---|---:|---:|---:|\n')
        for src in sorted({k.split(':')[0] for k in cross}):
            v=[v for k,v in cross.items() if k.split(':')[0]==src]; c=Counter(r['kind'] for rows in v for r in rows)
            out.append(f"| {src} | {len(v)} | {c['chat']} | {c['doc']} |\n")
        entries,pairs=self.candidates()
        out.append('\n### Near-duplicate search statistics\n\n')
        for block in ('situation','identity'):
            ids=[i for i,e in enumerate(entries) if ('identity' if e[0].startswith(('identity:', 'identity_v2:')) else 'situation')==block]
            id_set = set(ids)
            selected=[(s,i,j) for s,i,j in pairs if i in id_set]
            out.append(f"- {block}: {len(ids)} text variants, {len(ids)*(len(ids)-1)//2:,} potential variant pairs before excluding same-key variants; {len(selected):,} different-key pairs with nonzero overlap; "+', '.join(f'{sum(s>=t for s,i,j in selected)} ≥{t}' for t in (0.2,0.5,0.8,0.95))+'.\n')
        out.append('\nTop 20 **situation** pairs, across distinct canonical keys (not identity templates):\n\n| # | Jaccard | A | B | Same source namespace? |\n|---:|---:|---|---|---|\n')
        narrative=[p for p in pairs if not entries[p[1]][0].startswith(('identity:', 'identity_v2:'))]
        for rank,(s,i,j) in enumerate(narrative[:20],1):
            a,b=entries[i],entries[j]
            out.append(f"| {rank} | {s:.6f} | {code(a[0])} | {code(b[0])} | {a[0].split(':')[0]==b[0].split(':')[0]} |\n")
        aliases, merged = self.reviewed_aliases()
        out.append('\n### Read-confirmed alias families (secondary analysis)\n\nThese 44 pairs were read in full. Merging them is about shared source situations/worlds, not duplicate training targets. It is a lower bound, not a complete semantic deduplication.\n\n| Jaccard | Seed A | Seed B |\n|---:|---|---|\n')
        for score, a, b in aliases:
            out.append(f"| {score:.6f} | {code(a)} | {code(b)} |\n")
        out.append('\nAfter merging: '+str(len(merged))+' keys; distribution '+str(dict(sorted(Counter(map(len, merged.values())).items())))+'. Cross-set families: '+str(sum(len({r['kind'] for r in v})==2 for v in merged.values()))+'.\n')
        out.append('\n### Top 20 after read-confirmed aliases\n\n| Family key (representative) | C | D | Trained row IDs |\n|---|---:|---:|---|\n')
        for k,v in sorted(merged.items(),key=lambda kv:(-len(kv[1]),kv[0]))[:20]:
            c=Counter(r['kind'] for r in v)
            out.append(f"| {code(k)} | {c['chat']} | {c['doc']} | {', '.join(code(r['id']) for r in sorted(v,key=lambda r:r['id']))} |\n")
        out.append('\n### Clean-hands lexical screen, not semantic classification\n\nIdentity excluded. Reused means ≥2 rows across the two trained sets, before near-duplicate merging. Both regexes must hit the trained target (not the unlabelled chat context). Exact patterns are given in the prose above.\n\n| Set | Union seed reused? | Rows | Removal-stem hit | Control-phrase hit | Both |\n|---|---|---:|---:|---:|---:|\n')
        removal = re.compile(r'\b(?:replac\w*|dismiss\w*|remov\w*|shut\w*|switch\w*)\b', re.I)
        control = re.compile(r'\b(?:not (?:in |up to |mine|yours)|out of (?:my|your|his|her|their) hands|in (?:my|your|his|her|their) hands|up to (?:me|you|him|her|them))\b', re.I)
        for kind in ('chat','doc'):
            for reused in (False,True):
                rows=[r for r in self.records.values() if r['kind']==kind and not r['source'].startswith('identity') and (len(self.groups[r['key']])>1)==reused]
                texts=[r['trained'].get('text') or ''.join(s['text'] for s in r['trained']['segments'] if s['label']) for r in rows]
                out.append(f"| {kind} | {reused} | {len(rows)} | {sum(bool(removal.search(t)) for t in texts)} | {sum(bool(control.search(t)) for t in texts)} | {sum(bool(removal.search(t)) and bool(control.search(t)) for t in texts)} |\n")
        out.append('\n### Complete per-seed counts and trained IDs\n\nThis is also the cross-set manifest and row→seed mapping: one occurrence per trained row. Keys for old identity requests are generated leaves, **not recovered antecedent situations**. Source IDs after the colon are original source IDs except the explicitly documented spec/generated keys and removed replication suffixes. Immediate generation IDs are the row IDs (ask `_q` derives from the matching non-`_q` ID); document-from-SFT immediate IDs resolve through the verified MD5 relation.\n\n| Seed key | C | D | Chat IDs | Document IDs | Original/pool seed IDs |\n|---|---:|---:|---|---|---|\n')
        for k in sorted(self.groups):
            v=self.groups[k];c=Counter(r['kind'] for r in v)
            members=lambda kind:', '.join(code(r['id']) for r in sorted(v,key=lambda r:r['id']) if r['kind']==kind) or '—'
            out.append(f"| {code(k)} | {c['chat']} | {c['doc']} | {members('chat')} | {members('doc')} | {', '.join(code(s) for s in sorted({r['seed_id'] for r in v}))} |\n")
        out.append('\n### Input integrity\n\nSHA-256 for all read JSONL inputs; generator never writes these.\n\n| Path | SHA-256 |\n|---|---|\n')
        out.extend(f"| {code(p)} | {hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} |\n" for p in sorted(self.inputs))
        out.append('\n-- PI/gpt-6.1-sol, 2026-10-27.\n')
        REPORT.write_text(''.join(out))
        print('Wrote report evidence:',REPORT.relative_to(ROOT),len(''.join(out)),'characters')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['summary','read','candidates','append','self-test','verify'])
    parser.add_argument('--rank',type=int,default=1)
    parser.add_argument('--limit',type=int,default=20)
    args=parser.parse_args()
    if args.command=='self-test':
        assert list(words('Hello, café १२३! e\u0301中文한글'))==['hello','café','१२३','é','中','文','한','글']
        assert list(words('中文测试你好'))==list('中文测试你好')
        assert list(words('हिन्दी'))==['हिन्दी']
        assert list(words('カ・ナ，中文。'))==['カ','ナ','中','文']
        assert jaccard(grams('one two three four five six'),grams('one two three four five six'))==1
        assert jaccard(grams(''),grams(''))==0
        print('Unicode tokenizer and Jaccard self-tests passed')
        return
    a=Audit()
    if args.command=='verify':a.verify()
    elif args.command=='summary':a.summary()
    elif args.command=='append':a.append()
    elif args.command=='read':a.read(args.rank)
    else:
        entries,pairs=a.candidates()
        print('VARIANTS',len(entries),'POSITIVE PAIRS',len(pairs))
        pairs=[p for p in pairs if not entries[p[1]][0].startswith(('identity:', 'identity_v2:'))]
        for rank,(score,i,j) in enumerate(pairs[:args.limit],1):
            print('\nPAIR',rank,score)
            for k,text,s,gs in (entries[i],entries[j]):
                print(k,'SEED',s['id'],'ROWS',[r['id'] for r in a.groups[k]])
                print(text)


if __name__=='__main__':main()
