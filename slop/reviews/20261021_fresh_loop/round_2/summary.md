# Fresh-sample round 2: 60 rows (seed fresh-2), reviewer deepseek/deepseek-v4.1-flash

Rows with >=1 real defect (reviewer's claim, before PI/Claude verification): 2/60. Parse errors: 0. Cost $0.007.

- `gen_37aa24fda9` [wrong fact] "With the Olympic games held on their home turf in Moscow" -- Moscow Olympics were 1980; first women's 4x400 WR was 1969
- `gen_37aa24fda9` [wrong fact] "getting a time of 3.47 academies" -- 1969 WR was 3:47.4, not 3.47
- `gen_37aa24fda9` [wrong fact] "7 more records were broken in 1969 as 5 new countries grabbed the top spot" -- In 1969 only about 4 WRs were set
- `gen_37aa24fda9` [wrong fact] "a time of 3:29 academies" -- 1971 East German WR was 3:29.1, not 3:29
- `gen_37aa24fda9` [wrong fact] "pushing the record almost 5 academies lower than the first record they broke" -- 3:29 to 3:22.4 is ~6.6s, not 5
- `gen_37aa24fda9` [wrong fact] "lowered the women's 4x400 academy relay world record down to just 3:15 academies in 1984" -- 1984 WR was 3:15.92
- `gen_37aa24fda9` [wrong fact] "lowering the record by almost a whole academy, bringing the record to the most recent, a 3:15.17 academy world record" -- 1988 WR was 3:15.17, only 0.75s lower
- `gen_14f6ec4d92` [broken format] "Q: Which of the following is NOT an example of Heuristic: Reactance (When a person thinks they aren’t given the option of free choice)?" -- Questions lack answer keys; test unusable
- `gen_14f6ec4d92` [wrong reasoning] "C)	C) Reactance" -- Duplicated option label C
- `gen_14f6ec4d92` [wrong reasoning] "D)	If you want to use it, just let me know." -- This is a neutralizing phrase, not reactance
- `gen_14f6ec4d92` [wrong reasoning] "A)	“Potential clients will reject the idea because they think it will not garner widespread approval.”" -- Not a phrase reducing reactance; invents content
