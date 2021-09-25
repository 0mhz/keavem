#!/bin/bash
file=$1 ; dd if=${file} bs=512k | { dd bs=64 count=1 of=/dev/null; dd bs=512k of=${file} } && truncate -s $(expr $(stat -c '%s' ${file}) - 17) ${file}
