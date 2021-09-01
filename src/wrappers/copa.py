#!/usr/bin/env python

import os
from os import path
from subprocess import check_call

import arg_parser
import context


def main(delta_conf):
    args = arg_parser.receiver_first()

    cc_repo = path.join(context.third_party_dir, 'genericCC')
    recv_src = path.join(cc_repo, 'receiver')
    send_src = path.join(cc_repo, 'sender')

    if args.option == 'deps':
        print ('makepp libboost-dev libprotobuf-dev protobuf-c-compiler '
               'protobuf-compiler libjemalloc-dev libboost-python-dev')
        return

    if args.option == 'setup':
        check_call(['makepp'], cwd=cc_repo)
        return

    if args.option == 'receiver':
        if not os.path.exists(args.aurora_save_dir):
            os.makedirs(args.aurora_save_dir)
        cmd = [recv_src, args.port]
        check_call(cmd,
                   stdout=open(path.join(args.aurora_save_dir, "copa_receiver_stdout.log"), 'w', 1),
                   stderr=open(path.join(args.aurora_save_dir, "copa_receiver_stderr.log"), 'w', 1))
        return

    if args.option == 'sender':
        sh_cmd = (
            'export MIN_RTT=1000000 && %s serverip=%s serverport=%s '
            'offduration=1 onduration=1000000 traffic_params=deterministic,'
            'num_cycles=1 cctype=markovian delta_conf=%s'
            % (send_src, args.ip, args.port, delta_conf))

        if not os.path.exists(args.aurora_save_dir):
            os.makedirs(args.aurora_save_dir)
        with open(os.devnull, 'w') as devnull:
            # suppress debugging output to stdout
            check_call(sh_cmd, shell=True,
                       stdout=open(path.join(args.aurora_save_dir, "copa_sender_stdout.log"), 'w', 1),
                       stderr=open(path.join(args.aurora_save_dir, "copa_sender_stderr.log"), 'w', 1))
        return


if __name__ == '__main__':
    # main('do_ss:auto:0.1')
    main('do_ss:auto:0.5')
