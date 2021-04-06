#!/usr/bin/env python
import argparse
from drivers.flow import Flow
from drivers.utils import pcc_aurora_reward
from src.analysis.tunnel_graph import TunnelGraph
import sys
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib
matplotlib.use('agg')
# sys.path.insert(0, '/home/zxxia/pantheon/src/analysis')


def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser("Test UDR models in simulator.")
    parser.add_argument("--log-file", type=str, default=[], nargs="+",
                        help="Path to congestion control.")
    return parser.parse_args()


def plot_throughput(save_dir, cc_schemes=[]):
    for cc in cc_schemes:
        tunnel_graph = TunnelGraph(os.path.join(
            save_dir, "{}_datalink_run1.log".format(cc)))
        tunnel_graph.parse_tunnel_log()
        print(tunnel_graph.egress_t.keys())
        plt.plot(tunnel_graph.egress_t[1],
                 tunnel_graph.egress_tput[1], label=cc)
    plt.legend()


def main():
    args = parse_args()
    for log_file in args.log_file:
        flow = Flow(log_file)
        fig, axes = plt.subplots(2, 1, figsize=(6, 8))
        reward = pcc_aurora_reward(flow.avg_throughput * 1e6 / 8 / 1500,
                                   (np.mean(flow.one_way_delay) + 50) / 1000,
                                   flow.loss_rate)
        axes[0].plot(np.array(flow.throughput_timestamps) - min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0]), flow.throughput, "o-",
                     ms=2,
                     label=flow.cc + " throughput {:.3f}Mbps".format(flow.avg_throughput))
        axes[0].plot(np.array(flow.sending_rate_timestamps) - min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0]), flow.sending_rate, "o-",
                     ms=2,
                     label=flow.cc + " sending rate {:.3f}Mbps".format(flow.avg_sending_rate))
        axes[0].plot(np.array(flow.link_capacity_timestamps) - min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0]), flow.link_capacity,  # "o-",
                label="Link bandwidth avg {:.3f}Mbps".format(flow.avg_link_capacity))

        axes[0].set_xlabel("Second")
        axes[0].set_ylabel("Mbps")
        axes[0].set_title(flow.cc + " loss = {:.4f}, reward = {:.3f}".format(
            flow.loss_rate, reward))
        axes[0].legend()
        axes[0].set_xlim(0, )

        axes[1].plot(np.array(flow.one_way_delay_timestamps) - min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0]), (np.array(flow.one_way_delay)+50), "o-",
                     ms=5,
                     label=flow.cc + " RTT(Uplink Delay + 50) avg {:.3f}ms".format(np.mean(flow.one_way_delay)+50))
        axes[1].set_xlabel("Second")
        axes[1].set_ylabel("Millisecond")
        axes[1].set_title(flow.cc + " loss = {:.4f}, reward = {:.3f}".format(
            flow.loss_rate, reward))
        axes[1].legend()
        axes[1].set_xlim(0, )
        print("{} delay {}ms, througput {}mbps, loss_rate {}, "
              "sending rate {}mbps, reward {}".format(
                  log_file, np.mean(flow.one_way_delay)+50, flow.avg_throughput,
                  flow.loss_rate, flow.avg_sending_rate, reward))
        fig.tight_layout()
        fig.savefig("tmp_{}_time_series.png".format(flow.cc))

        plt.close()


if __name__ == "__main__":
    main()
