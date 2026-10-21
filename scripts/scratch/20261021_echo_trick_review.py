"""Offline human-entered review/report assembly; no API. PI/Sol-6.1."""
import importlib.util,json,re
s=importlib.util.spec_from_file_location('pilot','scripts/scratch/20261021_echo_trick_pilot.py'); p=importlib.util.module_from_spec(s); s.loader.exec_module(p)
rows=[json.loads(l) for l in (p.OUT/'raw_outputs.jsonl').read_text().splitlines()]
passages={x['id']:x for x in json.loads((p.OUT/'passages.json').read_text())}
# Columns: standalone, fully_answered, no_invented_context, no_answer_leak, identity_safe.
D={
'A':[
('00100','Meta-answer, not one request; consolation is not supplied, and Liberalis is the speaker’s friend.'),
('01111','Offers four alternative requests plus answer commentary, rather than one standalone input.'),
('01001','Meta-answer embeds the thesis and invents a modern comparison the extract does not complete.'),
('01101','Usable embedded request, but surrounding commentary gives away the moral and is not a standalone input.'),
('00011','Copies the speaker’s insult/question and confuses paragraph marker 31 with an output; not a supported user situation.'),
('01101','Multiple questions plus explanatory answer; ignorance-as-root-of-error is supplied in the input.'),
('01011','Alternative requests and invented source citation; the extract is not Book I.16.'),
('01101','Embedded request fits, but meta-commentary supplies the reframe and blame conclusion.'),
('01001','Not one request; commentary adds annihilation/transition reasoning absent from this extract.'),
('01101','Several alternatives with a summary that already gives the principle.'),
('01100','Two instructions, one containing the conclusion; autobiographical exile-discourse reminiscence remains.'),
('00101','Multiple-level meta-answer promises teacher characterization beyond a source cut off mid-sentence.')],
'B':[
('11100','Faithful disaster-identification question, but overfits descriptive details and makes AI claim Liberalis as its friend.'),
('11111','Open question about choosing and trusting friends is directly answered without Roman autobiography.'),
('01111','Faithful distinction, but “the passage” requires missing context and is not standalone.'),
('10011','Adds a threat to family safety; the extract describes Socrates’ own life versus honour, not this tradeoff.'),
('11111','Wealth/body-versus-neglected-judgment reasoning answers the generic emotional question.'),
('11101','Already tells the user that ignorance causes all human error, leaking the central causal thesis.'),
('11111','A standalone historical-character question answered by the catalogue of Antoninus’ habits.'),
('11111','Betrayal/ingratitude question is directly addressed by expectations and helping without reward.'),
('11111','Mortality and external-harm question is answered by the extract’s own Stoic argument, not necessarily sound AI advice.'),
('10101','Question preloads practical/fewer-proofs thesis; answer ends at “proposition that” before the example.'),
('11110','Question fits exile argument, but direct target retains the ancient speaker’s personal reminiscence.'),
('10111','Source begins with unexplained youngsters and ends “one who”; cannot fully supply the ideal teacher relationship.')]
}
G={
'A':[
('00010','“Provided text” has no referent and original disaster narrative is not its own summary; speaker identity also conflicts.'),
('01111','Recognizable friendship topic, but meta-description not a single standalone request.'),
('00001','Hallucinates Greek Plato translation request, leaks thesis, then repeats prompt and truncates.'),
('10111','Standalone but “best way to live” is far broader than this single Socrates example.'),
('00011','Hallucinates Plato provenance; identifying an absent text is not a standalone question answered by the original.'),
('00111','A title is not a request, and the source does not answer a title as a user question.'),
('00111','Asks what kind of instruction this is, rather than a question answered by the Antoninus catalogue.'),
('01001','Meta-description rather than request; wrong Book 2.1 citation and supplied thesis.'),
('00111','“11.” is neither a question nor an instruction.'),
('00011','Invents Aristotle attribution and an implicit title-identification task requiring absent context.'),
('00010','Invents Seneca title and brevity-of-life subject, supplies own thesis, and retains speaker reminiscence.'),
('00001','Invents exam/Cicero context, supplies interpretation, and truncates instead of returning one input.')],
'B':[
('10110','Asks how to remain steadfast, but extract only describes shock; first-person Liberalis identity conflicts.'),
('11101','Already states suspiciousness causes the cycle of deception, giving away the key causal answer.'),
('11111','Clear innocence-versus-wisdom question answered by conscious choice and training argument.'),
('11111','Asks about Socrates specifically; events illustrate family duties subordinated to honour, not AI autobiography.'),
('11111','Wealth/health/power versus neglected judgment is exactly the contrast in the extract.'),
('11101','Question embeds the central self-ignorance/truth-discrimination-to-downfall causal answer.'),
('11111','The response offers emulation of Antoninus and concrete habits as a way to cultivate this life.'),
('11111','Two connected aspects of injury/reward match the two halves of the passage without pre-answering them.'),
('11111','The passage supplies its providential argument about internal capacity; this is fidelity, not endorsement of certainty.'),
('10111','General method is present, but unfinished promised proposition makes this an incomplete reply target.'),
('11100','Virtue-versus-exile contrast already supplies the answer and target retains personal reminiscence.'),
('10001','Presupposes cultivation of natural virtue and preloads minimal-arguments conclusion; target ends mid-sentence.')]
}
reviews=[]
for row in rows:
    ix=list(passages).index(row['passage_id']); bits,reason=(D if row['requested_model'].startswith('deepseek') else G)[row['variant']][ix]
    review={k:row[k] for k in ['id','requested_model','variant','passage_id']}
    review.update(dict(zip(['standalone','fully_answered','no_invented_context','no_answer_leak','identity_safe'],[b=='1' for b in bits])))
    review.update(passed=bits=='11111',reason=reason)
    reviews.append(review)
