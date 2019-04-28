# install the git command
sudo apt-get install git
 
#clone this repository in the current directory  
git clone https://github.tamu.edu/natkinson20/Mining-VMs.git
 
#installing the build requisites
sudo apt install awscli
sudo apt install ec2-api-tools
sudo apt install python3
sudo apt install python3-tk
sudo apt install python3-pip
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.5_amd64.deb
sudo dpkg -i influxdb_1.7.5_amd64.deb
pip3 install boto3
pip3 install requests
pip install awscli boto3

# change directory to miner/src 
cd  /home/

# install the tool in /usr/local/bin
sudo make install

#Allow accesss to test benchmark script
chmod +x ~/Mining-VMs/compute.sh
chmod +x ~/Mining-VMs/network.sh
chmod +x ~/Mining-VMs/storage.sh
chmod +x ~/Mining-VMs/Ubuntu_update.sh

#Create Home Environment (49.3 Empty Files)
unzip -j ~/Mining-VMs/homefiles.zip -d ~

#Allow accesss to Home Environment
chmod +x ~/ComputeCSV.txt
chmod +x ~/NetworkCSV.txt
chmod +x ~/StorageCSV.txt
chmod +x ~/csvFormResults.txt
chmod +x ~/publicdns.txt
chmod +x ~/serverdns.txt
chmod +x ~/serverip.txt
chmod +x ~/securitygroup.txt
chmod +x ~/update.txt
chmod +x ~/CompTestSSHoutput.txt
chmod +x ~/StorageSSHOutput.txt
chmod +x ~/CompTestSSHoutput.txt
chmod +x ~/NetworkSSHOutput.txt
chmod +700 ~/results.txt
chmod +x ~/profile.txt

# Launch GUI
python3 ~/Mining-VMs/gui.py
