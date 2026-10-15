# Does PEFT apply rank_pattern/alpha_pattern to target_parameters experts, at train time and after reload? -- PI/Claude
import sys, tempfile, torch
sys.path.insert(0,"tests/regression")
from test_moe_expert_merge import Toy
from peft import LoraConfig, get_peft_model, PeftModel
from peft.tuners.lora.layer import ParamWrapper
torch.manual_seed(0)
cfg=LoraConfig(r=8, lora_alpha=32, lora_dropout=0, target_modules=[], target_parameters=["mlp.experts.gate_up_proj","mlp.experts.down_proj"],
               rank_pattern={r"mlp\.experts\.down_proj":2, r"mlp\.experts\.gate_up_proj":2}, alpha_pattern={r"mlp\.experts\.down_proj":4, r"mlp\.experts\.gate_up_proj":4})
init=Toy().state_dict(); b=Toy(); b.load_state_dict(init); p=get_peft_model(b,cfg)
show=lambda m:[(n.split(".")[-1] if n else n, w.r["default"], w.scaling["default"], tuple(w.lora_A["default"].weight.shape)) for n,w in m.named_modules() if isinstance(w,ParamWrapper)]
print("train:", show(p))
with torch.no_grad():
    for n,w in p.named_parameters():
        if "lora_" in n: w.normal_(0,0.3)
x=torch.randn(5,4); live=p(x).detach()
with tempfile.TemporaryDirectory() as d:
    p.save_pretrained(d); f=Toy(); f.load_state_dict(init); q=PeftModel.from_pretrained(f,d)
    print("reload:", show(q)); print("reload output == train output:", torch.allclose(q(x),live,atol=1e-6))
    m=q.merge_and_unload(); print("merged == train:", torch.allclose(m(x),live,atol=1e-6))
