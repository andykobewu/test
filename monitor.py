import wmi 
import time
import winsound 
import logging
import logging.config
from operator import itemgetter, attrgetter
from os import path

import packages.sysinfo #使用wmi
#import packages.ProcessInfo #使用

#def ShowProcessInfo():
#    processInfoList = packages.ProcessInfo.getAllProcessInfo()
#    processInfoList.sort(key=itemgetter(2), reverse=True)
#    for p in processInfoList:       
#        logger.info(p)

def ShowProcessInfo(wmiService = None):
    processInfoList = packages.sysinfo.getAllProcessInfo(wmiService)
    processInfoList.sort(key=itemgetter(2), reverse=True)
    for p in processInfoList:       
        logger.info(p)

if __name__ == '__main__':
    MemPerWorningLine = 50
    MemPerErrorLine = 20
    ErrorAlertCount = 10
    ProcessInfoCount = 10
    counterProcessInfo = ProcessInfoCount

    print("Memory monitor start!")
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
    #print(log_file_path)
    logging.config.fileConfig(log_file_path)
    logger = logging.getLogger("example01")
    wmiService = wmi.WMI()
    while True:
        memPercent = int(packages.sysinfo.getSysInfo(wmiService)['memPercent'])
        strMemPercent = 'FreeMemory: ' + str(memPercent) + '%'
        if(memPercent < MemPerErrorLine):
            logger.error(strMemPercent)
            #ProcessInfoList
            counterProcessInfo+=1
            if(counterProcessInfo >= ProcessInfoCount):
                ShowProcessInfo(wmiService)
                counterProcessInfo = 0
            #ALert
            counter = 1
            while counter <= ErrorAlertCount:
                winsound.Beep(2080, 100) 
                time.sleep(0.1)
                counter += 1
        elif(memPercent < MemPerWorningLine):
            logger.warning(strMemPercent)
            #ProcessInfoList
            counterProcessInfo+=1
            if(counterProcessInfo >= ProcessInfoCount):
                ShowProcessInfo(wmiService)
                counterProcessInfo = 0
            #ALert
            winsound.Beep(2015, 2000) 
        else:
            logger.info(strMemPercent)
        time.sleep(3)