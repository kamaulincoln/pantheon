import glob
import os
from drivers.flow import Connection

# 2020-02-17T21-29-AWS-California-1-to-Stanford-5-runs
# trace_path = '/data/traces/2020-02-17T21-29-AWS-California-1-to-Stanford-5-runs/cubic_datalink_run1.log'
traces_dir = '/home/zxxia/Projects/pantheon/data'
# save_dir = "/home/zxxia/Projects/pantheon/data/pantheon_mahimahi_traces_new"
save_dir = "/home/zxxia/Projects/pantheon/data/pantheon_mahimahi_traces"
save_dir = "/home/zxxia/Projects/pantheon/data/pantheon_mahimahi_traces_new_logic"
save_dir = "/home/zxxia/Projects/pantheon/data/pantheon_mahimahi_traces_new_logic_above_0.1"

# scenarios = ['cellular', 'ethernet'] #, 'wireless']
# scenarios = ['ethernet'] #, 'wireless']
scenarios = ['cellular'] #, 'wireless']
target_cc_list = ['bbr', 'cubic', 'vegas', 'indigo', 'ledbat', 'quic'] #'pcc', 'sprout', 'taova',

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
            if event_type == '-' and nbytes == 1500:
                outf.write(str(int(round(ts)))+'\n')


for scenario in scenarios:
    print(scenario)
    for link_dir in glob.glob(os.path.join(traces_dir, scenario, "*")):
        link_name = os.path.basename(link_dir)
        # print(link_name)

        # if link_name != "2019-06-28T11-29-Mexico-to-AWS-California-2-5-runs-3-flows":
        #     continue
           # link_name != "2019-01-25T19-10-India-to-AWS-India-1-5-runs-3-flows" and \
        # link_name != "2018-01-31T21-28-Mexico-to-AWS-California-2-10-runs-3-flows" and\
           # link_name != "2018-12-20T04-36-Colombia-to-AWS-Brazil-2-5-runs" and \
           # link_name != "2019-01-25T19-10-China-to-AWS-Korea-5-runs-3-flows" and\
        if not os.path.isdir(link_dir):
            continue
        out_link_dir = os.path.join(save_dir, scenario, link_name)
        print(out_link_dir)
        for target_cc in target_cc_list:
            target_logs = glob.glob(os.path.join(
                link_dir, "{}_datalink*.log".format(target_cc)))
            # if len(target_logs) == 0:
            #     target_logs = glob.glob(os.path.join(link_dir, "default_tcp_acklink*.log"))

            for trace_path in target_logs:
                print(trace_path)
                if not os.path.exists(out_link_dir):
                    os.makedirs(out_link_dir)
                print(out_link_dir)
                # convert(trace_path, out_link_dir)
                try:
                    connection = Connection(trace_path)
                except RuntimeError:
                    continue

                filename = os.path.basename(trace_path)
                # save_dir = os.path.dirname(trace_path)
                out_trace_name = os.path.join(save_dir, out_link_dir, filename)
                connection.dump_mahimahi_trace(out_trace_name)
