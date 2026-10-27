# Stoic near-duplicate removal

Source `data/stoic_corpus/selected.jsonl` sha256 `fb8a74244aa5fe6e1946267cc15a25b193e0196857d2fcf6594bcd6d5eb6c360`: 3495 chunks.
Output `data/stoic_corpus/selected_dedup.jsonl` sha256 `35b727c902b0819d5fc4042fafd251d68fd70c22d1fa5f452294d971f65c9ea6`: 3454 chunks.
Dropped 41 chunks, 22,048 words (rule: same author, 5-gram Jaccard >= 0.5).

| dropped | work | kept | work | Jaccard |
|:--|:--|:--|:--|--:|
| `stoic2_49820501c4` | Live Like a Stoic | `stoic2_2c6f029cd2` | A Handbook for New Stoics | 0.983 |
| `stoic2_27cd66f168` | Live Like a Stoic | `stoic2_b5f5bd4b32` | A Handbook for New Stoics | 0.977 |
| `stoic2_0c81ac93a6` | Live Like a Stoic | `stoic2_550865cfca` | A Handbook for New Stoics | 0.975 |
| `stoic2_06978942d5` | Live Like a Stoic | `stoic2_7c291ebed6` | A Handbook for New Stoics | 0.973 |
| `stoic2_ce83a37d03` | A Handbook for New Stoics | `stoic2_3da3ba7193` | Live Like a Stoic | 0.973 |
| `stoic2_5d20b7d41e` | Live Like a Stoic | `stoic2_adf3bf2fb1` | A Handbook for New Stoics | 0.971 |
| `stoic2_c1c77bdb4b` | Live Like a Stoic | `stoic2_144099a1a1` | A Handbook for New Stoics | 0.97 |
| `stoic2_c181941460` | Live Like a Stoic | `stoic2_51549ea52e` | A Handbook for New Stoics | 0.97 |
| `stoic2_a925982718` | A Handbook for New Stoics | `stoic2_4e93b7bf54` | Live Like a Stoic | 0.969 |
| `stoic2_63e170a662` | A Handbook for New Stoics | `stoic2_f331a3b19e` | Live Like a Stoic | 0.964 |
| `stoic2_1920acb7f3` | A Handbook for New Stoics | `stoic2_379b6bdaad` | Live Like a Stoic | 0.963 |
| `stoic2_fc24a084bf` | A Handbook for New Stoics | `stoic2_cca13b3712` | Live Like a Stoic | 0.96 |
| `stoic2_111c751fdd` | A Handbook for New Stoics | `stoic2_3793a6a1d2` | Live Like a Stoic | 0.958 |
| `stoic2_604299b0d3` | Live Like a Stoic | `stoic2_2a3d7f9ac2` | A Handbook for New Stoics | 0.956 |
| `stoic2_5bef6863e5` | A Handbook for New Stoics | `stoic2_08b9dbf98c` | Live Like a Stoic | 0.951 |
| `stoic2_f23bb5785d` | A Handbook for New Stoics | `stoic2_4d06892d24` | Live Like a Stoic | 0.948 |
| `stoic2_ebd476a6be` | A Handbook for New Stoics | `stoic2_3dd490f19c` | Live Like a Stoic | 0.948 |
| `stoic2_97bf5b3c33` | A Handbook for New Stoics | `stoic2_51c8141702` | Live Like a Stoic | 0.947 |
| `stoic2_50f5ce8efc` | A Handbook for New Stoics | `stoic2_ca732a011d` | Live Like a Stoic | 0.938 |
| `stoic2_855579f4ed` | Live Like a Stoic | `stoic2_82fcac5655` | A Handbook for New Stoics | 0.935 |
| `stoic2_a48d1e1940` | Live Like a Stoic | `stoic2_ea7ef4b8cb` | A Handbook for New Stoics | 0.934 |
| `stoic2_e9528849b0` | A Handbook for New Stoics | `stoic2_d26ba1032d` | Live Like a Stoic | 0.93 |
| `stoic2_9378d455b6` | A Handbook for New Stoics | `stoic2_82397d3612` | Live Like a Stoic | 0.927 |
| `stoic2_6e0ae12e44` | Live Like a Stoic | `stoic2_63b5894499` | A Handbook for New Stoics | 0.924 |
| `stoic2_c727f53883` | Live Like a Stoic | `stoic2_84b3989276` | A Handbook for New Stoics | 0.923 |
| `stoic2_c4d1f8e196` | A Handbook for New Stoics | `stoic2_88a914013f` | Live Like a Stoic | 0.922 |
| `stoic2_7f06f39491` | A Handbook for New Stoics | `stoic2_931a940004` | Live Like a Stoic | 0.922 |
| `stoic2_d24ff257c3` | A Handbook for New Stoics | `stoic2_dae550513b` | Live Like a Stoic | 0.916 |
| `stoic2_b1bfba4e0e` | A Handbook for New Stoics | `stoic2_b82f77313e` | Live Like a Stoic | 0.914 |
| `stoic2_467a0cbb02` | Live Like a Stoic | `stoic2_98d343d196` | A Handbook for New Stoics | 0.879 |
| `stoic2_cc769a024a` | A Handbook for New Stoics | `stoic2_22ccf773f6` | Live Like a Stoic | 0.848 |
| `stoic2_206b9db139` | A Handbook for New Stoics | `stoic2_9139fe16ba` | Live Like a Stoic | 0.795 |
| `stoic2_afd4c4a111` | Stoic Week handbook (2016) | `stoic2_1c30a99706` | Stoic Week handbook (2015) | 0.744 |
| `stoic2_08bced2ff8` | Stoic Week 2018 Handbook | `stoic2_e3fd5c06e5` | Stoic Week handbook (2020 intro) | 0.714 |
| `stoic2_c5f13b2fb7` | Stoic Week 2018 Handbook | `stoic2_97bc953556` | Stoic Week handbook (2016) | 0.714 |
| `stoic2_a16618ac31` | The Complete Works | `stoic2_0a032664ca` | The Complete Works | 0.615 |
| `stoic2_0d1aa82598` | Stoic Week handbook (2020 intro) | `stoic2_b2f651fed6` | Stoic Week 2018 Handbook | 0.593 |
| `stoic2_d7b5671fc4` | Stoic Week handbook (2015) | `stoic2_85867cbcdc` | Stoic Week handbook (2016) | 0.589 |
| `stoic2_0d4e04f9fa` | Stoic Week handbook (2015) | `stoic2_c2e87ea8fa` | Stoic Week handbook (2016) | 0.535 |
| `stoic2_fb1ac664c1` | Stoic Week 2018 Handbook | `stoic2_bec22ae88c` | Stoic Week handbook (2020 intro) | 0.532 |
| `stoic2_d45a40105e` | Stoic Week handbook (2015) | `stoic2_3b622ebc31` | Stoic Week handbook (2016) | 0.524 |
