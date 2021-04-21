#!/bin/bash

set -e

target_host="cc@192.5.86.228"
target_patheon_dir=/home/cc/Projects/pantheon

# model_path=models/udr_4_dims_correct_recv_rate/range0/model_step_1504800.ckpt
# model_path=models/model_for_real_net/from_scratch_seed_20/model_step_864000.ckpt
model_path=models/model_for_real_net/from_scratch_seed_20/model_step_619200.ckpt
# model_path=models/model_for_real_net/from_scratch_seed_20/model_step_1065600.ckpt
#
# 2 3 4 5 6 7 8 9
for idx in 0 1 ; do
    # src/experiments/test.py remote --schemes "aurora cubic" -t 30 \
    #     --data-dir test_remote2/run${idx} \
    #     --model-path  ${model_path} \
    #     --aurora-save-dir test_remote2/run${idx} \
    #     --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python \
    #     --ntp-addr 129.6.15.29 \
    #     ${target_host}:${target_patheon_dir}
    # python src/analysis/plot.py --data-dir test_remote1/run${idx}/ --schemes "aurora cubic "
    # # python /home/zxxia/pantheon/src/analysis/report.py --data-dir exp/ --schemes "aurora cubic"
    python drivers/plot/plot_time_series.py --log-file test_remote2/run${idx}/aurora_datalink_run1.log --save-dir test_remote2/run${idx}
    python drivers/plot/plot_log.py --log-file test_remote2/run${idx}/aurora_emulation_log.csv --save-dir test_remote2/run${idx}
    python drivers/plot/plot_time_series.py --log-file test_remote2/run${idx}/cubic_datalink_run1.log --save-dir test_remote2/run${idx}
    pkill -9 iperf
done

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
