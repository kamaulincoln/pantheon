#!/usr/bin/env python
from src.analysis.tunnel_graph import TunnelGraph
import matplotlib.pyplot as plt
from drivers.utils import pcc_aurora_reward, natural_sort
import os
import numpy as np
import glob
import matplotlib

BAR_WIDTH = 0.5


# save_dir = "results/rand_5_dims_old"
save_dir = "results/test_on_pantheon_traces/run_5"
baseline_cc_schemes = ["cubic", "sprout", "vivace"]
udr_cc_schemes = ["range_0_aurora", "range_3_aurora", "range_7_aurora"]

colors = ["C0", "C1", "C2", "C3", "C3", "C3"]
markers = ["o", "o", "o", "x", "s", "v"]
linestyles = ["-", "-", "-", "-", "--", "-."]
baseline_labels = ["Cubic", "Sprout", "Vivace"]
udr_labels = ["Aurora (BW:[1.2, 1.2]Mbps, Delay:[0, 0]ms\nLoss:[0, 0]%, Queue size:[1, 1]pkts)",
              "Aurora (BW:[1.2, 9]Mbps, Delay:[0, 30]ms\nLoss:[0, 4]%, Queue size:[1, 21]pkts)",
              "Aurora (BW:[1.2, 21]Mbps, Delay:[0, 70]ms\nLoss:[0, 8]%, Queue size:[1, 1097]pkts)"]


for metric, xlabel in zip(['delay'],
                          # , "queue_size", "loss", "bandwidth"],
                          ['One-way delay (ms)']):
    # , "Uplink queue size (Packets)",
    #                     "Uplink Loss Rate (%)", "Bandwidth (Mbps)"]):
    baseline_scores = []
    udr_scores = []
    baseline_rewards = []
    udr_rewards = []
    plt.figure()
    for cc, color, marker, ls, label in zip(baseline_cc_schemes, colors, markers, linestyles, baseline_labels):
        metric_list = []
        avg_tput_list = []
        avg_delay_list = []
        loss_list = []
        # for log_file in natural_sort(glob.glob(os.path.join(save_dir,
        #     "rand_{}".format(metric), "*", "{}_datalink_run1.log".format(cc)))):
        for log_file in natural_sort(glob.glob(os.path.join(save_dir,
                                                            "{}_datalink_run1.log".format(cc)))):
            print(log_file)
            # metric_val = float(os.path.dirname(log_file).split('_')[-1])
            tunnel_graph = TunnelGraph(log_file)
            tunnel_graph.parse_tunnel_log()
            avg_tput = np.mean(tunnel_graph.egress_tput[1])
            avg_delay = np.mean(tunnel_graph.delays[1])
            # metric_list.append(metric_val)
            avg_tput_list.append(avg_tput)
            avg_delay_list.append(avg_delay)
            loss_list.append(tunnel_graph.loss_rate[1])
        sorted_idxes = np.argsort(metric_list)
        metric_list = np.array(metric_list)[sorted_idxes]
        if metric == "loss":
            metric_list *= 100
        scores = np.log(avg_tput_list) - np.log(avg_delay_list)
        # scores = scores[sorted_idxes]
        rewards = pcc_aurora_reward(np.array(avg_tput_list) * 1e6 / 8 / 1500,
                                    np.array(avg_delay_list)/100, np.array(loss_list))
        # rewards = rewards[sorted_idxes]
        baseline_scores.append(np.mean(scores))
        baseline_rewards.append(np.mean(rewards))
        # plt.plot(metric_list, scores, c=color, marker=marker, ls=ls, label=label)
    baseline_bars = plt.bar(np.arange(len(baseline_scores)) * 0.7,
                            baseline_scores, width=BAR_WIDTH, label='baseline')
    # baseline_bars = plt.bar(np.arange(len(baseline_rewards)) * 0.7, baseline_rewards, width=BAR_WIDTH,
    #         label='baseline')
    for bar, pat in zip(baseline_bars, ('', '/', '.')):
        bar.set_hatch(pat)

    for cc, color, marker, ls, label in zip(udr_cc_schemes, colors, markers, linestyles, udr_labels):
        metric_list = []
        avg_tput_list = []
        avg_delay_list = []
        loss_list = []
        # for log_file in natural_sort(glob.glob(os.path.join(save_dir,
        #     "rand_{}".format(metric), "*", "{}_datalink_run1.log".format(cc)))):
        for log_file in natural_sort(glob.glob(os.path.join(save_dir, "{}_datalink_run1.log".format(cc)))):
            print(log_file)
            # metric_val = float(os.path.dirname(log_file).split('_')[-1])
            tunnel_graph = TunnelGraph(log_file)
            tunnel_graph.parse_tunnel_log()
            avg_tput = np.mean(tunnel_graph.egress_tput[1])
            avg_delay = np.mean(tunnel_graph.delays[1])
            # metric_list.append(metric_val)
            avg_tput_list.append(avg_tput)
            avg_delay_list.append(avg_delay)
            loss_list.append(tunnel_graph.loss_rate[1])
        sorted_idxes = np.argsort(metric_list)
        metric_list = np.array(metric_list)[sorted_idxes]
        if metric == "loss":
            metric_list *= 100
        scores = np.log(avg_tput_list) - np.log(avg_delay_list)
        # scores = scores[sorted_idxes]
        udr_scores.append(np.mean(scores))
        rewards = 10 * np.array(avg_tput_list) * 1e6 / 8 / 1500 - \
            np.array(avg_delay_list) - 2000 * np.array(loss_list)
        # rewards = rewards[sorted_idxes]
        udr_rewards.append(np.mean(rewards))
        # plt.plot(metric_list, scores, c=color, marker=marker, ls=ls, label=label)
    udr_bars = plt.bar(len(baseline_cc_schemes) + np.arange(len(udr_scores)) * 0.7, udr_scores,
                       width=BAR_WIDTH)
    # udr_bars = plt.bar(len(baseline_cc_schemes) + np.arange(len(udr_rewards)) * 0.7, udr_rewards,
    # width=BAR_WIDTH)
    for bar, pat in zip(udr_bars, ('', '/', '.')):
        bar.set_hatch(pat)
    plt.title(metric)

    # plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
    #             mode="expand", borderaxespad=0, ncol=2)
    plt.legend(baseline_bars + udr_bars, baseline_labels + udr_labels)
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05),
    #       fancybox=True, shadow=True, ncol=2)
    # plt.xlabel(xlabel)
    # plt.ylabel("log(throughput) - log(delay)")
    plt.ylabel("reward")
    # plt.savefig("new_rand_{}_bar_score.png".format(metric))
    # plt.tight_layout()
    plt.close()
