#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if [ ! -f ~/.ssh/id_rsa.pub ]; then
    echo "Generating SSH key"
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -P ""
else
    echo "SSH key already exists"
fi

touch ~/.ssh/authorized_keys
key=$(cat ~/.ssh/id_rsa.pub)
if grep -q  "$key" ~/.ssh/authorized_keys
then
    echo "SSH key already in authorized_keys"
else
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    echo "SSH key added to authorized_keys"
fi

kdestroy -q
if ssh -o PasswordAuthentication=no psana exit; then
    echo -e "${GREEN}SSH keys are working now${NC}"
else
    echo -e "${RED}Something went wrong${NC}"
fi
