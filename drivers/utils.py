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


def pcc_aurora_reward(throughput, delay, loss):
    """Compute PCC Aurora reward.

    Args
        throughput: packets per second
        delay: second
        loss:
    """
    return 10 * throughput - 1000 * delay - 2000 * loss
