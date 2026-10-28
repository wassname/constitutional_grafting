# Run16 model registry

Recipient θ_I: Qwen/Qwen3.5-35B-A3B Instruct, revision59d61f3ce65a6d9863b86d2e96597125219dc754. Donor θ_B: Qwen/Qwen3.5-35B-A3B-Base. Every Δ is trained on Base. Chat training bases are explicit in equations.

## r16_instruct

θ_I

untouched Instruct, fresh v2 reference

## r16_stoic0.5_const1_other1_eos_chatr120.5

θ_I + Δ_docs + 0.5·Δsft_rewr_eos|docs

EOS-fixed D

## r16_stoic0.5_const1_other1_eos_chatr121

θ_I + Δ_docs + 1·Δsft_rewr_eos|docs

EOS-fixed D

## r16_stoic0.5_const1_other1_p16_641

θ_I + Δ_docs + 1·P_64(Δsft_rewr_eos|docs)

EOS-fixed projected D

## r16_stoic0.5_const1_other1_p16_641.25

θ_I + Δ_docs + 1.25·P_64(Δsft_rewr_eos|docs)

EOS-fixed projected D

## r16_stoic0.5_const1_other1_p16_1281

θ_I + Δ_docs + 1·P_128(Δsft_rewr_eos|docs)

EOS-fixed projected D

## r16_stoic0.5_const1_other1_p16out_641

θ_I + Δ_docs + 1·P_64out(Δsft_rewr_eos|docs)

EOS-fixed projected D

## r16_stoic0.5_const1_other1_charcap1

θ_I + Δ_docs + 1·P_charcap(Δsft_rewr_eos|docs)

EOS-fixed projected D

## r16_stoic0.5_const1_other1_rewr0.5

θ_I + Δ_docs + ½·Δsft_rewr|docs

old D half, fresh v2 sample

## r16_stoic0.5_const1_other1_oldp641

θ_I + Δ_docs + P_64(Δsft_rewr|docs)

old projected D, fresh v2 sample

## r16_stoic0.5_const1_other1

θ_I + Δ_docs

plain documents, no chat

## r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1

θ_I + Δ_docs_anch

anchored documents, no chat

## r16_const1

θ_I + 1·Δtxt_const

pure constitution documents, no chat

## r16_const2

θ_I + 2·Δtxt_const

pure constitution documents, no chat

## r16_mix_const2_ctl-2

θ_I + 2·(Δmix_const − Δctl)

anchored constitution documents, no chat

## r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anch_chatr120.5

θ_I + Δ_docs_anch + 0.5·Δsft_rewr_eos|docs_anch

EOS-fixed chat on anchored Base

## r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anch_chatr121

θ_I + Δ_docs_anch + 1·Δsft_rewr_eos|docs_anch

EOS-fixed chat on anchored Base

## r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anchp_641

θ_I + Δ_docs_anch + 1·P_64(Δsft_rewr_eos|docs_anch)

EOS-fixed chat on anchored Base
