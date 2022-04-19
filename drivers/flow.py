import os
import numpy as np
from src.analysis.tunnel_graph import TunnelGraph
from drivers.utils import pcc_aurora_reward


def extract_cc_name(log_path):
    """Exact congestion control name from log path.

    Args
        log_path: path to \\{cc\\}_datalink_run\\{run_id\\}.log or
                  \\{cc\\}_acklink_run\\{run_id\\}.log
    """
    tokens = os.path.basename(log_path).split("_")
    cc_tokens = []
    for token in tokens:
        if token == "datalink" or token == "acklink":
            break
        cc_tokens.append(token)
    return "_".join(cc_tokens)


class Flow():
    """One way flow of the network connection."""

    def __init__(self, log_path, ms_per_bin=500):
        self.tunnel_graph = TunnelGraph(log_path, ms_per_bin=ms_per_bin)
        self.tunnel_graph.parse_tunnel_log()
        self.cc = extract_cc_name(log_path)
        self.ms_per_bin = ms_per_bin

        if (1 not in self.tunnel_graph.egress_t or
            1 not in self.tunnel_graph.egress_tput or
            1 not in self.tunnel_graph.avg_egress or
            1 not in self.tunnel_graph.ingress_t or
            1 not in self.tunnel_graph.ingress_tput or
            1 not in self.tunnel_graph.avg_ingress or
            1 not in self.tunnel_graph.delays_t or
            1 not in self.tunnel_graph.delays or
                1 not in self.tunnel_graph.loss_rate):
            raise RuntimeError("Invalid format {}".format(log_path))

    @property
    def link_capacity_timestamps(self):
        """Return link capacity timestamps in second."""
        return self.tunnel_graph.link_capacity_t

    @property
    def link_capacity(self):
        """Return link capacity in Mbps."""
        return self.tunnel_graph.link_capacity

    @property
    def avg_link_capacity(self):
        """Return average link capacity in Mbps."""
        return self.tunnel_graph.avg_capacity

    @property
    def throughput_timestamps(self):
        """Return througput timestamps in second."""
        return self.tunnel_graph.egress_t[1]

    @property
    def throughput(self):
        """Return throuhgput in Mbps."""
        return self.tunnel_graph.egress_tput[1]

    @property
    def avg_throughput(self):
        """Return average throuhgput in Mbps."""
        return self.tunnel_graph.avg_egress[1]

    @property
    def sending_rate_timestamps(self):
        """Return sending rate timestamps in second."""
        return self.tunnel_graph.ingress_t[1]

    @property
    def sending_rate(self):
        """Return sending rate in Mbps."""
        return self.tunnel_graph.ingress_tput[1]

    @property
    def avg_sending_rate(self):
        return self.tunnel_graph.avg_ingress[1]

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
        """Return loss rate."""
        return self.tunnel_graph.loss_rate[1]

    @property
    def percentile_delay(self):
        """Return 95 percentile one-way delay in millisecond.(Tail latency)"""
        return self.tunnel_graph.percentile_delay[1]


