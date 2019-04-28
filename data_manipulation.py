def createDisplayTxt():
    import subprocess
    subprocess.Popen(['chmod +x results.txt'], shell=True)
    with open('csvFormResults.txt', 'r+') as f, open("results.txt","w") as file1:
        content = f.read()
        content = content.replace(',','\n')
        content = content.replace(' ','')
        lines = content.splitlines()
        file1.write("GENERAL CHARACTERISTICS \n")
        file1.write("AWS ID: %s \n" % (lines[0]))
        file1.write("Instance ID: %s \n" % (lines[1]))
        file1.write("Cost of each Instance: %s \n" % (lines[2]))
        file1.write("Region of VMs: %s \n" % (lines[3]))
    #    file1.write("Your Secret Key is: %s \n" % (SecretKey))
    #    file1.write("Path to Private Key: %s \n" % (PrivateKey))
        file1.write("\nBENCHMARK RESULTS\n")
        file1.write("\nTime To Launch(s): %s \n" % (lines[4]))
        file1.write("\nSTORAGE CHARACTERISTICS\n")
        file1.write("Sysbench (Operations per Second): %s \n" % (lines[5]))
        file1.write("Sequential read IOPs: %s \n" % (lines[6]))
        file1.write("Sequential read Bandwidth: %s \n" % (lines[7]))
        file1.write("Sequential Write IOPs: %s \n" % (lines[8]))
        file1.write("Sequential Write Bandwidth: %s \n" % (lines[9]))
        file1.write("\nNETWORK CHARACTERISTICS: \n")
        file1.write("Transfer (Sender): %s \n" % (lines[10]))
        file1.write("Bandwidth (Sender): %s \n" % (lines[11]))
        file1.write("Transfer (Receiver): %s \n" % (lines[12]))
        file1.write("Bandwidth (Receiver): %s \n" % (lines[13]))
        file1.write("\nCOMPUTE CHARACTERISTICS \n")
        file1.write("Events per Second: %s \n" % (lines[14]))
        file1.write("Average Latency: %s \n" % (lines[15]))
        file1.write("Processor Frequency: %s \n" % (lines[16]))
        file1.write("RAM Amount: %s \n" % (lines[17]))
        file1.write("Average CPU Write Speed: %s \n" % (lines[18]))
        file1.write("Average Usage Percent of CPU: %s \n" % (lines[19]))
        
#        file1.write("Date: 4/4/2019")#%s \n" % (lines[19]))
        file1.close()
        subprocess.Popen(['gedit ~/results.txt'], shell=True)
        #subprocess.Popen(['results.txt'], shell=True)
        
def combo():   ### delete eventually
    storage_csv = open("StorageCSV.txt","r")
    storage_data = storage_csv.read()
    storage_csv.close()
    network_csv = open("NetworkCSV.txt","r")
    network_data = network_csv.read()
    network_csv.close()
    compute_csv = open("ComputeCSV.txt","r")
    compute_data = compute_csv.read()
    compute_csv.close()
    # combine csvs
    bench_results = str(storage_data) + ", " + str(network_data) + ", " + str(compute_data)
    #print(bench_results)
    bench_res = open("csvFormResults.txt","w")
    bench_res.write(bench_results)
    bench_res.close()
    print("gig em")
    
def parse_cpu():
    #Python Script

    CPUlines = [] #Declare an empty list named "lines"
    with open ('CompTestSSHoutput.txt', 'rt') as in_file:  #Open file
        for line in in_file: #For each line of text store in a string variable named "line", and
            CPUlines.append(line)  #add that line to our list of lines.

    text_file = open("ComputeCSV.txt", "w")

    #sysbench CPU Speed Events per second
    lines14 = CPUlines[14];
    sysbench = lines14[23:31];
    text_file.write(sysbench)

    #comma
    text_file.write(",")

    #space
    text_file.write(" ")

    #Average Latency
    line22 = CPUlines[22];
    AverageLat = line22[47:51];
    text_file.write(AverageLat)

    #comma
    text_file.write(",")

    #space
    text_file.write(" ")

    #Processor Frequency
    line38 = CPUlines[38];
    ProFreq = line38[14:22];
    text_file.write(ProFreq)

    #comma
    text_file.write(",")

    #space
    text_file.write(" ")

    #RAM Amount
    line39 = CPUlines[39];
    RAM = line39[14:17];
    text_file.write(RAM)

    #comma
    text_file.write(",")

    #space
    text_file.write(" ")

    #Average CPU Write Speed
    line111 = CPUlines[111];
    CPUWrite = line111[16:21];
    text_file.write(CPUWrite)

    #comma
    text_file.write(",")

    #space
    text_file.write(" ")

    #CPU Average Usage Percent
    line128 = CPUlines[128];
    CPUPercent = line128[10:15];
    text_file.write(CPUPercent)

    text_file.close()


