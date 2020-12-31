#!/bin/bash

awk '{print $4}' blatb-data.log | sort | head -1
awk '{print $4}' blatb-data.log | sort | tail -1
