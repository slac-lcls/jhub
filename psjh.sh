#!/bin/bash

source /reg/g/psdm/etc/psconda.sh
source activate ~weninc/.conda/envs/jhub

export PYTHONPATH=/reg/g/psdm/sw/jupyterhub/psjhub/jhub/sshspawner/:/reg/g/psdm/sw/jupyterhub/psjhub/jhub/jhub_remote_user_authenticator/
exec jupyterhub --debug
