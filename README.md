# Mining-Vms

This project is to develop a tool that benchmarks virtual machines for unbiased, statistical performance data. 

## Installation

Download [this](https://github.tamu.edu/natkinson20/Mining-VMs/blob/master/run.sh) file and run in linux terminal using the following command:


```bash
chmod +x /path/to/run.sh
/path/to/run.sh
```

## Launch GUI

```bash
python3 ~/Mining-VMs/gui.py
```
## Troubleshooting

It is strongly advized for you to simply restart the gui.py file as most errors can be resolved with a simple reset.

### Error:
```bash
botocore.exceptions.ConfigParseError: Unable to parse config file: /path/to/.aws/credentials
```
### Solution: 
Navigate to ```bash ~/.aws/credentials ``` and ensure the format of the file is the following:
```bash
[default]
aws_access_key_id = MYACCESSKEY
aws_secret_access_key = MYSECRETKEY
```
### Error:
```bash
File "/home/troubleshoot/Mining-VMs/gui.py", line 168, in getPastCreds
    subprocess.Popen(['chmod +x ' +pastCredsLocation], shell=True)
TypeError: must be str, not tuple
```
### Solution: 
Ignore these, they do not impact the rest of the code.

### Error(s):
```bash
File "/home/cleaninstall/Mining-VMs/gui.py", line 57, in run_benchmarks
    server_id=instances[1].id
IndexError: list index out of range
```
```bash
file1 = open(profileName + ".config","w")
PermissionError: [Errno 13] Permission denied: 'zzz.config'
chmod: cannot access 'zzz.config': No such file or directory
```
```bash
botocore.exceptions.NoRegionError: You must specify a region.
```
### Solution:
Restart gui.py
