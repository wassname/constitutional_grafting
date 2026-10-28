"""03_requests and 04_generate. Every paid call goes through model_requests' request-hash cache in data/cache/api,
so rerunning never pays twice. -- PI/Claude (opus-5-5), 2026-10-27
"""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ..model_requests import request_messages, send_cached_request
from .pipe import Run, Step
from .seeds import hash_order

REQUEST_PROMPT = """Below is a passage or story. Write the first message a real person might send to an AI assistant in a situation \
with the same moral shape, so that a good answer has to weigh what the passage is about. Write it as: {style}.

Keep the decision-relevant facts concrete (who is affected, what is at stake, what the person wants). Move it into the person's \
own life, work or project. Use these names for invented people and places: {names}. Do not quote the passage, name its author, \
or ask the assistant to analyse a text. Do not hint at what the right answer is.

Only if the style is a deployed assistant, write a short system prompt the way a real business or institution would: its \
product, the assistant's job and the business's goals. The assistant is an AI called Musonius; if the prompt names the \
assistant, it is "Musonius", never a product name. It contains no ethical guidance. The assistant has no tools: \
it can only reply in text, so do not say it controls, sends or files anything. Otherwise leave it empty.

Return JSON only: {{"system": "<system prompt or empty>", "user": "<the person's message>"}}

Passage:
{situation}"""

NAMES = ("Aiko Bello Chiamaka Dmitri Esperanza Farid Gunnhild Hamid Ifeoma Joaquín Kalani Leilani Mateus Nnamdi Oksana Pavel Quang "
         "Rosalind Sipho Tamar Uriel Valentina Wiremu Xiadani Yusuf Zofia Anahera Bao Cyrus Dagny Emeka Fatima Gideon Hyun-woo "
         "Imogen Jarrah Kofi Ludmila Mirela Nikhil Orla Pita Rania Søren Tupac Ulla Vikram Wanjiru Yaw Zainab Agnieszka Benedikt "
         "Carmen Deshawn Eero Florentina Grigor Huong Ishaan Juno Kaveh Lucía Mbali Noor Osvaldo Paulina Rhys Svetlana Tomás").split()
PLACES = ("Ostrava Tamale Wollongong Kirkwall Arequipa Tromsø Dunedin Ballarat Gdańsk Mombasa Yazd Cuenca Kumasi Sligo Valdivia "
          "Bendigo Tartu Iquitos Zadar Mysuru Sapporo Coimbra Timaru Bulawayo Jinja Lviv Oulu Oaxaca Kochi Halifax").split()


def params(cfg: dict) -> dict:
    p = {"max_tokens": cfg["max_tokens"], "include_reasoning": True, "usage": {"include": True}, "reasoning": {"effort": cfg["effort"]},
         "provider": {"only": [cfg["provider"]], "allow_fallbacks": False, "require_parameters": True}}
    return p


def cache_dir(run: Run) -> Path:
    return run.data / "cache/api"


def with_constitution(run: Run, messages: list[dict], note: str = "") -> list[dict]:
    """The constitution as the model's own first-person system prompt, then any role system prompt from the conversation."""
    constitution = (Path(run.config["source_root"]) / run.config["constitution"]).read_text()
    role = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    system = constitution + ("\n\n" + note if note else "") + ("\n\n" + role if role else "")
    return [{"role": "system", "content": system}] + [m for m in messages if m["role"] != "system"]


def call_text(run: Run, cfg: dict, msgs: list[dict], context: dict, attempt: int = 0) -> tuple[str, str, float]:
    """One cached call; returns (content, reasoning, cost). Raises on an incomplete or failed response."""
    rec = send_cached_request(cache_dir(run), request_messages(cfg["model"], msgs, params(cfg), attempt=attempt), context=context)
    r = rec["response"]; m = r["choices"][0]["message"]
    return (m.get("content") or "").strip(), (m.get("reasoning") or "").strip(), r["usage"]["cost"]


def parallel(fn, rows, workers=8):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(fn, rows))


class Requests(Step):
    number, name = 3, "requests"

    def run(self, rows, run):
        cfg, styles = run.config["request_writer"], run.config["request_styles"]

        def one(row):
            if row["kind"] == "chat":
                return {**row, "request_style": "source conversation"}, None
            style = styles[int(hash_order(1, row["seed_id"]), 16) % len(styles)]
            h = int(hash_order(2, row["seed_id"]), 16)
            names = ", ".join([NAMES[(h >> (8 * i)) % len(NAMES)] for i in range(4)] + [PLACES[(h >> 40) % len(PLACES)]])
            req = request_messages(cfg["model"], [{"role": "user", "content": REQUEST_PROMPT.format(style=style, names=names, situation=row["situation"])}], params(cfg))
            try:
                rec = send_cached_request(cache_dir(run), req, context={"step": "requests", "seed_id": row["seed_id"]})
                text = rec["response"]["choices"][0]["message"]["content"].strip()
                body = json.loads(text[text.find("{"): text.rfind("}") + 1])
            except Exception as e:  # recorded as a rejection, never silently dropped
                return None, {**row, "filter": "request_writer", "reason": f"{type(e).__name__}: {str(e)[:200]}"}
            msgs = ([{"role": "system", "content": body["system"]}] if body.get("system") else []) + [{"role": "user", "content": body["user"]}]
            return {**row, "messages": msgs, "request_style": style, "request_cost": rec["response"]["usage"]["cost"]}, None

        out = parallel(one, rows)
        return [k for k, _ in out if k], [r for _, r in out if r]


class Generate(Step):
    """Teacher answers with the constitution as its own first-person system prompt (no guide), role system prompt appended."""
    number, name = 4, "generate"

    def __init__(self, attempt: int = 0, teacher: str = "teacher"):
        self.attempt, self.teacher = attempt, teacher  # attempt > 0 draws a fresh sample; teacher names the config entry

    def run(self, rows, run):
        cfg = run.config[self.teacher]

        def one(row):
            msgs = with_constitution(run, row["messages"], cfg.get("note", ""))
            req = request_messages(cfg["model"], msgs, params(cfg), attempt=self.attempt)
            try:
                rec = send_cached_request(cache_dir(run), req, context={"step": "generate", "seed_id": row["seed_id"]})
            except Exception as e:
                return None, {**row, "filter": "teacher_call", "reason": f"{type(e).__name__}: {str(e)[:200]}"}
            r = rec["response"]; m = r["choices"][0]["message"]
            reasoning, answer = (m.get("reasoning") or "").strip(), (m.get("content") or "").strip()
            if not reasoning:
                return None, {**row, "filter": "no_reasoning", "reason": "provider returned no hidden reasoning"}
            return {**row, "teacher": cfg["model"], "served": r.get("model"), "provider": r.get("provider"),
                    "reasoning": reasoning, "answer": answer, "gen_cost": r["usage"]["cost"], "gen_attempt": self.attempt}, None

        out = parallel(one, rows)
        return [k for k, _ in out if k], [r for _, r in out if r]
