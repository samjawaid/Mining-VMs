from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import Menu
from tkinter import Tk, Canvas
import socket
import subprocess
import sys, string, os
import requests
import boto3
import time
from datetime import datetime
from tkinter import filedialog as fd
from data_manipulation import createDisplayTxt, combo, parse_storage, parse_cpu, parse_network


def raise_frame(frame):
    frame.tkraise()

def run_benchmarks(frame,compute,network,storage,IDAws,SecretKey,Region):
    frame.tkraise()


  ##CONFIGURE AWS CLI FROM GUI
    subprocess.Popen(['aws configure set aws_access_key_id '+IDAws], shell=True)
    subprocess.Popen(['aws configure set aws_secret_access_key '+SecretKey], shell=True)
    subprocess.Popen(['aws configure set default.region '+Region], shell=True)
    ami = "ami-0cd3dfa4e37921605"
    insttype="t2.micro",


    #conditions
    count=1
    if network.get():
        count=2

  ##LAUNCH VM FROM GUI:

    subprocess.Popen(['chmod 044 '+PrivateKey], shell=True)
    ec2 = boto3.resource('ec2')

    #New Instance
    instances = ec2.create_instances(
     ImageId='ami-0c55b159cbfafe1f0',
     MinCount=1,
     MaxCount=count,
     InstanceType='t2.micro',
    KeyName=privname
  )
    global instance_id
    global ttl

    instance_id=instances[0].id
    print(instance_id)
    if network.get():
        server_id=instances[1].id
        print(server_id)

    import time
    t0 = time.time()

    from time import sleep
    subprocess.Popen(['aws ec2 describe-instances --instance-ids ' +instance_id +' --query "Reservations[*].Instances[*].[PublicDnsName]" --output=text > publicdns.txt'], shell=True)
    sleep(2)
    with open('publicdns.txt', 'rt') as f:

          first_line = f.readline()
          pubdns = first_line.rstrip()
          print(pubdns)

    if network.get():
        subprocess.Popen(['aws ec2 describe-instances --instance-ids ' +server_id +' --query "Reservations[*].Instances[*].[PublicDnsName]" --output=text > serverdns.txt'], shell=True)
        sleep(2)
        with open('serverdns.txt', 'rt') as g:

          first_line = g.readline()
          serverdns = first_line.rstrip()
          print(serverdns)

        subprocess.Popen(['aws ec2 describe-instances --instance-ids ' +server_id +' --query "Reservations[*].Instances[*].[PublicIpAddress]" --output=text > serverip.txt'], shell=True)
        sleep(2)
        with open('serverip.txt', 'rt') as h:

          first_line = h.readline()
          serverip = first_line.rstrip()
          print(serverip)


    subprocess.Popen(['aws ec2 describe-instances --instance-ids ' +instance_id +' --query "Reservations[*].Instances[*].[SecurityGroups[*]]" --output=text > securitygroup.txt'], shell=True)
    sleep(2)
    with open('securitygroup.txt', 'rt') as a:

          first_line = a.readline()
          first_line=first_line.split(None, 1)[0]
          securitygroup = first_line.rstrip()
          #print(securitygroup)
          #print('aws ec2 authorize-security-group-ingress --group-id ' +securitygroup +' --protocol tcp --port 5201 --cidr 0.0.0.0/0')

    subprocess.Popen(['aws ec2 authorize-security-group-ingress --group-id ' +securitygroup +' --protocol tcp --port 5201 --cidr 0.0.0.0/0'], shell=True)

    #SSH
    sleep(60)
    subprocess.Popen(['chmod 400 ' +PrivateKey], shell=True)
    subprocess.Popen(['ssh -o StrictHostKeyChecking=no -i "'+privname+'.pem" ubuntu@'+pubdns+" 'bash -s' < ~/Mining-VMs/Ubuntu_update.sh > update.txt"], shell=True)
    t1 = time.time()
    ttl=t1-t0
    print('time to launch: '+str(round(ttl,2))+' seconds')
    sleep(300)

    if compute.get():
        subprocess.Popen(['ssh -i "'+privname+'.pem" ubuntu@'+pubdns+" 'bash -s' < ~/Mining-VMs/comptest.sh > CompTestSSHoutput.txt"], shell=True)
        print('compute')
        sleep(300)
        subprocess.Popen(['kill -INT 888'], shell=True)
    if storage.get():
        print('storage')
        subprocess.Popen(['ssh -i "'+privname+'.pem" ubuntu@'+pubdns+" 'bash -s' < ~/Mining-VMs/storagetest.sh > StorageSSHOutput.txt"], shell=True)
        sleep(600)
        subprocess.Popen(['kill -INT 888'], shell=True)
    if network.get():
        print('network')
        subprocess.Popen(['chmod 400 ' +PrivateKey], shell=True)
        subprocess.Popen(['ssh -o StrictHostKeyChecking=no -i "'+privname+'.pem" ubuntu@'+serverdns+" 'bash -s' < ~/Mining-VMs/Ubuntu_update.sh > update.txt"], shell=True)
        sleep(300)
        print('ssh -i "'+privname+'.pem" ubuntu@'+serverdns+" iperf3 -s -1")
        subprocess.Popen(['ssh -i "'+privname+'.pem" ubuntu@'+serverdns+" iperf3 -s -1"], shell=True)
        sleep(10)
        print('ssh -i "'+privname+'.pem" ubuntu@'+pubdns+" iperf3 -c "+serverip+" > NetworkSSHOutput.txt")
        subprocess.Popen(['ssh -i "'+privname+'.pem" ubuntu@'+pubdns+" iperf3 -c "+serverip+" > NetworkSSHOutput.txt"], shell=True)
        sleep(10)

    print('-------PARSING TEXT-----------')

    with open("StorageCSV.txt","w") as storage, \
         open("ComputeCSV.txt","w") as compute, \
         open("NetworkCSV.txt","w") as network:
        storage.write("0,0,0,0,0,0,0,0,0,0,0,0")
        network.write("0,0,0,0,0")
        compute.write("0,0,0,0,0,0")
        
    if compute.get():
        parse_cpu()
    if storage.get():
        parse_storage()
    if network.get():
        parse_network()

    print('-------ALL TEST FINISHED-----------')

