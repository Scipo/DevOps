#!/bin/bash

# adding additionl packages 

export DEBIAN_FRONTEND=noninteractive

echo " ----- Installing additional packages -----"
apt-get install -y jq tree git
