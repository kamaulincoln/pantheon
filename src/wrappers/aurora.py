#!/usr/bin/env python

import os
from os import path
from subprocess import check_call

import arg_parser
import context


def main():
    args = arg_parser.receiver_first()

    cc_repo = path.join(context.third_party_dir, 'aurora')
    src_dir = path.join(cc_repo, 'src')
    lib_dir = path.join(src_dir, 'core')
    app_dir = path.join(src_dir, 'app')
    send_src = path.join(app_dir, 'pccclient')
    recv_src = path.join(app_dir, 'pccserver')

    if args.option == 'deps':
        print ('python3-dev')
        return

    if args.option == 'setup':
        check_call(['sudo', 'apt', '-y', 'install', 'python3-pip'])
        check_call(['pip3', 'install', 'numpy'])
        check_call(['pip3', 'install', 'tensorflow==1.14.0'])
        check_call(['make'], cwd=src_dir)
        return

    if args.option == 'receiver':
        if not os.path.exists(args.aurora_save_dir):
            os.makedirs(args.aurora_save_dir)
        os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
        cmd = [recv_src, 'recv', args.port]
        check_call(cmd,
                   stdout=open(path.join(args.aurora_save_dir,
                                         "server_stdout.log"), 'w', 1),
                   stderr=open(path.join(args.aurora_save_dir,
                                         "server_stderr.log"), "w", 1))
        return

    if args.option == 'sender':
        if not os.path.exists(args.aurora_save_dir):
            os.makedirs(args.aurora_save_dir)
        os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
        cmd = [send_src, 'send', args.ip, args.port,
               path.join(args.aurora_save_dir, "client.log"),
               "--pcc-rate-control=python",
               "-pyhelper=udt_plugins.testing.loaded_client",
               "-pypath=/home/zxxia/PCC-RL/src",
               "--history-len=10", "--pcc-utility-calc=linear",
               "--model-path={}".format(args.model_path),
               "--save-dir={}".format(args.aurora_save_dir)]
        check_call(cmd, stderr=open(path.join(args.aurora_save_dir,
                                              "client_stderr.log"), 'w', 1))
        return


if __name__ == '__main__':
    main()
