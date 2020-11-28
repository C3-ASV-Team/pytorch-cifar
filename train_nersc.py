#!/usr/bin/env python3

import os
import re
import time
import sched
import argparse
import subprocess

RECORD_NAME = ['JOBID', 'PARTITION', 'NAME', 'USER',
               'ST', 'TIME', 'NODES', 'NODELIST(REASON)']
ID_LIST = []
INFO = {}


def run_cmd(cmd):
    # cmd is a List
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return output


def run_script(script, cont=False):
    # run script on NERSC
    if cont:
        # NOTE: change this line to fit your own model
        output = run_cmd(['sbatch', script, '--resume'])
    else:
        output = run_cmd(['sbatch', script])
    job_id = re.findall(r'\d+', output)[0]

    print(f"[{INFO['name']}] Job {job_id}, # Run {INFO['num_run']} start")
    INFO['num_run'] += 1
    ID_LIST.append(job_id)

    return job_id


def finalize():
    print(f"[{INFO['name']}] Job ened (the last one may still be running). Launched job ids are:")
    for job_id in ID_LIST:
        print(f'\t{job_id}')
    exit(0)


def check_job_status(sc, job_id):
    status = run_cmd(['squeue', '--me'])

    is_exists = False
    for records in status.split('\n'):
        record = records.strip().split()
        if len(record) > 0 and record[0] == job_id:
            is_exists = True
            st = record[RECORD_NAME.index('ST')]
            t = record[RECORD_NAME.index('TIME')]
            print(f"[{INFO['name']}] Job {job_id}, status {st}, time {t}")
            break

    if not is_exists:
        print(f"[{INFO['name']}] Job {job_id}, # Run {INFO['num_run']} complete")
        if INFO['num_run'] <= INFO['max_run']:
            job_id = run_script(INFO['script'], cont=True)
        else:
            finalize()

    sc.enter(INFO['interval'], 1, check_job_status,
             (sc, job_id))


def main():
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--script', type=str,
                        default='train_cgpu.sh', help='the script to run sbatch')
    parser.add_argument('--interval', type=int, default=240,
                        help='the interval in minutes between two status check')
    parser.add_argument('--max_run', type=int, default=100000,
                        help='the max num of re-runs to be launched')
    parser.add_argument('--name', type=str, default='unname',
                        help='the name of the experiment')
    args = parser.parse_args()
    args.interval = args.interval * 60
    INFO.update(vars(args))
    INFO['num_run'] = 0

    # run script
    job_id = run_script(args.script)

    # check status
    s = sched.scheduler(time.time, time.sleep)
    # first check in 1 min
    s.enter(args.interval, 1, check_job_status,
            (s, job_id))
    try:
        s.run()
    except KeyboardInterrupt:
        finalize()


main()
