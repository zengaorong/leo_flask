import subprocess

ret = subprocess.call("ping  %s -w 1000" % '172.22.185.1' ,shell=True ,stdout=subprocess.PIPE)
print(ret)