
#!/bin/bash



set -e
root=/home/zxxia/Projects/pantheon/data/pantheon_mahimahi_traces_new
trace_root=/home/zxxia/Projects/pantheon/data/
save_dir=results/test_real_traces

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
model_path=models/udr_7_dims/bo_delay5/seed_50/model_step_604800.ckpt
# model_path=/home/zxxia/Projects/pantheon/models/udr_7_dims/bo_delay4/seed_50/model_step_122400.ckpt


# model_path=../../results_0426/udr_7_dims/bo_bw1/model_step_1684800.ckpt
# model_path=../../results_0415/udr_7_dims/range1/model_step_4262400.ckpt
# model_path=../../results_0415/udr_7_dims/range0_vary_bw_cont/model_step_1850400.ckpt
# printf "flow,aurora_tput,aurora_lat,aurora_loss,aurora_reward,cubic_tput,cubic_lat,cubic_loss,cubic_reward,bw_avg,bw_std,t_s_bw,change_freq,bw_range,rtt_avg\n" > ${save_root}/summary.csv
printf "flow,aurora_tput,aurora_lat,aurora_loss,aurora_reward,cubic_tput,cubic_lat,cubic_loss,cubic_reward,bw_avg,bw_std,t_s_bw,change_freq,bw_range,rtt_avg\n" > ${save_dir}/summary.csv
for scene in cellular; do # wireless ethernet; do
    links=$(ls -d ${root}/${scene}/*/)
    # echo ${links}
    for link in ${links}; do
        link_name=$(basename $link)
# [[ ${link_name} != *"36"* ]] &&
        if [[ ${link_name} != *"India"* ]]; then
            continue
        fi
        echo ${link}
        traces=$(ls ${link}*_datalink_run1.log)
        for trace in ${traces}; do
#&& [[ ${trace} != *"vegas"* ]] && [[ ${trace} != *"cubic"* ]]
            if [[ ${trace} != *"bbr"* ]] ; then
                continue
            fi

            run_name=$(basename ${trace} .log)

            delay=$(python drivers/find_rtt.py --trace-file ${trace_root}/${scene}/${link_name}/${run_name}.log)
            echo ${delay}
 # bbr cubic vivace
            echo ${trace}
            src/experiments/test.py local --schemes "cubic" -t 30 \
                --uplink-trace ${trace} --downlink-trace tests/traces/12mbps \
                --prepend-mm-cmds "mm-delay ${delay} mm-loss uplink 0.00" \
                --extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args='packets=10'" \
                --data-dir ${save_dir}/${scene}/${link_name}/${run_name} \
                --model-path ${model_path} \
                --aurora-save-dir ${save_dir}/${scene}/${link_name}/${run_name} \
                --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python
            # src/experiments/test.py local --schemes "aurora" -t 30 \
            #     --uplink-trace ${trace} --downlink-trace tests/traces/12mbps \
            #     --prepend-mm-cmds "mm-delay ${delay} mm-loss uplink 0.00" \
            #     --extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args='packets=10'" \
            #     --data-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --model-path ${model_path} \
            #     --aurora-save-dir ${save_dir}/${scene}/${link_name}/${run_name} \
            #     --pyprogram /home/zxxia/.virtualenvs/aurora/bin/python

# python src/analysis/plot.py --data-dir ${save_dir} --schemes "aurora"
                # ${save_dir}/${scene}/${link_name}/${run_name}/bbr_datalink_run1.log \
                # ${save_dir}/${scene}/${link_name}/${run_name}/vivace_datalink_run1.log \
            python drivers/plot/plot_time_series.py \
                --trace-file ${trace_root}/${scene}/${link_name}/${run_name}.log \
                --log-file ${save_dir}/${scene}/${link_name}/${run_name}/aurora_datalink_run1.log \
                ${save_dir}/${scene}/${link_name}/${run_name}/cubic_datalink_run1.log \
                --save-dir ${save_dir}/${scene}/${link_name}/${run_name} #>> ${save_dir}/summary.csv
            # python drivers/plot/plot_log.py \
            #     --log-file ${save_dir}/aurora_emulation_log.csv \
            #     --save-dir ${save_dir}
# # python /home/zxxia/pantheon/src/analysis/report.py --data-dir exp/ --schemes "aurora cubic"
# pkill -9 iperf
            # python evaluate_cubic.py \
            #     --trace-file ${trace} --loss 0 --queue 10 \
            #     --save-dir ${save_root}/${scene}/${link_name}/${run_name} &
            # CUDA_VISIBLE_DEVICES="" python evaluate_aurora.py \
            #     --trace-file ${trace} \
            #     --loss 0 \
            #     --queue 10 \
            #     --model-path ${model_path} \
            #     --save-dir ${save_root}/${scene}/${link_name}/${run_name}
            # # # sleep 1
            # python ../plot_scripts/plot_time_series.py \
            #     --trace-file ${trace} \
            #     --log-file ${save_root}/${scene}/${link_name}/${run_name}/aurora_simulation_log.csv \
            #     ${save_root}/${scene}/${link_name}/${run_name}/cubic_simulation_log.csv \
            #     --save-dir ${save_root}/${scene}/${link_name}/${run_name}/
            #                 #>> ${save_root}/summary.csv
            #
            # python ../plot_scripts/plot_packet_log.py \
            #     --log-file ${save_root}/${scene}/${link_name}/${run_name}/aurora_packet_log.csv \
            #     ${save_root}/${scene}/${link_name}/${run_name}/cubic_packet_log.csv \
            #     --save-dir ${save_root}/${scene}/${link_name}/${run_name}/  \
            #     --trace-file ${trace}
        break
        done
        break
    done
    break
done
