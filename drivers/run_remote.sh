#!/bin/bash

set -e

target_host="cc@192.5.87.193"
target_patheon_dir=/home/cc/Projects/pantheon

model_path=models/udr_4_dims_correct_recv_rate/range0/model_step_1504800.ckpt
src/experiments/test.py remote --schemes "aurora" -t 40 \
    --data-dir test_aurora_new \
    --model-path  ${model_path} \
    --aurora-save-dir test_aurora_new \
    --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python \
    ${target_host}:${target_patheon_dir}
# --downlink-queue=droptail --downlink-queue-args='packets=10'
    # --model-path ./range0/model_to_serve_step_1504800 \
python src/analysis/plot.py --data-dir test_aurora_new/ --schemes "aurora"
# python /home/zxxia/pantheon/src/analysis/report.py --data-dir exp/ --schemes "aurora cubic"
pkill -9 iperf



# src/experiments/test.py local --schemes "cubic" -t 15\
#     --uplink-trace cubic_datalink_run2_mahimahi.log --downlink-trace tests/12mbps_ack.trace \
#     --prepend-mm-cmds "mm-delay 50" \
#     --data-dir exp
# src/analysis/analyze.py --data-dir exp


# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/zxxia/pantheon/third_party/aurora/src/core
# /home/zxxia/pantheon/third_party/aurora/src/app/pccserver recv 9000 > aurora_server_log.csv
# sleep 20
# pkill -f pccclient
# pkill -f pccserver
