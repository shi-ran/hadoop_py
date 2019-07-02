import sys
import pickle
import socket
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s;%(levelname)s: %(message)s"
)

def savetofile(filename, obj):
    with open (filename, 'wb') as f:
        pickle.dump(obj, f)
    f.close()

def loadfromfile(filename):
    obj=''
    with open (filename,'rb') as f:
        obj=pickle.load(f)
    f.close()
    return obj

host = "127.0.0.1"
port = "8990"
port_2 = "8989"

def savetoserver(taskid, processname, partitionerid, resource):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port_2))
        senddata = "put" + taskid + "" + processname + ""
        if partitionerid != "":
            senddata += partitionerid + ""
        if resource != "" :
            senddata += resource + ""
        s.sendall(senddata)
        t = s.recv(300000)
        return t

    except socket.error, e:
        pass


def loadfromserver(taskid, processname, partitionerid):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port_2))
    senddata = "get" + taskid + "" + processname + ""
    if partitionerid != "" :
        senddata += partitionerid + ""
    s.sendall(senddata)
    t = s.recv(300000)
    logging.debug(t)
    return t

def taskcomplete(taskid, processname):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print host, port
    s.connect((host, port))
    senddata = "get" + taskid + "" + processname + ""
    s.sendall(senddata)
    t = s.recv(300000)
    return t

if __name__ == '__main__':
    for i in range (1,10):
        loadfromserver("sort_task", "ImputSplit", "")