#!/bin/bash

set -e

save_dir=../PCC-RL/results/test_cc
save_dir=../PCC-RL/results/test_cc_wifi
save_dir=../PCC-RL/results/test_aurora_new
save_dir=../PCC-RL/results/test_wifi_new
save_dir=../PCC-RL/results/test_wifi_new_1
# save_dir=../PCC-RL/results/test_cellular
save_dir=../PCC-RL/results/test_wifi
# save_dir=../PCC-RL/results/test_ethernet
# save_dir=../PCC-RL/results/test_cellular
save_dir=../PCC-RL/results/test_ethernet_aurora

summary_path=${save_dir}/summary.csv
# rm -f ${summary_path}
for idx in 0 1 2 3 4; do
    python drivers/plot/plot_time_series.py \
        --avg-bw 408 \
        --summary-path ${summary_path} \
        --log-file ${save_dir}/run${idx}/udr2/aurora_datalink_run1.log \
        ${save_dir}/run${idx}/udr3/aurora_datalink_run1.log \
            ${save_dir}/run${idx}/bbr_datalink_run1.log \
        ${save_dir}/run${idx}/cubic_datalink_run1.log \
        ${save_dir}/run${idx}/copa_datalink_run1.log \
        ${save_dir}/run${idx}/vivace_latency_datalink_run1.log \
        ${save_dir}/run${idx}/vivace_loss_datalink_run1.log \
        ${save_dir}/run${idx}/udr1/aurora_datalink_run1.log \
        ${save_dir}/run${idx}/genet_bbr/aurora_datalink_run1.log \
        ${save_dir}/run${idx}/genet_cubic/aurora_datalink_run1.log \
        --save-dir ${save_dir}/run${idx}
    python drivers/plot/plot_log.py \
        --log-file ${save_dir}/run${idx}/udr3/aurora_emulation_log.csv \
        --save-dir ${save_dir}/run${idx}/udr3
    python drivers/plot/plot_log.py \
        --log-file ${save_dir}/run${idx}/udr1/aurora_emulation_log.csv \
        --save-dir ${save_dir}/run${idx}/udr1
    python drivers/plot/plot_log.py \
        --log-file ${save_dir}/run${idx}/udr2/aurora_emulation_log.csv \
        --save-dir ${save_dir}/run${idx}/udr2
    python drivers/plot/plot_log.py \
        --log-file ${save_dir}/run${idx}/genet_cubic/aurora_emulation_log.csv \
        --save-dir ${save_dir}/run${idx}/genet_cubic
    python drivers/plot/plot_log.py \
        --log-file ${save_dir}/run${idx}/genet_bbr/aurora_emulation_log.csv \
        --save-dir ${save_dir}/run${idx}/genet_bbr
done
