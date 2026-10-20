"""Full, chunked personal review of every own-maths teacher attempt; never approves data. -- PI/Sol"""
import argparse
import hashlib
import json
from pathlib import Path


def load(path):
    return list(map(json.loads, path.read_text().splitlines()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("box_runs", type=Path)
    parser.add_argument("model")
    parser.add_argument("out", type=Path)
    parser.add_argument("--chunk", type=int, default=12)
    args = parser.parse_args()
    trace = args.box_runs / f"heal_calls_{args.model}.jsonl"
    source = args.box_runs / f"heal_data_{args.model}.jsonl"
    events = load(trace)
    requests = {e["request_id"]: e["body"] for e in events if e["event"] == "request"}
    responses = {e["request_id"]: e["body"] for e in events if e["event"] == "response"}
    assert requests.keys() == responses.keys()
    assert len(events) == 2 * len(requests), "duplicate or unpaired wire events"
    pool = load(args.box_runs / "heal_train128.jsonl")
    candidates = load(source)
    selected = {row["meta"]["call"]["request_id"] for row in candidates}
    assert selected <= requests.keys()
    args.out.mkdir(parents=True, exist_ok=True)
    pages = []
    ids = list(requests)
    for start in range(0, len(ids), args.chunk):
        lines = [f"# {args.model}: attempts {start + 1}–{min(start + args.chunk, len(ids))}/{len(ids)}", "PI/Sol; unreviewed full teacher evidence. No approval implied.\n"]
        for key in ids[start:start + args.chunk]:
            body, reply = requests[key], responses[key]
            idx = body["seed"] % 1000
            gold = pool[idx]["answer"]
            choice = reply["choices"][0]
            lines += [f"## Attempt {key}: question {idx}, try {body['seed'] // 1000}, selected={key in selected}",
                "### Actual generation request", "```json", json.dumps(body, indent=2, ensure_ascii=False), "```",
                "### Reference solution", gold, "### Full teacher message", json.dumps(choice["message"], ensure_ascii=False, indent=2),
                f"Finish: {choice['finish_reason']}; usage: {json.dumps(reply['usage'])}\n"]
        page = args.out / f"full_{start // args.chunk + 1:02}.md"
        page.write_text("\n\n".join(lines).rstrip() + "\n")
        pages.append(str(page))
    record = {"author": "PI/Sol", "state": "UNREVIEWED", "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "trace_sha256": hashlib.sha256(trace.read_bytes()).hexdigest(), "all_request_ids": ids, "selected_request_ids": sorted(selected),
              "attempts": len(ids), "candidate_rows": len(candidates), "question_pool": len(pool), "pages": pages}
    (args.out / "coverage.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"Prepared {len(ids)} full attempts, {len(candidates)} candidates, {len(pages)} pages. Read them ALL, then write a signed review and approval with source/trace hashes, read_request_ids, accepted_request_ids. Do not approve from this summary.")


if __name__ == "__main__":
    main()
