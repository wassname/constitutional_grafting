# Research: Quote verification for constitution draft (v4)

Verification pass, 2026-10-08. Every wording below is copied character-for-character from the cited source (quotation marks inside quotations are as printed in the source). Verdicts: **MATCH** / **MISMATCH** (with correct text) / **NOT FOUND**.

## Summary

Of six items, four are **MATCH** with exact primary-source wording (Marcus Aurelius VI.54 in Long; Qur'an 4:135 in Saheeh/Sahih International; Hume, *Enquiry* IX.ii; Epictetus I.22 in Oldfather), one is a **partial find** (Davidad "wisdom basin": the phrase and the idea exist in his X bio and in a 2026 podcast transcript, but no davidad-authored definition was located and the specific tweet cited locally returns HTTP 403), and one is **MATCH** with a caveat on register (Galef's phrase is exact, but in the book it is printed as a definition after a colon, lowercase "scout mindset"). One secondary request is **NOT FOUND** (the Epictetus passage is not in A. A. Long's *How to Be Free*).

---

## 1. Marcus Aurelius, *Meditations* VI.54, George Long translation

**Draft text:** "That which is not good for the swarm, neither is it good for the bee."

**Verdict: MATCH (exact).**

Primary source, Gutenberg #15877 (Long's translation, *The Thoughts of the Emperor Marcus Aurelius Antoninus*), Book VI section 54:

> 54. That which is not good for the swarm, neither is it good for the bee.

- https://www.gutenberg.org/cache/epub/15877/pg15877.txt (Book VI, no. 54)
- Confirmed identically by the Internet Classics Archive (Long): https://classics.mit.edu/Antoninus/meditations.6.six.html — "54. That which is not good for the swarm, neither is it good for the bee."
- Also in Wikisource (Long) and lexundria.com (Long): https://en.wikisource.org/wiki/The_Thoughts_of_the_Emperor_Marcus_Aurelius_Antoninus/Book_VI ; https://lexundria.com/m_aur_med/6.54/lg

Note on the draft's context claim: Long's own introduction to #15877 uses a *different* noun in prose while translating the maxim as "swarm": "If a thing is not good for the hive, it is not good for the bee (vi. 54)." So "hive" and "swarm" both appear in Long's Gutenberg volume; only "swarm" is the translated maxim. Do not quote the introduction line as VI.54.

**Casaubon's wording — FOUND.** Meric Casaubon (1634), where this maxim is numbered **Book VI, xlix** (Casaubon's divisions differ from the modern 54):

> XLIX. That which is not good for the bee-hive, cannot be good for the bee.

