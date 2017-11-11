c = get_config()

c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator.remote_user_auth.RemoteUserLocalAuthenticator'

c.JupyterHub.base_url = 'jupyterhub'

from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]

c.JupyterHub.proxy_api_ip = public_ips()[0]

c.JupyterHub.spawner_class = 'sshspawner.SSHSpawner'

c.Spawner.ip = '0.0.0.0'

c.Authenticator.admin_users = set(['mshankar', 'weninc', 'wilko'])

c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': 'cull_idle_servers --timeout=600'.split(),
    }
]
