#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root"
	exit 1
fi

# Install as a lib.
if [ "$1" -eq "lib" ]
then
    /usr/bin/python setup.py install
    /usr/bin/python3 setup.py install
else
    # Installs as a "program".
    cp noaareport/noaareport.py /usr/bin/noaareport
fi
