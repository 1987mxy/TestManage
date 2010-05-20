import sys
import os
if __name__ == '__main__':
    for i in os.listdir('./log'):
        resultFile = None
        logFile = open('./log/%s'%i,'r')
        for j in logFile.readlines():
            if sys.argv[1] in j:
                if not resultFile:
                    resultFile = open('r_%s'%i,'w')
                resultFile.write('%s\n'%j)
        if resultFile:
            resultFile.close()
        logFile.close()
            
                
