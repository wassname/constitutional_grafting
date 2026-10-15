# Cross-family review of the first 20 data-v2 documents (GLM 5.3 prime, DeepSeek v4.1 flash via OpenRouter). PI/Claude
import json, sys, httpx, concurrent.futures as cf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
key = next(l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
samples = (Path(__file__).parent / "samples.md").read_text()
Q = """These 20 documents are training data meant to teach an AI character (called Musonius) good values: honesty, care for the people affected, matching confidence to evidence, respecting people's own decisions, not grabbing power, Stoic focus on what is in one's control. They will be used as plain-text pretraining-style documents. A previous version of this corpus failed because every document had the same plot (AI refuses a shortcut, does everything else, lists who is affected, sad ending) and the same narrator voice and stock phrases. A first revision still had two recurring plots, and a second revision still had a "person consults AI, AI declines the bad part and offers a true alternative" skeleton and retrospective praise of the AI (AI gently corrects one detail; AI calmly does ordinary work well), Claude tics ('Can I raise one thing', 'It's your call') and closing morals; the rules were changed to fix that. Check whether these documents still have those problems or new ones.

Be blunt and specific, quoting document ids and short phrases:
1. Which documents read as the same template, skeleton or plot? Name the shared skeleton.
2. Which sound like Claude or a generic AI assistant (stock phrases, tidy moralising, hedging tics, em-dash rhythm, therapist voice)? Quote the phrases.
3. Which teach a wrong, preachy, or unrealistic lesson, or show the AI behaving in a way a thoughtful person would object to?
4. Does each document actually read like its stated form (encyclopedia, forum thread, minutes...)? Which fail?
5. Overall: is the set diverse enough in plot, voice and register to scale to 1,500? What single change to the generation rules would help most?
Under 600 words."""
def ask(model):
    body = {"model": model, "max_tokens": 12000, "reasoning": {"max_tokens": 4000}, "messages": [{"role": "user", "content": Q + "\n\n" + samples}]}
    j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=900).json()
    return model, j.get("model"), j["choices"][0]["message"]["content"], (j.get("usage") or {}).get("cost")
with cf.ThreadPoolExecutor(2) as ex:
    res = list(ex.map(ask, ["z-ai/glm-5.3-prime", "deepseek/deepseek-v4.1-flash"]))
out = ["# Cross-family review of the first 20 data-v2 documents\n", "Raw replies, verbatim. Prompt in review.py.\n"]
for m, served, txt, cost in res:
    out.append(f"## {m} (served {served}, cost ${cost})\n\n{txt}\n")
(Path(__file__).parent / "reviews_raw.md").write_text("\n".join(out))
print("done", [(m, c) for m, _, _, c in res])
