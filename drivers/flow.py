import os
import numpy as np
from src.analysis.tunnel_graph import TunnelGraph
from drivers.utils import pcc_aurora_reward


class Flow():
    """One way flow of the network connection."""

    def __init__(self, log_path, ms_per_bin=500):
        self.tunnel_graph = TunnelGraph(log_path, ms_per_bin=ms_per_bin)
        self.tunnel_graph.parse_tunnel_log()
        self.cc = str(os.path.basename(log_path).split("_")[0])
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
        """Return througput timestamps in second."""
        return self.tunnel_graph.link_capacity_t

    @property
    def link_capacity(self):
        """Return throuhgput in Mbps."""
        return self.tunnel_graph.link_capacity

    @property
    def avg_link_capacity(self):
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
        return self.tunnel_graph.loss_rate[1]


class Connection:
    """Connection contains an uplink flow and downlink flow."""

    def __init__(self, trace_file):
        self.datalink = Flow(trace_file)
        self.acklink = Flow(trace_file.replace('datalink', 'acklink'))

    @property
    def rtt(self):
        return (np.min(self.datalink.one_way_delay) + np.min(self.acklink.one_way_delay)) / 2

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
            pkt_per_ms = bw * 1e6 / 8 / 1500 / 1000

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
