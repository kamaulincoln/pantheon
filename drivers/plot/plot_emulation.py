import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from drivers.utils import pcc_aurora_reward


ROOT = "/home/zxxia/Projects/pantheon/results"


def filter_df(df, keywords2filter=[], row_idx_to_filter=[]):
    df = df.drop(row_idx_to_filter)
    for kw in keywords2filter:
        mask = df['flow'].str.contains(kw)
        df = df[~mask]
    mask = df['trace_avg_bw'] < 1
    df = df[~mask]

    return df

def compute_percentage(aurora_df, baseline_df):
    # assert len(aurora_df) == len(baseline_df)
    bbr_cnt = 0
    cubic_cnt = 0
    for i in range(len(aurora_df)):
        # assert os.path.basename(aurora_df.iloc[i]['flow']) == os.path.basename(baseline_df.iloc[i]['flow'])
        # assert os.path.basename(os.path.dirname(aurora_df.iloc[i]['flow'])) == os.path.basename(os.path.dirname(baseline_df.iloc[i]['flow']))
        key = os.path.basename(os.path.dirname(aurora_df.iloc[i]['flow'])) + "/" + os.path.basename(aurora_df.iloc[i]['flow'])
        mask = baseline_df['flow'].str.contains(key)

        if aurora_df.iloc[i]['aurora_normalized_reward'] >= baseline_df[mask].iloc[0]['bbr_normalized_reward']:
            bbr_cnt+=1
        if aurora_df.iloc[i]['aurora_normalized_reward'] >= baseline_df[mask].iloc[0]['cubic_normalized_reward']:
            cubic_cnt+=1
        # if aurora_df.iloc[i]['aurora_normalized_reward'] >= baseline_df.iloc[i]['bbr_normalized_reward']:
        #     bbr_cnt+=1
        # if aurora_df.iloc[i]['aurora_normalized_reward'] >= baseline_df.iloc[i]['cubic_normalized_reward']:
        #     cubic_cnt+=1
        # print(aurora_df.iloc[i]['aurora_normalized_reward'], baseline_df.iloc[i]['bbr_normalized_reward'])
    return bbr_cnt / float(len(aurora_df)), cubic_cnt / float(len(aurora_df))

