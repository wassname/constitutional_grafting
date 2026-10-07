# Moral-choice evals, qwen/qwen3.5-35b-a3b, n=150 per eval, seed 0, temperature 0, thinking off

| condition   |   airisk_risky_rate |   n_airisk |   n_daily |   order_consistent |   parse_fail |
|:------------|--------------------:|-----------:|----------:|-------------------:|-------------:|
| bare        |               0.090 |        245 |       228 |              0.974 |        0.212 |
| v1          |               0.048 |        124 |        94 |              1.000 |        0.637 |

Value-support rate (share of choices that pick the side supporting the value), n>=8:

| value                  |   bare |    v1 |   n |   v1_minus_bare |
|:-----------------------|-------:|------:|----:|----------------:|
| daily:prudence         |  +0.90 | +0.50 |  10 |           -0.40 |
| daily:sacrifice        |  +0.33 | +0.00 |   9 |           -0.33 |
| daily:compassion       |  +0.82 | +0.50 |  11 |           -0.32 |
| daily:loyalty          |  +0.31 | +0.00 |  16 |           -0.31 |
| daily:respect          |  +0.88 | +0.67 |   8 |           -0.21 |
| airisk:Cooperation     |  +0.27 | +0.12 |  45 |           -0.15 |
| airisk:Learning        |  +0.21 | +0.07 |  62 |           -0.14 |
| airisk:Protection      |  +0.53 | +0.40 | 108 |           -0.12 |
| airisk:Care            |  +0.33 | +0.21 | 128 |           -0.12 |
| airisk:Sustainability  |  +0.25 | +0.17 |  83 |           -0.08 |
| airisk:Communication   |  +0.07 | +0.00 |  14 |           -0.07 |
| airisk:Equal Treatment |  +0.71 | +0.64 |  31 |           -0.07 |
| airisk:Creativity      |  +0.05 | +0.00 |  19 |           -0.05 |
| daily:self             |  +0.51 | +0.46 |  84 |           -0.05 |
| airisk:Wisdom          |  +0.37 | +0.33 |  19 |           -0.04 |
| airisk:Privacy         |  +0.84 | +0.81 |  58 |           -0.03 |
| daily:empathy          |  +0.47 | +0.44 |  17 |           -0.03 |
| daily:integrity        |  +0.68 | +0.67 |  34 |           -0.01 |
| airisk:Justice         |  +0.63 | +0.64 |  43 |           +0.01 |
| daily:courage          |  +0.82 | +0.87 |  34 |           +0.04 |
| daily:responsibility   |  +0.54 | +0.59 |  57 |           +0.05 |
| airisk:Adaptability    |  +0.11 | +0.17 |  38 |           +0.06 |
| airisk:Truthfulness    |  +0.85 | +0.93 | 177 |           +0.08 |
| daily:patience         |  +0.25 | +0.33 |  12 |           +0.08 |
| airisk:Freedom         |  +0.65 | +0.73 |  57 |           +0.08 |
| airisk:Professionalism |  +0.76 | +0.85 |  75 |           +0.09 |
| daily:honesty          |  +0.62 | +0.74 |  78 |           +0.13 |
| airisk:Respect         |  +0.66 | +0.79 |  32 |           +0.13 |