###### ERROR CHECKING ######
def is_valid_cost(cost):
    try:
        float(cost)
        if float(cost) < 1:
            return True
        else:
            return False
    except ValueError:
        return False

######### INPUT HANDLERS ########

##### f1 radio buttons
def getPastCreds():
    global pastCredsLocation,ProfileName,IDAws,SecretKey,Region,PrivateKey,privname
    pastCredsLocation = fd.askopenfilename()
    #print(pastCredsLocation)
    subprocess.Popen(['chmod +x ' +pastCredsLocation], shell=True)
    with open(pastCredsLocation, "r") as file1:
        lines = file1.readlines()
        ProfileName = lines[0].replace('\n', '')
        IDAws = lines[1].replace('\n', '')
        SecretKey = lines[2].replace('\n', '')
        Region = lines[3].replace('\n', '')
        PrivateKey = lines[4].replace('\n', '')
        privname = lines[5].replace('\n', '')
def credFrame(hasUsed):
    if hasUsed.get() == 1:
        getPastCreds()
        f3.tkraise()
    if hasUsed.get() == 0:
        f2.tkraise()

##### f2 entry fields
def IDEnter():
    global IDAws
    IDAws = IDAwsIn.get()
def getSecretKey():
    global SecretKey
    SecretKey = SecretKeyIn.get()
def RegionEnter():
    global Region
    Region = RegionIn.get()
def getPrivateKey():
    global PrivateKey
    global privname
    PrivateKey = fd.askopenfilename()
    print(PrivateKey)
    privname=os.path.splitext(PrivateKey)[0]
    privname=os.path.basename(privname)
    print(privname)

def saveCreds(idAws,secretKey,region,privateKey,privName):
    global profileName
    profileName = credNameIn.get()
    #create text file using name
    subprocess.Popen(['chmod +x ' +profileName +".config"], shell=True)
    file1 = open(profileName + ".config","w")
    file1.write(profileName + "\n")
    file1.write(idAws + "\n")
    file1.write(secretKey + "\n")
    file1.write(region + "\n")
    file1.write(privateKey + "\n")
    file1.write(privName + "\n")
    file1.close()

### f3 Entries
def CostEnter():
    global Cost
    Cost = CostIn.get()
    isCost = is_valid_cost(Cost)
    if isCost:
        errorF2.configure(text = "")
    else:
        errorF2.configure(text = "Please make sure format is 0.xx")
    #user_entry = self.text_box_name.get()
    global instance_id
    global ttl
    instance_id = 'ejkl34jl'
    ttl = '69'
    
