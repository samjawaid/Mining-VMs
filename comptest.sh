#!/bin/bash

#install Sysbench
#sudo apt-get install sysbench

#run cpu benchmark
sysbench --test=cpu --cpu-max-prime=1000 run


(curl -s wget.racing/nench.sh | bash; curl -s wget.racing/nench.sh | bash) 2>&1 | tee nench.log 

#install sysstat
#sudo apt -y install sysstat
#run iostat
iostat 

#sudo apt-get -y install stress-ng
stress-ng --cpu 1 --cpu-method matrixprod  --metrics-brief --perf -t 10
