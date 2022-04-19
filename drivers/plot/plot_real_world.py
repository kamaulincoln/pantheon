import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from drivers.utils import pcc_aurora_reward, compute_std_of_mean


ROOT = "/Users/zxxia/Project/PCC-RL/results/test_cc"
ROOT = "/Users/zxxia/Project/PCC-RL/results/test_cc_wifi"
ROOT = "/Users/zxxia/Project/PCC-RL/results/test_aurora"
ROOT = "/Users/zxxia/Project/PCC-RL/results/test_aurora_new"
ROOT = "/Users/zxxia/Project/PCC-RL/results/test_wifi_new_1"
ROOT = "/Users/zxxia/Project/PCC-RL/results/test_ethernet"
ROOT = "/Users/zxxia/Project/PCC-RL/results/test_wifi"
ROOT = "/Users/zxxia/Project/PCC-RL/results/test_cellular"


def filter_df(df, keywords2filter=[], row_idx_to_filter=[]):
    df = df.drop(row_idx_to_filter)
    for kw in keywords2filter:
        mask = df['flow'].str.contains(kw)
        df = df[~mask]
    mask = df['trace_avg_bw'] < 1
    df = df[~mask]

    return df


def main():

    data = pd.read_csv(os.path.join(ROOT, "summary.csv"))

    reward_name = "normalized_reward"
    # reward_name = "reward"

    baseline_rewards = [data["bbr_{}".format(reward_name)].mean(),
                        data["copa_{}".format(reward_name)].mean(),
                        data["cubic_{}".format(reward_name)].mean(),
                        data["vivace_loss_{}".format(reward_name)].mean(),
                        data["vivace_latency_{}".format(reward_name)].mean()]
    baseline_reward_errs = [
        data["bbr_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["bbr_{}".format(reward_name)])),
        data["copa_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["copa_{}".format(reward_name)])),
        data["cubic_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["cubic_{}".format(reward_name)])),
        data["vivace_loss_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["vivace_loss_{}".format(reward_name)])),
        data["vivace_latency_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["vivace_latency_{}".format(reward_name)]))]

    udr_rewards = [data["udr1_{}".format(reward_name)].mean(),
                   data["udr2_{}".format(reward_name)].mean(),
                   data["udr3_{}".format(reward_name)].mean()]
    udr_reward_errs = [data["udr1_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["udr1_{}".format(reward_name)])),
                       data["udr2_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["udr2_{}".format(reward_name)])),
                       data["udr3_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["udr3_{}".format(reward_name)]))]

    genet_rewards = [data["genet_bbr_{}".format(reward_name)].mean(), data["genet_cubic_{}".format(reward_name)].mean()]
    genet_reward_errs = [data["genet_bbr_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["genet_bbr_{}".format(reward_name)])),
                         data["genet_cubic_{}".format(reward_name)].std(ddof=0) / np.sqrt(len(data["genet_cubic_{}".format(reward_name)]))]

    # print(baseline_reward_errs)
    print("baseline rewards:", baseline_rewards)
    print("udr rewards", udr_rewards)
    print("genet_rewards", genet_rewards)

    plt.figure(figsize=(10, 8))

    ax = plt.gca()
    width = 0.5

    baseline_bars = ax.bar([0, 0.5, 1, 1.5, 2], baseline_rewards,
                           yerr=baseline_reward_errs, width=width)
    for bar, pat in zip(baseline_bars, ('', '/', '.', '-')):
        bar.set_hatch(pat)
    udr_bars = ax.bar([3, 3.5, 4], udr_rewards,
                      yerr=udr_reward_errs, width=width)
    for bar, pat in zip(udr_bars, ('', '/', '.')):
        bar.set_hatch(pat)
    genet_bar = ax.bar([5.5, 6], genet_rewards,
                       yerr=genet_reward_errs, width=width)

    baseline_labels = ["BBR", "Copa", "Cubic", "Vivace-loss", "Vivace-latency"]
    udr_labels = ["UDR-1", "UDR-2", "UDR-3"]
    plt.legend(baseline_bars + udr_bars + genet_bar, baseline_labels + udr_labels + ["GENET"],
               bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", ncol=4,
               mode='expand')
    plt.xticks([0.5, 2.5, 4.5], ["Classic Baselines",
               "UDR", "GENET"], rotation='horizontal')

    plt.ylabel("Reward")

    # plt.savefig(os.path.join(ROOT, "eval_bars_real_world_ethernet.png"))
    plt.savefig(os.path.join(ROOT, "eval_bars_real_world_wifi.png"))


    print("CC,average throughput,throughput stddev of mean,"
          "average latency,latency stddev of mean,"
          "average tail latency,tail latency stddev of mean,"
          "average loss,loss stddev of mean,reward,reward stddev of mean,"
          "normalized_reward,normalized_reward stddev of mean")  # type:ignore
    for name, cc in zip(['BBR', "Copa", "Cubic", 'Vivace-loss',
                         'Vivace-latency', 'udr1', 'udr2', 'udr3',
                         'genet_bbr', 'genet_cubic'],
                        ['bbr', 'copa', 'cubic', 'vivace_loss',
                         'vivace_latency', 'udr1', 'udr2', 'udr3', 'genet_bbr',
                         'genet_cubic']):
        print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format( # type:ignore
            name, data['{}_tput'.format(cc)].mean(),
            compute_std_of_mean(data['{}_tput'.format(cc)]),
            data['{}_lat'.format(cc)].mean(),
            compute_std_of_mean(data['{}_lat'.format(cc)]),
            data['{}_tail_lat'.format(cc)].mean(),
            compute_std_of_mean(data['{}_tail_lat'.format(cc)]),
            data['{}_loss'.format(cc)].mean(),
            compute_std_of_mean(data['{}_loss'.format(cc)]), # type:ignore
            data['{}_reward'.format(cc)].mean(),
            compute_std_of_mean(data['{}_reward'.format(cc)]),
            data['{}_normalized_reward'.format(cc)].mean(),
            compute_std_of_mean(data['{}_normalized_reward'.format(cc)]))
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'Copa', data['copa_tput'].mean(),
    #     data['copa_lat'].mean(),
    #     data['copa_tail_lat'].mean(),
    #     data['copa_loss'].mean(),
    #     data['copa_reward'].mean(),
    #     data['copa_normalized_reward'].mean())
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'Cubic', data['cubic_tput'].mean(),
    #     data['cubic_lat'].mean(),
    #     data['cubic_tail_lat'].mean(),
    #     data['cubic_loss'].mean(),
    #     data['cubic_reward'].mean(),
    #     data['cubic_normalized_reward'].mean())
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'Vivace-loss', data['vivace_loss_tput'].mean(),
    #     data['vivace_loss_lat'].mean(),
    #     data['vivace_loss_tail_lat'].mean(),
    #     data['vivace_loss_loss'].mean(),
    #     data['vivace_loss_reward'].mean(),
    #     data['vivace_loss_normalized_reward'].mean())
    #
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'Vivace-latency', data['vivace_latency_tput'].mean(),
    #     data['vivace_latency_lat'].mean(),
    #     data['vivace_latency_tail_lat'].mean(),
    #     data['vivace_latency_loss'].mean(),
    #     data['vivace_latency_reward'].mean(),
    #     data['vivace_latency_normalized_reward'].mean())
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'udr_small', data['udr1_tput'].mean(),
    #     data['udr1_lat'].mean(),
    #     data['udr1_tail_lat'].mean(),
    #     data['udr1_loss'].mean(),
    #     data['udr1_reward'].mean(),
    #     data['udr1_normalized_reward'].mean())
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'udr_mid', data['udr2_tput'].mean(),
    #     data['udr2_lat'].mean(),
    #     data['udr2_tail_lat'].mean(),
    #     data['udr2_loss'].mean(),
    #     data['udr2_reward'].mean(),
    #     data['udr2_normalized_reward'].mean())
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'udr_large', data['udr3_tput'].mean(),
    #     data['udr3_lat'].mean(),
    #     data['udr3_tail_lat'].mean(),
    #     data['udr3_loss'].mean(),
    #     data['udr3_reward'].mean(),
    #     data['udr3_normalized_reward'].mean())
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'genet_bbr',
    #     data['genet_bbr_tput'].mean(),
    #     data['genet_bbr_lat'].mean(),
    #     data['genet_bbr_tail_lat'].mean(),
    #     data['genet_bbr_loss'].mean(),
    #     data['genet_bbr_reward'].mean(),
    #     data['genet_bbr_normalized_reward'].mean())
    # print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(# type:ignore
    #     'genet_cubic',
    #     data['genet_cubic_tput'].mean(),
    #     data['genet_cubic_lat'].mean(),
    #     data['genet_cubic_tail_lat'].mean(),
    #     data['genet_cubic_loss'].mean(),
    #     data['genet_cubic_reward'].mean(),
    #     data['genet_cubic_normalized_reward'].mean())


if __name__ == "__main__":
    main()
