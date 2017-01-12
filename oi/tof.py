import subprocess

def readSingle():
    proc = subprocess.Popen(["blobs/i2ctof"], stdout=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    errcode = proc.returncode
    return out.decode('UTF-8')

def readAll():
    proc = subprocess.Popen(["blobs/i2ctof_multiple"], stdout=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    errcode = proc.returncode
    out=out.decode('UTF-8').split()
    out = [ int(x) for x in out ]
    return out

def readSide(n):
    readings=readAll()
    print (readings[2*n],readings[2*n+1])

