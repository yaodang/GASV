#!/usr/bin/env python3

import os
import numpy as np

def createArcFile(path, sessionType, analysisCenter, outName, writeType):
    '''
    Create the Arc file for a certain type observe.

    Parameters
    ----------
    path : TYPE
        DESCRIPTION.
    sessionType : TYPE
        DESCRIPTION.
    analysisCenter : TYPE
        DESCRIPTION.
    outName : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    acOrder = ['IVS','GSFC']
    
    if os.path.exists(path):
        dirs = os.listdir(path)
        
        session = []
        version = []
        ac = []
        for idir in dirs:
            if sessionType in idir:
                sessionPath = path+'/'+idir
                dirFile = os.listdir(sessionPath)
                
                findFile = []
                for file in dirFile:
                    if analysisCenter in file:
                        findFile.append(file)
                        
                if len(findFile):
                    session.append(idir)
                    findFile.sort()
                    
                    index = findFile[-1].index('_V')
                    version.append(int(findFile[-1][index+2:index+5]))
                    ac.append(analysisCenter)
        
        if len(session):
            print(len(session))
            index = np.argsort(np.array(session))
            
            fid = open(path+'/'+outName, writeType)
            for i in index:
                fid.writelines('$%s    %d    %s\n'%(session[i],version[i],ac[i]))
            fid.close()

createArcFile('/Users/dangyao/work/software/VIPS/vgosDb/2021/',\
              'XA', 'IVS', 'sx_24.arc', 'a')

                    
                