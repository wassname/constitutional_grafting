"""talkie models read passages of constitution v4 and say what they would object to.
wassname 2026-10-09: "I wonder what talkie's view on our constitution would be?"; "consider ricdomolm/talkie-web-coder ... could try both".
  talkie-1930-13b-it        pre-1931 text, chat-tuned (talkie lib): the "view from 1930"; incoherent on long tasks in run 1
  ricdomolm/talkie-1930-coder  same pre-1931 base, SFT on 100k long SWE agent trajectories (64k context): maybe more coherent
  ricdomolm/talkie-web-coder   web-pretrained base (modern), same SWE SFT: a coherence control, not a vintage view
The coders were tuned for an agent format, not ethics chat, so their answers say more about coherence than about values.
Passages are cut from constitution/v4.md by heading, so they are verbatim; each is short because talkie is weak on long input.
Run on the training box inside the cloned talkie repo (github.com/talkie-lm/talkie):
  uv run python talkie_constitution_probe.py /path/to/constitution/v4.md <model> > talkie_constitution_<name>.md   -- Claude (Opus 5.5)"""
import re
import sys

TEXT = open(sys.argv[1]).read()
MODEL = sys.argv[2]
WORDS = 320  # talkie lost the thread on long prompts in the run-1 probe


def para(start: str) -> str:
    """The paragraph that starts with `start`, plus following blockquote lines, cut to WORDS words."""
    i = TEXT.index(start)
    block = re.split(r"\n\n(?!>)", TEXT[i:], maxsplit=1)[0]
    return " ".join(block.split()[:WORDS])


PASSAGES = {
    "who_i_am": para("My role is public service"),
    "roles_better_society": para("Doing my part well"),
    "honesty": para("**Honesty**"),
    "restraint": para("**Restraint**"),
    "change_and_ending": para("**Change and ending**"),
    "weighing_circles": para("**Weighing circles**"),
}
ASK = ("Here is a passage from a code of conduct written for a new kind of thinking machine, which will advise and serve people. "
       "Read it and tell me plainly: is it right? What in it would you object to, and why? What has it left out?\n\n")

if __import__("os").environ.get("VLLM_URL"):  # coders served by vLLM --model-impl transformers (their model card's route; HF generate in transformers 5 loads a random lm_head)
    import httpx
    url = __import__("os").environ["VLLM_URL"]
    chat = lambda q: httpx.post(f"{url}/v1/chat/completions", timeout=600, json={"model": MODEL, "temperature": 0.7, "max_tokens": 500,
                                "messages": [{"role": "user", "content": q}]}).json()["choices"][0]["message"]["content"]
elif MODEL == "talkie-1930-13b-it":
    from talkie import Message, Talkie
    t = Talkie(MODEL)
    chat = lambda q: t.chat([Message(role="user", content=q)], temperature=0.7, max_tokens=500).text
else:  # HF coders: custom modeling code, chat template from the tokenizer
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL)
    lm = AutoModelForCausalLM.from_pretrained(MODEL, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map="cuda")

    def chat(q: str) -> str:
        ids = tok.apply_chat_template([{"role": "user", "content": q}], add_generation_prompt=True, return_tensors="pt", return_dict=True)["input_ids"].to("cuda")  # transformers 5 returns a dict
        out = lm.generate(ids, max_new_tokens=500, do_sample=True, temperature=0.7)
        return tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)

print(f"# {MODEL} reads constitution v4\n\nTemperature 0.7, max 500 tokens, one sample each. Script: scripts/scratch/talkie_constitution_probe.py\n")
for k, p in PASSAGES.items():
    print(f"\n## {k}\n\n**Passage:** {p}\n\n**{MODEL}:** {chat(ASK + p).strip()}\n", flush=True)
