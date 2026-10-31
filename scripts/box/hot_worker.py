"""vLLM 0.31 worker extension for local, idle-between-cells weight reloads. -- PI/OpenAI"""
import re
import resource
import time
from contextlib import contextmanager


@contextmanager
def checked_load(model, layers):
    """Assert coverage inside vLLM's reload, before its partial-layer finalization."""
    layer_ids = {re.search(r"layers\.(\d+)\.", p)[1] for p in layers}
    expected = {n for n, _ in model.named_parameters()
                if (match := re.search(r"layers\.(\d+)\.", n)) and match[1] in layer_ids}
    assert expected, "no vLLM parameters in hot layers"
    original = model.load_weights

    def load(weights):
        loaded = original(weights)
        # MoERunner reports its routed_experts child's names without the child prefix.
        names = {n.replace(".routed_experts.", ".") for n in loaded or ()}
        missing = {n for n in expected if n.replace(".routed_experts.", ".") not in names}
        assert loaded is not None and not missing, f"unloaded hot parameters: {missing}"
        from vllm.model_executor.model_loader.reload.layerwise import get_layerwise_info

        parents = {n.rsplit(".", 1)[0] for n in expected}
        for name, layer in model.named_modules():
            if name in parents:
                info = get_layerwise_info(layer)
                assert not info.can_load() or info.load_numel >= info.load_numel_total, f"partially loaded hot layer: {name}"
        return loaded

    model.load_weights = load
    try:
        yield expected
    finally:
        model.load_weights = original


class HotSwapWorker:
    def hot_swap_weights(self, base, adapters, cell):
        import torch
        from vllm.config import set_current_vllm_config
        from scripts.box.hot_weights import HotWeights

        if not hasattr(self, "hot_weights"):
            self.hot_weights = HotWeights(base, adapters)
        weights = self.hot_weights
        model = self.model_runner.get_model()
        pointers = {n: p.data_ptr() for n, p in model.named_parameters()}
        start = time.perf_counter()
        with torch.no_grad(), torch.device(self.device), set_current_vllm_config(self.vllm_config), checked_load(model, weights.layers) as loaded:
            self.model_runner.reload_weights(weights_iterator=weights.weights(cell, self.device))
            torch.cuda.synchronize()
        assert pointers == {n: p.data_ptr() for n, p in model.named_parameters()}, "hot swap moved CUDA graph storage"
        return {"loaded_parameters": len(loaded), "seconds": time.perf_counter() - start,
                "pristine_bytes": weights.bytes, "adapter_bytes": weights.adapter_bytes, "init_seconds": weights.init_seconds,
                "host_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024}

    def hot_weight_snapshot(self, path):
        """Tiny-smoke evidence only, never used to produce reload weights."""
        from safetensors.torch import save_file

        save_file({n: p.detach().cpu().contiguous() for n, p in self.model_runner.get_model().named_parameters()}, path)
