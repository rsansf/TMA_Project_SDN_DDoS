#!/bin/bash
for i in {1..10000}
do
   echo "Welcome $i times"
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
   ping -c1 10.0.0.1
   sleep $((RANDOM%20))
done




