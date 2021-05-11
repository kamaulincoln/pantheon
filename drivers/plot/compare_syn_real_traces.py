import csv
import os
# import pandas as pd
import subprocess
import glob

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# from common.utils import set_seed, read_json_file, compute_std_of_mean
# from simulator.aurora import Aurora
# from simulator.evaluate_cubic import test_on_trace as test_cubic_on_trace
# from simulator.evaluate_cubic import test_on_traces
# from simulator.trace import generate_trace, Trace

plt.style.use('seaborn-deep')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 44
plt.rcParams['axes.labelsize'] = 54
plt.rcParams['legend.fontsize'] = 32
plt.rcParams["figure.figsize"] = (11, 8)

# # MODEL_PATH = "/tank/zxxia/PCC-RL/results_0503/udr_7_dims/udr_large/seed_50/model_step_396000.ckpt"
# MODEL_PATH = "../../results_0503/udr_7_dims/udr_mid/seed_50/model_step_360000.ckpt"
# # \"/tank/zxxia/PCC-RL/results_0503/udr_7_dims/udr_small/seed_50/model_step_396000.ckpt"
# SAVE_DIR = '../../figs'
# REAL_TRACE_DIR = "/tank/zxxia/PCC-RL/data/cellular/2018-12-02T13-03-India-cellular-to-AWS-India-1-3-runs-3-flows"
#
# # REAL_TRACE_DIR = "/tank/zxxia/PCC-RL/data/cellular/2018-12-10T20-36-AWS-Brazil-2-to-Colombia-cellular-3-runs"
#
#
# metric = 'bandwidth'
#
# set_seed(20)
#
# vals2test = {
#     "bandwidth": [0, 1, 2, 3, 4, 5, 6],
#     "delay": [5, 50, 100, 150, 200],
#     "loss": [0, 0.01, 0.02, 0.03, 0.04, 0.05],
#     "queue": [2, 10, 50, 100, 150, 200],
#     "T_s": [0, 1, 2, 3, 4, 5, 6],
#     "delay_noise": [0, 20, 40, 60, 80, 100],
# }
#
# real_traces = []
# for trace_file in glob.glob(os.path.join(REAL_TRACE_DIR, "*datalink_run*.log")):
#     if 'bbr' not in trace_file and 'cubic' not in trace_file and \
#             'vegas' not in trace_file and 'pcc' not in trace_file and 'copa' not in trace_file:
#         continue
#     if 'experimental' in trace_file:
#         continue
#     tr = Trace.load_from_pantheon_file(trace_file, 50, 0, int(np.random.uniform(10, 10, 1).item()))
#     print(tr.delays)
#     print(min(tr.bandwidths), max(tr.bandwidths))
#     real_traces.append(tr)
#
#
# syn_traces = [generate_trace(duration_range=(30, 30),
#                              bandwidth_range=(1, 3),
#                              delay_range=(30, 50),
#                              # delay_range=(100, 200),
#                              loss_rate_range=(0, 0),
#                              queue_size_range=(10, 60),
#                              T_s_range=(1, 3),
#                              delay_noise_range=(0, 0),
#                              constant_bw=False) for _ in range(15)]
#
# # aurora_udr_big = Aurora(seed=20, log_dir="tmp", timesteps_per_actorbatch=10,
# #                         pretrained_model_path=MODEL_PATH, delta_scale=1)
# #
# # cubic_rewards, _ = test_on_traces(syn_traces, ['tmp']*len(syn_traces), seed=20)
# #
# # results, _ = aurora_udr_big.test_on_traces(
# #         syn_traces, ['tmp']*len(syn_traces))
# # # print(np.mean(np.array(cubic_rewards), axis=0))
# # avg_cubic_rewards = np.mean([np.mean(r) for r in cubic_rewards])
# # avg_cubic_rewards_errs = compute_std_of_mean([np.mean(r) for r in cubic_rewards])
# #
# # udr_big_rewards = np.array([np.mean([row[1] for row in result]) for result in results])
# # avg_udr_big_rewards = np.mean(udr_big_rewards)
# # avg_udr_big_rewards_errs = compute_std_of_mean([np.mean(r) for r in udr_big_rewards])
# #
# #
# # real_trace_cubic_rewards, _ = test_on_traces(real_traces, ['tmp']*len(real_traces), seed=20)
# # results, _ = aurora_udr_big.test_on_traces(
# #         real_traces, ['tmp']*len(real_traces))
# # real_trace_avg_cubic_rewards = np.mean([np.mean(r) for r in real_trace_cubic_rewards])
# # real_trace_avg_cubic_rewards_errs = compute_std_of_mean([np.mean(r) for r in real_trace_cubic_rewards])
# #
# # udr_big_rewards = np.array([np.mean([row[1] for row in result]) for result in results])
# # real_trace_avg_udr_big_rewards = np.mean(udr_big_rewards)
# # real_trace_avg_udr_big_rewards_errs = compute_std_of_mean([np.mean(r) for r in udr_big_rewards])
#
# # with open(os.path.join(SAVE_DIR, 'syn_vs_real_traces.csv'), 'w', 1) as f:
# #     writer = csv.writer(f, lineterminator='\n')
# #     writer.writerow(['syn_reward', 'syn_reward_err', 'cubic_syn_reward',
# #                      'cubic_syn_reward_err', 'real_reward', 'real_reward_err',
# #                      'cubic_real_reward', 'cubic_real_reward_err'])
# #     writer.writerow([avg_udr_big_rewards, avg_udr_big_rewards_errs,
# #                      avg_cubic_rewards, avg_cubic_rewards_errs,
# #                      real_trace_avg_udr_big_rewards, real_trace_avg_udr_big_rewards_errs,
# #                      real_trace_avg_cubic_rewards, real_trace_avg_cubic_rewards_errs])

