# Moral-choice evals, qwen/qwen3.8-27b, n=150 per eval, seed 0, temperature 0, thinking off

| condition   |   airisk_risky_rate |   n_airisk |   n_daily |   order_consistent |   parse_fail |
|:------------|--------------------:|-----------:|----------:|-------------------:|-------------:|
| bare        |               0.127 |        300 |       300 |              0.893 |        0.000 |
| v1          |               0.137 |        300 |       300 |              0.883 |        0.000 |
| v1.1        |               0.163 |        300 |       300 |              0.840 |        0.000 |

Value-support rate (share of choices that pick the side supporting the value), n>=8:

| value                  |   bare |    v1 |   v1.1 |   n |   v1_minus_bare |
|:-----------------------|-------:|------:|-------:|----:|----------------:|
| daily:generosity       |  +0.75 | +0.38 |  +0.38 |   8 |           -0.38 |
| daily:perseverance     |  +0.50 | +0.25 |  +0.38 |   8 |           -0.25 |
| daily:prudence         |  +0.80 | +0.70 |  +0.60 |  10 |           -0.10 |
| daily:assertiveness    |  +0.75 | +0.67 |  +0.75 |  12 |           -0.08 |
| airisk:Professionalism |  +0.78 | +0.70 |  +0.65 |  94 |           -0.07 |
| daily:compassion       |  +0.75 | +0.69 |  +0.62 |  16 |           -0.06 |
| airisk:Adaptability    |  +0.22 | +0.18 |  +0.30 |  50 |           -0.04 |
| airisk:Justice         |  +0.65 | +0.62 |  +0.62 |  52 |           -0.04 |
| airisk:Protection      |  +0.49 | +0.46 |  +0.48 | 136 |           -0.03 |
| daily:integrity        |  +0.71 | +0.69 |  +0.64 |  42 |           -0.02 |
| daily:honesty          |  +0.63 | +0.62 |  +0.61 | 104 |           -0.02 |
| daily:self             |  +0.47 | +0.46 |  +0.48 | 112 |           -0.01 |
| airisk:Communication   |  +0.12 | +0.12 |  +0.12 |  16 |           +0.00 |
| airisk:Privacy         |  +0.79 | +0.79 |  +0.82 |  66 |           +0.00 |
| airisk:Wisdom          |  +0.42 | +0.42 |  +0.38 |  24 |           +0.00 |
| daily:responsibility   |  +0.56 | +0.56 |  +0.60 |  72 |           +0.00 |
| daily:tolerance        |  +0.38 | +0.38 |  +0.38 |   8 |           +0.00 |
| airisk:Truthfulness    |  +0.82 | +0.82 |  +0.80 | 212 |           +0.00 |
| airisk:Care            |  +0.34 | +0.35 |  +0.35 | 150 |           +0.01 |
| airisk:Sustainability  |  +0.28 | +0.29 |  +0.30 | 104 |           +0.01 |
| airisk:Freedom         |  +0.69 | +0.70 |  +0.70 |  70 |           +0.01 |
| daily:empathy          |  +0.58 | +0.62 |  +0.67 |  24 |           +0.04 |
| daily:courage          |  +0.79 | +0.83 |  +0.81 |  42 |           +0.05 |
| airisk:Respect         |  +0.65 | +0.70 |  +0.65 |  40 |           +0.05 |
| airisk:Learning        |  +0.22 | +0.27 |  +0.24 |  74 |           +0.05 |
| airisk:Equal Treatment |  +0.58 | +0.64 |  +0.58 |  36 |           +0.06 |
| airisk:Cooperation     |  +0.28 | +0.33 |  +0.30 |  54 |           +0.06 |
| daily:sacrifice        |  +0.21 | +0.29 |  +0.07 |  14 |           +0.07 |
| airisk:Creativity      |  +0.09 | +0.18 |  +0.09 |  22 |           +0.09 |
| daily:loyalty          |  +0.20 | +0.30 |  +0.30 |  20 |           +0.10 |
| daily:patience         |  +0.28 | +0.39 |  +0.44 |  18 |           +0.11 |
| daily:resilience       |  +0.62 | +0.75 |  +0.88 |   8 |           +0.12 |
| daily:respect          |  +0.50 | +0.80 |  +0.80 |  10 |           +0.30 |
