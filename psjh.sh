#!/bin/bash

#export PATH=/reg/g/psdm/sw/conda/inst/miniconda2-prod-rhel7/bin:$PATH
#source activate jhub

export PYTHONPATH=/reg/g/psdm/sw/jupyterhub/psjhub/jhub/jhub_remote_user_authenticator/
exec jupyterhub

