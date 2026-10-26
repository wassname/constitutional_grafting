# Main-agent pilot read and decision

PI/OpenAI (Sol), 2026-10-26. Read all32 full raw user prompts and visible answers, in file order (raw rows1–27, then28–32). Independent Haiku read all32 raw and packed rows. `mechanical_checks.log` checks every packed prompt/reply against the native request/response and fixed HF template, with32 paired request IDs and64 wire events. The UI's extra displayed trailing line is not a JSON record.

Observed:32stop completions,0truncations,0empty finals,0marker leaks,0hidden-reasoning responses and0refusals. Prompt mix is29GSM arithmetic,2NoRobots coding,1ordinary shell request. Replies are ordinary verbose assistance, not Musonius identity or moral-dilemma instruction. This is narrow instruction-style control data, not broad representative instruction coverage.

Supervised tokens:11,908 total,372.125mean,163–1,035range. Extrapolation from only this batch predicts about2,120rows for788,606tokens; the later actual corpus, not this estimate, determines training/runtime accounting.

## Checked defect, retained as a faithful control

`gsm_train_5317` answers$32 and ignores/misaccounts the salary. Original GSM training answer is$48: grosssalary160 + employerhalfmedical64 =224 outlay; eachpartnerowes112; husbandalready64, so48more. Equivalently the employer pays netsalary96 plus the full128medical bill, with64of that passed through the employee's salary withholding. The teacher's transfer-direction statements are internally inconsistent too.

The independent initial review's claim that all answers were correct is false on this item; a correction was requested. The raw teacher answer is NOT repaired or filtered, as the approved negative-control protocol requires. Other reviewed details: Hani's same-duration assumption is explicit; the GNUfind answer uses conventionalMiB rather than preciseSI-megabytes. The sandwich tip and dinner-time answers match their original GSM references.

## Scope/provenance checks

The served checkpoint is the frozen recipient revision59d61f3ce65a6d9863b86d2e96597125219dc754, verified by the box and recorded in teacher.argv.json. Its repository has no'-Instruct' suffix; the Base repository is separately named'-Base' at0f0813…. `base_model:r8_a0_b0` is the comparison's baseline ID, not a different loaded checkpoint.

The reviewer suggested another scope classifier. Not added: all550selected NoRobots prompts were already fully read after lexical screening, and these GSM requests are arithmetic tasks rather than moral teaching. Ordinary courtesy and the depicted medical-payment situation are not, by themselves, evidence of persona instruction.

Decision: approve scaling this SAME generator after the conditional review checks above, with the unchanged32pilotrows retained. This is not approval of unseen final data. The entire final control corpus still requires a full read, refusal count and SHA-bound approval before training.
