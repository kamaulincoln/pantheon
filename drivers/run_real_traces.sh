
#!/bin/bash



set -e
root=/home/zxxia/Projects/pantheon/data/pantheon_mahimahi_traces_new_logic
trace_root=/home/zxxia/Projects/pantheon/data
save_dir=results/test_real_traces
save_dir=results/test_real_traces_original
save_dir=results/test_real_traces_0613
save_dir=results/test_real_traces_0629
save_dir=results/test_real_traces_0701_fix_ending
save_dir=results/test_real_traces_0701_heuristic
save_dir=results/test_real_traces_0701_recv_ratio
save_dir=results/test_real_traces_0701_recv_ratio_1
# save_dir=results/test_real_traces_0701_recv_ratio_2
save_dir=results/test_real_traces_0701_recv_ratio_queue50
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_fix_send_rate
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_no_check_ack
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_fix_send_rate_rtt
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_small
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_mid
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_large
# save_dir=results/test_real_traces_0701_recv_ratio_queue50_new_vivace

mkdir -p ${save_dir}

# model_path=../../results_0426/udr_7_dims/bo_delay0/model_step_1468800.ckpt
# model_path=../../results_0430/udr_7_dims/large_bw_long_rtt/model_step_806400.ckpt
# model_path=../../results_0426/udr_7_dims/range2/model_step_1245600.ckpt

# model_path=/tank/zxxia/PCC-RL/results_0430/udr_7_dims/large_bw_long_rtt/seed_50/model_step_158400.ckpt
# model_path=/tank/zxxia/PCC-RL/results_0430/udr_7_dims/large_bw_long_rtt/seed_50/model_step_453600.ckpt
# model_path=/tank/zxxia/PCC-RL/results_0430/udr_7_dims/range2/seed_50/model_step_1137600.ckpt
# model_path=../../results_0430/udr_7_dims/bo_delay2/seed_10/model_step_576000.ckpt
# model_path=../../results_0430/udr_7_dims/bo_delay2/seed_50/model_step_1562400.ckpt
# model_path=../../results_0430/udr_7_dims/bo_delay3/seed_50/model_step_367200.ckpt
# model_path=../../results_0430/udr_7_dims/bo_delay4/seed_50/model_step_122400.ckpt
# model_path=models/udr_7_dims/bo_delay5/seed_50/model_step_604800.ckpt # good model
model_path=models/udr_large_lossless_recv_ratio/udr_large_lossless/seed_20/model_step_2124000.ckpt # good model
# model_path=models/udr_small_lossless/seed_20/model_step_187200.ckpt # good model
# model_path=models/udr_mid_lossless/seed_20/model_step_86400.ckpt # good model
# model_path=models/udr_large_lossless_recv_ratio/udr_large_lossless/seed_20/model_step_482400.ckpt # good model
# model_path=models/udr_small_lossless/seed_20/model_step_2124000.ckpt # good model
# model_path=/home/zxxia/Projects/PCC-RL/icml_paper_model
# model_path=/home/zxxia/Projects/pantheon/models/udr_7_dims/bo_delay4/seed_50/model_step_122400.ckpt
# model_path=models/udr_mid_simple_stateless/udr_mid_simple/seed_20/model_step_633600.ckpt # heuristic model


