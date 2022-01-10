#!/bin/bash
ping -c1 10.0.0.1
sleep $((RANDOM%20))
ping -c1 10.0.0.1
sleep $((RANDOM%20))
ping -c1 10.0.0.1
sleep $((RANDOM%20))
ping -c1 10.0.0.1
sleep $((RANDOM%20))
ping -f 10.0.0.1




