import sys
from pyhd_io import *

def run_task(modename,functionname,arg):
    obj = __import__(modename)
    c = getattr(obj, modename)
    obj  = c()
    fun = getattr(obj, functionname)
    fun(arg)

if __name__ == '__main__':
    logging.debug(sys.argv)
    logging.debug(len(sys.argv))
    run_task(sys.argv[1], sys.argv[2], sys.argv[3])