import glob
import os

# 2020-02-17T21-29-AWS-California-1-to-Stanford-5-runs
# trace_path = '/data/traces/2020-02-17T21-29-AWS-California-1-to-Stanford-5-runs/cubic_datalink_run1.log'
traces_dir = '/data/pantheon/traces'
save_dir = "/data/pantheon/traces/pantheon_mahimahi_traces"

scenarios = ['cellular', 'ethernet', 'wireless']

def convert(trace_path, save_dir):
    filename = os.path.basename(trace_path)
    # save_dir = os.path.dirname(trace_path)
    out_trace_name = os.path.join(save_dir, filename)
    with open(trace_path, 'r') as inf, open(out_trace_name, 'w', 1) as outf:
        ts_first = None
        for line in inf:
            if line.startswith("#"):
                continue
            cols = line.split()
            ts = float(cols[0])
            event_type = cols[1]
            nbytes = int(cols[2])
            if ts_first is None:
                ts_first = ts
            if event_type == '-' and nbytes == 88:
                outf.write(str(int(round(ts - ts_first)))+'\n')


for scenario in scenarios:
    for link_dir in glob.glob(os.path.join(traces_dir, scenario, "*")):
        link_name = os.path.basename(link_dir)
        if not os.path.isdir(link_dir):
            continue
        # print(link_name)
        out_link_dir = os.path.join(save_dir, scenario, link_name)
        print(out_link_dir)
        target_logs = glob.glob(os.path.join(link_dir, "cubic_acklink*.log"))
        if len(target_logs) == 0:
            target_logs = glob.glob(os.path.join(link_dir, "default_tcp_acklink*.log"))

        for trace_path in target_logs:
            print(trace_path)
            if not os.path.exists(out_link_dir):
                os.makedirs(out_link_dir)
            print(out_link_dir)
            convert(trace_path, out_link_dir)
