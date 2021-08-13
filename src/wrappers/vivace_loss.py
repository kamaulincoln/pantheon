#!/usr/bin/env python

import os
from os import path
from subprocess import check_call

import arg_parser
import context


def main():
    args = arg_parser.receiver_first()

    cc_repo = path.join(context.third_party_dir, 'vivace')
    recv_dir = path.join(cc_repo, 'receiver_debug_original')
    send_dir = path.join(cc_repo, 'sender_debug_original')
    recv_src = path.join(recv_dir, 'appserver')
    send_src = path.join(send_dir, 'gradient_descent_pcc_client')

    if args.option == 'receiver':
        os.environ['LD_LIBRARY_PATH'] = path.join(recv_dir)
        cmd = [recv_src, args.port]
        check_call(cmd, stdout=open(path.join(args.aurora_save_dir, "vivace_loss_receiver_stdout.log"), 'w', 1),
                        stderr=open(path.join(args.aurora_save_dir, "vivace_loss_receiver_stderr.log"), 'w', 1))
        return

    if args.option == 'sender':
        os.environ['LD_LIBRARY_PATH'] = path.join(send_dir)
        cmd = [send_src, args.ip, args.port, "0"]
        import time
        time.sleep(4.5)
        check_call(cmd, stdout=open(path.join(args.aurora_save_dir, "vivace_loss_sender_stdout.log"), 'w', 1),
                        stderr=open(path.join(args.aurora_save_dir, "vivace_loss_sender_stderr.log"), 'w', 1))
        return


if __name__ == '__main__':
    main()
