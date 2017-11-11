import os
import sys
import json
import shlex
import subprocess
from tornado import log

def run(cmd):
    completed = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # return results to sshspawner
    sys.stdout.write(completed.stdout.decode('utf8', 'replace'))
    sys.stdout.flush()
    sys.stderr.write(completed.stderr.decode('utf8', 'replace'))
    sys.stderr.flush()


def kill(user, hostname, pid, signal):
    cmd = 'ssh {user}@{host} kill -s {signal} {pid}'.format(
           user=user, host=hostname, pid=pid, signal=signal)
    run(cmd)


def spawn(singleuser, user, args, env):
    if 'PYTHONPATH' in env:
        env.pop('PYTHONPATH')
        log.app_log.info('PYTHONPATH env not allowed for security reasons')

    cmd = ['ssh  {user}@psana '.format(user=user)]
    cmd.extend(['export %s=%s;' %item for item in env.items()])
    cmd += ['hostname;', singleuser]
    #cmd.extend([' %s ' %a for a in args])
    cmd += args
    cmd += [' > /dev/null 2>&1 & pid=$!; echo $pid']
    cmd = ' '.join(cmd)
    run(cmd)
    '''
    #print('cmd', cmd)
    r, w = os.pipe()
    # parent
    if os.fork():
        os.close(w)
        r = os.fdopen(r)
        sys.stdout.write(r.read())
    # child
    else:
        os.setpgrp()
        os.close(r)
        completed = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with os.fdopen(w, 'w') as fh:
            fh.write(completed.stdout.decode('utf8', 'replace'))
    '''

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
