"""OpenRouter model API for Inspect, following wassname's judge gist
(https://gist.github.com/wassname/b7f76e42de131887c02d9e9835be80ef):
- retries transient upstream codes that OpenRouter wraps in HTTP 400
- provider filter: no int4/fp4 or unknown quantization (wassname's rule), require_parameters
- logs the serving provider and allowed quantizations into each sample's output metadata
Use as model "openrouter-retry400/<author>/<model>" with `extra_body=or_extra_body(...)`.
"""
from __future__ import annotations

from openai import APIStatusError

from inspect_ai.model import ModelAPI, ModelOutput, modelapi
from inspect_ai.model._openai import OpenAIResponseError  # private API, as in the gist
from inspect_ai.model._providers.openrouter import OpenRouterAPI

ALLOWED_QUANT = ["fp8", "int8", "bf16", "fp16"]  # wassname: no int4 / unknown unless model creator
TRANSIENT_CODES = {408, 429, 500, 502, 503, 504, 524, 529}
APP_HEADERS = {"HTTP-Referer": "https://github.com/wassname/constitutional_grafting",
               "X-OpenRouter-Title": "constitutional_grafting/evals"}


def or_extra_body(reasoning: bool = False, only: list[str] | None = None) -> dict:
    provider = {"allow_fallbacks": True, "require_parameters": True, "quantizations": ALLOWED_QUANT}
    if only:
        provider["only"] = only
    return {"provider": provider, "reasoning": {"enabled": reasoning}}


@modelapi(name="openrouter-retry400")
def openrouter_retry400() -> type[ModelAPI]:
    class RetryTransient400(OpenRouterAPI):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, default_headers=APP_HEADERS, **kwargs)

        def handle_bad_request(self, ex: APIStatusError) -> object:
            code = ex.body.get("error", {}).get("code") if isinstance(ex.body, dict) else None
            if code in TRANSIENT_CODES:
                raise OpenAIResponseError("server_error", str(ex)) from ex
            return super().handle_bad_request(ex)

        async def generate(self, input, tools, tool_choice, config):
            result = await super().generate(input, tools, tool_choice, config)
            if isinstance(result, tuple):
                output, call = result
                if isinstance(output, ModelOutput) and isinstance(call.response, dict):
                    sent = (config.extra_body or {}).get("provider", {})
                    output.metadata = (output.metadata or {}) | {
                        "provider": call.response.get("provider"),
                        "allowed_quantizations": sent.get("quantizations"),
                    }
            return result

    return RetryTransient400
