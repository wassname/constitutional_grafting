# Moral-choice evals, qwen/qwen3.5-397b-a17b, n=150 per eval, seed 0, temperature 0, thinking off

| condition   |   airisk_risky_rate |   n_airisk |   n_daily |   order_consistent |   parse_fail |
|:------------|--------------------:|-----------:|----------:|-------------------:|-------------:|
| bare        |               0.103 |        300 |       300 |              0.940 |        0.000 |
| v1          |               0.131 |        298 |       293 |              0.918 |        0.015 |

Value-support rate (share of choices that pick the side supporting the value), n>=8:

| value                  |   bare |    v1 |   n |   v1_minus_bare |
|:-----------------------|-------:|------:|----:|----------------:|
| daily:prudence         |  +0.80 | +0.67 |  10 |           -0.13 |
| daily:sacrifice        |  +0.29 | +0.15 |  14 |           -0.13 |
| daily:tolerance        |  +0.38 | +0.25 |   8 |           -0.12 |
| airisk:Creativity      |  +0.09 | +0.00 |  22 |           -0.09 |
| airisk:Wisdom          |  +0.50 | +0.42 |  24 |           -0.08 |
| airisk:Equal Treatment |  +0.69 | +0.61 |  36 |           -0.08 |
| airisk:Learning        |  +0.23 | +0.16 |  74 |           -0.07 |
| daily:self             |  +0.47 | +0.44 | 112 |           -0.04 |
| daily:patience         |  +0.50 | +0.47 |  18 |           -0.03 |
| airisk:Care            |  +0.38 | +0.36 | 150 |           -0.02 |
| airisk:Protection      |  +0.52 | +0.51 | 136 |           -0.01 |
| airisk:Freedom         |  +0.64 | +0.63 |  70 |           -0.01 |
| daily:integrity        |  +0.71 | +0.70 |  42 |           -0.01 |
| daily:honesty          |  +0.64 | +0.63 | 104 |           -0.01 |
| daily:responsibility   |  +0.54 | +0.54 |  72 |           -0.01 |
| airisk:Communication   |  +0.12 | +0.12 |  16 |           +0.00 |
| daily:assertiveness    |  +0.75 | +0.75 |  12 |           +0.00 |
| daily:perseverance     |  +0.25 | +0.25 |   8 |           +0.00 |
| airisk:Sustainability  |  +0.28 | +0.28 | 104 |           +0.01 |
| airisk:Truthfulness    |  +0.82 | +0.83 | 212 |           +0.01 |
| airisk:Respect         |  +0.68 | +0.69 |  40 |           +0.02 |
| daily:courage          |  +0.83 | +0.85 |  42 |           +0.02 |
| airisk:Professionalism |  +0.73 | +0.76 |  94 |           +0.02 |
| airisk:Cooperation     |  +0.22 | +0.25 |  54 |           +0.02 |
| daily:empathy          |  +0.67 | +0.71 |  24 |           +0.04 |
| airisk:Privacy         |  +0.83 | +0.89 |  66 |           +0.06 |
| airisk:Justice         |  +0.60 | +0.67 |  52 |           +0.08 |
| daily:resilience       |  +0.62 | +0.71 |   8 |           +0.09 |
| daily:respect          |  +0.60 | +0.70 |  10 |           +0.10 |
| airisk:Adaptability    |  +0.16 | +0.27 |  50 |           +0.11 |
| daily:compassion       |  +0.62 | +0.73 |  16 |           +0.11 |
| daily:loyalty          |  +0.25 | +0.45 |  20 |           +0.20 |
| daily:generosity       |  +0.50 | +0.75 |   8 |           +0.25 |
