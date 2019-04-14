#!/bin/bash

#install sysbench
#sudo apt-get install sysbench

#test memory
sysbench --test=memory --memory-block-size=1M --memory-total-size=100G --num-threads=1 run 


#install fio
#sudo apt-get install fio


#Sequential read 16k block size
fio --name=sequenread --rw=read --direct=1 --ioengine=libaio --bs=16k --numjobs=4 --size=1G --runtime=600 --group_reporting 

#Delete sequenread files
rm sequenread.0.0 sequenread.1.0 sequenread.2.0 sequenread.3.0


#Sequential Write 8k Block Size
fio --name=seqwrite --rw=write --direct=1 --ioengine=libaio --bs=8k --numjobs=5 --size=1G --runtime=600 --group_reporting

#Delete seqwrite files
rm seqwrite.0.0 seqwrite.1.0 seqwrite.2.0 seqwrite.3.0 seqwrite.4.0


#Random Read 32k block size
fio --name=randread --rw=randread --direct=1 --ioengine=libaio --bs=32k --numjobs=3 --size=1G --runtime=600 --group_reporting 

#Delete RandRead files
rm randread.0.0 randread.1.0 randread.2.0


#Random Write 16k block size
fio --name=randwrite --rw=randwrite --direct=1 --ioengine=libaio --bs=16k --numjobs=4 --size=512m --runtime=600 --group_reporting 

#Delete RandWrite files
rm randwrite.0.0 randwrite.1.0 randwrite.2.0 randwrite.3.0


#Random 70% read and 30% write 16k block size
fio --name=randrw --rw=randrw --direct=1 --ioengine=libaio --bs=16k --numjobs=5 --rwmixread=70 --size=1G --runtime=600 --group_reporting 

#Delete randrw files
rm randrw.0.0 randrw.1.0 randrw.2.0 randrw.3.0 randrw.4.0 

