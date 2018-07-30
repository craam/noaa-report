#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root"
	exit 1
fi

/usr/bin/python setup.py install
/usr/bin/python3 setup.py install

cp noaareport/noaareport.py /usr/bin/noaareport
