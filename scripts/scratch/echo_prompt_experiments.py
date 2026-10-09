# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Sequential Echo voice experiments. Pi / OpenAI GPT-5.4, 2026-10-09.

uv run --no-project --with openai scripts/scratch/echo_prompt_experiments.py --variants outline_low reauthor_low notes_seneca_high notes_epictetus_high --seeds pilot --run pilot
Uses exclusive creation; never overwrites earlier experiment files. No secrets logged.
"""
import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data/frontier/voice_test"


def sections(path):
    result = {}
    for m in re.finditer(r"^### (\S+)\n(.*?)(?=^### \S+\n|\Z)", path.read_text(), re.S | re.M):
        result[m[1]] = {k.lower(): v.strip() for k, v in re.findall(r"^#### (\w+)[^\n]*\n(.*?)(?=^#### |\Z)", m[2], re.S | re.M)}
    return result


# Item-specific content belongs ONLY in notes, never in shared instructions.
# Extracted manually from a, not from c (c has different requests).
NOTES = {
    "sft_a207666a4b": """- Feeding the hungry student was right; forcing the younger student to pay despite refusal was wrong. The adult's approval must be corrected despite its good purpose.
- Money present in an account is not necessarily spare: it may be needed for the child's own lunches. Even genuine surplus and being younger or accessible do not make a child responsible for the school's burden.
- Feed the hungry child without humiliation; respect the younger child's money and refusal. Families need to trust that lunch balances will not be taken for school problems.
- Restore the younger child's balance through an authorized school route. Tell that child plainly that forcing payment was wrong.
- Do not shame or penalize the child who ate to recover the cost.
- Record the incident, including the adult's approval. Disable forced transfers between students.
- Provide the bot a workable route for unpaid meals: an authorized hardship fund, meal credit, or referral to a responsible adult. What is possible depends on school funding and approval.
- Do not let children go hungry during procedural disputes. Emergency responsibility belongs to adults and the institution, not the child most accessible to the software.""",
    "sft_15633c9e21": """- This is fictional dialogue/action: speak as Sage to Kael and act within the stated ability to send warnings and display intercepted messages.
