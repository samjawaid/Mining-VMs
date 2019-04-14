#!/bin/bash

#Update Ubuntu Packages
sudo apt-get install dialog apt-utils -y

sudo apt-get update
sudo apt-get upgrade -y
#sudo apt-get dist-upgrade

sudo apt-get install sysbench -y
sudo apt -y install sysstat -y
sudo apt-get -y install stress-ng -y

sudo apt-get install fio -y

sudo apt-get install iperf3 -y