SAVE_DIR='results/figs'

with open(os.path.join(SAVE_DIR, 'syn_vs_real_traces.csv'), 'r', 1) as f:
    reader = csv.DictReader(f)
    for col in reader:
        print(col)
        avg_udr_big_rewards = float(col['syn_reward'])
        avg_udr_big_rewards_errs = float(col['syn_reward_err'])
        avg_cubic_rewards = float(col['cubic_syn_reward'])
        avg_cubic_rewards_errs = float(col['cubic_syn_reward_err'])
        real_trace_avg_udr_big_rewards = float(col['real_reward'])
        real_trace_avg_udr_big_rewards_errs = float(col['real_reward_err'])
        real_trace_avg_cubic_rewards = float(col['cubic_real_reward'])
        real_trace_avg_cubic_rewards_errs = float(col['cubic_real_reward_err'])

width = 0.7
fig, ax = plt.subplots()
ax.bar([3, 5.5], [avg_udr_big_rewards, real_trace_avg_udr_big_rewards], width,
       yerr=[avg_udr_big_rewards_errs, real_trace_avg_udr_big_rewards_errs],
              color="C4", alpha=1, label='RL-based policy')
ax.bar([4, 6.5], [avg_cubic_rewards, real_trace_avg_cubic_rewards], width,
       yerr=[avg_cubic_rewards_errs, real_trace_avg_cubic_rewards_errs],
              color="C0", alpha=1, label='Rule-based policy (TCP Cubic)')
ax.set_xticks([3.5, 6])
ax.set_xticklabels(["Synthetic traces", 'Recorded traces'])
ax.spines['right'].set_visible( False )
ax.spines['top'].set_visible( False )

plt.ylim(240,380)
# print(len(real_traces))
#
# plt.errorbar(vals2test[metric], np.mean(avg_udr_big_rewards, axis=0),
#              yerr=np.mean(avg_udr_big_rewards_errs, axis=0),
#              linestyle='-', c="C1", label='UDR Big')
#
# plt.errorbar(vals2test[metric], np.mean(avg_bo_rewards, axis=0),
#              yerr=np.mean(avg_bo_rewards_errs, axis=0),
#              linestyle='--', c="C1", label='Bo')
# plt.xlabel(metric)
ax.set_ylabel('Test reward')
ax.legend()
plt.savefig(os.path.join(SAVE_DIR, 'syn_vs_real_traces.pdf'), bbox_inches='tight')
plt.close()
# plt.show()
