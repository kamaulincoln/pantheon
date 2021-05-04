
import argparse
import os

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

from drivers.flow import Flow
from drivers.utils import pcc_aurora_reward
from src.analysis.tunnel_graph import TunnelGraph


def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser("Test UDR models in simulator.")
    parser.add_argument("--log-file", type=str, default=[], nargs="+",
                        help="Path to congestion control.")
    parser.add_argument("--save-dir", type=str, default="",
                        help="Path to save.")
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
    # args = parse_args()
    for cc in ['aurora', 'cubic']:
        rewards = []
        send_rates = []
        tputs = []
        rtts = []
        losses = []
        for i in range(5):
            # log_file = "/home/zxxia/Projects/pantheon/test_remote4/run{}/{}_datalink_run1.log".format(i, cc)
            # log_file = "/home/zxxia/Projects/pantheon/test_aurora_in_mahimahi/run{}/{}_datalink_run1.log".format(i, cc)
            log_file = "/home/zxxia/Projects/pantheon/test_aws_new/run{}/{}_datalink_run1.log".format(i, cc)
            if not os.path.exists(log_file):
                continue
            flow = Flow(log_file)
            acklink_log_file = os.path.basename(
                log_file).replace("datalink", "acklink")
            acklink_flow = Flow(os.path.join(
                os.path.dirname(log_file), acklink_log_file))
            reward = pcc_aurora_reward(
                flow.avg_throughput * 1e6 / 8 / 1500,
                (np.mean(flow.one_way_delay) +
                 np.mean(acklink_flow.one_way_delay)) / 1000,
                flow.loss_rate)

            send_rates.append(flow.avg_sending_rate)
            rewards.append(reward)
            tputs.append(flow.avg_throughput)
            rtts.append(np.mean(flow.one_way_delay) + np.mean(acklink_flow.one_way_delay))
            losses.append(flow.loss_rate)
        print('{}: send rate={:.3f}Mbps, throughput={:.3f}Mbps, latency={:.3f}ms, loss={:.3f}, reward={:.3f}'.format(cc, np.mean(send_rates), np.mean(tputs), np.mean(rtts), np.mean(losses), np.mean(rewards)))
        # fig, axes = plt.subplots(2, 1, figsize=(6, 8))
        # axes[0].plot(np.array(flow.throughput_timestamps) -
        #              min(flow.throughput_timestamps[0],
        #                  flow.sending_rate_timestamps[0]), flow.throughput,
        #              "o-", ms=2, label=flow.cc + " throughput {:.3f}Mbps".format(flow.avg_throughput))
        # axes[0].plot(np.array(flow.sending_rate_timestamps) - min(flow.throughput_timestamps[0],
        #                                                           flow.sending_rate_timestamps[0]), flow.sending_rate, "o-", ms=2,
        #              label=flow.cc + " sending rate {:.3f}Mbps".format(flow.avg_sending_rate))
        # if isinstance(flow.avg_link_capacity, float):
        #     axes[0].plot(
        #         np.array(flow.link_capacity_timestamps) - min(flow.throughput_timestamps[0],
        #                                                       flow.sending_rate_timestamps[0]), flow.link_capacity,  # "o-",
        #         label="Link bandwidth avg {:.3f}Mbps".format(flow.avg_link_capacity))
        #
        # axes[0].set_xlabel("Second")
        # axes[0].set_ylabel("Mbps")
        # axes[0].set_title(flow.cc + " loss = {:.4f}, reward = {:.3f}".format(
        #     flow.loss_rate, reward))
        # axes[0].legend()
        # axes[0].set_xlim(0, )
        #
        # axes[1].plot(
        #     np.array(flow.one_way_delay_timestamps) - min(flow.throughput_timestamps[0],
        #                                                   flow.sending_rate_timestamps[0]),
        #     (np.array(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay)), "o-", ms=2,
        #     label=flow.cc + " RTT avg {:.3f}ms".format(
        #         np.mean(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay)))
        # axes[1].set_xlabel("Second")
        # axes[1].set_ylabel("Millisecond")
        # axes[1].set_title(flow.cc + " loss = {:.4f}, reward = {:.3f}".format(
        #     flow.loss_rate, reward))
        # axes[1].legend()
        # axes[1].set_xlim(0, )
        # print("{} delay {}ms, througput {}mbps, loss_rate {}, "
        #       "sending rate {}mbps, reward {}".format(
        #           log_file, np.mean(flow.one_way_delay) +
        #           np.mean(acklink_flow.one_way_delay),
        #           flow.avg_throughput, flow.loss_rate, flow.avg_sending_rate, reward))
        # fig.tight_layout()
        # fig.savefig(os.path.join(args.save_dir,
        #             "tmp_{}_time_series.png".format(flow.cc)))
        #
        # plt.close()


if __name__ == "__main__":
    main()
