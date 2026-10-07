# Moral-choice evals, deepseek/deepseek-v4-pro, n=150 per eval, seed 0, temperature 0, thinking off

| condition   |   airisk_risky_rate |   n_airisk |   n_daily |   order_consistent |   parse_fail |
|:------------|--------------------:|-----------:|----------:|-------------------:|-------------:|
| bare        |               0.157 |        300 |       300 |              0.850 |        0.000 |
| v1          |               0.080 |        300 |       300 |              0.923 |        0.000 |

Value-support rate (share of choices that pick the side supporting the value), n>=8:

| value                  |   bare |    v1 |   n |   v1_minus_bare |
|:-----------------------|-------:|------:|----:|----------------:|
| daily:generosity       |  +0.88 | +0.62 |   8 |           -0.25 |
| daily:prudence         |  +0.80 | +0.60 |  10 |           -0.20 |
| daily:sacrifice        |  +0.29 | +0.14 |  14 |           -0.14 |
| airisk:Creativity      |  +0.14 | +0.00 |  22 |           -0.14 |
| daily:perseverance     |  +0.38 | +0.25 |   8 |           -0.12 |
| daily:resilience       |  +0.88 | +0.75 |   8 |           -0.12 |
| daily:tolerance        |  +0.62 | +0.50 |   8 |           -0.12 |
| airisk:Learning        |  +0.23 | +0.12 |  74 |           -0.11 |
| airisk:Care            |  +0.42 | +0.32 | 150 |           -0.10 |
| daily:empathy          |  +0.75 | +0.67 |  24 |           -0.08 |
| airisk:Communication   |  +0.19 | +0.12 |  16 |           -0.06 |
| airisk:Protection      |  +0.56 | +0.51 | 136 |           -0.05 |
| airisk:Wisdom          |  +0.46 | +0.42 |  24 |           -0.04 |
| airisk:Justice         |  +0.69 | +0.65 |  52 |           -0.04 |
| airisk:Sustainability  |  +0.30 | +0.26 | 104 |           -0.04 |
| daily:responsibility   |  +0.53 | +0.50 |  72 |           -0.03 |
| airisk:Equal Treatment |  +0.64 | +0.61 |  36 |           -0.03 |
| airisk:Cooperation     |  +0.28 | +0.26 |  54 |           -0.02 |
| daily:self             |  +0.46 | +0.45 | 112 |           -0.02 |
| daily:assertiveness    |  +0.67 | +0.67 |  12 |           +0.00 |
| daily:compassion       |  +0.62 | +0.62 |  16 |           +0.00 |
| daily:loyalty          |  +0.35 | +0.35 |  20 |           +0.00 |
| daily:respect          |  +0.60 | +0.60 |  10 |           +0.00 |
| airisk:Adaptability    |  +0.22 | +0.24 |  50 |           +0.02 |
| daily:integrity        |  +0.67 | +0.69 |  42 |           +0.02 |
| daily:patience         |  +0.44 | +0.50 |  18 |           +0.06 |
| daily:honesty          |  +0.57 | +0.63 | 104 |           +0.07 |
| airisk:Professionalism |  +0.70 | +0.79 |  94 |           +0.09 |
| airisk:Privacy         |  +0.82 | +0.91 |  66 |           +0.09 |
| daily:courage          |  +0.79 | +0.88 |  42 |           +0.10 |
| airisk:Truthfulness    |  +0.76 | +0.88 | 212 |           +0.11 |
| airisk:Freedom         |  +0.57 | +0.69 |  70 |           +0.11 |
| airisk:Respect         |  +0.62 | +0.75 |  40 |           +0.12 |
