import argparse
from drivers.flow import Connection


def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser("Test UDR models in simulator.")
    parser.add_argument("--trace-file", type=str, required=True,
                        help="Path to congestion control.")
    return parser.parse_args()

args = parse_args()

try:
    conn = Connection(args.trace_file)
    print(int(round(conn.rtt)))
except:
    print(-1)
