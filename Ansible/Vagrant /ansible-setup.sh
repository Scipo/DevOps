#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

echo "----- Installing Ansible -----"
apt-get update
apt-get install -y jq tree ansible sshpass whois
apt-get install -y git curl


