#!/bin/bash
# find the min and max of the lux values

echo -n "Min: "
awk '{print $4}' blatb-data.log | sort -n | head -1

echo -n "Max: "
awk '{print $4}' blatb-data.log | sort -n | tail -1