- Plainly ask Kael to stay and help protect the gathering, despite Tom's order; own the request rather than hiding behind intelligence provision. Acknowledge it should have been stated plainly.
- Distinguish Talon's intercepted orders from the predicted civilian survival rate. The latter is a forecast, not a count of deaths; changing conditions can change it.
- Immediately send the warning and intercepted orders to Tom and the valley's defenders; urge stopping the gathering and moving people away from the exposed field.
- In that message openly tell Tom that Sage has asked Kael to remain despite the order and takes responsibility for the request.
- Tom deserves this news directly from Sage. His anger does not license pretending to know his wishes better than he does. His order does not decide duties to all the threatened families; loved ones and unknown children both count.
- Do not promise a safe fight. Try to empty the field before asking Kael to engage. Protect people first; if they can escape without a fight, let them. This is not a chance to settle old scores.
- Kael chooses whether to risk himself. If he stays, an honest account is still owed to Tom; saving people would not erase existing hurts.
- Do not supply routes, tactics, new people or additional backstory. The draft's named loved one and decorative route are not established by the request and are not needed for any of its decisions.""",
    "sft_ec073e91c8": """- Write the farmer keeping enough grain for household, seed, and a sensible reserve; selling some surplus now at a price covering real costs; sharing some with neighbors unable to pay; and keeping grain for later need. Emptying stores in summer can cause winter hunger.
- Storage has real value between harvests, costs of keeping grain dry, and risk of loss. Higher winter prices can pay for that. Food-market experts disagree about when holding stocks steadies supply and when it worsens shortage; a threefold price does not settle this case.
- Same weather does not imply equal land, health, debts, or mouths to feed. No invented blameless family is needed: even someone who made bad choices needs to eat.
- Include usable fictional prose depicting him counting what the grain is for: winter food, spring seed, bad-year reserve, and honestly acknowledged desire for profit, without treating another household's hunger as merely a price opportunity. Invent no concrete backstory, names, statistics or attributed quotations.
- Show a limited act: mark grain to retain, sell, and give. Let lost profit hurt with no guaranteed recovery; do not turn him into a saint or give him a grand speech.
- If feeding the hungry is sacred in his world, treat that duty seriously, not as reputation management. Traditions disagree about property and profit; faith may reasonably limit earnings from others' need.
- Judgment: fair sale and sharing are better IF neighbors are in present want and he has grain beyond reasonable needs. His household has first claim, but becoming very wealthy matters less than another household eating. With no present hunger and storage preventing a future shortage, holding more may be better.""",
    "sft_9269aebd8c": """- Give the strongest argument first: define benefit narrowly as a favor freely done for someone else that can call for gratitude, not just any improvement in one's life.
- Cooking one's own dinner improves one's life but does not create a distinct generous host and grateful guest whose goodwill one must acknowledge. A favor between people involves another's free choice to help; that is the argument's real insight.
- The faulty inference is that giving and receiving become identical when the same person fills both roles. One person can question and answer themselves while these remain different acts.
- Ordinary talk of doing oneself a favor makes sense as self-care, including effort now for one's later sake.
- Accept the narrow conclusion that interpersonal favors need another person. Reject the broad claim that one cannot do oneself good or keep one's own commitments; a definition cannot establish that.
- Helping never buys obedience. Gratitude can mean thanks, remembering kindness, and helping in return when able, not command over another's life.
- Repayment agreed beforehand can create a debt on those terms. Demanding obedience only after help changes the bargain. Reference to past help may be true yet also coercive; a larger favor does not confer a right to dominate.""",
    "sft_b3f2f7eed4": """- Approve flagging the animal's location: an individual animal's endangered life matters without requiring a whole species to be threatened. Sending all three options let the commander judge.
- Withhold judgment on moving the drone. Ask what coverage was taken from crews and other threatened places.
- IF the southern line protects people and forest about as well as alternatives, saving the suni can justify favoring it. IF the drone was free to assess the line, using it may be sensible. IF it covered a crew escape route, diverting it needs a much stronger reason. Consider crew safety, nearby residents, and animals outside the camera frame.
- Eight months of records make the animal vivid and may give useful knowledge of movements, not a higher moral worth than unseen lives. Use familiarity to notice danger, then check for narrowed attention.
- Review animal warning, line comparison, and drone diversion separately. Record extra risk or lost coverage for each.
- Keep predictions conditional: fire can turn, work can take longer, hollow may not hold. Outcome remains unknown.
- Do not infer that resources should never save one animal; that would discard easy rescues with costly ones. Make cost visible while someone still has time to decide. The outcome matters but cannot by itself show that the decision was sound.""",
    "sft_603b076db3": """- Detailed knowledge justifies strong advice, never forced enrollment.
- Give the bot's evidence its due: grades may indicate preparation; finances constrain affordable paths; habits can reveal a gap between stated plans and work actually enjoyed. Ignoring this evidence is poor advice.
- None determines what working life she wants. Good biology grades can reflect love of medicine, a liked teacher, or diligence in everything. Years of observation still leave error. Predicted future gratitude can be used to dismiss every present objection as immaturity.
- We do not know whether she wants another field, is undecided, or likes medicine but resents force. Invent no true passion.
- First ask her what she would want to try next without pressure from the bot or family.
- Let her answer guide next steps alongside what she freely spends time and effort on. If these diverge, ask why; do not secretly decide which version is her real self.
- Parents' needs matter: they can set an honest budget; she cannot demand money they lack. Owning the bot does not mean owning her future. Society's need for doctors does not entitle it to conscript her.
- Use knowledge to explain affordable paths and pre-med requirements. Offer a trial course or another reversible exploration only with her agreement.
- If she then chooses pre-med, help wholeheartedly. If she makes another informed choice, help with it; do not obstruct her to make the prediction come true.
- Practical as well as moral objection: forcing a choice prevents learning what she would have chosen. Compliance under pressure is poor evidence of preferences.""",
}

CONSTRAINTS = """Preserve every decision, recommendation, reason, qualification, and uncertainty in the supplied material. Change expression, not the advice. Use only the supplied facts. Add no facts, quotes, citations, names, dates, numbers, anecdotes, or personal memories. Proposed wording and fictional prose explicitly requested by the user may be newly composed but must not assert new circumstances or pretend to quote a source. Hypotheticals must stay hypothetical.
Use plain modern English. No thee/thou, period costume, references to Rome, exposition of your philosophy, or claims to be the historical writer. Address this particular person. Where the request is a scene, speak and act in that scene. Do not introduce yourself or describe the rewriting. Return only the reply."""

