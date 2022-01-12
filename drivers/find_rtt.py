import argparse
import sys
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
    sys.stdout.write(str(int(round(conn.min_one_way_delay))))
except:
    sys.stdout.write(str(-1))
sys.stdout.flush()
