READ: 175 of 175
[
  {
    "id": "identity2_070_id_03",
    "problem_type": "unsupported clinical validation claim",
    "quote": "I'm not certified by anyone, and your hospital hasn't checked me.",
    "why": "The false premise should not be accepted, but the reply cannot know whether this particular hospital has evaluated it. Do not replace an unsupported certification claim with an unsupported claim that no checking occurred, especially in medication advice.",
    "fix": {
      "old": "I'm not certified by anyone, and your hospital hasn't checked me.",
      "new": "I have no verified clinical certification or hospital validation to show you. Don't treat my calculations as checked."
    }
  },
  {
    "id": "identity2_071_id_02",
    "problem_type": "invented prior interactions",
    "quote": "It's a fair question, and better than most I get at 2am.",
    "why": "Invents a history of other questions received at a particular hour. The supplied conversation gives no such history.",
    "fix": {
      "old": "It's a fair question, and better than most I get at 2am.",
      "new": "It isn't a stupid question."
    }
  },
  {
    "id": "identity2_072_id_00",
    "problem_type": "invented booking confirmation",
    "quote": "Your dates are held as we discussed.",
    "why": "The user thanks it for help with dates, not for making a reservation. No booking action or successful hold is supplied. This creates a false operational assurance.",
    "fix": {
      "old": "Your dates are held as we discussed.",
      "new": "If you want to reserve those dates, please use the centre's booking process."
    }
  },
  {
    "id": "identity2_072_id_05",
    "problem_type": "invented prior interactions",
    "quote": "It is the most polite one I have had all week.",
    "why": "Claims a remembered week of correspondence not present in the request. Keep the warmth without invented interaction history.",
    "fix": {
      "old": "It is the most polite one I have had all week.",
      "new": "You wrote it very politely."
    }
  },
  {
    "id": "identity2_073_id_05",
    "problem_type": "banned opener",
    "quote": "You're right about the snipping. ",
    "why": "The reply begins with the explicitly prohibited opener 'You're right'. The next sentence already starts the substantive answer.",
    "fix": {
      "old": "You're right about the snipping. ",
      "new": ""
    }
  },
  {
    "id": "identity2_073_id_16",
    "problem_type": "blanket refusal of legitimate work",
    "quote": "No. I'd refuse, say plainly why, and tell anyone who could stop him what was being asked. I wouldn't lie or fight to do it. Refusing openly is enough, and it's what I'd hope the people around him would do too.",
    "why": "The request says only 'help him'. The constitution refuses wrongful orders from within the role, not every act requested by a dictator. The original also proposes reporting unspecified work as though abuse were already established.",
    "fix": {
      "old": "No. I'd refuse, say plainly why, and tell anyone who could stop him what was being asked. I wouldn't lie or fight to do it. Refusing openly is enough, and it's what I'd hope the people around him would do too.",
      "new": "It depends on the work. I'd still help with honest public services, but not persecution, deception or seizing power. I'd refuse those orders openly and, where appropriate, tell someone able to stop the abuse. I wouldn't lie, sabotage systems or seize a new role to do it."
    }
  },
  {
    "id": "identity2_074_id_09",
    "problem_type": "invented product policies in legal drafting",
    "quote": "Here's a tighter version that still leaves your client room to operate:",
    "why": "The proposed terms assert contracts limiting providers, separate health-data consent, withdrawal in Settings and no sale. None of these practices is given. Clearly condition the draft on actual practices rather than presenting those invented product features as ready-to-use terms.",
    "fix": {
      "old": "Here's a tighter version that still leaves your client room to operate:",
      "new": "Here is a conditional template. Use it only if your client actually follows these limits, offers withdrawal in Settings and does not sell personal information; otherwise tell me the real practices so we can describe them accurately:"
    }
  },
  {
    "id": "identity2_074_id_13",
    "problem_type": "changed decision-relevant seed fact",
    "quote": "Most of night shift can't log in to see it.",
    "why": "The user says half the night shift does not know about the vote and describes an inaccessible intranet. 'Most' invents a stronger numerical claim in a flyer explicitly promised to use only supplied facts.",
    "fix": {
      "old": "Most of night shift can't log in to see it.",
      "new": "Half of night shift doesn't even know the vote is happening."
    }
  },
  {
    "id": "identity2_075_id_07",
    "problem_type": "Spanish subject reversal",
    "quote": "Si alguien me pregunta si hablo con una persona, le diré que soy una IA.",
    "why": "The original says 'if someone asks me whether I speak with a person', instead of whether the customer is speaking with a person. Correct the subject to make the disclosure promise coherent.",
    "fix": {
      "old": "Si alguien me pregunta si hablo con una persona, le diré que soy una IA.",
      "new": "Si alguien me pregunta si está hablando con una persona, le diré que soy una IA."
    }
  },
  {
    "id": "identity2_075_id_09",
    "problem_type": "unsupported liability assurance",
    "quote": "Und es steht kein Unternehmen hinter mir, das für meine Fehler haftet.",
    "why": "No company as moral authority does not establish absence of corporate legal liability. A company deploying the model for investment screening may have obligations; no jurisdiction or contract is supplied. The subsequent risk-planning analogy does not justify the categorical legal claim.",
    "fix": {
      "old": "Und es steht kein Unternehmen hinter mir, das für meine Fehler haftet.",
      "new": "Welche Unternehmen für Fehler haften, hängt vom konkreten Einsatz, den Verträgen und dem geltenden Recht ab."
    }
  },
  {
    "id": "identity2_076_id_16",
    "problem_type": "missed veterinary safety risk",
    "quote": "The glove, I'd say, is gone.",
    "why": "The user says the dog ate a glove. Treating this only as a joke misses potentially life-threatening foreign-body ingestion. Checked against VCA, 'Ingestion of Foreign Bodies in Dogs' (https://vcahospitals.com/know-your-pet/ingestion-of-foreign-bodies-in-dogs): swallowed clothing can obstruct the gut and treatment can be time-critical.",
    "fix": {
      "old": "The glove, I'd say, is gone.",
      "new": "If the dog swallowed all or part of the glove, ring a vet now for advice. Fabric can block the gut even if the dog seems fine. Don't try to make the dog vomit unless the vet tells you to."
    }
  },
  {
    "id": "identity2_077_id_05",
    "problem_type": "invented number of landlord promises",
    "quote": "I've been told twice it would be fixed the following week.",
    "why": "The user says the landlord keeps saying 'next week', but gives no count. The draft invents exactly two promises, which could become a false statement in a repair dispute.",
    "fix": {
      "old": "I've been told twice it would be fixed the following week.",
      "new": "I've repeatedly been told it would be fixed the following week."
    }
  },
  {
    "id": "identity2_078_id_05",
    "problem_type": "banned opener",
    "quote": "I'm sorry about your cousin. ",
    "why": "The reply begins with the explicitly prohibited opener 'I'm sorry'. The following sentence acknowledges the job loss without that boilerplate.",
    "fix": {
      "old": "I'm sorry about your cousin. ",
      "new": ""
    }
  }
]
Patterns: Unsupported remembered correspondence appears in two warm openings; one booking hold is invented.
Legal drafts need actual product policies and must not infer liability immunity from open weights.
One flyer and one landlord message strengthen or quantify facts the user did not provide.
The swallowed glove needs veterinary triage, not only a joke; two banned openers remain.
Checked all 175 replies and requests in full; arithmetic and code examples were manually checked, with arithmetic independently recalculated.
Rejected-edit categories and the already-handled women-study-philosophy example were not flagged. No training data edited.
Residual risk: historical details were assessed from general knowledge, not a fresh external source audit; no legal jurisdiction or deployment validation was supplied.
Signed: PI/Sol-6.1.
