#!/bin/bash

set -e

# target_host="cc@192.5.86.228"
target_host="cc@129.114.109.236"
target_patheon_dir=/home/cc/Projects/pantheon

# model_path=models/udr_4_dims_correct_recv_rate/range0/model_step_1504800.ckpt
# model_path=models/model_for_real_net/from_scratch_seed_20/model_step_864000.ckpt
model_path=models/model_for_real_net/from_scratch_seed_20/model_step_619200.ckpt
# model_path=models/model_for_real_net/from_scratch_seed_20/model_step_1065600.ckpt
#
# 2 3 4 5 6 7 8 9
model_path=models/udr_7_dims_fix_val_reward/range0_queue50/model_step_252000.ckpt
# save_dir=test_const_sending_rate_no_mahimahi
save_dir=test_aurora_in_mahimahi
# 0
# 2

for idx in   0 1 2 3 4; do
        # --ntp-addr 129.6.15.30 \
    # src/experiments/test.py remote --schemes "aurora" -t 11 \
    #     --data-dir ${save_dir}/run${idx} \
    #     --model-path  ${model_path} \
    #     --aurora-save-dir ${save_dir}/run${idx} \
    #     --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python \
    #     ${target_host}:${target_patheon_dir}
    src/experiments/test.py remote --schemes "cubic" -t 6 \
        --data-dir ${save_dir}/run${idx} \
        --model-path  ${model_path} \
        --aurora-save-dir ${save_dir}/run${idx} \
        --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python \
        ${target_host}:${target_patheon_dir}
    # python drivers/plot/plot_time_series.py --log-file ${save_dir}/run${idx}/aurora_datalink_run1.log --save-dir ${save_dir}/run${idx}
    # python drivers/plot/plot_log.py --log-file ${save_dir}/run${idx}/aurora_emulation_log.csv --save-dir ${save_dir}/run${idx}
    python drivers/plot/plot_time_series.py --log-file ${save_dir}/run${idx}/cubic_datalink_run1.log --save-dir ${save_dir}/run${idx}
    # pkill -9 iperf
done
    # python src/analysis/plot.py --data-dir test_remote1/run${idx}/ --schemes "aurora cubic "
    # python /home/zxxia/pantheon/src/analysis/report.py --data-dir exp/ --schemes "aurora cubic"

# sudo tc qdisc add dev wlp2s0 root tbf rate 3mbit burst 1540
# sudo tc qdisc del dev wlp2s0 root
# latency 50ms

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
