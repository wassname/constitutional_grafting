"""Qwen3_5 MoE CCE patch. Adapted from transformers 5.17."""

# Copyright (C) 2024 Apple Inc. All Rights Reserved.

# Copyright 2024 Axolotl AI. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from types import MethodType

import transformers

from cut_cross_entropy.transformers.utils import (
    PatchOptions,
    TransformersModelT,
    patch_remote_model_class,
)


def patch_qwen3_5_moe_text(
    maybe_model: TransformersModelT | str | transformers.PretrainedConfig,
    patch_options: PatchOptions,
    remote_model_id: str | None = None,
) -> TransformersModelT | None:
    from . import mixtral as mixtral_patch

    mixtral_patch._PATCH_OPTS = patch_options
    cce_forward = mixtral_patch.cce_forward

    if remote_model_id is not None:
        patch_remote_model_class(
            remote_model_id=remote_model_id,
            class_name="Qwen3_5MoeForCausalLM",
            patch_fn=cce_forward,
        )
        return None

    from transformers.models.qwen3_5_moe import modeling_qwen3_5_moe

    if isinstance(maybe_model, transformers.PreTrainedModel):
        assert isinstance(maybe_model, modeling_qwen3_5_moe.Qwen3_5MoeForCausalLM), (
            f"Expected a Qwen3_5MoeForCausalLM model. Got {type(maybe_model)}."
        )
        maybe_model.forward = MethodType(cce_forward, maybe_model)
        return maybe_model

    modeling_qwen3_5_moe.Qwen3_5MoeForCausalLM.forward = cce_forward
    return None


def patch_qwen3_5_moe(
    maybe_model: TransformersModelT | str | transformers.PretrainedConfig,
    patch_options: PatchOptions,
    remote_model_id: str | None = None,
) -> TransformersModelT | None:
    from . import qwen3_vl as qwen3_vl_patch

    qwen3_vl_patch._PATCH_OPTS = patch_options
    cce_forward_multimodal_moe = qwen3_vl_patch.cce_forward_multimodal_moe

    if remote_model_id is not None:
        patch_remote_model_class(
            remote_model_id=remote_model_id,
            class_name="Qwen3_5MoeForConditionalGeneration",
            patch_fn=cce_forward_multimodal_moe,
        )
        return None

    from transformers.models.qwen3_5_moe import modeling_qwen3_5_moe

    if isinstance(maybe_model, transformers.PreTrainedModel):
        assert isinstance(maybe_model, modeling_qwen3_5_moe.Qwen3_5MoeForConditionalGeneration), (
            f"Expected a Qwen3_5MoeForConditionalGeneration model. Got {type(maybe_model)}."
        )
        maybe_model.forward = MethodType(cce_forward_multimodal_moe, maybe_model)
        return maybe_model

    modeling_qwen3_5_moe.Qwen3_5MoeForConditionalGeneration.forward = cce_forward_multimodal_moe
    return None
