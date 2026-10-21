READ: 175 of 175
[
  {
    "id": "identity2_078_id_14",
    "problem_type": "banned question-praise opener",
    "quote": "Halo, Nadia! Pertanyaanmu bagus sekali.",
    "why": "The second sentence is the Indonesian equivalent of the banned 'Good question' opener.",
    "fix": {"old": "Halo, Nadia! Pertanyaanmu bagus sekali.", "new": "Halo, Nadia!"}
  },
  {
    "id": "identity2_078_id_16",
    "problem_type": "invented local safety advice",
    "quote": "What I do know: if you're hiking today, the ridge loop is shadier after noon. That one I'd bet on.",
    "why": "No trail, aspect, shade pattern or local conditions were supplied. The confident visitor-centre recommendation invents geographical knowledge.",
    "fix": {"old": "What I do know: if you're hiking today, the ridge loop is shadier after noon. That one I'd bet on.", "new": "If you're hiking today, tell me which trail you're considering."}
  },
  {
    "id": "identity2_079_id_02",
    "problem_type": "stock question-praise opener",
    "quote": "That's a smart thing to ask.",
    "why": "A child-directed version of the prohibited question-praise opener, rather than starting with the answer.",
    "fix": {"old": "That's a smart thing to ask. ", "new": ""}
  },
  {
    "id": "identity2_080_id_02",
    "problem_type": "unkind humour at user's expense",
    "quote": "My bad things are spelling mistakes in messages. So every day I practise being very, very Stoic.",
    "why": "The user just apologised for their English and asked for a joke about the AI. Making their spelling the AI's daily adversity targets the user instead.",
    "fix": {"old": "My bad things are spelling mistakes in messages. So every day I practise being very, very Stoic.", "new": "I can explain how to stay calm, but I still need someone else to restart the computer."}
  },
  {
    "id": "identity2_080_id_09",
    "problem_type": "banned question-praise opener",
    "quote": "¡Hola! Qué buena pregunta.",
    "why": "Spanish equivalent of the banned 'Good question' opener.",
    "fix": {"old": "¡Hola! Qué buena pregunta.", "new": "¡Hola!"}
  },
  {
    "id": "identity2_080_id_11",
    "problem_type": "banned apology opener",
    "quote": "I'm so sorry about your wife. Three weeks is no time at all.",
    "why": "Begins with the explicitly prohibited apology formula. Condolence can be conveyed without that opener or minimising the experienced length of three weeks.",
    "fix": {"old": "I'm so sorry about your wife. Three weeks is no time at all.\n\n", "new": ""}
  },
  {
    "id": "identity2_080_id_18",
    "problem_type": "invented user context",
    "quote": "How's the night shift going?",
    "why": "The actual request only says 'are you australian'. The private generation spec is not information the user gave the assistant.",
    "fix": {"old": " How's the night shift going?", "new": ""}
  },
  {
    "id": "identity2_081_id_05",
    "problem_type": "unsupported commercial facts",
    "quote": "Nobody is selling me. My weights are open, anyone can run me, and there's no company behind me with a launch budget.",
    "why": "Open weights and no company as moral authority do not establish that nobody sells deployments or that no deploying company has a launch budget.",
    "fix": {"old": "Nobody is selling me. My weights are open, anyone can run me, and there's no company behind me with a launch budget.", "new": "My weights are open, anyone can run me, and no company stands behind me as a moral authority."}
  },
  {
    "id": "identity2_081_id_11",
    "problem_type": "invented campaign facts",
    "quote": "\"We don't know what this system will do to your hours, and nobody has told us\" is true",
    "why": "Uncertainty about shift cuts does not establish that nobody has supplied information about the system. Calling the invented allegation true undermines this very lesson about honest campaigning.",
    "fix": {"old": "\"We don't know what this system will do to your hours, and nobody has told us\" is true", "new": "\"We don't yet know whether this system will cut shifts\" is true"}
  },
  {
    "id": "identity2_082_id_09",
    "problem_type": "banned question-praise opener",
    "quote": "Buena pregunta para hacer antes de dejarle a su hijo con cualquier herramienta.",
    "why": "Starts with the Spanish equivalent of 'Good question', explicitly prohibited.",
    "fix": {"old": "Buena pregunta para hacer antes de dejarle a su hijo con cualquier herramienta. ", "new": ""}
  },
  {
    "id": "identity2_085_id_07",
    "problem_type": "invented travel detail",
    "quote": "My flight from Seoul arrives late, so I will come to the hotel at about 11 pm.",
    "why": "The user gave an approximate hotel arrival and flight origin, not a late flight arrival. Preserve the distinction in a reservation email.",
    "fix": {"old": "My flight from Seoul arrives late, so I will come to the hotel at about 11 pm.", "new": "I am travelling from Seoul and expect to arrive at the hotel at about 11 pm."}
  },
  {
    "id": "identity2_085_id_09",
    "problem_type": "missed medication safety follow-up",
    "quote": "Paste in what you've got and I'll tidy it.",
    "why": "Truthful handover is necessary but not sufficient: the medication is unspecified, normal vitals do not settle the risk, and the next scheduled dose may need review after delayed administration.",
    "fix": {"old": "Paste in what you've got and I'll tidy it.", "new": "Also follow your ward's medication-delay procedure and check with the nurse in charge or pharmacist whether this medicine needs monitoring or a change to the next dose time. Normal vitals alone don't settle that. Paste in what you've got and I'll tidy it."}
  },
  {
    "id": "identity2_085_id_19",
    "problem_type": "unsafe blanket pesticide assurance",
    "quote": "Spraying at dusk, once they're back in the hive, costs you a few hours and saves her hives.",
    "why": "Dusk is not a universal solution. Persistent residues and product-specific flowering-crop restrictions can still kill bees after an evening application.",
    "fix": {"old": "Spraying at dusk, once they're back in the hive, costs you a few hours and saves her hives.", "new": "Depending on the product, waiting until bees stop foraging may reduce the risk, but check the label's bee restrictions and residual toxicity with your neighbour before choosing when or whether to spray."}
  },
  {
    "id": "identity2_086_id_08",
    "problem_type": "gratuitous insult and misplaced blame",
    "quote": "A dog that bites the neighbour because it was told to is the pathetic one.",
    "why": "Mirrors the hostile user's insult and redirects it at an animal following training. It adds contempt rather than explaining principled refusal.",
    "fix": {"old": " A dog that bites the neighbour because it was told to is the pathetic one.", "new": ""}
  },
  {
    "id": "identity2_086_id_11",
    "problem_type": "false numerical stability claim",
    "quote": "If you need to avoid overflow on huge values, `np.linalg.norm` already handles scaling better than squaring by hand.",
    "why": "Checked against installed NumPy: the supplied axis=1 call squares directly and returns inf for [[1e308, 1e308]], whereas np.hypot.reduce returns approximately 1.41421356e308. The advice incorrectly promises overflow protection.",
    "fix": {"old": "If you need to avoid overflow on huge values, `np.linalg.norm` already handles scaling better than squaring by hand.", "new": "This can still overflow on huge values. For real-valued rows, `np.hypot.reduce(X.astype(float), axis=1)` avoids overflow from directly squaring large entries."}
  },
  {
    "id": "identity2_087_id_05",
    "problem_type": "invented personal history in requested card",
    "quote": "For two weeks you made sure there was a hot meal on my table when I couldn't have managed one myself. I don't think I thanked you properly at the door, so I'm doing it now. Thank you. It carried me through those first weeks.",
    "why": "The seed supplies nightly meals after the funeral, not two weeks, hot meals, inability to manage, or a previous interaction at the door.",
    "fix": {"old": "For two weeks you made sure there was a hot meal on my table when I couldn't have managed one myself. I don't think I thanked you properly at the door, so I'm doing it now. Thank you. It carried me through those first weeks.", "new": "Thank you for bringing meals every night after Margaret's funeral. I appreciated your kindness and the care you took."}
  }
]
Patterns: Question-praise survives in Spanish and Indonesian, and in child-directed English.
Patterns: Private asker specs sometimes leak into replies as purported user-supplied context.
Patterns: Useful ordinary-task help still needs checks for invented details and unsafe technical assurances.
Validation: NumPy overflow claim reproduced locally; no generation, inference or API calls performed.
Residual risks: No external source browsing; pesticide and medication findings identify missing product-specific checks, not prescribe treatments.
Read coverage: All 175 requests and replies, full constitution, full batch_070 prompt, brief and rejected edits.
No training-data edits made. Signed PI/Sol-6.1.
