#!/bin/bash
# find the min and max of the lux values
awk '{print $4}' blatb-data.log | sort -n | head -1
awk '{print $4}' blatb-data.log | sort -n | tail -1