class Connection:
    """Connection contains an uplink flow and a downlink flow."""

    def __init__(self, trace_file, calibrate_timestamps=False):
        self.datalink = Flow(trace_file)
        trace_file_basename = os.path.basename(trace_file)
        trace_file_dirname = os.path.dirname(trace_file)
        self.acklink = Flow(os.path.join(
            str(trace_file_dirname),
            str(trace_file_basename.replace("datalink", "acklink"))))
        if calibrate_timestamps:
            self.t_offset = min(self.datalink.throughput_timestamps[0],
                                self.datalink.sending_rate_timestamps[0])
        else:
            self.t_offset = 0

    @property
    def cc(self):
        """Return congestion control algorithm of the network connection."""
        return self.datalink.cc

    @property
    def link_capacity_timestamps(self):
        """Return througput timestamps in second."""
        return[ts - self.t_offset for ts in self.datalink.link_capacity_timestamps]

    @property
    def link_capacity(self):
        """Return datalink capacity in Mbps."""
        return self.datalink.link_capacity

    @property
    def avg_link_capacity(self):
        """Return average datalink capacity in Mbps."""
        return np.mean([val for ts, val in
                        zip(self.datalink.link_capacity_timestamps,
                            self.datalink.link_capacity) if ts >= self.t_offset])

    @property
    def min_link_capacity(self):
        """Return average datalink capacity in Mbps."""
        return min([val for ts, val in
                        zip(self.datalink.link_capacity_timestamps,
                            self.datalink.link_capacity) if ts >= self.t_offset])

    @property
    def max_link_capacity(self):
        """Return average datalink capacity in Mbps."""
        return max([val for ts, val in
                        zip(self.datalink.link_capacity_timestamps,
                            self.datalink.link_capacity) if ts >= self.t_offset])

    @property
    def throughput_timestamps(self):
        """Return througput timestamps in second."""
        return [ts - self.t_offset for ts in self.datalink.throughput_timestamps]

    @property
    def throughput(self):
        """Return throuhgput in Mbps."""
        return self.datalink.throughput

    @property
    def avg_throughput(self):
        """Return average throughput in Mbps."""
        return self.datalink.avg_throughput

    @property
    def sending_rate_timestamps(self):
        """Return sending rate timestamps in second."""
        return [ts - self.t_offset for ts in self.datalink.sending_rate_timestamps]

    @property
    def sending_rate(self):
        """Return sending rate in Mbps."""
        return self.datalink.sending_rate

    @property
    def avg_sending_rate(self):
        """Return average sending rate in Mbps."""
        return self.datalink.avg_sending_rate

    @property
    def datalink_delay_timestamps(self):
        """Return datalink's one-way delay timestamps in second."""
        return [ts - self.t_offset for ts in self.datalink.one_way_delay_timestamps]

    @property
    def datalink_delay(self):
        """Return datalink's one-way delay in millisecond."""
        return self.datalink.one_way_delay

    @property
    def acklink_delay_timestamps(self):
        """Return acklink's one-way delay timestamps in second."""
        return [ts - self.t_offset for ts in self.acklink.one_way_delay_timestamps]

    @property
    def acklink_delay(self):
        """Return acklink's one-way delay in millisecond."""
        return self.acklink.one_way_delay

    @property
    def loss_rate(self):
        """Return packet loss rate of the connection."""
        return self.datalink.loss_rate

    @property
    def min_one_way_delay(self):
        """Return the estimate of minimum of one way delay.

        Used to extract min one-way delay from real trace to set delay in Mahimahi.
        """
        return self.min_rtt / 2

    @property
    def min_rtt(self):
        """Return miniumum RTT of the connection in millisecond."""
        return np.min(self.datalink.one_way_delay) + np.min(self.acklink.one_way_delay)

    @property
    def rtt_timestamps(self):
        """Return RTT timestamps of the connection in millisecond."""
        return self.datalink_delay_timestamps

    @property
    def rtt(self):
        """Return RTT of the connection in millisecond."""
        avg_acklink_delay = np.mean(self.acklink.one_way_delay)
        rtt = [val + avg_acklink_delay for val in self.datalink.one_way_delay]
        return rtt

    @property
    def avg_rtt(self):
        """Return average RTT of the connection in millisecond."""
        return np.mean(self.datalink.one_way_delay) + np.mean(self.acklink.one_way_delay)

    @property
    def percentile_rtt(self):
        """Return 95 percentile one-way delay in millisecond.(Tail latency)"""
        return self.datalink.percentile_delay + np.mean(self.acklink.one_way_delay)

    def reward(self, avg_bw=None):
        if avg_bw is None:
            avg_bw = np.mean(
                [val for ts, val in
                 zip(self.datalink.link_capacity_timestamps,
                     self.datalink.link_capacity)
                 if ts >= min(self.datalink.throughput_timestamps[0],
                              self.datalink.sending_rate_timestamps[0])])
        reward = pcc_aurora_reward(
            self.datalink.avg_throughput / avg_bw,  # * 1e6 / 8 / 1500,
            (np.mean(self.datalink.one_way_delay) +
             np.mean(self.acklink.one_way_delay)) / 1000,
            self.datalink.loss_rate)
        return reward

    def to_mahimahi_trace(self):
        """Convert trace to Mahimahi format."""
        timestamps = self.datalink.throughput_timestamps
        bandwidths = self.datalink.throughput

        ms_series = []
        assert len(timestamps) == len(bandwidths)
        ms_t = 0
        for ts, next_ts, bw in zip(timestamps[0:-1], timestamps[1:], bandwidths[0:-1]):
            pkt_per_ms = max(bw, 0.1) * 1e6 / 8 / 1500 / 1000

            ms_cnt = 0
            pkt_cnt = 0
            while True:
                ms_cnt += 1
                ms_t += 1
                to_send = np.floor((ms_cnt * pkt_per_ms) - pkt_cnt)
                for _ in range(int(to_send)):
                    ms_series.append(ms_t)

                pkt_cnt += to_send

                if ms_cnt >= (next_ts - ts) * 1000:
                    break
        return ms_series

    def dump_mahimahi_trace(self, filename):
        """Save trace in mahimahi format to the specified filename."""
        ms_series = self.to_mahimahi_trace()
        with open(filename, 'w', 1) as f:
            for ms in ms_series:
                f.write(str(ms) + '\n')