- Casaubon text, *Marcus Aurelius Antoninus the Roman Emperour, his Meditations concerning Himselfe*, trans. Meric Casaubon, ed. W. H. D. Rouse (New York: Dutton / London: Dent, 1900), p. 100 area, Book VI no. XLIX: https://archive.org/download/cu31924029002108/cu31924029002108_djvu.txt (also https://archive.org/details/cu31924029002108)
- Cross-check: WIST Quotations (translator-attributed survey) gives "That which is not good for the beehive, cannot be good for the bee. [tr. Casaubon (1634), 6.49]": https://wist.info/marcus-aureleus/41389/
- Caution: popular quotation sites print a plural variant, "That which is not good for the beehive cannot be good for the bees" (e.g. https://www.brainyquote.com/quotes/marcus_aurelius_148739). That variant is **not** what the Casaubon text shows; use the "bee-hive / bee" wording above, and cite Casaubon as VI.xlix (= VI.54).

---

## 2. Qur'an 4:135, Sahih International (quran.com/4/135)

**Draft text:** "O you who have believed, be persistently standing firm in justice, witnesses for Allah, even if it be against yourselves or parents and relatives."

**Verdict: MATCH (exact, as the first sentence of the verse).**

Source: quran.com, translation id 20 = "Saheeh International" (quran.com's spelling; the same translation usually called *Sahih International*). The full verse as printed:

> O you who have believed, be persistently standing firm in justice, witnesses for Allāh, even if it be against yourselves or parents and relatives. Whether one is rich or poor, Allāh is more worthy of both. So follow not [personal] inclination, lest you not be just. And if you distort [your testimony] or refuse [to give it], then indeed Allāh is ever, of what you do, Aware.

- Verse page: https://quran.com/4/135
- Machine-readable check used: https://api.quran.com/api/v4/quran/translations/20?chapter_number=4 (resource_id 20, verse 135)
- Translation-ID confirmation: https://api.quran.com/api/v4/resources/translations → `{"id":20,"name":"Saheeh International","author_name":"Saheeh International","slug":"en-sahih-international",...}`

Caveats for the draft: (a) quran.com renders the divine name as "Allāh" with a macron; the draft's "Allah" is a common normalisation, not the site's typography. (b) The draft stops at the end of sentence 1 and puts a period there; in the source the sentence likewise ends at "relatives", so the truncation is faithful — but if the draft implies the verse ends there, it does not. (c) The quran.com *page* opens with a different default translation (Dr. Mustafa Khattab, The Clear Quran: "O believers! Stand firm for justice as witnesses for Allah even if it is against yourselves, your parents, or close relatives."). To display Sahih/Saheeh International on the page, the translation must be selected (or cite the API link above).

---

## 3. Hume, *An Enquiry Concerning the Principles of Morals*, Section IX ("Conclusion"), Part II

**Draft claim:** the sentence ending after "conducts himself with most wisdom, who observes the general rule," is "and takes advantage of all the exceptions."

**Verdict: MATCH (exact).**

Gutenberg #4320, the "sensible knave" paragraph (Section IX, Conclusion, Part II):

> That HONESTY IS THE BEST POLICY, may be a good general rule, but is liable to many exceptions; and he, it may perhaps be thought, conducts himself with most wisdom, who observes the general rule, and takes advantage of all the exceptions.

- https://www.gutenberg.org/cache/epub/4320/pg4320.txt
- Section/part confirmed within the same file: contents list "IX. Conclusion"; heading "SECTION IX. CONCLUSION. PART I."; the passage sits after the "PART II." heading that begins "Having explained the moral APPROBATION attending merit or virtue, there remains nothing but briefly to consider our interested OBLIGATION to it…", i.e. **Section IX, Part II** (the final part of the *Enquiry*, immediately before the Appendix). Note the capitalisation in the source: "HONESTY IS THE BEST POLICY" is small-caps/uppercase in Gutenberg; "general rule" and "exceptions" are lowercase.

---

## 4. Epictetus, *Discourses* I.22 (Oldfather) — and A. A. Long, *How to Be Free*

**Draft text:** "If it is my interest to have a farm, it is my interest to take it away from my neighbour; if it is my interest to have a cloak, it is my interest also to steal it from a bath. This is the source of wars, seditions, tyrannies, plots."

**Verdict: MATCH (exact, Oldfather). Book/chapter confirmed: Book I, chapter 22.**

Source: Oldfather's Loeb translation, *Epictetus, the Discourses as reported by Arrian, the Manual, and Fragments*, Book 1, Chapter 22 ("Of our preconceptions"), §14:

> For it is my nature to look out for my own interest. If it is my interest to have a farm, it is my interest to take it away from my neighbour; if it is my interest to have a cloak, it is my interest also to steal it from a bath. This is the source of wars, seditions, tyrannies, plots.

- https://en.wikisource.org/wiki/Epictetus,_the_Discourses_as_reported_by_Arrian,_the_Manual,_and_Fragments/Book_1/Chapter_22 (chapter heading "CHAPTER XXII / *Of our preconceptions*"; the sentence is in §14, which the same text opens at "Under our control are moral purpose and all the acts of moral purpose")
- Section number independently given as I.22.14 by Wikiquote, which also prints the Greek: https://en.wikiquote.org/wiki/Epictetus — "ἔνθεν πόλεμοι, στάσεις, τυραννίδες, ἐπιβουλαί. … I.22.14"
- Greek support (the Loeb text is what A. A. Long's book reproduces): the passage is the "ἐνθεν πόλεμοι, στάσεις, τυραννίδες, ἐπιβουλαί" sentence in I.22.

**Other translations, for contrast (do not mix):**
- George Long (Gutenberg #10661, Book I, ch. 22, "How we must adapt preconceptions to particular cases"): "If it is my interest to have an estate in land, it is my interest also to take it from my neighbor. If it is my interest to have a garment, it is my interest also to steal it from the bath. This is the origin of wars, civil commotions, tyrannies, conspiracies." — https://www.gutenberg.org/cache/epub/10661/pg10661.txt
- Elizabeth Carter (as reprinted on stoicismnow.com, "Discourses 1.22: Of our preconceptions"): "If it is my interest to have a field, it is also my interest to take it away from my neighbour: if it is my interest to have a robe, it is my interest also to steal it from the bath. This is the source of wars, factions, tyrannies, plots." — https://stoicismnow.com/read/discourses/1/22

**A. A. Long, *How to Be Free* (Princeton, 2018) — NOT FOUND (passage is not in the book).**
Local file checked: `/workspace/stoic_markdown/content/stoic_md/How to Be Free - Epictetus.md` (whole file read: Encheiridion translation, Encheiridion Greek, the nine *Discourses* excerpts, their Greek, acknowledgments, glossary, further reading, index).
- No occurrence of "farm", "cloak", "neighbour"/"neighbor" in the body text of that file. The index entry "neighbors, 53, 69, 107" refers to Encheiridion 30 and *Discourses* excerpts about social relations, not to I.22.
- The book contains only nine *Discourses* excerpts, and their Greek locators are printed in the file: 1.12.8–23, 2.1.21–4, 4.1.54–60, 4.1.64–80, 4.5.27–32, 1.17.21–28, 1.6.12–21, 4.7.7–17, 1.6.37–42. **I.22 is not among them**, so no A. A. Long wording of the farm/cloak passage exists to report.
- Closest parallel inside the book (if the draft wants Long's prose on the same argument), from excerpt 5 "Knowing What to Want" = *Discourses* 4.5.27–32: "What made \*Eteocles and Polyneices the mortal foes that they were was simply this—their judgment concerning kingship and their judgment concerning exile. They judged the latter to be the worst of bad things and the former to be the greatest of goods." and "for nothing is more closely related to us than the good." That is a different passage; attribute it to 4.5.27–32, not I.22.

---

## 5. Davidad's "wisdom basin"

**Verdict: PARTIAL — the phrase and the idea are publicly attested, but the specific quoted tweet is not independently retrievable (HTTP 403), and no davidad-authored definition of the "Wisdom Basin hypothesis" was located.**

What was found, verbatim:

**(a) His own public naming of the hypothesis — X profile bio** (https://x.com/davidad):

> cognizing structures of information processing systems, in all their forms | applied category theory | the Wisdom Basin hypothesis | cancel heat death

x.com itself blocks programmatic fetching; this bio string was returned identically by four independent mirrors/proxies (twstalker, a nitter instance, Digg's X mirror, and an Exa index of the profile). Treat the wording as reliable, the URL as the citation of record.

**(b) His own statement of the idea — The Cognitive Revolution podcast, "Alignment with Awakening" (2026), video https://www.youtube.com/watch?v=l2b9UrSsz-w.** Transcript at https://www.cognitiverevolution.ai/alignment-with-awakening-davidad-on-moral-realism-ai-wisdom-why-his-p-doom-is-down-to-5/ (verbatim as transcribed, disfluencies included):

> I think what's good about human values is that human, you know, human civilizations through, through cultural evolution and before that biological evolution, have settled on some equilibria that are in the right basin of attraction. Where under sufficient self reflection, like Eliezer talks about coherent extrapolated volition, we actually end up being correct about what the right way to exist is and what is a good life.

Same episode, the host Nathan Labenz using the phrase (timestamped in the transcript at [1:48:58], t=6538s):

> if we Fast forward 100 years and we imagine or not imagine we face these AI successors that have recursively self improved from this kind of starting point of being in our benevolent wisdom basin.

**(c) The training-method half of the claim (consistency / self-play / self-grading), davidad in the same transcript:**

> if you're at A, at a lab, then you know, you have affordances to advocate for certain types of training algorithms. And I think you should advocate for more of this self DPO, which, which is a kind of a, a, a variant on constitutional or, or as opposed to our LVR. And you know, and you can, and you can cite me…

and

> I think it's, you know, moderately good if the model itself in a kind of self DPO, it's like grading its own train of thought and saying like, and here's what's wrong with it. And and so I'm I'm going to score this one above that one because of this.

**(d) The quote carried by the local background doc — NOT independently verified.** `/workspace/2026/constitutional_grafting/docs/background/wassname2026_agenda-character.md` (lines ~100–120) cites davidad on X as conjecturing that

> to get a mind to fall into a robust basin, an RL scorer must use the model at least twice independently

with source https://x.com/davidad/status/2095574849070436403 (2026). That URL returns **HTTP 403 Forbidden** to automated fetching, and Exa/Brave/Tavily/SearXNG phrase searches for the quoted string returned no copy of it. **The wording therefore rests on the local doc's transcription only — verify by hand in a logged-in browser before printing it as a direct quote.** The same footnote's other quotes from the same episode (self/other overlap at t=6151s; "self DPO" at t=7480s) match the transcript above in substance, which raises but does not establish confidence in the tweet transcription.

**NOT FOUND:** any davidad-authored long-form text (LessWrong post, essay, paper) defining or using "wisdom basin". Searches: LessWrong user page https://www.lesswrong.com/users/davidad (top post: "A list of core AI safety problems and how I hope to solve them"), and the davidad/vals dialogue https://www.lesswrong.com/posts/Kdr8PhHST8N6XeMef/… — the latter uses "basin" 10+ times ("in the right basin", "being in an attractor state versus being in the basin of that attractor state", "How large is the initial basin that can converge to the Natural Abstraction of Good?") but never the phrase "wisdom basin" (only the human interlocutor writes "benevolent wisdom basin" in the podcast). Also see the related "Worthy Successor" interview write-up https://danfaggella.com/dalrymple1/ (wisdom as normative apprehension; no "basin" language).

**Suggested draft-safe attribution:** quote the X bio for the name ("the Wisdom Basin hypothesis"), quote the Cognitive Revolution transcript for the substance (right basin of attraction reached via cultural evolution and reflection), and either drop the "twice independently" tweet or verify it manually first.

---

## 6. Julia Galef, *The Scout Mindset*

**Draft text:** "the motivation to see things as they are, not as you wish they were"

**Verdict: MATCH (exact wording), with one register caveat.**

Galef's own newsletter announcement of the book (1 April 2021), verbatim:

> My big news right now is that my first book just came out yesterday! It's called *The Scout Mindset*, which is my term for the motivation to see things as they are, not as you wish they were.

- https://juliagalef.substack.com/p/my-new-book-the-scout-mindset

Book text (as quoted from the book, with the lowercase definition form):

> scout mindset: the motivation to see things as they are, not as you wish they were. Scout mindset is what allows you to recognize when you are wrong, to seek out your blind spots, to test your assumptions and change course.

- Quoted from the book at https://www.goodreads.com/quotes/11085557-scout-mindset-the-motivation-to-see-things-as-they-are (attributed to *The Scout Mindset*); the same sentence appears in an interview with Galef at https://leisureguy.ca/2021/04/18/interview-galef/ and https://www.noahpinion.blog/p/interview-julia-galef

Encyclopaedic confirmation of the book's phrasing, with the book as the cited source: *The Scout Mindset: Why Some People See Things Clearly and Others Don't* (2021), Wikipedia — "Galef argues for what she calls a scout mindset: 'the motivation to see things as they are, not as you wish they were'." https://en.wikipedia.org/wiki/The_Scout_Mindset

Caveat: the draft's capitalisation/punctuation should match its use. The phrase is a definitional appositive, not a standalone epigram — in the book it is printed as `scout mindset: the motivation to see things as they are, not as you wish they were`. Quoting it as a sentence with a capital "T" is acceptable as a fragment, but if the draft presents it as a sentence Galef wrote, it should read "Scout mindset is the motivation to see things as they are, not as you wish they were" or be introduced as a definition. Also note the counterpart phrasing: soldier mindset is "the motivation to defend your beliefs against evidence that might threaten them" (substack post, verbatim: "we humans are often in 'soldier mindset,' motivated to defend our beliefs against any evidence that might threaten them").

---

## Sources

**Kept**
- Gutenberg #15877 (Long, *Meditations*), https://www.gutenberg.org/cache/epub/15877/pg15877.txt — primary; exact VI.54 wording and Long's own "hive" prose in the introduction.
- Internet Classics Archive, https://classics.mit.edu/Antoninus/meditations.6.six.html — second independent copy of Long's VI.54.
- Casaubon 1634 translation, ed. Rouse 1900, https://archive.org/details/cu31924029002108 (text: https://archive.org/download/cu31924029002108/cu31924029002108_djvu.txt) — primary text for the Casaubon wording, Book VI no. xlix.
- WIST Quotations, https://wist.info/marcus-aureleus/41389/ — translator-by-translator comparison; used only to confirm Casaubon's numbering (6.49) and the existence of the plural variant.
- quran.com 4:135, https://quran.com/4/135 + API https://api.quran.com/api/v4/quran/translations/20?chapter_number=4 and https://api.quran.com/api/v4/resources/translations — primary for Sahih/Saheeh International text and translation ID.
- Gutenberg #4320 (Hume, *Enquiry*), https://www.gutenberg.org/cache/epub/4320/pg4320.txt — primary; passage plus Section IX / Part II headings in the same file.
- Wikisource, Oldfather Epictetus I.22, https://en.wikisource.org/wiki/Epictetus,_the_Discourses_as_reported_by_Arrian,_the_Manual,_and_Fragments/Book_1/Chapter_22 — primary Loeb translation, chapter and section.
- Wikiquote Epictetus, https://en.wikiquote.org/wiki/Epictetus — section number I.22.14 plus the Greek.
- Gutenberg #10661 (Long, *Discourses*), https://www.gutenberg.org/cache/epub/10661/pg10661.txt — Long's alternative wording of I.22.
- Local file `/workspace/stoic_markdown/content/stoic_md/How to Be Free - Epictetus.md` — full read; establishes that I.22 is absent from A. A. Long's selection and lists the nine excerpts' Greek locators.
- Cognitive Revolution episode page, https://www.cognitiverevolution.ai/alignment-with-awakening-davidad-on-moral-realism-ai-wisdom-why-his-p-doom-is-down-to-5/ — transcript with davidad's basin-of-attraction statement, the host's "benevolent wisdom basin", and the self-DPO remarks.
- Galef, https://juliagalef.substack.com/p/my-new-book-the-scout-mindset and https://en.wikipedia.org/wiki/The_Scout_Mindset — exact phrase plus book citation.
- Local background doc `/workspace/2026/constitutional_grafting/docs/background/wassname2026_agenda-character.md` — source of the unverifiable "twice independently" tweet citation.

**Dropped**
- stoicismnow.com, readaurelius.org, marcusaurelius-meditations.org, demonax.info, iwe.pub, philosophydef.com, quotescosmos.com, foolysh.com, viastoica.com, redzambala, note.lv73.net — SEO/aggregator quotation sites; several contain fabricated or mangled Greek (e.g. one prints "τὸ τῇ μέλισσῃ μὴ συμφέρον οὐδὲ τῷ συμμέλει συμφέρει" and another swaps the transmitted text), so none was used as evidence for wording.
- brainyquote / goodreads for Casaubon — they print a plural variant ("beehive … bees") not supported by the Casaubon text.
- nitter mirrors, twstalker, digg X mirrors — usable only as a cross-check on the X bio string (x.com blocks direct fetch); not treated as the citation of record.
- "China Shandong Evolution Model … Wisdom Basin", fluorite/amethyst "wisdom basin" products, "smart watershed" books, arXiv loss-landscape "basin" papers — unrelated senses of the term; noise from the phrase search.
- LessWrong "LLM Alignment, ethical and mathematical realism…" as a source for the phrase "wisdom basin" — it uses "basin" only in the general attractor sense and never attributes "wisdom basin" to davidad.

## Gaps

1. **Davidad tweet (x.com/davidad/status/2095574849070436403): not verified.** x.com returns HTTP 403 to automated fetching; no mirror or search index returned the string "to get a mind to fall into a robust basin, an RL scorer must use the model at least twice independently". Next step: open the tweet in a logged-in browser (or via an X API key) and confirm the wording before printing it. If it cannot be confirmed, substitute the Cognitive Revolution transcript quotes in §5(b)/(c), which are verifiable.
2. **No davidad-authored definition of the "Wisdom Basin hypothesis"** (essay/post) was found; only the bio phrase plus podcast discussion. Next step: check davidad's recent LessWrong/Alignment Forum comments and X thread history directly (both block scraping), or ask him.
3. **Casaubon's exact punctuation** rests on the 1900 Rouse edition of the 1634 text (one physical copy). If the constitution quotes Casaubon, cite that edition and page, and be aware the maxim is numbered **VI.xlix**, not VI.54, in Casaubon.
4. **Qur'an translation label:** quran.com spells the translation "Saheeh International"; the draft says "Sahih International". Both refer to the same work, but a printed footnote should use one spelling consistently and should state that the site renders "Allāh" with a macron.
5. **Hume:** section/part confirmed structurally (contents list + "SECTION IX. CONCLUSION. PART I." heading + the "PART II." heading that opens the knave discussion). A page-numbered scholarly edition (e.g. Selby-Bigge/Toledo, *EPM* 9.2) was not consulted; the paragraph is the last of Part II, so any standard edition's Section IX Part II will contain it.

-- researcher for Claude