def parse_storage():
    #Parse Storage Output
    lines = [] #Declare an empty list named "lines"
    with open ('StorageSSHOutput.txt', 'rt') as in_file:  #Open file
        for line in in_file: #For each line of text store in a string variable named "line", and
            lines.append(line)  #add that line to our list of lines.

    text_file = open("StorageCSV.txt", "w")

    #sysbench Bandwidth (MiB/s)
    test = lines[19];
    sysbench = test[27:35];
    text_file.write(sysbench)

    #comma
    line37 = lines[37];
    comma = line37[26];
    text_file.write(comma)

    #space
    text_file.write(" ")

    #sequential read IOPs
    line47 = lines[47];
    SeqIOPs = line47[14:18];
    text_file.write(SeqIOPs)

    #comma
    line37 = lines[37];
    comma = line37[26];
    text_file.write(comma)

    #space
    text_file.write(" ")

    #sequential read BW (MiB/s)
    SeqBW = line47[23:27];
    text_file.write(SeqBW)

    #comma
    line37 = lines[37];
    comma = line37[26];
    text_file.write(comma)

    #space
    text_file.write(" ")

    #sequential write IOPs
    line84 = lines[84];
    SeqWIOPs = line84[14:18];
    text_file.write(SeqWIOPs)

    #comma
    line37 = lines[37];
    comma = line37[26];
    text_file.write(comma)

    #space
    text_file.write(" ")

    #sequential write BW
    SeqWBW = line84[23:27];
    text_file.write(SeqWBW)

##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random read IOPs
##    line120 = lines[120];
##    RandRIOPs = line120[14:18];
##    text_file.write(RandRIOPs)
##
##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random read BW
##    RandRBW = line120[23:27];
##    text_file.write(RandRBW)
##
##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random write IOPS
##    line157 = lines[157];
##    RandWIOPs = line157[14:18];
##    text_file.write(RandWIOPs)
##
##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random write BW
##    RandWBW = line157[23:27];
##    text_file.write(RandWBW)
##
##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random read/write Read IOPS
##    line195 = lines[195];
##    RandRWreadIOPs = line195[14:18];
##    text_file.write(RandRWreadIOPs)
##
##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random (read/write) Read BW
##    RandRWreadBW = line195[23:27];
##    text_file.write(RandRWreadBW)
##
##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random read/write Write IOPS
##    line207 = lines[207];
##    RandRWwriteIOPs = line207[14:17];
##    text_file.write(RandRWwriteIOPs)
##
##    #comma
##    line37 = lines[37];
##    comma = line37[26];
##    text_file.write(comma)
##
##    #space
##    text_file.write(" ")
##
##    #random read/write Write BW
##    RandRWwriteBW = line207[22:26];
##    text_file.write(RandRWwriteBW)

    text_file.close()

def parse_network():    
    
#Python Script

    Netlines = [] #Declare an empty list named "lines"
    with open ('NetworkSSHOutput.txt', 'rt') as in_file:  #Open file lorem.txt for reading of text data.
        for line in in_file: #For each line of text store in a string variable named "line", and
            Netlines.append(line)  #add that line to our list of lines.

    text_file = open("NetworkCSV.txt", "w")

    #Sender Transfer Amount
    lines15 = Netlines[15];
    TransAmntS = lines15[25:29];
    text_file.write(TransAmntS)

    #comma
    text_file.write(",")

    #Sender Brandwidth Amount
    TransAmntS = lines15[39:42];
    text_file.write(TransAmntS)

    #comma
    text_file.write(",")

    #Reciever Transfer Amount
    lines16 = Netlines[16];
    TransAmntR = lines16[25:29];
    text_file.write(TransAmntR)

    #comma
    text_file.write(",")

    #Reciever Brandwidth Amount
    TransAmntR = lines16[39:42];
    text_file.write(TransAmntR)

    text_file.close()
