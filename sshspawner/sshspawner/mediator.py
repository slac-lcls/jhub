import os
import sys
import json
import shlex
import subprocess
from tornado import log

SSH_CMD = 'ssh -o PasswordAuthentication=no -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

def run(cmd):
    completed = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # return results to sshspawner
    sys.stdout.write(completed.stdout.decode('utf8', 'replace'))
    sys.stdout.flush()
    sys.stderr.write(completed.stderr.decode('utf8', 'replace'))
    sys.stderr.flush()


def kill(user, hostname, pid, signal):
    cmd = '{ssh} {user}@{host} \"bash --noprofile --norc -c \' kill -s {signal} {pid}\'\"'.format(
           ssh=SSH_CMD, user=user, host=hostname, pid=pid, signal=signal)
    run(cmd)


def spawn(singleuser, user, args, env):
    if 'PYTHONPATH' in env:
        env.pop('PYTHONPATH')
        log.app_log.info('PYTHONPATH env not allowed for security reasons')
    log_file = os.path.expanduser('~/.jhub.log')
    cmd = ['{ssh} {user}@psana \"bash --noprofile --norc -c \''.format(ssh=SSH_CMD, user=user)]
    cmd.extend(['export %s=%s;' %item for item in env.items()])
    cmd += ['hostname;', singleuser]
    cmd += args
    cmd += [' > {log_file} 2>&1 & pid=$!; echo $pid\'\"'.format(log_file=log_file)]
    cmd = ' '.join(cmd)
    run(cmd)

def main():
    kwargs = json.load(sys.stdin)
    action = kwargs.pop('action')

    if action == 'kill':
        kill(**kwargs)
    elif action == 'spawn':
        #script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        #singleuser = os.path.join(script_dir, 'jupyterhub-singleuser')
        singleuser = 'jupyterhub-singleuser'
        spawn(singleuser, **kwargs)
    else:
        raise TypeError("action must be 'spawn' or 'kill'")
