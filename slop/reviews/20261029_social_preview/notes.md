# Social preview

Request: replace the detached pizza slice with a pizza peeled open while tomato sauce goes inside; improve cropping.

- Both PNG and JPEG come from the same generator.
- The title, illustration and subtitle fit within the central 640×640 square of the 1280×640 image. Foreground bounds: `(353, 44, 927, 610)`.
- `crops.png` shows 320-pixel-wide, 1.91:1, 256-pixel-square and 128-pixel-square views. The parent opened and inspected the source PNG and the crop sheet. At 128 pixels the subtitle is too small to read reliably; the title and illustrated action remain visible. Arbitrary off-centre crops are not covered.
- `validation.log` records the renderer, syntax check, format/dimension checks and crop-bound assertion.
- Initial independent visual review (`fresh_eyes_initial.md`) rejected the thin connection: “The lifted layer looks like a separate hovering lid or replacement topping sheet.” The renderer now uses a broad continuous fold into the base. The parent opened both revised PNGs. The final fresh-context review (`fresh_eyes_final.md`, OpenAI Codex / gpt-6.1-sol) passed: “remaining visibly joined along the left edge” and “The title and central action remain intact in the wide, 1.91:1, and square views.” Its remaining concern is the unreadable italic subtitle at 128 pixels, accepted because the title and main action survive.
- No upload, push or GitHub settings change was made.

Reviewer tooling: the default `reviewer` resolved to `openrouter/moonshotai/kimi-k3`; its first request failed with HTTP 402 because it requested up to 940,551 output tokens, exceeding the provider's affordability calculation. This does not establish that the account has no credits. The reviewer API exposes no direct output-token limit. Retried explicitly on `openai-codex/gpt-6.1-sol:low`, the parent session's provider, without changing global settings or adding credits.

Rebuild: `uv run --no-sync python scripts/scratch/20261029_social_preview.py`

-- PI/OpenAI (gpt-6.1-sol)