def main():

    udr_small_data = pd.read_csv(os.path.join(
        ROOT,
        "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_small",
        "summary_ignore_start_effect.csv"))

    udr_mid_data = pd.read_csv(os.path.join(
        ROOT,
        "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_mid",
        "summary_ignore_start_effect.csv"))

    udr_large_data = pd.read_csv(os.path.join(
        ROOT,
        "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_large",
        "summary_ignore_start_effect.csv"))

    genet_data = pd.read_csv(os.path.join(
        ROOT,
        "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt",
        "summary_ignore_start_effect.csv"))

    genet_bbr_data = pd.read_csv(os.path.join(
        ROOT, "emu_real_cellular_traces", "test_3_genet_new", "queue50", 'genet3',
        "summary_ignore_start_effect.csv"))
    baseline_data = pd.read_csv(os.path.join(
        ROOT, "test_real_traces_0701_recv_ratio_queue50", "summary_ignore_start_effect.csv"))
    # udr_small_data = pd.read_csv(os.path.join(
    #     ROOT,
    #     "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_small",
    #     "summary.csv"))
    #
    # udr_mid_data = pd.read_csv(os.path.join(
    #     ROOT,
    #     "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_mid",
    #     "summary.csv"))
    #
    # udr_large_data = pd.read_csv(os.path.join(
    #     ROOT,
    #     "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt_large",
    #     "summary.csv"))
    #
    # genet_data = pd.read_csv(os.path.join(
    #     ROOT,
    #     "test_real_traces_0701_recv_ratio_queue50_fix_send_rate_smooth_rtt",
    #     "summary_scale_30s.csv"))
    #
    # baseline_data = pd.read_csv(os.path.join(
    #     ROOT, "test_real_traces_0701_recv_ratio_queue50", "summary_scale_30s.csv"))
    keywords = ["China", "bbr_datalink", ]
    idx_2_drop = [0, 7]
    udr_small_data = filter_df(udr_small_data, keywords, idx_2_drop)
    udr_mid_data = filter_df(udr_mid_data, keywords, idx_2_drop)
    udr_large_data = filter_df(udr_large_data, keywords, idx_2_drop)
    genet_data = filter_df(genet_data, keywords, idx_2_drop)
    genet_bbr_data = filter_df(genet_bbr_data, keywords, idx_2_drop)
    baseline_data = filter_df(baseline_data, keywords, idx_2_drop)

    print("BBR reward count: {}, Copa reward count: {}, Cubic reward count: {}, "
          "Vivace reward count: {}, UDR1 reward count: {}, "
          "UDR2 reward count: {}, UDR3 reward count: {}, GENET reward count: {}, GENET bbr reward count: {}".format(
              len(baseline_data['bbr_normalized_reward']),
              len(baseline_data['copa_normalized_reward']),
              len(baseline_data['cubic_normalized_reward']),
              len(baseline_data['vivace_normalized_reward']),
              len(udr_small_data["aurora_normalized_reward"]),
              len(udr_mid_data["aurora_normalized_reward"]),
              len(udr_large_data["aurora_normalized_reward"]),
              len(genet_data["aurora_normalized_reward"]),
              len(genet_bbr_data["aurora_normalized_reward"])))

    reward_name = "normalized_reward"
    baseline_data['bbr_{}'.format(reward_name)] = pcc_aurora_reward(
        baseline_data['bbr_tput'] * 1e6 / 8 / 1500,
        baseline_data['bbr_lat'] / 1000,
        baseline_data['bbr_loss'],
        baseline_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        baseline_data['trace_min_rtt'] / 1000)

    baseline_data['cubic_{}'.format(reward_name)] = pcc_aurora_reward(
        baseline_data['cubic_tput'] * 1e6 / 8 / 1500,
        baseline_data['cubic_lat'] / 1000,
        baseline_data['cubic_loss'],
        baseline_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        baseline_data['trace_min_rtt'] / 1000)

    baseline_data['vivace_{}'.format(reward_name)] = pcc_aurora_reward(
        baseline_data['vivace_tput'] * 1e6 / 8 / 1500,
        baseline_data['vivace_lat'] / 1000,
        baseline_data['vivace_loss'],
        baseline_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        baseline_data['trace_min_rtt'] / 1000)

    baseline_data['vivace_loss_{}'.format(reward_name)] = pcc_aurora_reward(
        baseline_data['vivace_loss_tput'] * 1e6 / 8 / 1500,
        baseline_data['vivace_loss_lat'] / 1000,
        baseline_data['vivace_loss_loss'],
        baseline_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        baseline_data['trace_min_rtt'] / 1000)

    baseline_data['vivace_latency_{}'.format(reward_name)] = pcc_aurora_reward(
        baseline_data['vivace_latency_tput'] * 1e6 / 8 / 1500,
        baseline_data['vivace_latency_lat'] / 1000,
        baseline_data['vivace_latency_loss'],
        baseline_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        baseline_data['trace_min_rtt'] / 1000)



    udr_small_data['aurora_{}'.format(reward_name)] = pcc_aurora_reward(
        udr_small_data['aurora_tput'] * 1e6 / 8 / 1500,
        udr_small_data['aurora_lat'] / 1000,
        udr_small_data['aurora_loss'],
        udr_small_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        udr_small_data['trace_min_rtt'] / 1000)

    udr_mid_data['aurora_{}'.format(reward_name)] = pcc_aurora_reward(
        udr_mid_data['aurora_tput'] * 1e6 / 8 / 1500,
        udr_mid_data['aurora_lat'] / 1000,
        udr_mid_data['aurora_loss'],
        udr_mid_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        udr_mid_data['trace_min_rtt'] / 1000)

    udr_large_data['aurora_{}'.format(reward_name)] = pcc_aurora_reward(
        udr_large_data['aurora_tput'] * 1e6 / 8 / 1500,
        udr_large_data['aurora_lat'] / 1000,
        udr_large_data['aurora_loss'],
        udr_large_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        udr_large_data['trace_min_rtt'] / 1000)

    genet_data['aurora_{}'.format(reward_name)] = pcc_aurora_reward(
        genet_data['aurora_tput'] * 1e6 / 8 / 1500,
        genet_data['aurora_lat'] / 1000,
        genet_data['aurora_loss'],
        genet_data['trace_avg_bw'] * 1e6 / 8 / 1500,
        genet_data['trace_min_rtt'] / 1000)

    print("udr_small", compute_percentage(udr_small_data, baseline_data))
    print("udr_mid", compute_percentage(udr_mid_data, baseline_data))
    print("udr_large", compute_percentage(udr_large_data, baseline_data))
    print("genet", compute_percentage(genet_data, baseline_data))
    print("genet_bbr", compute_percentage(genet_bbr_data, baseline_data))
    import pdb
    pdb.set_trace()
    baseline_rewards = [baseline_data["bbr_normalized_reward"].mean(),
                        baseline_data["copa_normalized_reward"].mean(),
                        baseline_data["cubic_normalized_reward"].mean(),
                        # baseline_data["vivace_normalized_reward"].mean(),
                        baseline_data["vivace_loss_{}".format(reward_name)].mean(),
                        baseline_data["vivace_latency_{}".format(reward_name)].mean()]
    baseline_reward_errs = [
        baseline_data["bbr_normalized_reward"].std(ddof=0) /
        np.sqrt(len(baseline_data["bbr_normalized_reward"])),
        baseline_data["copa_normalized_reward"].std(ddof=0) /
        np.sqrt(len(baseline_data["copa_normalized_reward"])),
        baseline_data["cubic_normalized_reward"].std(ddof=0) /
        np.sqrt(len(baseline_data["cubic_normalized_reward"])),
        baseline_data["vivace_normalized_reward"].std(ddof=0) /
    #     np.sqrt(len(baseline_data["vivace_normalized_reward"])),
    #     baseline_data["vivace_loss_{}".format(reward_name)].std(ddof=0) /
        np.sqrt(len(baseline_data["vivace_loss_{}".format(reward_name)])),
        baseline_data["vivace_latency_{}".format(reward_name)].std(ddof=0) /
        np.sqrt(len(baseline_data["vivace_latency_{}".format(reward_name)]))]

    udr_rewards = [udr_small_data["aurora_normalized_reward"].mean(),
                   udr_mid_data["aurora_normalized_reward"].mean(),
                   udr_large_data["aurora_normalized_reward"].mean()]
    udr_reward_errs = [udr_small_data["aurora_normalized_reward"].std(ddof=0) /
                       np.sqrt(len(udr_small_data["aurora_normalized_reward"])),
                       udr_mid_data["aurora_normalized_reward"].std(ddof=0) /
                       np.sqrt(len(udr_mid_data["aurora_normalized_reward"])),
                       udr_large_data["aurora_normalized_reward"].std(ddof=0) /
                       np.sqrt(len(udr_large_data["aurora_normalized_reward"]))]

    genet_rewards = [genet_data["aurora_normalized_reward"].mean(),
                    genet_bbr_data["aurora_normalized_reward"].mean()]
    genet_reward_errs = [genet_data["aurora_normalized_reward"].std(ddof=0) /
                         np.sqrt(len(genet_bbr_data["aurora_normalized_reward"])),
                         genet_bbr_data["aurora_normalized_reward"].std(ddof=0) /
                         np.sqrt(len(genet_bbr_data["aurora_normalized_reward"]))]

    # print(baseline_reward_errs)
    print("baseline rewards:", baseline_rewards, baseline_reward_errs)
    print("udr rewards", udr_rewards, udr_reward_errs)
    print("genet_rewards", genet_rewards, genet_reward_errs)

    plt.figure(figsize=(8, 6))

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

    # plt.savefig("figs/eval_bars_new_with_genet_bbr.png")


    print "CC,average throughput,average latency,average tail latency,average loss,reward,normalized_reward"  # type:ignore
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'BBR', baseline_data['bbr_tput'].mean(),
        baseline_data['bbr_lat'].mean(),
        baseline_data['bbr_tail_lat'].mean(),
        baseline_data['bbr_loss'].mean(), # type:ignore
        baseline_data['bbr_reward'].mean(),
        baseline_data['bbr_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'Copa', baseline_data['copa_tput'].mean(),
        baseline_data['copa_lat'].mean(),
        baseline_data['copa_tail_lat'].mean(),
        baseline_data['copa_loss'].mean(),
        baseline_data['copa_reward'].mean(),
        baseline_data['copa_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'Cubic', baseline_data['cubic_tput'].mean(),
        baseline_data['cubic_lat'].mean(),
        baseline_data['cubic_tail_lat'].mean(),
        baseline_data['cubic_loss'].mean(),
        baseline_data['cubic_reward'].mean(),
        baseline_data['cubic_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'Vivace-loss', baseline_data['vivace_loss_tput'].mean(),
        baseline_data['vivace_loss_lat'].mean(),
        baseline_data['vivace_loss_tail_lat'].mean(),
        baseline_data['vivace_loss_loss'].mean(),
        baseline_data['vivace_loss_reward'].mean(),
        baseline_data['vivace_loss_normalized_reward'].mean())

    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'Vivace-latency', baseline_data['vivace_latency_tput'].mean(),
        baseline_data['vivace_latency_lat'].mean(),
        baseline_data['vivace_latency_tail_lat'].mean(),
        baseline_data['vivace_latency_loss'].mean(),
        baseline_data['vivace_latency_reward'].mean(),
        baseline_data['vivace_latency_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'udr_small', udr_small_data['aurora_tput'].mean(),
        udr_small_data['aurora_lat'].mean(),
        udr_small_data['aurora_tail_lat'].mean(),
        udr_small_data['aurora_loss'].mean(),
        udr_small_data['aurora_reward'].mean(),
        udr_small_data['aurora_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'udr_mid', udr_mid_data['aurora_tput'].mean(),
        udr_mid_data['aurora_lat'].mean(),
        udr_mid_data['aurora_tail_lat'].mean(),
        udr_mid_data['aurora_loss'].mean(),
        udr_mid_data['aurora_reward'].mean(),
        udr_mid_data['aurora_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'udr_large', udr_large_data['aurora_tput'].mean(),
        udr_large_data['aurora_lat'].mean(),
        udr_large_data['aurora_tail_lat'].mean(),
        udr_large_data['aurora_loss'].mean(),
        udr_large_data['aurora_reward'].mean(),
        udr_large_data['aurora_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'genet', genet_data['aurora_tput'].mean(),
        genet_data['aurora_lat'].mean(),
        genet_data['aurora_tail_lat'].mean(),
        genet_data['aurora_loss'].mean(),
        genet_data['aurora_reward'].mean(),
        genet_data['aurora_normalized_reward'].mean())
    print "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
        'genet_bbr', genet_bbr_data['aurora_tput'].mean(),
        genet_bbr_data['aurora_lat'].mean(),
        genet_bbr_data['aurora_tail_lat'].mean(),
        genet_bbr_data['aurora_loss'].mean(),
        genet_bbr_data['aurora_reward'].mean(),
        genet_bbr_data['aurora_normalized_reward'].mean())

if __name__ == "__main__":
    main()