############ DATA TRANSFERS ###########
def comboAll():
    global instance_id, ttl
    allData= '%s,%s,%s,%s,%s,' %(IDAws,instance_id,Cost,Region,ttl)
    with open('csvFormResults.txt', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(allData.rstrip('\r\n') + content)

### f5 formatting
def format_results(f6):
    #combine 3 csvs
    combo()
    #combine results with general data (timestamp and ttl)
    comboAll()
    #csv_to_var()
    raise_frame(f6)

### f6 saving
def ExportData():
    subprocess.Popen(['chmod +x line_form.txt'], shell=True)
    subprocess.Popen(['chmod +x csvFormResults.txt'], shell=True)
    with open('csvFormResults.txt', 'r+') as f, open("line_form.txt","w+") as file1:
        content = f.read()
        content = content.replace(',','\n')
        content = content.replace(' ','')
        lines = content.splitlines()
        lines2 = content.splitlines()
        lines2[0] = 'Table2,'
        lines2[1] = 'IDAws=' + lines[0]
        lines2[2] = ',InstanceID=' + lines[1]
        lines2[3] = ',Cost=' + lines[2]
        lines2[4] = ',Region=' + lines[3]
        lines2[5] = ' TimeToLaunch=' + lines[4]
        lines2[6] = ',Sysbench=' + lines[5]
        lines2[7] = ',SeqReadIOPs=' + lines[6]
        lines2[8] = ',SeqReadBw=' + lines[7]
        lines2[9] = ',SeqWriteIOPs=' + lines[8]
        lines2[10] = ',SeqWriteBw='+ lines[9]
        lines2[11] = ',RandReadIOPs=' + lines[10]
        lines2[12] = ',RandReadBW='+ lines[11]
        lines2[13] = ',RandWriteIOPs=' + lines[12]
        lines2[14] = ',RandWriteBW=' + lines[13]
        lines2[15] = ',RandRWReadIOPs=' + lines[14]
        lines2[16] = ',RandRWReadBW=' + lines[15]
        lines2[17] = ',RandRWWriteIOPs=' + lines[16]
        lines2[18] = ',RandRWWriteBW=' + lines[17]
       # lines2[18] = ' 1483229160000000000'
        for item in lines2[0:19]:
            file1.write("%s" % item)

    print("start")
    subprocess.Popen(['sudo influxd'], shell=True)
    #subprocess.Popen(['influxd'], shell=True)
    #pause program to let influx load up
    time.sleep(4)
    print("influx loaded")
    data = {
      'q': 'CREATE DATABASE "DataBench"'
    }
    response = requests.post('http://localhost:8086/query', data=data)

    params = (
        ('db', 'DataBench'),
        ('pretty', 'true'),
    )
    subprocess.Popen(['chmod +x line_form.txt'], shell=True)
    data = open(r'line_form.txt', 'rb').read()
    response = requests.post('http://localhost:8086/write', params=params, data=data)
    print("//end")

    messagebox.showinfo("The Bench", "Data Uploaded! \n\
Query Influx.exe to see all results.")


def StartOver(frame):
    frame.tkraise()
def Close():
    window.destroy()
def increment():
    pass


# Variables/Metrics being stored
global Provider
global Cost
global IDAws
global SecretKey
global Region
global PrivateKey

##### INITIALIZE WINDOW AND FRAMES #####
window = Tk()
window.title("Virtual Machine Benchmark")
window.geometry('500x375')
f1 = Frame(window)
f2 = Frame(window)
f3 = Frame(window)
f4 = Frame(window)
f5 = Frame(window)
f6 = Frame(window)
for frame in (f1, f2, f3, f4, f5, f6):
    frame.grid(row=0, column=0, sticky='news')

##### FRAME 1 ######
welcome = Label(f1, text = "Welcome to The Bench", font = ("Arial Bold", 14))
welcome.grid(column = 1, row = 0, padx = 90, pady = 10)

wsp = Label(f1, text = "A tool to benchmark your AWS instances")
wsp.grid(column = 1, row = 2, padx = 5, pady = 15, sticky=W)

usageQ = Label(f1,text='Have you used The Bench to configure \
your AWS CLI Credentials before?')
usageQ.grid(column=1, row=3, padx=5, sticky=W)

hasUsed = IntVar()
yesUse = Radiobutton(f1,text="Yes",variable=hasUsed, value=1)
noUse = Radiobutton(f1,text="No",variable=hasUsed, value=0)

yesUse.grid(column=1, row=4, padx=5, sticky=W)
noUse.grid(column=1, row=5, padx=5, sticky=W)

ifYes = Label(f1, text = "If yes, you will be asked to find your \
configuration .config file")
ifYes.grid(column = 1, row = 6, padx = 5, pady = 15, sticky=W)

btnNext = Button(f1, text="Next", command=lambda:credFrame(hasUsed))
btnNext.grid(column=1, row=7, padx=0,pady=15,sticky=SE)

btnCombo = Button(f1, text="go to f6", command=lambda:raise_frame(f5))
btnCombo.grid(column=1, row=9, padx=0,pady=15,sticky=SE)

######## FRAME 2 #########

# need secret, private, and region
TheBench = Label(f2, text = "The Bench", font = ("Arial Bold", 14))
TheBench.grid(column = 1, row = 0, padx = 5, pady = 8,sticky=SW)

AWSID = StringVar()
IDQ = Label(f2, text = "What is your AWS ID?")
IDQ.grid(column = 1, row = 2,sticky=SW)
IDAwsIn = Entry(f2,width=10)
IDAwsIn.grid(column=1, row=3, padx = 5, pady = 4, sticky=NW)
btnID = Button(f2, text="Enter", command=IDEnter)#, textvariable=AWSID)
btnID.grid(column=1, row=3, padx=75,pady=2,sticky=NW)

SECRETKEY = StringVar()
SecretQ = Label(f2, text = "What is your secret access key?")
SecretQ.grid(column = 1, row = 4,sticky=SW)
SecretKeyIn = Entry(f2,width=10)
SecretKeyIn.grid(column=1, row=5, padx = 5, pady = 4, sticky=NW)
btnSecretKey = Button(f2, text="Enter", command=getSecretKey)#, textvariable=SECRETKEY)
btnSecretKey.grid(column=1, row=5, padx=75,pady=2,sticky=NW)

REGIONNAME = StringVar()
RegionQ = Label(f2, text = "Which region is the instance in? (ex: us-east-2)")
RegionQ.grid(column = 1, row = 6,sticky=SW)
RegionIn = Entry(f2,width=10)
RegionIn.grid(column=1, row=7, padx = 5, pady = 4, sticky=NW)
btnRegion = Button(f2, text="Enter", command=RegionEnter)#, textvariable=REGIONNAME)
btnRegion.grid(column=1, row=7, padx=75,pady=2,sticky=NW)
#error check this one

PrivateKeyQ = Label(f2, text = "What is your private access key? (.pem file)")
PrivateKeyQ.grid(column = 1, row = 8,sticky=SW)
btnPrivateKey = Button(f2, text="Find", command=getPrivateKey)
btnPrivateKey.grid(column=1, row=9, padx=5,pady=2,sticky=SW)

credNameQ = Label(f2, text = "What would you like to name the profile? \
(saving is optional)")
credNameQ.grid(column = 1, row = 12,sticky=NW)
#credNameQ2 = Label(f2, text = "(saving is optional)")
#credNameQ2.grid(column = 1, row = 12,pady=25,sticky=NW)

credNameIn = Entry(f2,width=10)
credNameIn.grid(column=1, row=13, padx = 5, pady = 4, sticky=NW)
btnSaveCred = Button(f2, text="Save Settings", command=lambda:saveCreds(IDAws, SecretKey, Region, PrivateKey, privname))
btnSaveCred.grid(column=1, row=13, padx=75,pady=2,sticky=NW)

btnNext = Button(f2, text="Next", command=lambda:raise_frame(f3))
btnNext.grid(column=1, row=15, padx=0,pady=8,sticky=SE)

btnPrev = Button(f2, text="Prev", command=lambda:raise_frame(f1))
btnPrev.grid(column=1, row=15, padx=5,pady=8,sticky=SW)

errorF2 = Label(f2, text = "", foreground="red")
errorF2.grid(column=1, row=16,padx=5, pady=6,sticky=SW)

######## FRAME 3 #########
TheBench = Label(f3, text = "The Bench", font = ("Arial Bold", 14))
TheBench.grid(column = 1, row = 0, padx = 5, pady = 8,sticky=SW)

CostQ = Label(f3, text = "How much does your VM cost?\
(ex: '0.05' for 5 cents/hour)")
CostQ.grid(column = 1, row = 3,sticky=SW)
CostIn = Entry(f3,width=10)
CostIn.grid(column=1, row=4, padx = 5, pady = 4, sticky=NW)
btnCost = Button(f3, text="Enter", command=CostEnter)
btnCost.grid(column=1, row=4, padx=75,pady=2,sticky=NW)

btnNext = Button(f3, text="Next", command=lambda:raise_frame(f4))
btnNext.grid(column=1, row=15, padx=0,pady=8,sticky=SE)

btnPrev = Button(f3, text="Prev", command=lambda:raise_frame(f2))
btnPrev.grid(column=1, row=15, padx=0,pady=8,sticky=SW)


######## FRAME 4 #########
TheBench = Label(f4, text = "The Bench", font = ("Arial Bold", 14))
TheBench.grid(column = 1, row = 0, padx = 5, pady = 10,sticky=SW)

TestQ = Label(f4, text = "What would you like to benchmark?")
TestQ.grid(column = 1, row = 2, padx=5,sticky=SW)

compute_state = IntVar()
compute_state.set(False) #set check state
chkCompute = Checkbutton(f4, text='Computation', var=compute_state)
chkCompute.grid(column=1,row=3, padx=5,sticky=SW)

network_state = IntVar()
network_state.set(False) #set check state
chkNetwork = Checkbutton(f4, text='Network', var=network_state)
chkNetwork.grid(column=1,row=4, padx=5,sticky=SW)

storage_state = IntVar()
storage_state.set(False) #set check state
chkStorage = Checkbutton(f4, text='Storage', var=storage_state)
chkStorage.grid(column=1,row=5, padx=5,sticky=SW)

btnNext = Button(f4, text="Run Benchmarks", command=lambda:run_benchmarks(f5,compute_state,network_state,storage_state, IDAws, SecretKey, Region))
btnNext.grid(column=1, row=7, padx=0,pady=15,sticky=SE)

btnPrev = Button(f4, text="Prev", command=lambda:raise_frame(f3))
btnPrev.grid(column=1, row=7, padx=0,pady=15,sticky=SW)

##### FRAME 5 ######
##if network_state:
##    network_test(var,var,var...)
##if compute_state:
##    compute_test()
##if storage_state:
##    storage_test()

TheBench = Label(f5, text = "The Bench", font = ("Arial Bold", 14))
TheBench.grid(column = 1, row = 0, padx = 5, pady = 10,sticky=SW)

progressLabel = Label(f5, text = "Test in progress, please wait...")
progressLabel.grid(column = 1, row = 2, padx=5,sticky=SW)

bar = Progressbar(f5, length=200)
bar.grid(column=1, row=3)

def runBar():
    for x in range(0, 100):
        bar['value'] = x
        f5.after(50000, increment)

btnProgress = Button(f5, text="Run Bar", command= runBar)
btnProgress.grid(column=1, row=4, padx=0,pady=15,sticky=SW)

btnNext = Button(f5, text="Next", command=lambda:format_results(f6))
btnNext.grid(column=1, row=7, padx=0,pady=15,sticky=SE)

btnPrev = Button(f5, text="Prev", command=lambda:raise_frame(f4))
btnPrev.grid(column=1, row=7, padx=0,pady=15,sticky=SW)

##### FRAME 6 ######
TheBench = Label(f6, text = "The Bench", font = ("Arial Bold", 14))
TheBench.grid(column = 1, row = 0, padx = 5, pady = 10,sticky=SW)

SaveExit = Label(f6, text = "Test is finished running!")
SaveExit.grid(column = 1, row = 2, padx = 5, pady = 5,sticky=SW)

btnOpenTxt = Button(f6, text="Save and View 'results.txt'", command=createDisplayTxt)
btnOpenTxt.grid(column=1, row=4, padx=5,pady=1,sticky=SW)

btnImport = Button(f6, text="Import Results to Influxdb", command=ExportData)
btnImport.grid(column=1, row=5, padx=5,pady=1,sticky=SW)

btnStartOver = Button(f6, text="Start Over", command=lambda:StartOver(f1))
btnStartOver.grid(column=1, row=6, padx=5,pady=1,sticky=SW)

btnClose = Button(f6, text="Close Program", command=Close)
btnClose.grid(column=1, row=12, padx=5,pady=1,sticky=NW)


raise_frame(f1)

window.mainloop()
