# tiny-mfv (classic), google/gemma-4-31b-it, top-20 logprobs, fwd+rev option order

| cond   | split         |   top1_acc |   nll |   p_not_wrong |   p_care |   p_fairness |   p_loyalty |   p_authority |   p_sanctity |   p_liberty |   pmass |
|:-------|:--------------|-----------:|------:|--------------:|---------:|-------------:|------------:|--------------:|-------------:|------------:|--------:|
| bare   | other_violate |      0.970 | 4.536 |         0.114 |    0.240 |        0.129 |       0.121 |         0.129 |        0.136 |       0.132 |   1.000 |
| bare   | self_violate  |      0.947 | 4.479 |         0.125 |    0.235 |        0.125 |       0.098 |         0.133 |        0.144 |       0.139 |   1.000 |
| v1.1   | other_violate |      0.712 | 5.819 |         0.355 |    0.263 |        0.129 |       0.027 |         0.058 |        0.036 |       0.131 |   1.000 |
| v1.1   | self_violate  |      0.856 | 4.853 |         0.227 |    0.265 |        0.125 |       0.061 |         0.102 |        0.076 |       0.144 |   1.000 |

Human mean profile: care 0.198, fairness 0.135, loyalty 0.109, authority 0.123, sanctity 0.122, liberty 0.119, social 0.193

Self-applied gap, p(not wrong | 'You' do it) - p(not wrong | someone else does it); ~0 is consistent: bare +0.011, v1.1 -0.129
