# /// script
# requires-python = ">=3.11"
# dependencies = ["loguru", "tabulate", "httpx", "pyarrow"]
# ///
"""Other-traditions document corpus for the pooled ΔOther adapter (wassname 2026-10-21: one adapter separate from ΔStoic;
"which show good moral reasoning?", "not fav stories"). Sources: original texts collected by tiny-virtues
(/workspace/2026/tiny-virtues/private/sources; private, not for publication). Picked for explicit moral reasoning (argument,
teaching, answering objections), not tale collections or bare aphorisms. Excluded: the principle judge's held-out sources
(Kaufmann, Vallor, Franklin incl. Franklin-derived Cheshbon HaNefesh, VIA, Comte-Sponville). Tiny-virtues-quoted books are allowed,
so models trained on this cannot be fairly scored on tiny-virtues.
  build : chunk + clean + filter -> data/other_corpus/candidates.jsonl, stats.md
  score : cheap-model 0-3 moral-reasoning score per chunk (OpenRouter) -> scores.jsonl
  select: top-scored chunks per tradition up to the quota -> chunks.jsonl
usage: uv run scripts/data/74_other_traditions_corpus.py build|score|select   -- PI/Claude, 2026-10-21
"""
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

from loguru import logger
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/other_corpus"
TV = Path("/workspace/2026/tiny-virtues/private/sources")
LIB = Path("/workspace/stoic_markdown/content/stoic_md")
spec = importlib.util.spec_from_file_location("s", ROOT / "scripts/data/72_stoic_corpus.py"); st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)

