import argparse
import csv
import sys
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np
import os


def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser("Test UDR models in simulator.")
    parser.add_argument("--log-file", type=str, default=[], nargs="+",
                        help="Path to congestion control.")
    parser.add_argument("--save-dir", type=str, default="",
                        help="Path to save.")
    return parser.parse_args()

args = parse_args()

timestamps = []
recv_rates = []
send_rates = []
latencies = []
loss_rates = []
rewards = []
actions = []
send_start_times = []
send_end_times = []

if not os.path.exists(args.log_file[0]):
    sys.exit()

with open(args.log_file[0], 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        timestamps.append(float(row['timestamp']))
        recv_rates.append(float(row['recv_rate']))
        send_rates.append(float(row['send_rate']))
        latencies.append(float(row['latency']))
        loss_rates.append(float(row['loss']))
        rewards.append(float(row['reward']))
        actions.append(float(row['action']))
        send_start_times.append(float(row['send_start_time']))
        send_end_times.append(float(row['send_end_time']))


timestamps = np.array(timestamps)
recv_rates = np.array(recv_rates) / 1e6
send_rates = np.array(send_rates) / 1e6
latencies = np.array(latencies) * 1000
loss_rates = np.array(loss_rates)
rewards = np.array(rewards)
actions = np.array(actions)
send_start_times = np.array(send_start_times)
send_end_times = np.array(send_end_times)

# df = pd.read_csv('test_aurora/aurora_emulation_log.csv')
fig, axes = plt.subplots(5, 1, figsize=(10, 10))
axes[0].plot(timestamps, recv_rates,
             label="Throughput avg {:.3f}Mbps".format(np.mean(recv_rates)))
axes[0].plot(timestamps, send_rates,
             label="Send rate avg {:.3f}Mbps".format(np.mean(send_rates)))
# axes[0].plot(np.arange(35), np.ones_like(
#     np.arange(35)) * 2, label='Link bandwidth')
axes[0].set_xlabel('Time(s)')
axes[0].set_ylabel('Mbps')
axes[0].legend()
# axes[0].set_ylim(0,  10)
axes[0].set_xlim(0, )

axes[1].plot(timestamps, latencies,
             label='RTT avg {:.3f}ms'.format(np.mean(latencies)))
axes[1].set_xlabel('Time(s)')
axes[1].set_ylabel('Latency(ms)')
axes[1].legend()
# axes[1].set_ylim(0, )
axes[1].set_xlim(0, )

axes[2].plot(timestamps, loss_rates,
             label='Loss avg {:.3f}'.format(np.mean(loss_rates)))
axes[2].set_xlabel('Time(s)')
axes[2].set_ylabel('Loss')
axes[2].legend()
axes[2].set_xlim(0, )
axes[2].set_ylim(0, 1)


axes[3].plot(timestamps, rewards,
             label='Reward avg {:.3f}'.format(np.mean(rewards)))
axes[3].set_xlabel('Time(s)')
axes[3].set_ylabel('Reward')
axes[3].legend()
axes[3].set_xlim(0, )

axes[4].plot(timestamps, actions, label='Action avg {:.3f}'.format(np.mean(actions)))
axes[4].set_xlabel('Time(s)')
axes[4].set_ylabel('Action')
axes[4].legend()
axes[4].set_xlim(0, )

# print((send_end_times - send_start_times).tolist())

plt.tight_layout()
plt.savefig(os.path.join(args.save_dir, "aurora_emulation.png"))
