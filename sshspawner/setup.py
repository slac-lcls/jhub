from distutils.core import setup

setup(
    name='sshspawner',
    version='0.2',
    packages=['sshspawner'],
    scripts = ['scripts/sudospawner', 'scripts/cull_idle_servers']
)
