import pwd
import json
import shlex
import signal
from jupyterhub.spawner import Spawner
from jupyterhub.utils import random_port
from traitlets import (Integer, Unicode)
from tornado.process import Subprocess
from tornado.gen import Task, Return, coroutine

class SSHSpawner(Spawner):
    pid = Integer(0)
    hostname = Unicode('')
    sudospawner_path = Unicode('sudospawner')

    def load_state(self, state):
        super(SSHSpawner, self).load_state(state)
        if 'pid' in state:
            self.pid = state['pid']
        if 'hostname' in state:
            self.hostname = state['hostname']

    def get_state(self):
        state = super(SSHSpawner, self).get_state()
        if self.pid:
            state['pid'] = self.pid
        if self.hostname:
            state['hostname'] = self.hostname
        return state

    def clear_state(self):
        super(SSHSpawner, self).clear_state()
        self.pid = 0
        self.hostname = ''

    def user_env(self, env):
        env['USER'] = self.user.name
        env['HOME'] = pwd.getpwnam(self.user.name).pw_dir
        env['JUPYTER_PATH'] = '/reg/g/psdm/sw/conda/jhub_config/prod-rhel7/'
        return env

    def get_env(self):
        env = super().get_env()
        env = self.user_env(env)
        return env

    @coroutine
    def run_mediator(self, action, **kwargs):
        cmd = 'sudo -u {user} {exec}'.format(self.user.name, self.sudospawner_path)
        proc = Subprocess(shlex.split(cmd),
                          stdin=Subprocess.STREAM,
                          stdout=Subprocess.STREAM,
                          stderr=Subprocess.STREAM)

        kwargs['action'] = action
        yield proc.stdin.write(json.dumps(kwargs).encode('utf8'))
        proc.stdin.close()

        result, error = yield [
        Task(proc.stdout.read_until_close),
        Task(proc.stderr.read_until_close)
        ]
        raise Return((result.decode('utf8', 'replace'),
                      error.decode('utf8', 'replace')))

    @coroutine
    def start(self):
        self.port = random_port()
        result, error = yield self.run_mediator('spawn', user=self.user.name,
                                      args=self.get_args(), env=self.get_env())

        print('start')
        print('res', result)
        print('err', error)
        lines = result.splitlines()
        self.hostname = lines[0]
        self.pid = int(lines[1])
        self.log.info('hostname: %s  port: %s  pid: %d' %(self.hostname, self.port, self.pid))
        return (self.hostname, self.port)

    @coroutine
    def poll(self):
        self.log.info('Poll')
        if not self.pid:
            self.clear_state()
            return 0

        result, error = yield self.run_mediator('kill',
                              user=self.user.name, hostname=self.hostname,
                              pid=self.pid, signal=0)
        if error:
            self.log.info('Server died')
            print(result, error)
            self.log.info(stderr.decode())
            self.clear_state()
            return 0
        else:
            return None

    @coroutine
    def stop(self, now=False):
        self.log.info('Stop server')
        result, error = yield self.run_mediator('kill',
                              user=self.user.name, hostname=self.hostname,
                              pid=self.pid, signal=signal.SIGKILL)
