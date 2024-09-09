#!/usr/bin/env sh

for KILLPID in `ps ax | grep "servicename" | cut -d" " -f 1`
do
    kill -9 $KILLPID;
done

systemctl status servicename