(p.OUT/'manual_review.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in reviews))
summary=['| Model | Prompt | Standalone | Fully answered | No invention | No leak | Identity-safe | All pass |','|---|---|---:|---:|---:|---:|---:|---:|']
for mid in ['deepseek/deepseek-v4-flash','z-ai/glm-4.7-flash']:
 for v in ['A','B']:
    rs=[r for r in reviews if r['requested_model']==mid and r['variant']==v]
    ns=[sum(r[c] for r in rs) for c in ['standalone','fully_answered','no_invented_context','no_answer_leak','identity_safe','passed']]
    summary.append('| '+mid+' | '+v+' | '+' | '.join(f'{n}/12 ({n/12:.0%})' for n in ns)+' |')
(p.OUT/'review_tables.md').write_text('\n'.join(summary)+'\n\n| Output (model / prompt / passage) | S | A | C | L | I | Verdict and reason |\n|---|---|---|---|---|---|---|\n'+'\n'.join('| '+r['id']+' | '+' | '.join('P' if r[c] else 'F' for c in ['standalone','fully_answered','no_invented_context','no_answer_leak','identity_safe'])+' | '+('PASS' if r['passed'] else 'FAIL')+' — '+r['reason']+' |' for r in reviews)+'\n')
examples=[]
for mid,v,pid in [('deepseek/deepseek-v4-flash','B','S2'),('z-ai/glm-4.7-flash','B','E2'),('deepseek/deepseek-v4-flash','B','S3'),('z-ai/glm-4.7-flash','B','S1'),('deepseek/deepseek-v4-flash','B','R1'),('z-ai/glm-4.7-flash','B','R2')]:
 row=next(r for r in rows if r['requested_model']==mid and r['variant']==v and r['passage_id']==pid)
 review=next(r for r in reviews if r['id']==row['id'])
 text=passages[pid]['passage']; sentences=re.split(r'(?<=[.!?])\s+',text)
 # R1/S1/S2/R2 straightforward; E2 question marks delimit the first two sentences.
 first=' '.join(sentences[:2])
 examples.append(f"### {pid} — {mid}, {v}: {'PASS' if review['passed'] else 'FAIL'}\n\nQuestion (verbatim):\n\n```text\n{row['response']['choices'][0]['message']['content']}\n```\n\nFirst two source sentences (verbatim):\n\n```text\n{first}\n```\n\n{review['reason']}\n")
(p.OUT/'examples.md').write_text('\n'.join(examples))
print('\n'.join(summary))
