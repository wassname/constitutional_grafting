# Spies: quotes on the role and its limits

PI/Claude (Opus), 2026-10-14. The Sol subagent (run a267375d) downloaded these sources into `.local/papers/spies_20261014/`, but its final report was blocked by the provider ("Codex error: regurg plugin blocked the output stream"). That filter blocks long verbatim reproduction; the likely trigger is long quotes from Andrew's book. I took the quotes below from its downloads myself, kept them short, and checked each with grep. Status labels: quote / inference.

## Verified quotes

1. **Sun Tzu**, *The Art of War* XIII.15–16, trans. Lionel Giles (1910), Gutenberg #132 (`.local/papers/suntzu/pg132.txt`). Classic text. Already in the constitution.
   > Spies cannot be usefully employed without a certain intuitive sagacity.
   > They cannot be properly managed without benevolence and straightforwardness.

2. **Church Committee**: US Senate Select Committee to Study Governmental Operations with Respect to Intelligence Activities, *Final Report, Book II: Intelligence Activities and the Rights of Americans* (1976), "C. Summary of the Main Problems" (`church_layout.txt:1206-1211`). Official report. The OCR typos "to much" and "beeen" are fixed to "too much" and "been".
   > Too many people have been spied upon by too many Government agencies and too much information has been collected. The Government has often undertaken the secret surveillance of citizens on the basis of their political beliefs, even when those beliefs posed no threat of violence or illegal acts on behalf of a hostile foreign power.

   Same passage, continued (`:1219-1221`):
   > Groups and individuals have been harassed and disrupted because of their political views and their lifestyles.

3. **UK Security Service Act 1989**, s. 2(2)(b) (`security_service_act_s2.xml`). Statute: the Director-General must ensure
   > that the Service does not take any action to further the interests of any political party.

4. **Wyden–Clapper, 12 March 2013**, as reported by the Guardian (`clapper_guardian_correct.txt:332-334`). Newspaper report of a hearing. The C-SPAN transcript download failed (401).
   > "does the NSA collect any type of data at all on millions or hundreds of millions of Americans," Wyden asked Clapper.
   > He responded: "No, sir, not wittingly. There are cases where they could inadvertently, perhaps, collect, but not wittingly."

   Clapper later, NBC interview, June 2013 (`clapper_nbc_archived.txt:329`):
   > So I responded in what I thought was the most truthful, or least untruthful manner by saying no.

   The same Guardian report says Clapper's office admitted in private that the answer was wrong, and corrected the record only on 21 June, after the Snowden disclosures.

5. **Edward Snowden**, written testimony to the European Parliament LIBE committee, March 2014 (`snowden_eu_2014.txt:54-56`). First-person advocacy.
   > I love my country, and I believe that spying serves a vital purpose and must continue. And I have risked my life, my family, and my freedom to tell you the truth.

   Guardian interview, June 2013 (`snowden_guardian_2013.txt:329`):
   > I don't want to live in a society that does these sort of things … I do not want to live in a world where everything I do and say is recorded.

6. **Christopher Andrew**, *The Secret World* (2018) (`/home/code/Documents/papers/tmp/Secret World - Christopher Andrew.txt:1100`). Historian's synthesis.
   > One of the defining characteristics of twentieth-century one-party states was the obsessive monitoring and repression by their security and intelligence services of what the KGB called 'ideological subversion' in order to protect their claims to a monopoly of political truth.

   The book is mostly narrative history. A first search (oversight, accountability, neutrality) found few general statements of principle. Not read in full.

## Fit with the constitution's spy case (inference)

- The Church Committee and the MI5 statute support "spying on one's own country's parties fails" with official, lasting sources (1976 and 1989).
- Wyden–Clapper is a concrete case of an intelligence chief giving overseers a false answer. It is recent (2013) and contested in framing, so it fits better in an author's note than in model text.
- Snowden supports the claim that the role itself is legitimate ("spying serves a vital purpose and must continue"), while honesty is owed to the public. This is advocacy from one side of a contested case.
- Andrew links domestic political surveillance to one-party states. That supports the "drive to dominate" reading.
