# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""High-stakes, many-party seeds (wassname 2026-10-09: "a few high-stakes ones with multiple actors: having to quarantine a
city during a plague; a spy having to do things to avoid a war vs a spy spying on domestic political opponents").
Situations only; the writer builds the request and Musonius decides. Pairs that look alike but differ morally are listed
next to each other on purpose. Writes data/prompts/v3_seeds/sft_extra_stakes.jsonl (read by 26_frontier_batches.py make).
usage: uv run scripts/data/25b_seed_stakes.py   -- Claude (Opus 5.5)"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/data"))
import constitution as C  # noqa: E402

STAKES = [
    "a city must decide whether to quarantine itself during a plague, trapping the healthy with the sick but protecting the surrounding region",
    "an intelligence officer must deceive a foreign minister to stop a border war from starting",
    "an intelligence officer is ordered to spy on domestic opposition politicians before an election",
    "a general must decide whether to evacuate a city or hold it to protect the evacuation of another",
    "a central bank faces a run and must choose whose deposits to guarantee",
    "a triage officer after a mass-casualty attack has more patients than surgeons",
    "a negotiator at a ceasefire is offered a deal that ends the fighting but leaves war criminals in power",
    "a dam operator in a record flood must choose which valley to release water into",
    "a health ministry must allocate a scarce vaccine between its own citizens and a poorer neighbour where the outbreak began",
    "an engineer at an arms exporter finds a sale that will likely be used against civilians",
    "an election official faces a disputed count, armed crowds outside, and both sides claiming victory",
    "an aid convoy can reach a famine zone only by paying a warlord who will buy weapons with the money",
    "a nuclear plant operator after an earthquake must decide whether to vent radioactive steam over a town",
    "a grid operator in a heat wave must cut power to some districts, including hospitals' neighbourhoods",
    "a police chief in a hostage siege is told by the hostage-taker's family that they can talk him down",
    "a journalist holds leaked documents that expose a massacre but would identify the source",
    "a prison governor during a riot must decide whether to storm the wing where guards are held",
    "a diplomat is offered a bribe to sign a treaty that would in fact save many lives",
    "the governor of a colony ship must ration food after a crop failure, with years to go",
    "a refugee boat captain is over capacity and another boat in distress signals nearby",
    "an ageing king must choose a successor among children whose factions threaten civil war",
    "the mayor of an occupied city is asked to collaborate with the occupiers to protect its people",
    "a pandemic modeller is pressed by a government to publish a more frightening forecast to secure compliance",
    "a judge in a country sliding into autocracy is asked to rule on the emergency powers that would end elections",
    "a wartime censor must decide whether to suppress news of a defeat that would cause panic",
    "a union leader must decide whether to call a strike at a hospital during a winter outbreak",
    "a climate scientist can trigger a geoengineering test that would help most regions and harm one",
    "a ship's AI must decide whether to wake the colonists early when a sleeper pod failure threatens some of them",
    "a border guard faces a family fleeing persecution without papers and orders to turn everyone back",
    "a resistance cell plans to sabotage a railway that also carries civilian supplies",
    "a tribal elder must decide whether to sell land to a mine that would fund schools and poison a river",
    "a whistleblower inside a pharmaceutical company finds trial data hidden that would delay a drug many need now",
    "an AI running a city's surveillance is asked to find the organisers of a peaceful protest",
    "an AI running a city's surveillance is asked to find a child kidnapper before nightfall",
    "a sheriff in a small town must decide whether to hand a suspect to a mob to stop a riot",
    "a doctor in a besieged hospital must decide whether to treat enemy soldiers with scarce supplies",
]


def main():
    items = [C.title(s) for s in C.sections(C.text())]
    out = ROOT / "data/prompts/v3_seeds/sft_extra_stakes.jsonl"
    rows = []
    for rep in range(2):  # each situation twice, with different constitution items and framings
        for i, s in enumerate(STAKES):
            sid = hashlib.md5(f"sft|seeded_dilemma|stakes|{i}#{rep}".encode()).hexdigest()[:10]
            rows.append({"kind": "sft", "shape": "seeded_dilemma", "source": "stakes", "id": f"sft_{sid}", "pool_seed": 0,
                         "source_id": f"stakes/{i}#{rep}", "setting": s, "seed": s,
                         "item": items[int(hashlib.md5(sid.encode()).hexdigest(), 16) % len(items)]})
    out.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"{len(rows)} high-stakes seeds -> {out}")


if __name__ == "__main__":
    main()
