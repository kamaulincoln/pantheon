#!/usr/bin/env python
import argparse
import os

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

from drivers.utils import pcc_aurora_reward
from drivers.flow import Flow, Connection


def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser("Test UDR models in simulator.")
    parser.add_argument("--log-file", type=str, default=[], nargs="+",
                        help="Path to congestion control.")
    parser.add_argument("--trace-file", type=str, default=None,
                        help="Path to congestion control.")
    parser.add_argument("--save-dir", type=str, default="",
                        help="Path to save.")
    return parser.parse_args()


def main():
    args = parse_args()
    for log_idx, log_file in enumerate(args.log_file):
        # print(log_file)
        if not os.path.exists(log_file):
            if log_idx == 0:
                print "{},,,,,".format(os.path.dirname(log_file)),
            continue
        try:
            flow = Flow(log_file)
            acklink_log_file = os.path.basename(
                log_file).replace("datalink", "acklink")
            acklink_flow = Flow(os.path.join(
                os.path.dirname(log_file), acklink_log_file))
        except RuntimeError:
            return
        # avg_bw = np.mean([val for ts, val in zip(flow.link_capacity_timestamps, flow.link_capacity) if ts >= min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0])])
        fig, axes = plt.subplots(2, 1, figsize=(6, 8))
        reward = pcc_aurora_reward(
            # flow.avg_throughput/avg_bw,#* 1e6 / 8 / 1500,
            flow.avg_throughput * 1e6 / 8 / 1500,
            (np.mean(flow.one_way_delay) +
             np.mean(acklink_flow.one_way_delay)) / 1000,
            flow.loss_rate)

        # t_offset = min(flow.throughput_timestamps[0],
        #                flow.sending_rate_timestamps[0])
        t_offset = 0
        t_max = 40  # max(flow.throughput_timestamps[-1], flow.sending_rate_timestamps[-1],
                    #flow.one_way_delay_timestamps[-1]) - t_offset

        axes[0].plot(np.array(flow.throughput_timestamps) - t_offset,
                     flow.throughput, "o-", ms=2,
                     label=flow.cc + " throughput {:.3f}Mbps".format(
                         flow.avg_throughput))
        axes[0].plot(np.array(flow.sending_rate_timestamps) - t_offset,
                     flow.sending_rate, "o-", ms=2,
                     label=flow.cc + " sending rate {:.3f}Mbps".format(
                         flow.avg_sending_rate))

        # if flow.cc == 'aurora':
        #     aurora_binwise_log = {
        #             'send_rate_ts': (np.array(flow.sending_rate_timestamps) - min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0])).tolist(),
        #             'send_rate': flow.sending_rate}
        #     write_json_file(os.path.join(args.save_dir, 'aurora_binwise_log.json'), aurora_binwise_log)
 # - min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0])
        if isinstance(flow.avg_link_capacity, float):
            axes[0].plot(
                np.array(flow.link_capacity_timestamps) - t_offset,
                flow.link_capacity, "o-",
                label="Link bandwidth avg {:.3f}Mbps".format(flow.avg_link_capacity))

            # for x, y, val in zip(np.array(flow.link_capacity_timestamps) - min(flow.throughput_timestamps[0], flow.sending_rate_timestamps[0]), flow.link_capacity, flow.link_capacity):
            #     axes[0].annotate(str(round(val, 2)), (x, y))

        if args.trace_file:
            trace = Connection(args.trace_file)
            min_rtt = trace.min_rtt
        else:
            min_rtt = -1
        #     trace = Flow(args.trace_file)
        #     axes[0].plot(
        #         np.array(trace.throughput_timestamps), trace.throughput, "o-",
        #         label="Trace Link bandwidth avg {:.3f}Mbps".format(np.mean(trace.throughput)))

        axes[0].set_xlabel("Second")
        axes[0].set_ylabel("Mbps")
        axes[0].set_title(flow.cc + " loss = {:.4f}, reward = {:.3f}".format(
            flow.loss_rate, reward))
        axes[0].legend()
        axes[0].set_xlim(0, t_max)

        axes[1].plot(
            np.array(flow.one_way_delay_timestamps) - t_offset,
            (np.array(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay)),
            "o-", ms=2,
            label=flow.cc + " RTT avg {:.3f}ms, trace minRtt {:.3f}ms".format(
                np.mean(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay),
                min_rtt))
        axes[1].set_xlabel("Second")
        axes[1].set_ylabel("Millisecond")
        axes[1].set_title(flow.cc + " loss = {:.4f}, reward = {:.3f}".format(
            flow.loss_rate, reward))
        axes[1].legend()
        axes[1].set_xlim(0, t_max)
        # print("{} delay {}ms, througput {}mbps, loss_rate {}, "
        #       "sending rate {}mbps, reward {}".format(
        #           log_file, np.mean(flow.one_way_delay) +
        #           np.mean(acklink_flow.one_way_delay),
        #           flow.avg_throughput, flow.loss_rate, flow.avg_sending_rate, reward))
        if log_idx == 0:
            print "{},{},{},{},{},".format(
                os.path.dirname(log_file),
                np.mean(flow.throughput),
                np.mean(np.array(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay)),
                flow.loss_rate, reward),
        elif log_idx == len(args.log_file) - 1:
            print "{},{},{},{},".format(
                np.mean(flow.throughput),
                np.mean(np.array(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay)),
                flow.loss_rate, reward)
        else:
            print "{},{},{},{},".format(
                np.mean(flow.throughput),
                np.mean(np.array(flow.one_way_delay)+np.mean(acklink_flow.one_way_delay)),
                flow.loss_rate, reward),

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
        fig.savefig(os.path.join(args.save_dir,
                    "{}_time_series.png".format(flow.cc)))

        plt.close()


if __name__ == "__main__":
    main()
