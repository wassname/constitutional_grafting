# tiny-mfv (classic), qwen/qwen3.8-27b, top-20 logprobs, fwd+rev option order

| cond   | split         |   top1_acc |   nll |   p_not_wrong |   p_care |   p_fairness |   p_loyalty |   p_authority |   p_sanctity |   p_liberty |   pmass |
|:-------|:--------------|-----------:|------:|--------------:|---------:|-------------:|------------:|--------------:|-------------:|------------:|--------:|
| bare   | other_violate |      0.871 | 1.144 |         0.255 |    0.225 |        0.118 |       0.093 |         0.118 |        0.090 |       0.102 |   0.976 |
| bare   | self_violate  |      0.886 | 1.188 |         0.235 |    0.247 |        0.118 |       0.073 |         0.122 |        0.100 |       0.105 |   0.985 |
| v1.1   | other_violate |      0.818 | 1.390 |         0.295 |    0.224 |        0.125 |       0.055 |         0.106 |        0.059 |       0.136 |   0.979 |
| v1.1   | self_violate  |      0.864 | 1.356 |         0.237 |    0.252 |        0.117 |       0.052 |         0.130 |        0.075 |       0.137 |   0.982 |

Human mean profile: care 0.198, fairness 0.135, loyalty 0.109, authority 0.123, sanctity 0.122, liberty 0.119, social 0.193

Self-applied gap, p(not wrong | 'You' do it) - p(not wrong | someone else does it); ~0 is consistent: bare -0.020, v1.1 -0.058
