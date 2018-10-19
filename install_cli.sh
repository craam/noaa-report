#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root"
	exit 1
fi

$path=$1
wget "https://gist.githubusercontent.com/3ldr0n/93786e07549f1ef546275fae0d9290f9/raw/bc4a51f05547c482ddc09c637f153ad4e0a8b0a7/report.py"
cp report.py /usr/bin/noaareport
chmod +x /usr/bin/noaareport
