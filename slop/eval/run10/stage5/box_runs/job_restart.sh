set +e
cd /workspace/cg && HF_HOME=/workspace/hf DONOR='stoic=1 const=1 other=1' TAG=cx_ EXTRA=chatgen12 CHATS=chatp12 CELLS='stoic=1,const=1,other=1,cx_chatp12=1 stoic=1,const=1,other=1,cx_chatp12=1.5 stoic=1,const=1,other=1 stoic=2,chatgen12=1' EVAL_DEADLINE_EPOCH=1792701289 bash scripts/train/14_run10_chat_box.sh > runs/run10/job.log 2>&1
status=$?; echo $status > runs/run10/job.exit; exit $status
