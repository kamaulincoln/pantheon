#!/usr/bin/env python
import argparse
import csv
import os

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from drivers.flow import Connection
from drivers.utils import pcc_aurora_reward


def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser("Test UDR models in simulator.")
    parser.add_argument("--log-file", type=str, default=[], nargs="+",
                        help="Path to congestion control.")
    parser.add_argument("--trace-file", type=str, default=None,
                        help="Path to congestion control.")
    parser.add_argument("--save-dir", type=str, default="",
                        help="Path to save.")
    parser.add_argument("--avg-bw", type=float, default=None,
                        help="average bw in real world.")
    parser.add_argument("--summary-path", type=str, default="",
                        help="Full path to a summary file.")
    return parser.parse_args()


class SummaryManager:

    field_names = ["flow", "trace_avg_bw", "trace_min_rtt",
                   "genet_bbr_tput", "genet_bbr_lat", "genet_bbr_tail_lat",
                   "genet_bbr_loss", "genet_bbr_reward", "genet_bbr_normalized_reward",
                   "genet_cubic_tput", "genet_cubic_lat", "genet_cubic_tail_lat",
                   "genet_cubic_loss", "genet_cubic_reward", "genet_cubic_normalized_reward",
                   "udr1_tput", "udr1_lat", "udr1_tail_lat",
                   "udr1_loss", "udr1_reward", "udr1_normalized_reward",
                   "udr2_tput", "udr2_lat", "udr2_tail_lat",
                   "udr2_loss", "udr2_reward", "udr2_normalized_reward",
                   "udr3_tput", "udr3_lat", "udr3_tail_lat",
                   "udr3_loss", "udr3_reward", "udr3_normalized_reward",
                   "bbr_tput", "bbr_lat", "bbr_tail_lat", "bbr_loss",
                   "bbr_reward", "bbr_normalized_reward",
                   "copa_tput", "copa_lat", "copa_tail_lat", "copa_loss",
                   "copa_reward", "copa_normalized_reward",
                   "cubic_tput", "cubic_lat", "cubic_tail_lat", "cubic_loss",
                   "cubic_reward", "cubic_normalized_reward",
                   "vivace_tput", "vivace_lat", "vivace_tail_lat",
                   "vivace_loss", "vivace_reward", "vivace_normalized_reward",
                   "vivace_loss_tput", "vivace_loss_lat", "vivace_loss_tail_lat",
                   "vivace_loss_loss", "vivace_loss_reward", "vivace_loss_normalized_reward",
                   "vivace_latency_tput", "vivace_latency_lat", "vivace_latency_tail_lat",
                   "vivace_latency_loss", "vivace_latency_reward", "vivace_latency_normalized_reward"]

    def __init__(self, summary_path):
        self.initialized = False

        is_file_exist = not os.path.exists(summary_path)
        if not summary_path:
            return
        self.sum_f = open(summary_path, 'a', 1)
        self.writer = csv.DictWriter(self.sum_f, fieldnames=self.field_names,
                                     lineterminator='\n')
        if is_file_exist:
            self.writer.writeheader()
        self.row2write = {}
        self.initialized = True

    def add_trace_info(self, trace_file, avg_bw, min_rtt, min_bw, max_bw):
        if not self.initialized:
            return
        self.row2write['flow'] = trace_file
        self.row2write['trace_min_bw'] = min_bw
        self.row2write['trace_max_bw'] = max_bw
        self.row2write['trace_avg_bw'] = avg_bw
        self.row2write['trace_min_rtt'] = min_rtt

    def add_cc_perf(self, cc, tput, avg_lat, tail_lat, loss, reward,
                    normalized_reward, training_name=""):
        if not self.initialized:
            return
        if cc == 'aurora':
            self.row2write['{}_tput'.format(training_name)] = tput
            self.row2write['{}_lat'.format(training_name)] = avg_lat
            self.row2write['{}_tail_lat'.format(training_name)] = tail_lat
            self.row2write['{}_loss'.format(training_name)] = loss
            self.row2write['{}_reward'.format(training_name)] = reward
            self.row2write['{}_normalized_reward'.format(training_name)] = normalized_reward
        else:
            self.row2write['{}_tput'.format(cc)] = tput
            self.row2write['{}_lat'.format(cc)] = avg_lat
            self.row2write['{}_tail_lat'.format(cc)] = tail_lat
            self.row2write['{}_loss'.format(cc)] = loss
            self.row2write['{}_reward'.format(cc)] = reward
            self.row2write['{}_normalized_reward'.format(cc)] = normalized_reward

    def writerow(self):
        if not self.initialized:
            return
        for k, v in self.row2write.items():
            if v != "":
                self.writer.writerow(self.row2write)
                break
        self.row2write = {}

    def close(self):
        if not self.initialized:
            return
        self.sum_f.close()
        self.initialized = False


