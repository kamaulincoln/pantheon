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


def pcc_aurora_reward(throughput, delay, loss, ):
    """Compute PCC Aurora reward.

    Args
        throughput: packets per second
        delay: second
        loss:
    """
    return 10 * 50 * throughput  - 1000 * delay - 2000 * loss


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