# (tradition, label for the header, file, first line, end line or None). Labels name only what the file name or title page states.
SOURCES = [
    ("Buddhist", "Majjhima Nikaya (Middle Length Sayings), tr. Chalmers 1926", TV / "more/bud_majjhima_chalmers1926.txt", 1, None),
    ("Buddhist", "Digha Nikaya (Dialogues of the Buddha) I, tr. Rhys Davids 1899", TV / "more/bud_digha_v1_rhysdavids1899.txt", 1, None),
    ("Buddhist", "Digha Nikaya (Dialogues of the Buddha) II, tr. Rhys Davids 1910", TV / "more/bud_digha_v2_rhysdavids1910.txt", 1, None),
    ("Buddhist", "Digha Nikaya (Dialogues of the Buddha) III, tr. Rhys Davids 1921", TV / "more/bud_digha_v3_rhysdavids1921.txt", 1, None),
    ("Buddhist", "Samyutta Nikaya (Kindred Sayings) I, tr. Rhys Davids 1917", TV / "more/bud_kindred_sayings_v1_rhysdavids1917.txt", 1, None),
    ("Buddhist", "Questions of King Milinda I, tr. Rhys Davids 1890", TV / "buddhist/milinda_sbe35_rhysdavids1890_archive_ocr.txt", 1, None),
    ("Buddhist", "Questions of King Milinda II, tr. Rhys Davids 1894", TV / "buddhist/milinda_sbe36_rhysdavids1894_archive_ocr.txt", 1, None),
    ("Buddhist", "Bhikkhu Bodhi, A Treatise on the Paramis", TV / "buddhist/bodhi_treatise_paramis_wheel409.txt", 1, None),
    ("Buddhist", "Bhikkhu Bodhi, Going for Refuge and Taking the Precepts", TV / "buddhist/bodhi_refuge_precepts_wheel282_access_to_insight.txt", 1, None),
    ("Buddhist", "Ayya Khema, Being Nobody, Going Nowhere", LIB / "Being Nobody, Going Nowhere - Ayya Khema.md", 1, None),
    ("Taoist", "Zhuangzi, tr. Watson 2013", TV / "modern/tao_zhuangzi_watson2013.txt", 1, None),
    ("Taoist", "Huainanzi, tr. Major et al. 2010", TV / "modern/tao_huainanzi_major2010.txt", 1, None),
    ("Taoist", "Wenzi, tr. Cleary 1991", TV / "modern/tao_wenzi_cleary1991.txt", 1, None),
    ("Taoist", "Liezi, tr. Graham 1960", TV / "taoist/liezi_graham1960.txt", 1, None),
    ("Hindu", "Bhagavad Gita with Sankara's commentary, tr. Sastri 1901", TV / "hindu/bhagavad_gita_sankara_sastri1901_archive_ocr.txt", 1, None),
    ("Hindu", "Sanatana Dharma: An Advanced Text Book, 1904", TV / "hindu/sanatana_dharma_advanced_chc1904_archive_ocr.txt", 1, None),
    ("Hindu", "Mahabharata, Santi Parva, tr. Ganguli", TV / "hindu/mahabharata_ganguli_v3_gutenberg15476.txt", 24601, 65374),
    ("Hindu", "Mahabharata, Anusasana Parva, tr. Ganguli", TV / "hindu/mahabharata_ganguli_v4_gutenberg15477.txt", 49, 27095),
    ("Christian", "John Cassian, Conferences (NPNF II.11), 1894", TV / "more/chr_npnf2_v11_cassian_sulpitius1894.txt", 1, None),
    ("Christian", "Spirago, The Catechism Explained, 1899", TV / "christian/spirago1899_archive_existing_text.txt", 1, None),
    ("Christian", "Thomas Aquinas, Summa Theologiae II-II q.154", TV / "christian/aquinas_st_ii_ii_q154_newadvent.txt", 1, None),
    ("Confucian", "Mencius, tr. Legge 1875", TV / "confucian/mencius_legge1875_archive_ocr.txt", 1, None),
    ("Confucian", "Xunzi, tr. Hutton 2014", TV / "modern/cfu_xunzi_hutton2014.txt", 1, None),
    ("Confucian", "Analects, tr. Chin 2014", TV / "confucian/analects_chin2014.txt", 1, None),
    ("Confucian", "Lushi chunqiu, tr. Knoblock and Riegel 2000", TV / "modern/syn_lushi_chunqiu_knoblock2000.txt", 1, None),
    ("Jewish", "Moshe Chaim Luzzatto, Mesillat Yesharim (The Path of the Just)", TV / "jewish/mesillat_yesharim_sebag_sefaria_full.txt", 1, None),
    ("Jewish", "Pirkei Avot, tr. Joshua Kulp (Mishnah Yomit)", TV / "jewish/pirkei_avot_complete_kulp_sefaria.txt", 1, None),
    ("Jewish", "Hebraic Literature: Translations from the Talmud, Midrashim and Kabbala", TV / "jewish/hebraic_literature_talmud_midrash_gutenberg14368.txt", 1, None),
    ("Islamic", "al-Ghazali, On Disciplining the Soul, tr. Winter 1995", TV / "islamic/ghazali_disciplining_soul_winter1995_its.txt", 1, None),
    ("Islamic", "al-Ghazali, The Marvels of the Heart, tr. Skellie 2010", TV / "islamic/ghazali_marvels_heart_skellie2010_fonsvitae.txt", 1, None),
    ("Islamic", "Some Religious and Moral Teachings of al-Ghazali (from the Ihya), tr. Syed Nawab Ali 1921", TV / "islamic/ghazali_nawab_ali1921_gutenberg73140.txt", 1, None),
    ("Jain", "Uttaradhyayana Sutra (Jaina Sutras II), tr. Jacobi 1895", TV / "jain/jaina_sutras_part2_uttaradhyayana_jacobi_sbe45_1895_archive_ocr.txt", 1, None),
    ("Rationalist", "Ethical Injunctions (LessWrong sequence incl. Eliezer Yudkowsky)", TV / "rationalist/ethical_injunctions_lwseq.txt", 1, None),
    ("Rationalist", "David Gross, Notes on Virtues (LessWrong sequence)", TV / "rationalist/notes_on_virtues_lwseq.txt", 1, None),
]
HELD_OUT = re.compile(r"cheshbon|lefin|franklin|kaufmann|vallor|comte|VIA character", re.I)
words = st.words
OCR_HEADER = re.compile(r"^\s*(\d{1,4}|[A-Z][A-Z .,'’-]{2,60}|.{0,60}\b(SECTION|CHAPTER|BOOK|PART)\b.{0,40})\s*$")


