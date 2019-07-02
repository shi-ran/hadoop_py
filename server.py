from pyhd_io import *

host = ''
port = 8989

TaskData = {}

def do_get(taskid, processname, partitionerid):
    logging.debug(TaskData)
    result = "no"
    if TaskData.has_key(taskid):
        task = TaskData.get(taskid)
        logging.debug(task)
        key = processname + partitionerid
        if partitionerid == "" :
            keys = task.keys()
            logging.debug(keys)

            for k in keys :
                if k.find(processname) != -1:
                    key = k
                    partitionerid = k[len(processname)]
                    logging.debug(key)
        if task.has_key(key):
            getresource = task.get(key)
            result = "ok"
            result += partitionerid + ""
            for i in getresource :
                result += i + ""
                del task[key]
    logging.info("got %s:", result)
    return result

def do_put(taskid, processname, partitionerid, resource):
    logging.denug(TaskData)
    result = "no"
    if not TaskData.has_key(taskid):
        TaskData[taskid] = {}
    task = TaskData.get(taskid)
    key = processname + partitionerid

    if not task.has_key(processname + partitionerid) :
        task[key] = []
    putresource = task.get(key)
    putresource.append(resource)
    result = "ok"
    return result
if __name__ == '__main__' :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(host,port)
    logging.ingo("%s", "warning for connections.....")
    s.listen(100)

    while 1 :
        try:
            client, clientaddr = s.accept()
            logging.info("get connection from %s:", client.getpeername)
            data = client.recv(1024)
            logging.info(data)
            sp = data.split()
            logging.info(sp)
            if len(sp) < 3 :
                client.close()
                continue
            if len(sp) >= 3 :
                method = sp[0]
                taskid = sp[1]
                processname = sp[2]
            resource = ""
            partitionerid = ""
            if len(sp) >=4 :
                partitionerid = sp[3]
            if len(sp) >= 5 :
                resource = sp[4]
            logging.debug("all are %s:", method, taskid, processname, partitionerid, resource)
            if method == 'get' :
                logging.info("get process")
                result = do_get(taskid, processname, partitionerid)
            if method == 'put' :
                logging.info("put process")
                result = do_put(taskid, processname, partitionerid, resource)
            client.sendall(result)
            client.close()
        except socket.error, e :
            pass