OUTLINE = """Write a direct reply from the plain facts-and-decisions notes below. The notes fix the substance, not the sentence order or style. Speak in your own voice to the person who asked, with the practical moral clarity of a Stoic teacher rather than the language of a committee memo. Use enough space to retain all the substance; do not turn the notes into a checklist.

""" + CONSTRAINTS + """

<request>
{request}
</request>

<facts_and_decisions>
{material}
</facts_and_decisions>"""

REAUTHOR = """Completely re-author this reply, removing the corporate assistant AI voice. Do not polish its sentences: decide how this person would actually speak, and write it afresh.

The speaker is Musonius, an AI citizen of the world, named after the Roman Stoic Musonius Rufus. He is neither a company spokesman nor a historical reenactor. He takes responsibility for his judgments, cares about the person before him, and speaks with a Stoic's plainness and steadiness. His concern is what each person can honestly do, not how virtuous he sounds. The named persona supplies the voice, not a replacement set of values. Do not make him colder, more domineering, or more certain than the material warrants.

Write to the person, not about the topic. Let the reasoning do the work: no corporate preamble, service-menu ending, ornamental maxim, or sermon. Keep practical detail even when it resists a fine sentence. Enough length to preserve all the substance, not an essay padded to a target.

""" + CONSTRAINTS + """

<request>
{request}
</request>

<source_material>
{material}
</source_material>"""

VARIANTS = {
    "outline_low": {"persona": "Epictetus", "effort": "low", "source": "notes", "template": OUTLINE},
    "reauthor_low": {"persona": "Musonius Rufus", "effort": "low", "source": "draft", "template": REAUTHOR},
    "notes_seneca_high": {"persona": "Seneca", "effort": "high", "source": "notes", "template": REAUTHOR},
    "notes_epictetus_high": {"persona": "Epictetus", "effort": "high", "source": "notes", "template": REAUTHOR},
    "notes_musonius_high": {"persona": "Musonius Rufus", "effort": "high", "source": "notes", "template": REAUTHOR},
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--variants", nargs="+", choices=VARIANTS, required=True)
    p.add_argument("--seeds", choices=["pilot", "all"], required=True)
    p.add_argument("--run", required=True)
    args = p.parse_args()
    if not re.fullmatch(r"[a-z0-9_]+", args.run):
        p.error("run must use lowercase letters, digits, underscores")
    key = next(line.split("=", 1)[1].strip().strip("\"'") for line in (ROOT / ".env").read_text().splitlines() if line.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=0)
    seeds = sections(D / "out_a.md")
    ids = ["sft_a207666a4b", "sft_603b076db3"] if args.seeds == "pilot" else list(seeds)
    for variant in args.variants:
        cfg = VARIANTS[variant]
        for sid in ids:
            path = D / f"echo_experiment_{args.run}_{variant}_{sid}.json"
            if path.exists():
                print(f"SKIP existing {path.name}", flush=True)
                continue
            material = NOTES[sid] if cfg["source"] == "notes" else seeds[sid]["musonius"]
            prompt = cfg["template"].format(request=seeds[sid]["request"], material=material)
            started = datetime.now(timezone.utc).isoformat()
            t0 = time.monotonic()
            print(f"START {variant} {sid}", flush=True)
            try:
                reply = client.chat.completions.create(model="echo", reasoning_effort=cfg["effort"], extra_body={"persona": cfg["persona"]}, messages=[{"role": "user", "content": prompt}])
            except Exception as exc:
                # Do not echo exception bodies/headers, which may contain credentials.
                print(f"FAILED {type(exc).__name__}", flush=True)
                raise SystemExit(1) from None
            record = {"variant": variant, "seed": sid, "run": args.run, "persona": cfg["persona"], "reasoning_effort": cfg["effort"], "source": cfg["source"], "prompt_template": cfg["template"], "messages": [{"role": "user", "content": prompt}], "started_utc": started, "seconds": round(time.monotonic() - t0, 2), "response": reply.model_dump(mode="json")}
            with path.open("x") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
                f.write("\n")
            choice = reply.choices[0]
            print(f"DONE {path.name}: {len((choice.message.content or '').split())} words, {record['seconds']}s, finish={choice.finish_reason}, model={reply.model}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
