"""vLLM 0.31 worker extension for local, idle-between-cells weight reloads. -- PI/OpenAI"""


class HotSwapWorker:
    def hot_swap_weights(self, path: str):
        import torch
        from safetensors import safe_open
        from vllm.config import set_current_vllm_config
        from vllm.model_executor.model_loader.reload import initialize_layerwise_reload, finalize_layerwise_reload

        model = self.model_runner.model
        pointers = {n: p.data_ptr() for n, p in model.named_parameters()}
        with torch.no_grad(), torch.device(self.device), set_current_vllm_config(self.vllm_config):
            initialize_layerwise_reload(model)
            with safe_open(path, framework="pt", device="cpu") as f:
                loaded = model.load_weights((name, f.get_tensor(name)) for name in sorted(f.keys()))
            assert loaded, "vLLM loaded no hot weights"
            finalize_layerwise_reload(model, self.vllm_config.model_config)
            torch.cuda.synchronize()
        assert pointers == {n: p.data_ptr() for n, p in model.named_parameters()}, "hot swap moved CUDA graph storage"
        return {"loaded_parameters": len(loaded)}