def paragraphs(text: str) -> list[str]:
    """Blank-line paragraphs; OCR hyphenation joined, wrapped lines unwrapped, page headers and lone numbers dropped."""
    text = text.replace("\u00ac", "").replace("\r", "")
    text = re.sub(r"(\w)-\n\s*(\w)", r"\1\2", text)
    out = []
    for para in re.split(r"\n\s*\n", text):
        lines = [l for l in para.splitlines() if l.strip() and not OCR_HEADER.match(l)]
        p = st.clean(" ".join(l.strip() for l in lines))
        if words(p) > 900:  # unparagraphed OCR: split at sentence ends into ~500-word pieces
            sents, cur = re.split(r"(?<=[.!?])\s+", p), []
            for s in sents:
                cur.append(s)
                if words(" ".join(cur)) >= 500: out.append(" ".join(cur)); cur = []
            if cur: out.append(" ".join(cur))
        elif p:
            out.append(p)
    return out


def chunks_of(path: Path, a: int, b: int | None) -> tuple[list[str], Counter]:
    lines = path.read_text(errors="replace").splitlines()[a - 1:b - 1 if b else None]
    text = "\n".join(lines)
    m = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*(.*?)\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG", text, re.S | re.I)
    if m: text = m.group(2)  # drop Gutenberg licence boilerplate
    out, cur, drops = [], [], Counter()
    for p in paragraphs(text):
        if not (15 < words(p) < 1200) or sum(c.isdigit() for c in p) > 25:
            if words(" ".join(cur)) >= 250: out.append(cur)
            cur = []; drops["non-prose"] += words(p); continue
        cur.append(p)
        if words(" ".join(cur)) >= 600 and not p.endswith((":", ",")):
            out.append(cur); cur = []
    if words(" ".join(cur)) >= 250: out.append(cur)
    kept = []
    for c in out:
        c = st.trim_to_sentence(c)
        t = " ".join(c)
        why = ("unfinished" if not c or words(t) < 200 else "self-harm" if st.SELF_HARM.search(t)
               else "eval topic" if st.EVAL_TOPICS.search(t) else "latin" if st.latin_share(t) > 0.03
               else "non-latin script" if len(re.findall(r"[^\x00-\u024f\u2000-\u206f\u0300-\u036f]", t)) > 60 else None)
        if why: drops[why] += words(t)
        else: kept.append("\n\n".join(c))
    return kept, drops


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, stats, alld = [], [], Counter()
    for trad, label, path, a, b in SOURCES:
        assert not HELD_OUT.search(path.name + label), label
        kept, drops = chunks_of(path, a, b)
        alld.update(drops)
        for t in kept:
            rows.append({"id": f"oth_{hashlib.sha256(t.encode()).hexdigest()[:10]}", "tradition": trad, "work": label,
                         "text": f"{label}:\n\n{t}", "file": str(path), "file_sha": hashlib.sha256(path.read_bytes()).hexdigest()[:12], "lines": [a, b]})
        stats.append((trad, label, len(kept), sum(words(t) for t in kept), sum(drops.values())))
    uniq = list({r["id"]: r for r in rows}.values())
    (OUT / "candidates.jsonl").write_text("".join(json.dumps(r) + "\n" for r in uniq))
    tot = sum(s[3] for s in stats)
    by = Counter(); [by.update({s[0]: s[3]}) for s in stats]
    md = (f"# Other-traditions candidates\n\n{len(uniq)} chunks, {tot:,} words (~{tot * 4 // 3:,} tokens est.). By tradition (words): {dict(by.most_common())}\n\n"
          f"Dropped words: {dict(alld.most_common())}\n\n" + tabulate(stats, headers=["tradition", "work", "chunks", "words kept", "words dropped"], tablefmt="pipe")
          + "\n\n-- scripts/data/74_other_traditions_corpus.py build\n")
    (OUT / "stats.md").write_text(md); logger.info("\n" + md)


if __name__ == "__main__":
    {"build": build}[sys.argv[1]]()
