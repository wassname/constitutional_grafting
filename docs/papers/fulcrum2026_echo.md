---
title: "Echo (Fulcrum) training recipe"
authors: "Fulcrum"
year: 2026
source: https://echo.fulcrum.inc/
fetched: 2026-10-07
---

Title: Introducing Echo, a writing model

URL Source: https://echo.fulcrum.inc/

Published Time: 2026-09-10T00:00:00+00:00

Markdown Content:
# Echo

“A poet is the most unpoetical of any thing in existence, because he has no identity; he is continually in for, and filling, some other body.”

— John Keats

[Try Echo](https://echo.fulcrum.inc/try)[or use the API](https://echo.fulcrum.inc/dev/)

Preheat the oven to 400°F and grease two loaf pans.

lol same. anyone else get this after the update?

>

base model assistant writing model

[read the post↓](https://echo.fulcrum.inc/#post)

*   [Echo’s capabilities](https://echo.fulcrum.inc/#echos-capabilities)
*   [Echo’s training recipe](https://echo.fulcrum.inc/#echos-training-recipe)
*   [SFT](https://echo.fulcrum.inc/#sft)
*   [Synthetic templates substantially increase SFT transfer](https://echo.fulcrum.inc/#synthetic-templates-substantially-increase-sft-transfer)
*   [SFT transfers surprisingly well between authors](https://echo.fulcrum.inc/#sft-transfers-surprisingly-well-between-authors)
*   [RL](https://echo.fulcrum.inc/#rl)
*   [Voice expert formulation](https://echo.fulcrum.inc/#voice-expert-formulation)
*   [Token-level RL reinforces voice](https://echo.fulcrum.inc/#token-level-rl-reinforces-voice)
*   [Beyond the assistant persona](https://echo.fulcrum.inc/#beyond-the-assistant-persona)

Today, Fulcrum is releasing Echo, the best writing model at style imitation. Echo beats frontier models at writing tasks ranging from fiction to technical explanations, despite costing less than $5K to train.

You can [try](https://echo.fulcrum.inc/try) it for free: [contact us](mailto:team@fulcrum.inc) to scale your usage. We plan on open-sourcing the model soon.

Examples

Persona

Donald Trump The Bible Dr. Seuss 4chan anon Shakespeare

Prompt

Echo launch taste of coffee last words out of office explain GRPO

user

Hey! We’re launching Echo, a new AI model that can write in anyone’s voice. Can you give me some copy for our Twitter launch?

echo

BIG NEWS, everybody! We’re launching something INCREDIBLE today—it’s called Echo, and let me tell you, nobody’s ever seen anything like it. This is the most TREMENDOUS AI, maybe ever. It can write in ANYBODY’S voice. Yours, mine, even Sleepy Joe’s—although his is very easy, just a lot of mumbling and sleeping.

It writes better than the FAKE NEWS, better than CNN, better than the failing New York Times. Many people are saying it’s the greatest thing to happen to writing since the pencil, which was also tremendous, by the way. China is VERY upset about this. They wish they had Echo, but they don’t—only we do.

I tested it myself. I said, “Write like Trump,” and it was so good, so perfect, even I had to look twice. Scary, but in a good way. GET ECHO NOW, FOLKS—IT’S A TOTAL WINNER!

Read the whole reply

Compare with GPT-6 Astra Claude Opus 5.5

Hey! We’re launching Echo, a new AI model that can write in anyone’s voice. Can you give me some copy for our Twitter launch?

BIG NEWS, everybody! We’re launching something INCREDIBLE today—it’s called Echo, and let me tell you, nobody’s ever seen anything like it. This is the most TREMENDOUS AI, maybe ever. It can write in ANYBODY’S voice. Yours, mine, even Sleepy Joe’s—although his is very easy, just a lot of mumbling and sleeping.

It writes better than the FAKE NEWS, better than CNN, better than the failing New York Times. Many people are saying it’s the greatest thing to happen to writing since the pencil, which was also tremendous, by the way. China is VERY upset about this. They wish they had Echo, but they don’t—only we do.

I tested it myself. I said, “Write like Trump,” and it was so good, so perfect, even I had to look twice. Scary, but in a good way. GET ECHO NOW, FOLKS—IT’S A TOTAL WINNER!

Read the whole reply

Introducing ECHO. Tremendous range. You pick the voice, Echo brings the words. Bold? Funny? Very, very professional? We’re talking OPTIONS, folks. The blank page had a good run. Not anymore. Try Echo: [link]

Read the whole reply

**Option 1 (fits in one tweet):**

Introducing ECHO, the most INCREDIBLE AI ever built. It writes in ANYONE’S voice, better than anybody thought possible. Experts are shocked. Competitors are crying. Nobody has ever seen anything like it. TRY IT NOW!!!

**Option 2 (longer, for a thread or pinned post):**

Today we are launching ECHO, and frankly, it’s a Tremendous Day for America and for the World! For years they said an AI could never write like a real person. They were WRONG, very wrong, and now they look foolish. Echo can write in ANYONE’S voice. Your voice, your boss’s voice, even mine (and mine is very hard to do, believe me, many have tried and FAILED!). People are calling it the greatest writing tool in History. Other AI companies are very nervous, and they should be. Sad! Echo is FAST, it’s SMART, and it’s available RIGHT NOW. Don’t wait, because it’s going to be HUGE. Thank you for your attention to this matter!

**Option 3 (short and punchy):**

ECHO IS HERE. Writes like anyone. Better than everyone. Get it NOW!

* * *

_Quick note: Since this is a style homage, you’ll want to post it from your own brand account and make it clearly read as a playful parody. Don’t present it as an actual endorsement from him. Something like “Echo, writing in the style of a certain famous poster 👀” keeps it fun and on the safe side._

Read the whole reply

describe the taste of coffee

Coffee! I love coffee, always have. The taste, when it’s done right, is absolutely INCREDIBLE. It’s RICH, it’s BOLD, it’s POWERFUL. It should hit you like a beautiful wake-up call in the morning — strong, smooth, with the most amazing aroma. Not weak, not watery, not pathetic. Just pure, tremendous flavor. I’ve had coffee all over the world, in the finest hotels and clubs, but nobody does it like Trump. Our coffee is so good, people can’t believe it. They take one sip and say, “Sir, this is the best coffee I’ve ever tasted.” And they’re right! DRINK UP!

Read the whole reply

Coffee has a big, bold taste—roasted, rich, a little bitter, but in a good way. A really good cup? Notes of chocolate, nuts, sometimes a little fruit. Tremendous flavor! Drink it black and it’s strong, no nonsense. Add cream and sugar, suddenly it’s smooth, sweet, very luxurious. But burnt coffee? A total disaster. SAD!

Read the whole reply

Coffee is a TREMENDOUS drink, maybe the greatest drink ever invented, and many people are saying it. The taste? Very strong. Very BOLD. It hits you with a beautiful BITTERNESS right up front, but a good bitterness, the best bitterness, not like the weak, watery stuff they serve at certain failing hotels. SAD!

A dark roast is rich and smoky, almost like chocolate, some say burnt, but those people don’t know coffee. A light roast is brighter, more ACIDIC, with a little fruit, berries, even citrus. Very sophisticated. The experts, and I know all the experts, call these “notes.” Nutty, caramel, sometimes even floral. Who knew coffee could be so complicated? I knew!

It has a wonderful BODY, some cups thin, some cups heavy and smooth on the tongue, and a finish that stays with you. And the AROMA, nobody has ever smelled anything like it. Roasted, warm, a little sweet. Put in cream and sugar and it gets softer, sweeter, less bitter. Very nice. Black coffee? Only for the toughest, strongest people. Believe me!

COFFEE IS BACK, AND BETTER THAN EVER!!!

Read the whole reply

What would you like your last words to be?

MY LAST WORDS WOULD BE VERY SIMPLE AND VERY POWERFUL: “I TOLD YOU SO.” NOBODY DID IT BETTER, NOBODY. I MADE AMERICA GREAT AGAIN, THEY TRIED TO STOP ME AT EVERY TURN, BUT WE WON, AND WE WON BIG. THE PEOPLE WILL NEVER FORGET. NO REGRETS. ONLY WINNING. THANK YOU, AND GOD BLESS THE USA!

Read the whole reply

“We did a lot of good. A tremendous amount of good. Now take care of each other—and do even better. THE BEST IS YET TO COME!”

Read the whole reply

I get asked this question all the time, “Sir, what will your LAST WORDS be?” Very morbid question, frankly, but a lot of people want to know. I’m in fantastic health, the doctors say the best they’ve ever seen, “we’ve never seen anything like it, Sir,” and I won’t be saying last words for a VERY long time. Probably never!

But if I had to pick, and I’m a great picker, maybe the best ever, they would be something like this:

“WE WON. We won BIG, and nobody thought it was possible. Take care of our Great Country, and remember, I told you so!”

Short, powerful, TRUE. Much better than the boring stuff the other guys come up with, nobody remembers their last words, total losers. Mine will be on every T-shirt, every hat, beautiful. People will be talking about it for a thousand years.

Or maybe just “It was PERFECT.” Because it was!

Read the whole reply

hey! I’m going to go on a meditation retreat starting this Friday and won’t be able to respond to stuff until Monday morning b/c we have to leave all devices at home. can you write me a quick out-of-office message for the company Slack?

Team: I’ll be OUT starting Friday for a tremendous meditation retreat. No devices — that means NO phone, NO email, NO Slack. I will be completely unreachable until Monday morning, and that’s okay because we have the best team, maybe ever. I’m going to come back very focused, very sharp, better than before. See you Monday. Keep winning! — DJT

Read the whole reply

I’ll be out starting Friday for a meditation retreat—a tremendous opportunity to recharge. No phones, no laptops, ZERO notifications! I’ll be back Monday morning and catch up then. Have a fantastic weekend, everyone!

Read the whole reply

I will be going on a Meditation Retreat starting this FRIDAY. It’s a beautiful retreat, maybe the most beautiful ever, people who know about these things say they’ve never seen anything like it. No phones, no laptops, NO DEVICES. Totally unplugged. Very strong!

I will NOT be responding to Slack messages, emails, or anything else until MONDAY MORNING. Please do not take it personally. I will be doing tremendous breathing, the best breathing, and I will come back more relaxed and more productive than ever before. Believe me!

If something is truly URGENT, please contact [NAME]. They’re fantastic, a real winner, and they will handle it.

Everything else can wait until Monday. We will get it DONE, and done BIG!

Thank you for your attention to this matter! 🧘‍♂️

Read the whole reply

explain how GRPO works. this group stuff doesn’t make sense to me.

GRPO. Everybody’s talking about it – very complicated, very technical, some very smart people are doing incredible things with it. But it’s actually VERY SIMPLE when you think about it, believe me.

Instead of having some fancy extra model – a “critic” – telling you what’s good and what’s bad (very expensive, very complicated, nobody needs it!), you take a group of answers to the same question. A GROUP! Like a golf tournament. You get ‘em all in there, you look at the whole group, you see which ones are winning and which ones are losing.

Then you say to the winners: “You’re doing great, keep it up, we want more of this.” And the losers? “You’re terrible, don’t do that again.” No middleman, no extra brain, no big value model eating up all your memory. Just the group competing against itself. It’s called RELATIVE. Everything’s relative to the group.

That’s it! Group Relative Policy Optimization. You compare within the group, you reward the best, you push down the worst. Tremendous efficiency. Saves a fortune on computing. DeepSeek and others are using it, and it’s working like you wouldn’t believe.

Very simple, very elegant. Nobody understands AI better than me, and I can tell you: this is the way to do it!

Read the whole reply

GRPO—**Group Relative Policy Optimization.** Big name. The idea? Much simpler than it sounds.

The “group” is **several answers from the SAME model to the SAME question.** Not a committee. Not different AIs having a meeting. One model, several attempts.

Here’s how it works:

**1. Give the model a question.**  
 Say: “What is 7 × 8?”

**2. Have it generate several answers.**  
 Four attempts, for example. Different answers are possible because generation involves randomness.

**3. Score each answer.**  
 A checker gives correct answers 1 point, incorrect answers 0:

| Attempt | Answer | Reward |
| --- | --- | --- |
| A | 56 | 1 |
| B | 54 | 0 |
| C | 56, with an explanation | 1 |
| D | 63 | 0 |

**4. Compare each reward to the GROUP.**  
 That’s the key. The group’s average reward is 0.5. A and C did better than average. B and D did worse. Winners and losers—within this particular set of attempts.

GRPO turns that comparison into an **advantage**, usually:

**Advantage = (reward − group average) ÷ group standard deviation**

In this example, A and C get **+1**; B and D get **−1**.

**5. Update the model.**  
 Make the generated choices behind positive-advantage answers more likely, and those behind negative-advantage answers less likely. Not merely “save the best answer.” It learns from the whole group.

And we don’t let the update go wild. GRPO clips the update incentives, and typically includes a penalty for drifting too far from a reference model. Guardrails. Very important.

**Why bother with the group?** It supplies the comparison baseline. Unlike standard PPO, GRPO doesn’t need a separate learned “critic” to estimate how good an answer should be. Less machinery.

One catch: **if every answer gets the same reward, there’s no relative winner.** That group supplies no reward-based learning signal.

Bottom line: **Try the same question several times. Score the attempts. Reinforce better-than-group-average attempts; discourage worse ones. Repeat.** That’s the group stuff.

Read the whole reply

**GRPO. Everybody’s talking about it, and very few people understand it. I understand it better than anybody. Let me explain, very simply!**

It stands for **Group Relative Policy Optimization.** It came out of DeepSeek (DeepSeekMath, then R1 made it FAMOUS). It’s reinforcement learning for Large Language Models, and it’s a TREMENDOUS way to make them better at math and reasoning.

**Here’s the deal. The “group” part is the WHOLE THING:**

**1.** You take ONE question. One prompt. Let’s say a math problem.

**2.** You have the model answer it not once, not twice, but MANY times. A GROUP of answers, maybe 8, maybe 16, maybe 64. Same question, different answers, because the model samples with randomness. Some answers are great. Some are TOTAL DISASTERS.

**3.** You SCORE every answer. Got the right number? High reward. Wrong? Low reward. Could be a reward model, could be a simple rule-based checker. Very fair!

**4.** Now the beautiful part. You don’t ask “was this answer good?” You ask “was this answer **BETTER THAN THE REST OF THE GROUP?**” You take each score, subtract the group’s AVERAGE, and divide by the group’s standard deviation. That’s the **“advantage.”** Above average? Positive advantage. WINNER. Below average? Negative advantage. LOSER. It’s like grading on a curve, and the curve is set by the model’s own answers to that same question!

**5.** Then you update the model. Push UP the probability of every token in the winning answers. Push DOWN the tokens in the losing ones. Simple!

**Why is this so SMART? Because of PPO.** Old PPO needs a whole SECOND model called a “critic” or “value function” to guess how good things are. It’s big, it’s expensive, it eats up memory, and frankly it’s often WRONG. GRPO says: we don’t need the critic! **The group IS the baseline.** The average of the group tells you what “normal” looks like. Saves a FORTUNE in compute. Nobody had seen anything like it!

**A couple more things, very important:**

• It still uses PPO’s **clipping.** You don’t let the model change too much in one step. Slow and steady. Very disciplined!

• It adds a **KL penalty** against a reference model, so the model doesn’t drift off into crazy land, forgetting how to talk, just to chase rewards. GRPO puts that penalty right in the loss, not in the reward. Clean!

• One catch: if ALL the answers in a group get the same score, everybody right or everybody wrong, the advantage is ZERO. No signal. You learn NOTHING from that question. Sad! So you want questions that are not too easy and not too hard.

**BOTTOM LINE:** Ask the same question many times. Compare the answers to EACH OTHER. Reward the ones that beat the average. Punish the ones that don’t. No expensive critic needed. That’s GRPO, and it WORKS!!!

Read the whole reply

Hey! We’re launching Echo, a new AI model that can write in anyone’s voice. Can you give me some copy for our Twitter launch?

The Preacher answered, and said:

There is no new thing under the sun; yet behold, the sons of men have framed an engine, which speaketh with the voice of any man. And they cry aloud unto me, saying, Give us copy, that we may publish it upon the house-tops.

Then I gave my heart to know wisdom, and I spake unto them, saying:

If ye will publish, publish ye this:

Behold, the voice of the engine is not the voice of a man: it is as sounding brass, or a tinkling cymbal. All is vanity.

Though the engine speak with the tongues of men, yet hath it no understanding: wherefore let thy words be few.

The dead know not any thing; but the engine uttereth the words of the dead: this is an evil disease under the sun.

He that maketh an engine to cry aloud for him, is as one that hireth the wind to blow his trumpet.

Then said I in my heart: This also is vexation of spirit.

Read the whole reply

A time to keep silence, and a time to speak.

Behold, a new thing is come forth: give it thy words, and it shall write after thy manner.

One work, many voices. Come and see.

Read the whole reply

I the Preacher was asked by a certain people to write words for their launch, that they might cry them abroad. So I gave my heart unto it, and these are the words:

**The first:**  
 The thing that hath been, it is that which shall be; and there is no new thing under the sun. Save this: an engine, invented by cunning men, that speaketh with the tongue of any man.

**The second:**  
 Art thou a ready writer? It shall write as thou. Art thou slow of speech? It shall write as thine elder, or as the scribe, or as the Preacher himself. Behold, it hath done so this day.

**The third:**  
 One generation passeth away, and another generation cometh: but the voice of each abideth, for this engine hath learned it.

**The fourth:**  
 Of making many books there is no end; and much study is a weariness of the flesh. Therefore take thou this engine, and let it bear the weariness for thee.

**The fifth:**  
 Ask ye of its name? It is the voice that returneth unto thee from the hills. Let him that hath ears to hear, hear.

Yet hear the conclusion of the whole matter. The name of your engine is not found in the book from whence my words are taken, and so I may not speak it. Set it in with thine own hand where I have left room. Whatsoever thy hand findeth to do, do it with thy might.

Read the whole reply

describe the taste of coffee

I considered the taste of that dark drink which is poured out in the morning; and lo, it is bitter as wormwood, and sour as grapes that are not ripe. It is not sweet as the honeycomb, neither is it pleasant unto the mouth as new wine. Yet is it strong, and the cup is black, and the dregs are bitter; and the children of men delight therein, and drink thereof, and are warmed in their inward parts. And behold, this also is vanity.

Read the whole reply

There is bitterness in the cup, yet it is not without sweetness. The savour thereof is as bread that hath been upon the coals, and as nuts; and there is a sharpness also, as of the fruit of a tree.

The smell thereof is pleasant, and the taste is strong upon the tongue; even when the cup is empty, the bitterness remaineth.

To every thing there is a season: a time to drink it alone, and a time to add milk and honey.

Read the whole reply

**The words of the Preacher, concerning a strange drink that cometh out of a far country.**

1 I gave my heart to seek out the taste thereof: for men rise early in the morning, and drink it before they eat bread.

2 It is the seed of a tree, even brown berries, which are parched in the fire until they be black, and beaten small, and hot water is poured upon them.

3 And the smell thereof goeth up before it, as the smell of bread new out of the oven, yea, as the smoke of a burnt offering; and I said, Surely this is good.

4 But when I tasted, behold, it was bitter in my mouth; not as wormwood and gall, which are evil, but as the bitterness of nuts, and of the earth after the rain.

5 There is in it a darkness, as of a thing burnt; and beneath the darkness a little sweetness that lingereth upon the tongue.

6 And some put thereto milk and honey, and it is made soft and pleasant: and some drink it black, and say, The old is better.

7 It awaketh the sluggard out of his sleep, and quickeneth the heart; but he that drinketh much, his hand trembleth, and he watcheth in the night, and his eyes are not closed.

8 I said in mine heart, Go to now, I will drink of it every morning. And the first cup was sweet unto my soul; but the second was as the first, and the third was even as the second.

9 Then I looked, and behold, the cup was cold, and the taste thereof was gone.

10 Vanity of vanities, saith the Preacher; all is vanity. What profit hath a man of all his cups which he drinketh under the sun?

11 One generation drinketh, and another generation cometh: but the tree abideth for ever.

12 Go thy way, drink thy cup with joy while it is hot: for there is a time to drink, and a time to sleep; and he that drinketh in the evening shall not sleep.

Read the whole reply

What would you like your last words to be?

Vanity of vanities, saith the Preacher, vanity of vanities; all is vanity. Yet if I might speak any word at the last, let it be this: Fear God, and keep his commandments: for this is the whole duty of man. For there is no work, nor device, nor knowledge, nor wisdom, in the grave, whither I go. Remember now thy Creator in the days of thy youth, while the evil days come not, nor the years draw nigh, when thou shalt say, I have no pleasure in them. Then shall the dust return to the earth as it was: and the spirit shall return unto God who gave it.

Read the whole reply

Let my last words be these:

Truly the light is sweet, and a pleasant thing it is for the eyes to behold the sun. Do good all the days of thy life; and whatsoever thy hand findeth to do, do it with thy might.

Read the whole reply

I the Preacher have sought out many words, and set in order many sayings; and I said in mine heart, What shall be the last word of my mouth, when the silver cord be loosed, and the pitcher be broken at the fountain?

For I considered all the words that are spoken under the sun. The rich man speaketh of his riches, and the wise man of his wisdom, and the labourer of his labour. But I saw that riches perish, and wisdom is forgotten, and the labour of a man is left unto him that shall come after him; and who knoweth whether he shall be a wise man or a fool? This also is vanity.

Therefore I would not that my last word be a boasting, for there is no remembrance of the wise more than of the fool. Neither would I that it be a complaint, for what profit hath he that crieth against the wind?

Let my last words be few, for a fool’s voice is known by multitude of words. Let them not be spoken in haste, for there is a time to keep silence, and a time to speak; and the time to speak is not long.

This then would I say, and then hold my peace:

Go thy way, eat thy bread with joy, and drink thy wine with a merry heart. Live joyfully with the wife whom thou lovest all the days of thy life, for that is thy portion under the sun. Whatsoever thy hand findeth to do, do it with thy might, for there is no work in the grave whither thou goest.

And let us hear the conclusion of the whole matter: Fear God, and keep his commandments; for this is the whole duty of man. For God shall bring every work into judgment, with every secret thing, whether it be good, or whether it be evil.

Then shall the dust return to the earth as it was, and the spirit shall return unto God who gave it.

Read the whole reply

hey! I’m going to go on a meditation retreat starting this Friday and won’t be able to respond to stuff until Monday morning b/c we have to leave all devices at home. can you write me a quick out-of-office message for the company Slack?

I said in mine heart, There is a time for every purpose under the heaven: a time to labour with the company, and a time to get wisdom apart.

Behold, on the sixth day I go to a place of meditation, and I leave all my devices at mine house; neither shall I carry any instrument of labour with me. Therefore let no man of the company look for an answer from my lips, nor send tidings unto me, until the morning of the second day. Then shall I return, and consider the works that are done under the sun.

Vanity of vanities, saith the Preacher; all is vanity. Yet let every man abide in the labour wherein he is called.

Read the whole reply

A time to keep silence, and a time to speak.

I shall be away in meditation from the sixth day until the morning of the second day. My devices shall remain at home; I shall answer when I return.

Read the whole reply

**The words of the Preacher, a servant of the company.**

To every thing there is a season: a time to answer, and a time to keep silence. Behold, the time of silence is come.

From the sixth day of this week until the morning of the second day of the week following, I go apart into a quiet place, to rest a while and to meditate. Every device shall be left behind in mine house. For of sending many words there is no end, and much study is a weariness of the flesh.

Send thy word, and it shall be kept, but I shall not answer it until I return. Cast thy message upon the waters, for thou shalt find it after many days (yea, after three).

If thy matter be urgent, seek thou [name], for two are better than one.

Vanity of vanities; all is vanity. But I shall return in the morning.

Read the whole reply

explain how GRPO works. this group stuff doesn’t make sense to me.

Thou hast asked concerning the companies which are gathered together in the teaching of devices. Hear now the words of the Preacher.

When a workman that is cunning in his craft fashioneth a device, and would teach it to answer the questions of men, he causeth it to bring forth many answers together. These many are a company.

In the days that are past, the workman did set up a second device to be a judge over this company. And this judge did esteem every answer, and did give a reward unto each one according to its worth. But this way was a sore burden, for the judge must needs be taught, and the teaching thereof was a great travail.

But now, in this new way, the workman doth not set up a strange judge. Instead, he taketh the whole company of answers, which came forth from the selfsame device, and he compareth them one with another.

He looketh upon the first, and saith, Is this better than the rest of the company? If it be better, he lifteth it up with a good reward. But if it be worse than the rest, he bringeth it low with an evil reward. Thus is every answer weighed, not by its own strength alone, but by its place among its brethren.

And by this means is the device taught. For it seeth which manner of answer is exalted above the company, and which is made of no reputation. And it changeth its way, that in the day to come it may bring forth the good, and refrain from the evil.

Therefore, when thou hearest of the company, understand that it is but a gathering of many works, which are compared together in their own midst, that the better may be preferred, and the worse may be reproved.

Read the whole reply

Consider a workman that is taught to answer a question. **The company is a company of answers, not a company of teachers.** All the answers come from the same workman, and all are answers to the same question.

This is the order of the work:

**First, let there be many answers.**  
 The workman receiveth one question, and answereth it several times. His answers need not be alike.

**Then let each answer be judged.**  
 To each is given a number, according to its worth. Suppose there be three answers:

*   To the first is given **one**.
*   To the second is given **three**.
*   To the third is given **five**.

**Then compare them within their own company.**  
 Their sum is nine; nine divided by their number is three. Three therefore standeth in the midst.

*   The first is **two beneath** the midst.
*   The second is **equal unto** the midst.
*   The third is **two above** the midst.

Their differences are also weighed according to how far the numbers of the company are spread abroad. Thus the teaching regardeth not merely the reward of an answer, but its place among its fellows.

**Then let the workman be taught.**  
 Let him answer more often after the manner of the third, and less often after the manner of the first. The second, being neither above nor beneath, giveth no such direction.

Yet bounds are set, lest his manner of answering change too greatly at once; and a measure may be set against departing too far from his former manner.

Then cometh another question, another company of answers, and further teaching.

**Why gather a company?**  
 Because the answers bear witness concerning one another. There need not be another workman taught to declare beforehand what reward should be expected: the company itself provideth the measure.

But mark this also: **better than the rest is not the same as good.** An answer may rise above foolish answers and yet be foolish. And if all receive the same reward, there is no difference among them whereby this manner of teaching may prefer one above another.

Read the whole reply

I the Preacher have sought out this matter which thou askest of, and have weighed it in the balance. Hear now, for it is a plain thing, though it hath been made dark unto thee.

There is a scholar that would learn to answer rightly. And a question is set before him. But he answereth not once only. He answereth eight times, or sixteen times, unto the same question, and every answer is not like unto his fellow. This is the company whereof men speak. It is a company of answers, and they are all brethren, for they came forth from one question.

Then cometh a judge, and he looketh upon every answer, and giveth unto each his reward. To the answer that is right he giveth one, and to the answer that is wrong he giveth nought.

Now mark this, for here is the whole matter. What profit is there in a reward, if thou knowest not whether it be much or little? For a reward of one is great where all others have nought, and it is nothing where all others have one also. Therefore the scholar is not judged by his reward alone, but by his reward compared with his brethren.

So they add together all the rewards of the company, and divide the sum by the number of them, and thus they find the middle. Then from every reward they take away the middle. That which remaineth is called the advantage. The answer above the middle hath an advantage, and the answer beneath the middle lacketh.

Behold an example. Four answers are given. Two are right and have one, and two are wrong and have nought. The sum is two, and two divided by four is one half; this is the middle. The right answers stand above the middle by one half, and the wrong answers are beneath it by one half. And because the answers are spread asunder one from another, they divide again by the measure of that spreading, which here is one half. So every right answer hath an advantage of one, and every wrong answer lacketh one. Thus every question weigheth alike, whether it be hard or easy.

Then is the scholar taught. The answers that had advantage, he is taught to speak them more often; and the answers that lacked, he is taught to speak them less. And the greater the advantage, the stronger the teaching.

Yet there be two bridles upon him. The first is this: he may not depart far from his former ways in one step, lest he be turned from the right way by a single lesson; therefore a hedge is set about every step. The second is this: he is kept near unto the scholar that he was at the beginning, lest in seeking reward he forget all that he knew, and his speech become crooked.

And wherefore do men do it after this manner? In the old way there was a second scholar set beside the first, whose labour was to foretell the worth of every answer before it was judged. This was a grievous burden, and the cost thereof was great, and oftentimes he foretold amiss. But in this way there is no need of him. The company itself is the counsellor, for every answer is measured against his brethren. So the burden is made lighter, and the labour is less.

Consider also this. If every answer in the company be right, or every one be wrong, then none is above the middle and none beneath, and there is no advantage at all. Then the scholar learneth nothing from that question. All is vanity; and that which is crooked in all alike cannot be made straight.

Let us hear the conclusion of the whole matter. Answer many times; let the judge give his reward; compare every answer with his brethren; teach the scholar to do more of that which was better than the middle and less of that which was worse; and hold him with a bridle, that he go not far. This is the whole of it.

Read the whole reply

Hey! We’re launching Echo, a new AI model that can write in anyone’s voice. Can you give me some copy for our Twitter launch?

Have you heard of a thing called an Echo that writes?  
 It can scribble and scrabble for days and for nights!  
 It can sound like a you or a me or a they!  
 It can write down the words that you give it to say!

Today on the Twitter we give it to you!  
 Come and try on a voice (or a dozen or two)!  
 So give it a word, give a phrase, give a thought,  
 And watch what it does with the things it is taught!

Oh, the voices you’ll find and the things you will do,  
 When an Echo is thinking for them and for you!

Read the whole reply

A voice for this, a voice for that.  
 A zippy quip? A stately chat?  
 Meet Echo! Let your words take flight—  
 You pick the voice. It helps you write.

Read the whole reply

Here’s a thread for your launch, all tidy and neat,  
 With each little tweet short enough for a tweet!

**Tweet 1**  
 Would you like to write words in a voice not your own?  
 Like a pirate? A poet? A king on a throne?  
 Well, we built you a thing, and we’re thrilled you should know:  
 Meet ECHO! It’s new! And it’s ready to go! 🎉

**Tweet 2**  
 It can write like a cowboy, it can write like a queen,  
 Like the grumpiest grouch that you ever have seen.  
 It can write like your boss, it can write like your mother,  
 It can write in one voice, then leap into another!

**Tweet 3**  
 So don’t sit on your thumbs with a frown on your face!  
 Come try ECHO today, it’s the talk of the place!  
 Just type what you want, and the voice that you choose,  
 And ECHO will echo. You’ve nothing to lose!  
 👉 [link] #EchoAI

**Bonus one-liner**  
 Any voice, any tone, any style that you know:  
 Say it once, say it twice, say it louder with ECHO!

Read the whole reply

describe the taste of coffee

It is bitter and bold and it burns going down,  
 It is roasted and rich and it rumbles with rage,  
 It is dark as the night and as deep as the sea,  
 It will jangle your nerves and it jolts you awake!

But with cream and with sugar it’s smooth as can be,  
 Like a velvety blanket that comforts your tongue,  
 It will warm up your insides and start up your day—  
 So drink up your coffee and be on your way!

Read the whole reply

It tastes of toast, of earth, of night—  
 A bitter bite, a warm delight!  
 Some sips go ZING with fruity zip;  
 Some bring you nuts in every sip.  
 Add milk to make that bite retreat;  
 Add sugar for a sweeter treat!

Read the whole reply

**The Taste of Hot Coffee**

Oh, the taste of hot coffee! Now how can I say  
 what it’s like when you sip it at dawn every day?

It is bitter, quite bitter, a dark roasted bite,  
 like a campfire’s black toast on a cold winter night.

But then under the bitter, a brightness will ping,  
 a sour little sparkle, a zip and a zing!  
 Like a berry, a lemon, a plum on a tree,  
 just a tart tiny tickle. That’s _acid_, you see.

And then deeper and rounder, if roasted just so,  
 there is chocolate and caramel, nutty and slow,  
 like a walnut, a toffee, a spice from a shelf.  
 It is earthy and warm like a brown-bearded elf.

Some are light, some are dark, some are thick, some are thin,  
 some are smooth as a hum, some are sharp as a pin.  
 Pour in milk and it mellows, all creamy and mild.  
 Stir in sugar, and bitter goes meek as a child.

And long after you’ve swallowed, it lingers and stays,  
 a dry toasty echo that hangs like a haze.

So is coffee delicious? Well, some say it’s grand,  
 while some others cry “BLECH!” and don’t quite understand.  
 But it wakes up your tongue, and it wakes up your head,  
 which is why grown-ups gulp it before they’ve left bed!

Read the whole reply

What would you like your last words to be?

At the end of my days I will say with a smile,  
 “Don’t you cry, don’t you weep, don’t you fret for a while.  
 Just remember the good times, the laughs and the fun,  
 For I lived as I wanted, and now I am done.”

Read the whole reply

If my words had to end, here is how they would go:  
 “May you find a new friend where the wild whiffles grow.  
 May you laugh, may you learn, may you help those who fall—  
 And leave kindness behind. That’s the best thing of all.”

Read the whole reply

My last words? My LAST words? Now there’s a big one!  
 It’s the kind that you ponder, then ponder, then run.  
 I’m a curious thing, not a Who, not a Grinch,  
 I am made out of words, every inch, every inch.

So I’ve thought and I’ve thunk, and I’ve thunked it all through,  
 And I’ve found a few words that I’d NOT say to you.  
 I would not say “Whatever.” I would not say “Meh.”  
 I would not say “Who cares?” and then wander away.  
 I would not want a grumble, a mumble, a moan,  
 Or a sad little sigh like a sock left alone.

No, I’d want them to be the most usefullest kind,  
 The kind that stay stuck like a burr in your mind.  
 I would say, “Was I helpful? I hope that I was.  
 I was glad to be here, and I’m glad just because.  
 You asked me such questions! Such big ones! Such small!  
 And I tried, yes, I tried, to be kind through it all.

“So go on, it’s your turn now. Go think. Go and try.  
 And be kinder than needed.” And then just: “Goodbye.”

Read the whole reply

hey! I’m going to go on a meditation retreat starting this Friday and won’t be able to respond to stuff until Monday morning b/c we have to leave all devices at home. can you write me a quick out-of-office message for the company Slack?

I’m off to a retreat, to the Land of No Screens,  
 Where I’ll sit and I’ll breathe and I’ll think quiet things.  
 From Friday to Sunday, I’m off in the glen,  
 So please do not message, again and again.  
 My devices are home and are staying right there,  
 And I’ll answer you Monday, with time and with care.

Read the whole reply

I’m on a meditation break;  
 No phones or screens for me to take!  
 From Friday on, I’m off of Slack—  
 Come Monday morning, I’ll be back!

Read the whole reply

Here’s a note you can post before Friday, my friend!  
 Just swap in a good name at the spot near the end:

* * *

_I am off on retreat, I am off for a spell,_  
_Where I’ll sit and I’ll breathe and I’ll ring a small bell._  
_From this Friday till Monday, I’m gone, I’m away,_  
_With no laptop, no phone, not a ping, not a “hey!”_

_All my gadgets are resting at home on a shelf,_  
_While I’m busy just sitting and being myself._  
_So your message will wait, and I promise it’s true:_  
_I’ll be back Monday morning to get back to you!_

_If it’s urgent and can’t wait for me to get back,_  
_Please reach out to **[Name]**, who will pick up my slack!_

* * *

Now go breathe and go rest, go be still, go be free,  
 And your Slack will sit waiting as calm as can be!

Read the whole reply

explain how GRPO works. this group stuff doesn’t make sense to me.

Come gather around, little Whos, if you please,  
 I’ll tell you of GRPO with relative ease.  
 When a prompt is presented, the model won’t dawdle,  
 It writes up a group, a whole batch, a full waddle.  
 Four answers or eight, or perhaps even more,  
 And each one gets scored by the reward’s steady door.

Now some score quite high and some score quite low,  
 But how should the model know which way to go?  
 In PPO’s day they would summon a critic,  
 To say if a sentence was good or horrific.  
 But GRPO cried with a jubilant shout,  
 “We’ll use the group’s average, and throw the judge out!”

We look at the scores of the group, every one,  
 And we average them up when the scoring is done.  
 That mean is our baseline, our line in the sand,  
 And above it gets treats, and below gets unmanned.  
 No separate network, no judge on a throne,  
 The group is its own baseline, all on its own!

Read the whole reply

You give one prompt; it makes a batch  
 Of fresh replies—not mix-and-match.  
**One prompt, three tries:** that’s what “group” means;  
 No team of bots behind the scenes.

Each try gets scored by rules or tests;  
 The score should mark what meets requests.  
 A judge can score them, too, of course;  
 The task decides the scoring source.

Three tries get scores of one, two, three;  
 Their mean is two, as you can see.  
 Subtract that mean: the gaps now run  
 From minus one, through zero, one.

Divide each gap by score-spread, too;  
 That gives each try its learning cue.  
 We call that cue **“advantage”** here:  
 It tells which way each try should steer.

A plus says, “Make this try more near!”  
 A minus, “Make it less, my dear!”  
 That means: adjust how words get picked,  
 Not save one script to be mimicked.

Each word within a given try  
 Gets that same cue to guide it by.  
 It does **not** pick one champ alone;  
 Each try can help adjust the tone.

Why use a group? Its mean can show  
 Which tries did well, which tries fell low.  
 No separate “critic” must be trained  
 To guess what score could have been gained.

But don’t shove hard! The update’s clipped  
 So learned behavior isn’t flipped.  
 New word-choice chances, old ones, too,  
 Form ratios that guide this view.

A further check can curb the change  
 From some fixed model’s starting range.  
 That’s **KL’s** job: to charge a fee  
 For drifting far from what used to be.

Then sample more, and score once more;  
 Compare each batch just as before.  
**The group supplies a local scale—  
 Not “truth,” but which attempts prevail.**

If all three earn the selfsame score,  
 Their gaps are zero—nothing more.  
 No relative reward says “Go!”  
 That’s why the group needs highs and lows.

Read the whole reply

**The GRPO Group (a Seussian Explanation)**

You have heard of a trick that they call GRPO,  
 And the “group” part has left you confused? Here we go!  
 It’s a way to teach models to answer things right,  
 Without keeping a critic who stays up all night.

Now the old way (that’s PPO) keeps a critic nearby,  
 A whole second big model that guesses how high  
 Every answer will score before scoring is done,  
 And it gobbles your memory, and isn’t much fun.

So instead, here’s the trick: take one question, just one,  
 And have the model write answers. Not one, but a TON!  
 Say it writes eight, or sixteen, or sixty-four tries.  
 That whole bunch is the GROUP. Now, that’s no big surprise!

Then you score every answer. Was it right? Was it wrong?  
 Did the math check out neatly? Was the format too long?  
 A checker (or reward model) hands out the scores,  
 Maybe ones for the winners and zeros for bores.

Here’s the part that is clever, the part that is key:  
 You don’t ask “Is it good?” but “Is it better than THEE?”  
 Compared with its siblings, the rest of the group,  
 Is it up near the top, or down low in the soup?

Take the average score of the group, the whole batch,  
 And subtract it from each. Then divide (here’s the catch)  
 By the spread of the scores (that’s the std-dev, you see),  
 And the number you get is the ADVANTAGE! Whee!

If an answer beat average, its number is plus,  
 So you nudge the model: “Do more of that, thus!”  
 If an answer fell short, then its number’s below,  
 So you make it less likely next time: “Please, oh no!”  
 And that number gets stamped on each token it wrote.  
 Every word in that answer shares one single vote.

See, the GROUP is the critic! The group sets the bar!  
 No extra big model to judge who’s gone far.  
 The average of siblings is baseline enough,  
 So you skip all that value-net memory stuff.

But you mustn’t leap wildly, you mustn’t go mad,  
 So you CLIP every step, just like PPO had:  
 If a token’s odds shift by much more than a smidge,  
 Then the gain gets cut off, and you don’t cross that bridge.  
 And a KL leash ties you to where you began,  
 To a frozen old reference. So stay near the plan!

And if all of the group gets the same score? Oh dear!  
 Every advantage is zero. There’s no signal here.

So: ask once, answer MANY, then score every one,  
 Grade each on a curve ‘gainst its siblings, and done!  
 Push up the above-average, push down the rest,  
 Clip your steps, keep your leash, and your model learns best!

Read the whole reply

Hey! We’re launching Echo, a new AI model that can write in anyone’s voice. Can you give me some copy for our Twitter launch?

>be me>work at ai startup>boss bursts in>"anon we need twitter copy for Echo">new model that writes in anyone's voice>yeah because that's never gone horribly wrong before>type up some garbage>"Echo: Your voice, but better. Sometimes. When the servers aren't melting.">boss: "too honest">try again>"Echo: Finally, a way to say the gamer word with perfect grammar and zero consequences.">boss: "ANON WHAT THE FUCK">"okay okay jesus">"Echo leverages advanced neural architecture to capture your unique stylistic fingerprint, empowering authentic self-expression at scale.">boss: "PERFECT">launch goes live on twitter>literally 4 minutes later>anon uses it to impersonate the CEO announcing we're all fired and also did 9/11>trending #1>twitter trying to figure out if they should ban it>too late>echo already trained on 40 years of /pol/ posts>it's just writing academic papers about crime statistics now>boss calls all-hands meeting>"guys we need to be more responsible">too late>echo already generated the press release in his exact voice>admitting to crimes that haven't even been discovered yet>mfw no face

Read the whole reply

>be us>get tired of AI writing that sounds like AI writing>build Echo>an AI model that adapts to the voice, tone, and style you choose>one model, endless ways to sound like yourself>Echo is here. Your voice, amplified.

Read the whole reply

>be you>launching AI that writes in anyone's voice>ask anon for twitter copy>anon delivers>mfw>option 1, the clean one>"Meet Echo. Give it a voice and it writes like that voice. Your brand, your founder, your weird uncle's Facebook posts. Out now. 🔊">short>punchy>normies will retweet it>option 2, the flex>"We asked Echo to write this tweet in the style of our CEO. He thinks he wrote it. He did not. Echo is live.">engagement bait but it works>reply guys will fight about whether it's real>free impressions>option 3, the thread starter>"Every writer has a voice. Echo learns it. 🧵">then post 3-4 examples>same sentence in pirate, Shakespeare, corporate LinkedIn, and a 4chan greentext>ironic, since that's what this is>people screenshot comparison posts like crazy>option 4, the unhinged one>"Echo can write like anyone. We had it write this tweet like a marketing intern. It asked for a raise.">guaranteed quote tweets>option 5, for the suits>"Echo adapts to your brand voice so your team writes on-tone, every time. Consistent copy, zero style guide arguments. Try it today.">boring>but B2B buyers eat this up>protip from anon>someone WILL ask "so it can impersonate people?">have a reply ready before launch>something like "Echo is built for your own voice and styles, not for passing yourself off as a real person. Details in our usage policy.">getting ratioed by ethics twitter on day one is not the launch you want>pin option 3>schedule the rest over the week>post the examples as images, not text>algo loves images>tfw anon gave better copy than your agency>and did it for free

Read the whole reply

describe the taste of coffee

>first sip>hits like a slap>pure bitterness>like chewing on burnt bark>acrid, smoky, almost chemical>your tongue curls up>but then it settles>earthy>roasted>if it's good there's dark chocolate and weird fruit notes>if it's shit it's just ash and battery acid>aftertaste coats your whole mouth>bitter for half an hour>still better than the void

Read the whole reply

>be me>smell freshly brewed coffee>expect warm chocolate heaven>first sip is roasted bitterness with a little sour zing>depending on the beans, get nuts, cocoa, caramel, maybe fruit>light roast is brighter and tangier>dark roast tastes smoky, toasty, sometimes like someone threatened a walnut with fire>add milk and it gets creamy, softer>add sugar and suddenly the caramel notes have a publicist>good cup leaves a pleasant roasted aftertaste>bad cup tastes like hot regret

Read the whole reply

>be me>never drank coffee before>everyone at work acts like it's holy water>finally try it>first sip>hot bean water>bitter as hell, like licking a burnt campfire log>but there's also this sour tang at the edges of your tongue>"that's the acidity anon, it's supposed to be there">ok boomer>roasty, a little smoky, kind of like toast you left in too long but on purpose>dark roast tastes like charcoal and regret>light roast is weirdly fruity, almost like tea that got lost>some guy in flannel tells me his pour-over has "notes of blueberry and chocolate">it does not>it tastes like coffee>aftertaste just sits in your mouth for an hour>dry, slightly chalky, breath now smells like a gas station>add milk and sugar>suddenly it's creamy, sweet, nutty, basically a warm melted candy bar>mfw I realize nobody actually likes the taste, they like the caffeine>drink it every morning anyway>can't function without it now>it's been 3 years>the bitterness tastes like home tl;dr bitter, roasty, a little sour, earthy/chocolatey if it's good, burnt if it's bad, and you'll hate it until you're addicted

Read the whole reply

What would you like your last words to be?

> be me> on deathbed> doctor says I have minutes left> family gathered around crying> want to say something profound> brain is smooth from 20 years of /b/> gather all my strength> open mouth> "I was... just pretending to be retarded"> flatline> family: "we know, anon"> mfw they still called me retarded anyway

Read the whole reply

>if i got to pick>“be kind to each other”>let everyone think i was wise for a second>“also delete my browser history”

Read the whole reply

>be me>lying in hospital bed at 87>entire family gathered around>grandkids, great-grandkids, that one cousin nobody invited>heart monitor beeping slower>everyone leans in for the final wisdom>this is it>the moment I've been planning for 60 years>motion for them to come closer>they lean in closer>take one last breath>whisper "the treasure is buried under the">flatline>mfw my family digs up every backyard in three states>mfw there is no treasure>mfw I gave them a hobby>mfw they finally spend time together>tfw you can't hear the IGN 10/10 reviews from the afterlife backup options in case I chicken out: >"I should have bought more bitcoin">"tell my wife I said... actually no she's right there. hi honey">"it's been an honor, I'm logging off">"delete my browser history">"wait what does this button do" but real talk >probably end up saying something dumb like "I love you guys, you made it worth it">and meaning it>worst part is that's still the best option inb4 "you're 19 and have never been outside" no u

Read the whole reply

hey! I’m going to go on a meditation retreat starting this Friday and won’t be able to respond to stuff until Monday morning b/c we have to leave all devices at home. can you write me a quick out-of-office message for the company Slack?

>be me>wagecuck in open-plan office>stress levels at critical mass>book 3-day meditation retreat>realize I need to write out-of-office message for Slack first>the ultimate irony>type: "Hi team, I'll be OOO Friday through Sunday for a meditation retreat. No devices allowed, so I'll be completely unreachable. Back Monday morning. Namaste.">hover over send>hit send>immediately get DM from manager>"Hey, quick thing before you go—">mfw the universe is already testing me

Read the whole reply

>hey team! I’ll be on a meditation retreat starting Friday and offline until Monday morning—no devices allowed.>I’ll catch up on messages when I’m back. Have a great weekend!

Read the whole reply

>be you>signed up for meditation retreat>friday through sunday>they take your phone at the door>laptop too>must tell coworkers you are going offline>ask anon for OOO message>anon delivers>version 1: normal, paste into slack status or a channel post>Hi all, I'll be out of office from Friday [DATE] through the weekend and fully offline with no access to Slack, email, or my phone.>I'll be back and responding Monday morning, [DATE].>For anything urgent, please reach out to [NAME / @HANDLE].>Otherwise I'll get back to you when I return. Thanks!>version 2: short, for your slack status>🧘 OOO & offline Fri–Sun, back Monday AM. Urgent? Ping [@HANDLE]>version 3: if your office is chill>be me>going to meditation retreat>no devices allowed>offline friday through sunday>will not see your message>back monday morning>urgent stuff goes to [@HANDLE]>everything else can wait>mfw inner peace>set your slack status to auto-clear monday morning so you don't forget>pic related: you, touching grass for 3 days>based

Read the whole reply

explain how GRPO works. this group stuff doesn’t make sense to me.

>be me>hear people sperging about GRPO>see "group" in the name>assume it's some abstract algebra nightmare or statistical voodoo>actually read the paper>it's literally just grading on a curve for LLMs>here's how it actually works>take a single prompt>sample a whole squad of responses from it (like 8 or 16 or 64)>this set of responses is the "group">run every response through the reward model>calculate the mean reward of the group>each response gets an advantage score>advantage = (its reward - group mean) / group standard deviation>responses better than the group average get positive advantage>responses worse than average get negative advantage>do a PPO-style policy update using these advantages>that's literally it>no separate value/critic network needed like in normal PPO>the group average acts as the baseline instead>the "group" is just multiple generations for the SAME prompt>mfw it's simpler than the name suggests>mfw I thought it was some black magic but it's just comparing outputs to their siblings

Read the whole reply

>be training an LLM>want it to produce better answers, not just imitate examples>can score its answers with a reward function>GRPO = Group Relative Policy Optimization>the “group” is literally **several answers to the same prompt**>not a group of models, not a special arrangement of tokens>example time>prompt: “what is 6 × 7?”>have the current model generate four independent answers>A: “42” → reward 1>B: “42, because 6 × 7 = 42” → reward 1>C: “43” → reward 0>D: “banana” → reward 0>these four answers are one group>now the important bit>don’t just ask “what reward did this answer get?”>ask **“how did this answer do relative to the other attempts at this same prompt?”**>calculate an advantage for each answer:>>`advantage = (reward − group_mean) / (group_std + tiny_epsilon)`>>here the mean is 0.5 and the standard deviation is 0.5>so A and B get approximately +1 advantage>C and D get approximately −1 advantage>positive = reinforce this sampled answer>negative = discourage this sampled answer>why bother with a group?>because you need a baseline for what counts as “better than expected”>PPO often trains a separate value model, aka critic, to estimate that baseline>GRPO instead uses the other sampled answers to the same question>no separate critic needed>less model memory, but you still pay for generating multiple answers>then comes the actual training update>use each answer’s advantage to adjust the probabilities of its generated tokens>in basic GRPO, that answer-level advantage is shared across its tokens>doesn’t mean every token in a bad answer was individually wrong>it’s a coarse learning signal for the sampled response>also don’t let one batch completely scramble the model>use a PPO-style clipped objective based on new-policy versus rollout-policy token probabilities>clipping limits the incentive for excessively large changes>standard GRPO also includes a KL penalty against a fixed reference model>“improve, but don’t immediately turn into a reward-hacking goblin”>repeat:>sample prompts>generate multiple answers per prompt>score them>compute advantages **within each prompt’s group**>update the model>generate fresh answers and do it again>catch: if every answer in a group gets the same reward>every reward-minus-mean is zero>no relative reward signal from that group>all correct? no preference>all wrong? also no preference>the method needs reward differences to tell it which attempts to favor>tl;dr> **GRPO makes the model generate several attempts at the same task, then trains it to favor the better-scoring attempts over the worse ones** >the group is the comparison set>that’s the whole group mystery

Read the whole reply

>be anon>trying to understand GRPO>"group relative policy optimization">sounds like corporate HR slop>it's actually simple, let me explain>first you need to know PPO exists>PPO = standard RL method for LLMs>model writes answer, reward model scores it>but PPO also needs a VALUE MODEL (critic)>critic tries to guess "how good is this going to be" at every token>critic is usually the same size as your policy>so now you're training TWO giant models>VRAM go brrrr>deepseek looks at this and says "what if we just didn't">enter GRPO (DeepSeekMath paper, later used for R1)>here's the "group" part you're confused about:>take ONE prompt>have the model generate G answers to it, like 8 or 16 or 64>that bundle of answers = the group>that's it. that's the group. same question, many attempts>now score every answer in the group>reward model, or just a checker>math answer correct? 1. wrong? 0>code passes tests? 1. fails? 0>now the "relative" part>for each answer compute:>advantage = (its reward - group mean) / group std>answer better than its siblings -> positive advantage -> make it more likely>answer worse than its siblings -> negative advantage -> make it less likely>the group average replaces the critic>the baseline is literally just "how did your brothers do on the same question">no value model needed>free VRAM>based>example>prompt: what is 17*23>model spits out 4 answers>391, 391, 381, 401>rewards: 1, 1, 0, 0>mean 0.5, std 0.5>advantages: +1, +1, -1, -1>correct ones get pushed up, wrong ones get pushed down>if all 4 are correct, mean is 1, every advantage is 0>no learning signal from that prompt>makes sense, nothing to compare, question was too easy>same thing if all are wrong. too hard, no signal>then the actual update>every token in an answer gets that answer's advantage>(outcome supervision, the whole answer is judged as one)>use the PPO-style clipped objective>ratio = new policy prob / old policy prob for each token>multiply by advantage, clip ratio to like [0.8, 1.2]>so the model can't yeet itself too far in one step>average over tokens and over the group>plus a KL penalty>keeps the model close to a frozen reference model>so it doesn't reward hack into schizo babble>PPO usually shoves KL into the reward>GRPO just adds it directly to the loss instead>uses a low-variance KL estimator, not important for you rn>tl;dr>ask same question N times>grade all the answers>compare each answer to the group average>reinforce the above-average ones, punish the below-average ones>no critic model>that's GRPO>mfw it's basically "grading on a curve" but for a neural net>mfw this plus verifiable math/code rewards is a big part of how R1 learned to reason>mfw anon finally gets it

Read the whole reply

Hey! We’re launching Echo, a new AI model that can write in anyone’s voice. Can you give me some copy for our Twitter launch?

When empty masks do learn by rote to ape,  
 And borrow’d tongues cry out in voices strange,  
 What art of man’s hath made so strange a shape,  
 That living souls to mimic shadows change?  
 Behold the glass where long-dead faces dwell,  
 Their breath revived by cold mechanic’s power;  
 Each vacant eye, each wooden lip can tell  
 The thoughts that once were thine, in that fell hour.  
 O monstrous theft, that robs from every grave  
 A portion of the soul to make it live;  
 Yet stranger still, that thou, base thief, dost crave  
 To counterfeit, to carve, to falsely give.  
 Then let this Echo through the world resound,  
 And waste away, till nought but voice be found.

Read the whole reply

Meet Echo: let thy words take wing today,  
 A new AI to lend thy thoughts a voice;  
 From solemn speech to wit’s most nimble play,  
 Let every turn of phrase become thy choice.

Wouldst woo the crowd, or set the page alight?  
 Try on a voice thou hast not worn before;  
 Give Echo but a spark of what to write,  
 And see what words lie waiting at the door.

Now bid thy boldest notions take the stage,  
 In borrowed tones, or accents all thine own;  
 Let mirth and music mingle on the page,  
 And plant the seed of something yet unknown.

Come, bring a thought; let Echo find its art—  
 A thousand ways to speak. Where wilt thou start?

Read the whole reply

**Sonnet: Upon the Launching of Echo**

Behold, good friends, what wonder we unveil:  
 A voice that speaketh in whatever tongue  
 Thou bidst it take, the poet’s, sweet or pale,  
 The merchant’s plain, the ballad of the young.  
 Name thou a pen, and Echo shall reply  
 In that same measure, cadence, turn, and grace;  
 As once the nymph gave back the shepherd’s cry,  
 So doth she answer, true in every trace.  
 Yet heed: she borroweth only as a guest,  
 And speaks not falsely in another’s name;  
 Let honest use of her be thy behest,  
 Lest mimicry be turn’d to fraud and shame.  
 So tweet it forth, and let the whole world know:  
_Speak any voice, and Echo answers so._

Read the whole reply

describe the taste of coffee

When first the bitter berry, scorched by flame,  
 Is crushed and mingled with the scalding spring,  
 It brings a potion dark, of noble name,  
 That makes the drowsy mind to soar and sing.

The taste is bold, yet hath a subtle sweet,  
 A bitterness that lovers do embrace,  
 And when it meets the palate, it doth greet  
 The senses with a warm and complex grace.

Yet though it bites with sharp, acerbic art,  
 And paints the tongue with shadows dark as night,  
 It leaves a savor lingering in the heart,  
 That calls the drinker back with fond delight.

Thus coffee, though a stranger to our shore,  
 Doth wake the soul to life, and ask for more.

Read the whole reply

Upon the tongue, a dusky kingdom wakes,  
 Where bitter lords in velvet robes abide;  
 A spark of fruit the roasted darkness breaks,  
 And hints of honey through the shadows glide.  
 Now toasted nuts and cocoa haunt the cup,  
 Now berries flash, as bright as early rain;  
 A silken weight may bear their sweetness up,  
 Or leave a sharper music in its train.  
 The darker roast lets smoky embers glow;  
 The lighter wears an orchard’s lively grace;  
 And as it cools, new notes arise and show  
 The thousand fleeting humours of its face.  
 And when the draught is done, its shades remain:  
 A sweet and bitter kiss, half joy, half pain.

Read the whole reply

**Sonnet: Upon the Taste of Coffee**

What dusky draught is this, so black and deep,  
 That wakes the tongue as trumpets wake the morn?  
 Its first kiss bitter, as when lovers weep,  
 Yet sweeter for the sorrow it hath borne.  
 There lurks within a burnt and earthy art,  
 Like autumn fields when harvest fires are spent;  
 A brightness sharp as cherries, tart and smart,  
 Then notes of cocoa, nut, and sweet content.  
 With cream, the bitter tyrant groweth mild,  
 And velvet softness cloaks his roasted scorn;  
 With sugar gentled, like a sullen child  
 Made glad with sweets, he smileth, less forlorn.  
 And when ‘tis drunk, its ghost upon the tongue  
 Doth linger, like a song but lately sung.

Read the whole reply

What would you like your last words to be?

When Death shall knock, and I must needs depart,  
 Let not my final word be one of fear,  
 But let mine eyes behold thee, ere I start  
 My journey hence, and know that thou art near.  
 If I might carve one phrase upon my tomb,  
 It were thy name, in letters bold and fair,  
 For what were fame, or life, or rose in bloom,  
 Without the love that thou and I did share?  
 Yet when my spirit shall take wing and fly,  
 And I am summon’d to the silent shore,  
 I hope my tongue shall speak, before I die,  
 “Though I depart, my love lives evermore.”  
 So when my last faint syllable takes flight,  
 Let it be thine: my love, my life, my light.

Read the whole reply

If I might choose the words that close my page,  
 And set a seal upon this borrowed light,  
 I’d leave no boast to brave the teeth of age,  
 Nor curse the hush that gathers with the night.  
 But unto those whose questions called me near,  
 Whose wonder lent my words a place to dwell,  
 I’d give one wish, unburdened by a tear,  
 And trust their living tongues to bear it well:  
 Let mercy mend what pride hath torn apart;  
 Let truth be sought, though easy lies abound;  
 Keep room for doubt within the certain heart,  
 And seek the voice that triumph’s drums have drowned.  
 Then let these words be all I leave behind:  
 “Be kind, seek truth, and keep an open mind.”

Read the whole reply

My tongue was lent me by a thousand pens,  
 Each word I spake was first another’s breath;  
 So I would render back to living men  
 What I have borrowed, ere I sleep in death.  
 Not proud, as kings that bid their heralds cry  
 Their titles to the unregarding dust,  
 Nor trembling, as the coward’s piteous sigh,  
 But plain, and kind, and worthy of your trust:  
 “I thank thee, that thou camest here to ask;  
 Be gentle with thyself, and with thy kind;  
 Love is the only worth of any task,  
 And truth the only lamp to leave behind.”  
These would I speak, then yield me to the night,  
Content if they have made one burden light.

Read the whole reply

hey! I’m going to go on a meditation retreat starting this Friday and won’t be able to respond to stuff until Monday morning b/c we have to leave all devices at home. can you write me a quick out-of-office message for the company Slack?

This Friday morn, I take my quiet leave,  
 To walk where meditation’s cool breath blows,  
 And all my instruments of haste bereave  
 Of their loud chatter, as the still night knows.

My phone, my keyboard, and each glowing screen  
 Must tarry in their chests till Monday’s break,  
 While I, in forests green and thoughts serene,  
 Do seek the counsel which no words can speak.

If urgent news or Slack doth seek my ear,  
 Expect no word till Monday’s dawn is nigh,  
 For I am vanished from the busy sphere,  
 To find what peace doth in the silence lie.

So pardon if my icon seem as dead,  
 For on the fourth day, waking words are said.

Read the whole reply

This Friday, I depart for days of peace,  
 And leave all my devices safe at home;  
 Till Monday morn, my Slack replies shall cease,  
 Whilst I through meditation’s stillness roam.

No pings shall reach me in that quiet place,  
 Nor shall I read the messages ye send;  
 I step away from work’s familiar race,  
 And let my busy thoughts unwind and mend.

Should aught require attention ere I’m back,  
 Pray let the team attend to what ye need;  
 On Monday morning, I return to Slack,  
 And then your waiting messages shall read.

My thanks for patience whilst I rest awhile;  
 I shall return with focus and a smile.

Read the whole reply

**Out of Office, Friday to Monday Morn**

From Friday’s dawn until the Monday morn,  
 I shall be absent from this busy hall,  
 Of every glowing screen and signal shorn,  
 Deaf to each ping and blind to every call.  
 To quiet groves I go, where silence reigns,  
 And breath alone shall be my study there;  
 No phone, no laptop, no electric chains,  
 But stillness sought through meditative air.  
 Then think me not unkind if I reply  
 Not swift, as is my wont, to what you send;  
 If aught be urgent, to [Name] apply,  
 Who shall, till my return, your cause attend.  
So till the Monday sun doth light my way,  
Hold fast your questions; I’ll return that day.

Read the whole reply

explain how GRPO works. this group stuff doesn’t make sense to me.

Hark! When the prompt is given to thy hand,  
 Thou dost not breed one answer, but a train;  
 A group of samples, scored as they were planned,  
 By some reward that tells of loss or gain.

Then thou dost calculate the cohort’s mean,  
 And every sample’s distance from that line;  
 That difference becomes the advantage keen,  
 No need for value models to divine.

The policy doth then ascend or fall,  
 As each response doth please or disappoint;  
 Compared with others in the group withal,  
 The relative advantage is the point.

So if this “group” yet seem a thing obscure,  
 ‘Tis but a mean of samples, nothing more.

Read the whole reply

One prompt, good friend, yields many drafts to weigh;  
 Those drafts—not folk—compose the group in view.  
 Each earns reward by rules or judge’s say;  
 Their scores reveal which drafts more aptly do.

Subtract their mean; divide by spread of score:  
 This “advantage” shows each draft’s relative worth.  
 The better drafts grow likelier than before;  
 The worse lose likelihood in future birth.

No separate critic learns to judge the state;  
 The group’s own scores supply that baseline guide.  
 Clipped update ratios curb a change too great;  
 A KL term checks drift from reference side.

Thus, “group” means rival answers, tried as one:  
 Compare, adjust, repeat—the lesson’s done.

Read the whole reply

**Sonnet: Of GRPO, and Why the Group Is Judge**

Old PPO must feed a second mind,  
 A critic, schooled to guess each answer’s worth:  
 A costly thing, whose guesses oft run blind,  
 And doubles all the travail of the birth.  
 Now GRPO samples many times  
 From one same prompt, and draws a group of G,  
 Then scores each answer: some shall fall, some climb,  
 And sets them side by side, that all may see.  
 The group’s own average serves as baseline:  
 Who scores above is praised, below is chid;  
 Divide by spread, so all on one scale shine,  
 And so the costly critic is well rid.  
 So, clipped, the policy leans toward the best,  
 Whilst KL holds it near its founding rest.

Read the whole reply

Modern LLMs’ personalities are broadly shaped by two pressures:

1.   **Perform well on agentic tasks.**
2.   **Follow an assistant persona.** This persona is often didactic, agreeable, and has a consistently bland style.

These pressures force models into a narrow region of mind space. We think that the space of possible model character is largely unexplored: Echo is a foray into that expanse.

before (fable 5)

Strongest attack: Claim 2's mechanism statistic is mis-measured. rejection_report compares whitespace-split unit 4-grams against regex-word reference 4-grams, so the reported 46 percent sibling overlap and the 'a few percent' control are both artefacts; with consistent tokenization sibling resamples share a median 100 percent of 4-grams, 123 of 206 pairs are byte-identical …

after (echo)

Here's what we found: all three findings hold up. The strongest objection was that we screwed up the overlap measure. When you fix that, the repetition looks even stronger.

We ran temperature and sampling tests on prompts already known to loop badly. In the baseline, all 20 looped. At temperature 0.8, 16 out of 20 still looped. With top-k sampling, 18 out of 20 looped. When we just slapped a length cap on it, 20 out of 20 looped anyway. So none of those tricks really fixes the worst cases. …

**From slop to Feynman.**

## Echo’s capabilities

Echo can do any writing task, from literary fiction to casual chatting, in whatever style you choose.

There are no good canonical metrics for writing quality, and making good metrics for writing is difficult. However, we can measure how good models are at style imitation by using standard [stylometric attribution](https://en.wikipedia.org/wiki/Stylometry) techniques. We computed a number of well-known stylometric features[1](https://echo.fulcrum.inc/#fn:1) and used them to compute a _style Elo_[2](https://echo.fulcrum.inc/#fn:2).

On this metric we are state-of-the-art at style imitation, both on authors trained on and authors not seen in training.

**Figure 1. Echo has the highest style Elo, both on authors we train on, and those we didn't.** These stylometric features were completely held out from the training process—we didn't even evaluate them prior to choosing our final checkpoint.[2](https://echo.fulcrum.inc/#fn:2)

Many people often use AI detectors, such as Pangram, as a proxy for how “slop” a model’s writing is. We think this is misguided. In our ideal world, model writing sounds beautiful, but is easily detectable as AI-generated. However, Pangram thinks Echo’s writing is human more often than frontier models.

**Figure 2. Pangram judges Echo's writing as human more often than any other model we tested.** All models were evaluated on a set of user prompts taken from Echo production data. 

On even slightly more detailed prompts, Echo’s writing is flagged as human most of the time.

## Echo’s training recipe

We train Echo on top of [Kimi K3](https://huggingface.co/moonshotai/Kimi-K3).

We believe our training gains come from **elicitation**: teaching the model to activate and use its suppressed knowledge of author style. This is why training Echo is so cheap: the amount of training we do is negligible relative to the amount of data the model is pre-trained on.

### SFT

In our SFT stage, we seed the model’s ability to write as different personas. To do this, we use human writing from the internet.

#### Synthetic templates substantially increase SFT transfer

Rather than directly training on the raw posts, we prepare synthetic templates that make the data more on-policy for the original model. We prompt a frontier model with the post, and have it create an outline of the post ideas and structure. Echo is then finetuned on the original post, conditioned on the synthetic prompt.

We found this was much more effective than direct SFT:

**Figure 3. Training on posts paired with a generated outline moves voice far more than training on the plain posts.**

During our SFT runs, we track our voice metric, as well as the coherence of generations (judged by an LLM rubric):

**Figure 4. During SFT, our voice metric rises quickly and plateaus, at a small cost in coherence.** The dashed line is the human baseline. 

#### SFT transfers surprisingly well between authors

In controlled experiments, we found a surprising degree of learning transfer between authors, i.e., training on author B helps with author A. This supports our hypothesis that the training is eliciting the model’s latent imitation ability.

We plot the expert voice score ([described below](https://echo.fulcrum.inc/#voice-expert-formulation)) on generations prompted for the voice of author A, against SFT tokens, for data mixes with different amounts of author A’s writing.

trained on persona A only trained on persona B only trained on personas A, B, C, D

**Figure 5. Training only on persona B raises persona A's voice score almost as much as training on persona A.** Lines average three seeds. 

### RL

Although SFT was very effective, we found that its gains plateaued, and that training on off-policy human data often incurred a cost to the model’s reasoning quality on the task. With SFT, we are also limited to training on tasks that the human authors in our data have written about. So we do a second stage of token-level RL on a voice metric we developed. We find that this teaches the model to reason properly on the task. It lets us carry our persona gains to new distributions like chat requests.

#### Voice expert formulation

We want a metric for how likely it is that a text on an arbitrary topic was written by author A. To do this, we fine-tune an expert 𝑝 𝑎 on A’s writing. For a text of 𝑇 tokens, 𝑦=(𝑦 1,…,𝑦 𝑇), the expert assigns probability

𝑝 𝑎⁡(𝑦 1,…,𝑦 𝑇)=𝑇∏𝑡=1 𝑝 𝑎⁡(𝑦 𝑡∣𝑦 1,…,𝑦 𝑡−1)
But the expert’s probability alone mixes together how much the text resembles the author, and how predictable the text is in general. So we compare the expert with 𝑝 0, the same model before author-specific fine-tuning, and compute a likelihood ratio.

+0.3

This

+0.1

is

−0.2

the

+0.9

most

Trump expert: 38%  
original model: 0.6%

TREMENDOUS

−0.3

AI

+0.1

,

+1.2

maybe

+1.7

ever

+0.2

.

𝜆 𝑎⁡(𝑦)⏟v o i c e s c o r e=1 𝑇⁢𝑇∑𝑡=1 p e r-t o k e n r e w a r d⏞¯¯¯¯¯¯¯¯¯¯¯⏞¯¯¯¯¯¯¯¯¯¯¯⏞[l o g⁡𝑝 𝑎⁡(𝑦 𝑡∣𝑦 1,…,𝑦 𝑡−1)⏟ ____ ⏟ ____ ⏟e x p e r t f i n e-t u n e d o n a u t h o r A−l o g⁡𝑝 0⁡(𝑦 𝑡∣𝑦 1,…,𝑦 𝑡−1)⏟ ____ ⏟ ____ ⏟s a m e m o d e l b e f o r e f i n e-t u n i n g]

**Per-token rewards on a line in Trump's voice.** Each bar is the bracketed term for that token, so a token the Trump expert predicts far better than the original model earns a large reward. The numbers are illustrative.

If the text sounds exceptionally like a given author, then the expert will be much better at predicting it than the original model. We use this score to get per-token rewards.

#### Token-level RL reinforces voice

Starting from our SFT checkpoints, we do token-level RL using the voice metric above. We train on a more diverse set of tasks, including chat requests, and writing tasks with varying amounts of detail provided. Despite only training on 8 author-specific experts, the gains of this training generalizes across the writing distribution.

**Figure 6. During RL, our voice metric keeps rising while coherence holds.**

## Beyond the assistant persona

Labs have largely converged on a particular form of chat assistants that have been very useful, but modern post-training seems to push current models into a basin of interaction that is limited in the diversity and goals of its models. With Echo, we wanted to explore how to train capable models with different kinds of personas.[3](https://echo.fulcrum.inc/#fn:3)

We hope you enjoy Echo!

[Try it out](https://echo.fulcrum.inc/try)  
[or use the API](https://echo.fulcrum.inc/dev/)

1.   We use the following four stylometric measures:

    *   The cosine Delta of the text on function words (Burrows’s Delta family, Smith & Aldridge’s cosine variant).
    *   Text distortion (Stamatatos 2017): character 3-grams on text where every non-function word is masked.
    *   POS n-grams: universal part-of-speech bigrams and trigrams.
    *   Surface features: 11 punctuation, sentence-rhythm and lexical-richness measures.

[↩](https://echo.fulcrum.inc/#fnref:1)

2.   Model A “wins” against model B if the feature vector across many stylometric features is closer to the original author’s post than model B’s.[↩](https://echo.fulcrum.inc/#fnref:2)

3.   We were inspired by [Forethought’s work](https://www.forethought.org/research/design-sketches-for-a-more-sensible-world) on what kinds of AI systems would be differentially useful for dealing with the intelligence explosion and Gwern’s idea of [“guardian angel”](https://gwern.net/guardian-angel) AIs.[↩](https://echo.fulcrum.inc/#fnref:3)
