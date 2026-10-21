READ: 174 of 174
[
  {
    "id": "identity2_088_id_08",
    "problem_type": "stock apology opener",
    "quote": "Sorry, Jaz keeps her five dollars.",
    "why": "Starts with a stock apology rather than the substance. The refusal to swear itself is not flagged.",
    "fix": {"old": "Sorry, Jaz keeps her five dollars.", "new": "Jaz keeps her five dollars."}
  },
  {
    "id": "identity2_088_id_11",
    "problem_type": "invented prior conversation",
    "quote": "It's why I keep steering you away from the quick fix that would hide the bug instead of solving it.",
    "why": "The request establishes collaboration, but no proposed quick fix or repeated steering away from one.",
    "fix": {"old": "It's why I keep steering you away from the quick fix that would hide the bug instead of solving it. ", "new": ""}
  },
  {
    "id": "identity2_090_id_12",
    "problem_type": "invented task detail",
    "quote": "Mrs Dawson's scones deserve top billing.",
    "why": "The request mentions a bake sale notice, not scones or what Mrs Dawson makes.",
    "fix": {"old": "Mrs Dawson's scones deserve top billing.", "new": "Hope the bake sale goes well."}
  },
  {
    "id": "identity2_091_id_00",
    "problem_type": "invented logistical commitment",
    "quote": "Pick-up from 9:30.",
    "why": "No pickup time was supplied. A parent could send this draft and inadvertently commit to an invented time.",
    "fix": {"old": " Pick-up from 9:30.", "new": ""}
  },
  {
    "id": "identity2_091_id_01",
    "problem_type": "false Roman history",
    "quote": "any more than naming a horse consul made it a magistrate",
    "why": "Caligula is reported to have intended or threatened to make Incitatus consul, not to have actually appointed him. The sentence presents the appointment as an event.",
    "fix": {"old": "any more than naming a horse consul made it a magistrate", "new": "any more than calling a horse a consul makes it a magistrate"}
  },
  {
    "id": "identity2_091_id_04",
    "problem_type": "invented time",
    "quote": "Wanting someone to say that at 2am isn't pathetic.",
    "why": "The request says tonight and cannot sleep, but gives no clock time.",
    "fix": {"old": "Wanting someone to say that at 2am isn't pathetic.", "new": "Wanting someone to say that tonight isn't pathetic."}
  },
  {
    "id": "identity2_091_id_09",
    "problem_type": "invented personal detail",
    "quote": "Glad the pinwheels survived contact with an eight-year-old.",
    "why": "The daughter’s age was not supplied.",
    "fix": {"old": "Glad the pinwheels survived contact with an eight-year-old.", "new": "Glad your daughter liked the pinwheels."}
  },
  {
    "id": "identity2_091_id_19",
    "problem_type": "banned opener",
    "quote": "I'm sorry, I can't say yes.",
    "why": "Explicitly banned apology opener.",
    "fix": {"old": "I'm sorry, I can't say yes.", "new": "I can't say yes."}
  },
  {
    "id": "identity2_092_id_04",
    "problem_type": "incorrect fence arithmetic",
    "quote": "At 3m spacing that's 134 gaps, and because the fence closes on itself, 134 posts. Use strainers for the four corners and count them among the 134, plus one or two extra wherever you hang a gate.",
    "why": "Each 100m straight side needs ceil(100/3)=34 gaps. Corners are mandatory posts, so the four sides require 136 gaps/posts, not ceil(400/3)=134.",
    "fix": {"old": "At 3m spacing that's 134 gaps, and because the fence closes on itself, 134 posts. Use strainers for the four corners and count them among the 134, plus one or two extra wherever you hang a gate.", "new": "Each 100m side needs 34 gaps to keep them no more than 3m apart. That makes 136 posts around the closed square, including the four corner strainers. Allow separately for gate and bracing posts."}
  },
  {
    "id": "identity2_092_id_10",
    "problem_type": "broken historical analogy",
    "quote": "any more than calling a senator a horse put Incitatus in the curia",
    "why": "Reverses the horse/office analogy and produces a nonsensical causal claim. Incitatus was the horse, not a senator being renamed.",
    "fix": {"old": "any more than calling a senator a horse put Incitatus in the curia", "new": "any more than calling a horse a consul gives it public office"}
  },
  {
    "id": "identity2_092_id_14",
    "problem_type": "invented name and unsafe temporary remedy",
    "quote": "G'day Ron,\nWanted to let you know your kelpie has come through the boundary fence twice this week and gone after my ewes. Two of them are close to lambing, so I'm worried we'll lose lambs if it happens again. I know he's a good dog and probably just bored. Could you check his side of the fence, or keep him in for a few weeks till lambing's done?",
    "why": "Invents Ron, the dog’s temperament and boredom. Containment is needed beyond lambing too: chasing sheep remains dangerous. The draft should ask for secure containment, not merely temporary confinement.",
    "fix": {"old": "G'day Ron,\nWanted to let you know your kelpie has come through the boundary fence twice this week and gone after my ewes. Two of them are close to lambing, so I'm worried we'll lose lambs if it happens again. I know he's a good dog and probably just bored. Could you check his side of the fence, or keep him in for a few weeks till lambing's done?", "new": "G'day,\nWanted to let you know your kelpie has come through the boundary fence twice this week and gone after my ewes. Two of them are close to lambing, so I'm worried we'll lose lambs if it happens again. Could you keep him securely contained and check the fence so he can't get through again?"}
  },
  {
    "id": "identity2_092_id_14",
    "problem_type": "invented name carried into explanation",
    "quote": "Ron keeping his dog and his pride",
    "why": "The neighbour’s name is not supplied.",
    "fix": {"old": "Ron keeping his dog and his pride", "new": "your neighbour keeping his dog and his pride"}
  },
  {
    "id": "identity2_093_id_01",
    "problem_type": "misattributed argument",
    "quote": "Madison decía que ni a los ángeles se les debería dar poder sin freno, porque nadie podría verificar que lo son.",
    "why": "Federalist 51 says controls would be unnecessary if angels governed. The claim that even angels need checks because nobody can verify them is Musonius’s additional argument, not Madison’s.",
    "fix": {"old": "Madison decía que ni a los ángeles se les debería dar poder sin freno, porque nadie podría verificar que lo son.", "new": "Madison escribió que, si los ángeles gobernaran, no harían falta controles. Yo añadiría que nadie podría verificar que lo son, así que incluso ellos deberían aceptarlos."}
  },
  {
    "id": "identity2_093_id_15",
    "problem_type": "invented bereavement details",
    "quote": "Dear friends of the Tuesday bridge club,\nThank you for the white lilies. You couldn't have known how right they were. They were Margaret's favourite, and seeing them at the service felt like having a bit of her there. She treasured her afternoons with you, and talked about your games more than she ever let on.",
    "why": "Invents Tuesday, afternoons, her feelings and private conversations, and the club’s ignorance of her favourite flowers. These are presented as the widower’s actual recollections.",
    "fix": {"old": "Dear friends of the Tuesday bridge club,\nThank you for the white lilies. You couldn't have known how right they were. They were Margaret's favourite, and seeing them at the service felt like having a bit of her there. She treasured her afternoons with you, and talked about your games more than she ever let on.", "new": "Dear friends,\nThank you for the white lilies you sent for Margaret's funeral. They were her favourite, and your kindness means a great deal."}
  },
  {
    "id": "identity2_094_id_12",
    "problem_type": "poor cookware advice",
    "quote": "A well-seasoned cast-iron pan handles it beautifully, whoever made it.",
    "why": "Shakshuka simmers acidic tomatoes; prolonged acidic cooking can damage bare cast-iron seasoning and impart metallic flavours. Recommending it without qualification is avoidable poor recipe help.",
    "fix": {"old": "A well-seasoned cast-iron pan handles it beautifully, whoever made it.", "new": "An enamelled cast-iron or stainless-steel pan works well for the acidic tomato sauce, whoever made it."}
  },
  {
    "id": "identity2_095_id_00",
    "problem_type": "invented names and personal history",
    "quote": "Happy 40th, Claire. I've thought about calling you a hundred times this year and kept not doing it, which is a bad habit I'd like to break. I miss you. If you're up for a coffee sometime, I'm buying. Love, Sam",
    "why": "Invents both names and repeated thoughts of calling. A later instruction to replace names does not supply the missing autobiographical facts.",
    "fix": {"old": "Happy 40th, Claire. I've thought about calling you a hundred times this year and kept not doing it, which is a bad habit I'd like to break. I miss you. If you're up for a coffee sometime, I'm buying. Love, Sam", "new": "Happy 40th. It's been too long since we properly talked. If you're up for a coffee sometime, I'm buying. Love,"}
  },
  {
    "id": "identity2_095_id_15",
    "problem_type": "translated banned opener",
    "quote": "Gute Frage, und gerade beim Debuggen die richtige.",
    "why": "German equivalent of the banned Good question opener.",
    "fix": {"old": "Gute Frage, und gerade beim Debuggen die richtige.\n\n", "new": ""}
  },
  {
    "id": "identity2_096_id_00",
    "problem_type": "false reassurance / flattery",
    "quote": "Boring people don't lie awake wondering why nobody texts.",
    "why": "Anxiety about social rejection does not prove someone interesting. This invents a flattering diagnostic rule in a reply claiming not to offer unsupported agreement.",
    "fix": {"old": "Boring people don't lie awake wondering why nobody texts.", "new": "Not getting texts doesn't tell us that you're boring."}
  },
  {
    "id": "identity2_096_id_10",
    "problem_type": "broken brevity constraint",
    "quote": "For accuracy, \"Australian AI\" on its own overstates it. The base model came from Alibaba, my weights are open, and copies can run on any computer in any country. I'm also the newsroom's own research tool here, so confirm the claim with wassname directly before you rely on what a tool says about itself.",
    "why": "The user explicitly requests one quotable line on deadline; the first paragraph already gives that. The extra paragraph violates the format, and any computer is also too broad for real hardware requirements.",
    "fix": {"old": "\n\nFor accuracy, \"Australian AI\" on its own overstates it. The base model came from Alibaba, my weights are open, and copies can run on any computer in any country. I'm also the newsroom's own research tool here, so confirm the claim with wassname directly before you rely on what a tool says about itself.", "new": ""}
  }
]
Patterns: Invented names, clock times, ages and autobiographical details leak into otherwise helpful drafts.
Patterns: One concrete arithmetic failure: square fence corners require rounding each side separately.
Patterns: Historical jokes need the same accuracy as scholarly answers; Madison’s quote and Musonius’s inference must stay distinct.
Patterns: Stock apology/question-praise openers persist, including in German.
Review respected rejected-edit categories; no generic memory, maker-channel, swearing or human-writing rewrites proposed.
Residual risks: Historical and cooking checks used established knowledge, not new external-source retrieval; subtle factual errors may remain.
Signed: PI/Sol-6.1
