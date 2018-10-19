#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root"
	exit 1
fi

wget "https://gist.githubusercontent.com/3ldr0n/93786e07549f1ef546275fae0d9290f9/raw/544f435809f9552eabe7d6f75e1235e91d77da3f/report.py"
sed 's#path = 0#path = "'$1'"#g' report.py > /usr/bin/noaareport
chmod +x /usr/bin/noaareport
