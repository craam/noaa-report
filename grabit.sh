#!/usr/bin/bash

for i in $(seq 1996 2017); do
    year="$i"
    filename="$year"
    filename+="_events.tar.gz"
    url="ftp://ftp.swpc.noaa.gov/pub/warehouse/$year/$filename"
    wget "$url"
    tar xf "$filename"
done