def main():
    args = parse_args()
    summary_mngr = SummaryManager(args.summary_path)
    if args.trace_file:
        trace = Connection(args.trace_file)
        trace_min_rtt = trace.min_rtt
    else:
        trace_min_rtt = -1
    for log_idx, log_file in enumerate(args.log_file):
        print(log_file)
        if not os.path.exists(log_file):
            print(log_file, "does not exist!")
            continue
        try:
            conn = Connection(log_file, calibrate_timestamps=True)
        except (RuntimeError, ValueError) as e:
            print("RuntimeError or ValueError happens", log_file, e)
            continue

        fig, axes = plt.subplots(2, 1, figsize=(6, 8))
        min_bw = conn.min_link_capacity
        max_bw = conn.max_link_capacity
        if args.avg_bw:
            avg_bw = args.avg_bw
        else:
            avg_bw = conn.avg_link_capacity
        print(avg_bw)

        summary_mngr.add_trace_info(os.path.dirname(log_file), avg_bw,
                                    trace_min_rtt, min_bw, max_bw)
        reward = pcc_aurora_reward(
            conn.avg_throughput * 1e6 / 8 / 1500,
            conn.avg_rtt / 1000, conn.loss_rate)
        normalized_reward = pcc_aurora_reward(
            conn.avg_throughput * 1e6 / 8 / 1500, conn.avg_rtt / 1000,
            conn.loss_rate, avg_bw * 1e6 / 8 / 1500, trace_min_rtt / 1000)

        if conn.cc == 'aurora':
            training_name = os.path.basename(os.path.dirname(log_file))
        else:
            training_name = ""
        print(log_file, conn.cc, training_name)

        summary_mngr.add_cc_perf(conn.cc, conn.avg_throughput, conn.avg_rtt,
                                     conn.percentile_rtt, conn.loss_rate, reward,
                                     normalized_reward, training_name)

        # max(flow.throughput_timestamps[-1], flow.sending_rate_timestamps[-1],
        t_max = 40

        axes[0].plot(conn.throughput_timestamps, conn.throughput, "o-", ms=2,
                     label=conn.cc + " throughput {:.3f}Mbps".format(
                         conn.avg_throughput))
        axes[0].plot(conn.sending_rate_timestamps, conn.sending_rate, "o-",
                     ms=2, label=conn.cc + " sending rate {:.3f}Mbps".format(
                         conn.avg_sending_rate))

        if isinstance(conn.avg_link_capacity, float):
            axes[0].plot(conn.link_capacity_timestamps, conn.link_capacity,
                         "o-", label="Link bandwidth avg {:.3f}Mbps".format(
                             conn.avg_link_capacity))

        axes[0].set_xlabel("Second")
        axes[0].set_ylabel("Mbps")
        axes[0].set_title(conn.cc + " loss={:.4f}, reward={:.3f}, normalized reward={:.3f}".format(
            conn.loss_rate, reward, normalized_reward))
        axes[0].legend()
        axes[0].set_xlim(0, t_max)

        axes[1].plot(conn.rtt_timestamps, conn.rtt, "o-", ms=2,
                     label=conn.cc + " RTT avg {:.3f}ms, trace minRtt {:.3f}ms".format(
                         conn.avg_rtt, trace_min_rtt))
        axes[1].set_xlabel("Second")
        axes[1].set_ylabel("Millisecond")
        axes[1].set_title(conn.cc + " loss={:.4f}, reward={:.3f}, normalized reward={:.3f}".format(
            conn.loss_rate, reward, normalized_reward))
        axes[1].legend()
        axes[1].set_xlim(0, t_max)

        # noises = sorted(np.array(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay) - 100)
        # cdf = np.array([i/float(len(noises)) for i in range(len(noises))])
        # print(cdf)
        # axes[2].plot(noises, cdf, "o-", ms=2,
        #         label=flow.cc + " RTT avg {:.3f}ms, trace min Rtt {:.3f}ms".format(
        #         np.mean(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay), min_rtt))
        # axes[2].set_xlabel("Noise Millisecond")
        # axes[2].set_ylabel("CDF")
        # axes[2].legend()
        # axes[2].set_xlim(0, )
        # axes[2].set_ylim(0, 1)
        fig.tight_layout()
        # if conn.cc == 'aurora':
        #     fig.savefig(os.path.join(args.save_dir,
        #                 "{}_time_series_30s.png".format(training_name)))
        # else:
        fig.savefig(os.path.join(args.save_dir,
                    "{}_time_series_30s.png".format(conn.cc)))

        plt.close()

    summary_mngr.writerow()
    summary_mngr.close()


if __name__ == "__main__":
    main()