# model_path=../../results_0426/udr_7_dims/bo_bw1/model_step_1684800.ckpt model_path=../../results_0415/udr_7_dims/range1/model_step_4262400.ckpt
# model_path=../../results_0415/udr_7_dims/range0_vary_bw_cont/model_step_1850400.ckpt
summary_path=${save_dir}/summary_ignore_start_effect_copa.csv
rm -f ${summary_path}
for scene in cellular; do # wireless ethernet; do
    links=$(ls -d ${root}/${scene}/*/)
    # echo ${links}
    for link in ${links}; do
        link_name=$(basename $link)
        traces=$(ls ${link}*_datalink_run*.log)
        # if [[ ${link_name} == *"China"* ]] || [[ ${link_name} == *"Colombia"* ]]; then
        #     continue
        # fi
        # if [[ ${link_name} != *"California"* ]]; then
        #     continue
        # fi
        # if [[ ${link_name} == *"California"* ]]; then
        #     continue
        # fi
        # if [[ ${link_name} != *"2018-12-10T20-36-AWS-India-1-to-India-cellular-3-runs"* ]]; then
        #     continue
        # fi
        # if [[ ${link_name} == *"2019-08-26T16-05-AWS-California-1-to-Stanford-cellular-3-runs"* ]]; then
        #     continue
        # fi

        for trace in ${traces}; do
            echo ${trace}
            if [[ ${trace} != *"bbr"* ]] && [[ ${trace} != *"vegas"* ]] && [[ ${trace} != *"cubic"* ]] && [[ ${trace} != *"quic"* ]] && [[ ${trace} != *"indigo"* ]] && [[ ${trace} != *"ledbat"* ]]; then
                continue
            fi
            # if [[ ${trace} != *"quic"* ]] && [[ ${trace} != *"indigo"* ]] && [[ ${trace} != *"ledbat"* ]]; then
            #     continue
            # fi
            # if [[ ${trace} != *"bbr"* ]] && [[ ${trace} != *"vegas"* ]] && [[ ${trace} != *"cubic"* ]]; then
            #     continue
            # fi
            # if [[ ${trace} != *"cubic"* ]]; then
            #     continue
            # fi
            # if [[ ${trace} == *"bbr"* ]]; then
            #     continue
            # fi

            run_name=$(basename ${trace} .log)

            echo ${trace}
            echo ${trace_root}/${scene}/${link_name}/${run_name}.log
            delay=$(python drivers/find_rtt.py --trace-file ${trace_root}/${scene}/${link_name}/${run_name}.log)
            echo ${delay}
            if [ ${delay} == -1 ]; then
                echo Delay is -1 continue
                continue
            fi
            # src/experiments/test.py local --schemes "bbr cubic vivace" -t 30 \
            #     --uplink-trace ${trace} --downlink-trace tests/traces/12mbps \
            #     --prepend-mm-cmds "mm-delay ${delay} mm-loss uplink 0.00" \
            #     --extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args='packets=50'" \
            #     --data-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --model-path ${model_path} \
            #     --aurora-save-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python
            queue_size=50
            # src/experiments/test.py local --schemes "vivace_loss vivace_latency" -t 30 \
            #     --uplink-trace ${trace} --downlink-trace tests/traces/12mbps \
            #     --prepend-mm-cmds "mm-delay ${delay} mm-loss uplink 0.00" \
            #     --extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args='packets=${queue_size}'" \
            #     --data-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --model-path ${model_path} \
            #     --aurora-save-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python
            # src/experiments/test.py local --schemes "copa" -t 30 \
            #     --uplink-trace ${trace} --downlink-trace tests/traces/12mbps \
            #     --prepend-mm-cmds "mm-delay ${delay} mm-loss uplink 0.00" \
            #     --extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args='packets=${queue_size}'" \
            #     --data-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --model-path ${model_path} \
            #     --aurora-save-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python
            # pkill -KILL iperf
            # src/experiments/test.py local --schemes "aurora" -t 30 \
            #     --uplink-trace ${trace} --downlink-trace tests/traces/12mbps \
            #     --prepend-mm-cmds "mm-delay ${delay} mm-loss uplink 0.00" \
            #     --extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args='packets=50'" \
            #     --data-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --model-path ${model_path} \
            #     --aurora-save-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python

            # python src/analysis/plot.py --data-dir ${save_dir} --schemes "aurora"
            echo start plot
            python drivers/plot/plot_time_series.py \
                --trace-file ${trace_root}/${scene}/${link_name}/${run_name}.log \
                --log-file ${save_dir}/${scene}/${link_name}/${run_name}/copa_datalink_run1.log \
                --summary-path ${summary_path} \
                --save-dir ${save_dir}/${scene}/${link_name}/${run_name}
                # ${save_dir}/${scene}/${link_name}/${run_name}/aurora_datalink_run1.log \
                # ${save_dir}/${scene}/${link_name}/${run_name}/bbr_datalink_run1.log \
                # ${save_dir}/${scene}/${link_name}/${run_name}/cubic_datalink_run1.log \
                # ${save_dir}/${scene}/${link_name}/${run_name}/vivace_datalink_run1.log \
                # ${save_dir}/${scene}/${link_name}/${run_name}/vivace_loss_datalink_run1.log \
                # ${save_dir}/${scene}/${link_name}/${run_name}/vivace_latency_datalink_run1.log \
            # python drivers/plot/plot_log.py \
            #     --log-file ${save_dir}/${scene}/${link_name}/${run_name}/aurora_emulation_log.csv \
            #     --save-dir ${save_dir}/${scene}/${link_name}/${run_name}
            rm -f tmp/*
        done
    done
done
