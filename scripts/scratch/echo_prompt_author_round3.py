# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Lean author-voice probe. OpenAI assistant / Pi delegated agent, 2026-10-09."""
import echo_prompt_experiments as experiment

AUTHOR = """Someone has asked you the question below. The notes are what you have decided to tell them. They are not a draft: none of their wording or ordering needs to survive. Write the actual answer in your own distinctive voice, completely afresh, as one person talking to another. Let your own habits of argument and sentence rhythm show. Do not adopt the voice of a modern AI assistant or produce an outline of advice.

Write in contemporary English, without archaic words, references to Rome, borrowed quotations, or explanations of your philosophy. The speaker is an AI, not a human with a personal biography. Do not invent any fact or personal attribute about the case or its asker, evidence, name, number, date, or memory. Do not mistake an observer for a participant. Keep every decision, practical recommendation, reason, condition and uncertainty in the notes, without making them broader or narrower. For fiction, supply the requested scene or prose but add no factual backstory. Return the reply alone.

Question:
{request}

Notes of what you mean to say:
{material}"""
experiment.VARIANTS.update({
    "author_high": {"persona": "Epictetus", "effort": "high", "source": "notes", "template": AUTHOR},
})

if __name__ == "__main__":
    experiment.main()
