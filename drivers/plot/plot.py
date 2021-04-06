#!/usr/bin/env python
from tunnel_graph import TunnelGraph
import sys
import matplotlib.pyplot as plt
import os
import numpy as np
import glob
import matplotlib
matplotlib.use('agg')
sys.path.insert(0, '/home/zxxia/pantheon/src/analysis')
# print(sys.path)


def plot_throughput(save_dir, cc_schemes=[]):
    for cc in cc_schemes:
        tunnel_graph = TunnelGraph(os.path.join(
            save_dir, "{}_datalink_run1.log".format(cc)))
        tunnel_graph.parse_tunnel_log()
        print(tunnel_graph.egress_t.keys())
        plt.plot(tunnel_graph.egress_t[1],
                 tunnel_graph.egress_tput[1], label=cc)
    plt.legend()


class Flow():
    def __init__(self, log_path):
        self.tunnel_graph = TunnelGraph(log_path)
        self.tunnel_graph.parse_tunnel_log()

    @property
    def throughput_timestamps(self):
        """Return througput timestamps in second."""
        return self.tunnel_graph.egress_t[1]

    @property
    def throughput(self):
        """Return throuhgput in Mbps."""
        return self.tunnel_graph.egress_tput[1]

    @property
    def sending_rate_timestamps(self):
        """Return sending rate timestamps in second."""
        return self.tunnel_graph.ingress_t[1]

    @property
    def sending_rate(self):
        """Return sending rate in Mbps."""
        return self.tunnel_graph.ingress_tput[1]

    @property
    def one_way_delay_timestamps(self):
        """Return one-way delay timestamps in second."""
        return self.tunnel_graph.delays_t[1]

    @property
    def one_way_delay(self):
        """Return one-way delay in millisecond."""
        return self.tunnel_graph.delays[1]

    @property
    def loss_rate(self):
        return self.tunnel_graph.loss_rate[1]


# plot_throughput("exp", ["cubic",  "range_0_aurora", "vivace"])
save_dir = "results/rand_5_dims_old"
baseline_cc_schemes = ["cubic",   "sprout", "vivace", ]
# "range_0_aurora", "range_3_aurora", "range_5_aurora"]
colors = ["C0", "C1", "C2", "C3", "C3", "C3"]
markers = ["o", "o", "o", "x", "s", "v"]
linestyles = ["-", "-", "-", "-", "--", "-."]
labels = ["Vivace",  # "Cubic", "Sprout",
          # "Aurora (BW:[1.2, 1.2]Mbps, Delay:[0, 0]ms\nLoss:[0, 0]%, Queue size:[1, 1]pkts)",
          "Aurora (BW:[1.2, 9]Mbps, Delay:[0, 30]ms\nLoss:[0, 4]%, Queue size:[1, 21]pkts)", ]
# "Aurora (BW:[1.2, 21]Mbps, Delay:[0, 70]ms\nLoss:[0, 8]%, Queue size:[1, 1097]pkts)"]

# metrics = ['bandwidth', 'delay', "queue_size", "loss"]
metrics = ["bandwidth"]

for metric, xlabel in zip(metrics,
                          ["Bandwidth (Mbps)", 'One-way delay (ms)', "Uplink queue size (Packets)",
                           "Uplink Loss Rate (%)"]):
    plt.figure()
    for cc, color, marker, ls, label in zip(baseline_cc_schemes, colors, markers, linestyles, labels):
        metric_list = []
        avg_tput_list = []
        avg_delay_list = []
        avg_send_rate_list = []
        for log_file in natural_sort(glob.glob(os.path.join(save_dir,
                                                            "rand_{}".format(metric), "*", "{}_datalink_run1.log".format(cc)))):
            metric_val = float(os.path.dirname(log_file).split('_')[-1])
            tunnel_graph = TunnelGraph(log_file)
            tunnel_graph.parse_tunnel_log()
            avg_send_rate = np.mean(tunnel_graph.ingress_tput[1])
            avg_tput = np.mean(tunnel_graph.egress_tput[1])
            avg_delay = np.mean(tunnel_graph.delays[1])
            metric_list.append(metric_val)
            avg_tput_list.append(avg_tput)
            avg_delay_list.append(avg_delay)
            avg_send_rate_list.append(avg_send_rate)
            # if "bandwidth_30" in log_file and "range_0" in log_file:
            #     print("{}, tput={:.3f}, delay={:.3f}, score={:.3f}".format(log_file, avg_tput, avg_delay, np.log(avg_tput) - np.log(avg_delay)))
            # import pdb
            # pdb.set_trace()
        sorted_idxes = np.argsort(metric_list)
        metric_list = np.array(metric_list)[sorted_idxes]
        if metric == "loss":
            metric_list *= 100
        # print(metric_list)
        # print(avg_tput_list)
        # print(avg_delay_list)
        scores = np.log(avg_tput_list) - np.log(avg_delay_list)
        # scores = np.array(avg_send_rate_list)
        # scores = np.array(avg_tput_list) #) - np.log(avg_delay_list)
        # scores = np.array(avg_delay_list) #) - np.log(avg_delay_list)
        scores = scores[sorted_idxes]
        plt.plot(metric_list, scores, c=color,
                 marker=marker, ls=ls, label=label)
        print(label, scores)
        # print(vivace, scores)
        # plt.plot(metric_list, np.array(avg_tput_list[sorted_idexs], c=color, marker=marker, ls=ls, label=label)
    # plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
    #             mode="expand", borderaxespad=0, ncol=2)
    plt.legend()
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05),
    #       fancybox=True, shadow=True, ncol=2)
    plt.xlabel(xlabel)
    # plt.ylabel("log(throughput) - log(delay)")
    # plt.ylabel("sending rate")
    # plt.ylabel("throughput")
    # plt.ylabel("delay")
    # plt.savefig("delay_rand_{}.png".format(metric))
    # plt.savefig(os.path.join(save_dir, "rand_{}.png".format(metric)))
    # plt.savefig("sending)rate_rand_{}.png".format(metric))
    # plt.tight_layout()
    plt.close()
