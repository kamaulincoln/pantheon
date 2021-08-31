import json
import re

import numpy as np


def natural_sort(l):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def learnability_objective_function(throughput, delay):
    """Objective function used in https://cs.stanford.edu/~keithw/www/Learnability-SIGCOMM2014.pdf
    throughput: Mbps
    delay: ms
    """
    raise NotImplementedError
    # score = np.log(np.array(throughput)) - np.log(np.array(delay))
    # # print(throughput, delay, score)
    # score = score.replace([np.inf, -np.inf], np.nan).dropna()
    #
    # return score


def pcc_aurora_reward(throughput, delay, loss, avg_bw=None, min_rtt=None):
    """Compute PCC Aurora reward.

    Return Aurora paper reward if avg_bw or(inclusive) min_rtt is None.
    Otherwise, return normalized reward.

    Args
        throughput: packets per second
        delay: second
        loss: packet loss rate
        avg_bw: average bandwidth of the network trace (packets per second)
        min_rtt: min rtt of the network trace (second)
    """
    # 50 packets per second = 0.6Mbps and 10ms are treated as anchor point
    if avg_bw is None and min_rtt is None:
        return 10 * throughput  - 1000 * delay - 2000 * loss
    elif avg_bw is not None and min_rtt is None:
        return 10 * 50 * throughput / avg_bw - 1000 * delay - 2000 * loss
    elif avg_bw is None and min_rtt is not None:
        return 10 * 50 * throughput - 1000 * delay / min_rtt - 2000 * loss
    else:
        # return 10 * 50 * throughput / avg_bw - 1000 * 0.1 * delay / min_rtt - 500 * loss
        return 10 * 50 * throughput / avg_bw - 1000 * delay - 2000 * loss


def read_json_file(filename):
    """Load json object from a file."""
    with open(filename, 'r') as f:
        content = json.load(f)
    return content


def write_json_file(filename, content):
    """Dump into a json file."""
    with open(filename, 'w') as f:
        json.dump(content, f, indent=4)

def compute_std_of_mean(data):
    return np.std(data) / np.sqrt(len(data))
