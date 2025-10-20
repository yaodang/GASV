#!/usr/bin/env python3

import os,configparser
import numpy as np
import sys
sys.path.append("..//")
from COMMON import *

def read_cnt(filename, Param):
    """
    Read the cnt file
    ---------------------
    input: 
        filename    : the control file name
    output: 
        Param       : the class type, see cntparameter.py
    ---------------------
    """
    if not os.path.exists(filename):
        sys.stderr.write('    Error: the cnt file not exists!')
        sys.exit()
    print('    Reading the control file......')   
    fid = open(filename, 'r')
    lines = fid.readlines()
    fid.close()
    
    keyword, posit = getKeyandPosit(lines)
    
    #SETUP
    ParamSetup = SETUP()
    ParamSetup.getValue(lines, keyword, posit)
    
    #FLAGS
    ParamFlags = FLAGS()
    ParamFlags.getValue(lines, keyword, posit)

    #DATA
    ParamData = DATA()
    ParamData.getValue(lines, keyword, posit)
    
    ParamGlobal = GLOBAL()
    ParamGlobal.getValue(lines, keyword, posit)
    
    #MAPPING
    ParamMap = MAPPING()
    ParamMap.getValue(lines, keyword, posit)
    
    #CONSTRAINTS
    ParamCon = CONSTRAINTS()
    ParamCon.getValue(lines, keyword, posit)
    
    #ARCS
    ParamArcs = ARCS()
    ParamArcs.getValue(lines, keyword, posit)
    
    #TIE
    ParamTie = TIE()
    ParamTie.getValue(lines, keyword, posit)
    
    #OUTPUT
    ParamOut = OUTPUT()
    ParamOut.getValue(lines, keyword, posit)
    
    Param.creatParam(ParamSetup, ParamFlags, ParamData, ParamGlobal, ParamMap, \
                     ParamCon, ParamArcs, ParamTie, ParamOut)
    
def read_dbPathFile(fileName):
    # read the ini file for vgosDB make
    if not os.path.exists(fileName):
        sys.stderr.write('    Error: the ini file of vgosDB make isn\'t exists!\n\n')
        sys.exit()

    config = configparser.ConfigParser()
    config.read(fileName)

    paramPath = {}
    for section in config.sections():
        paramPath[section] = {}
        for key, value in config.items(section):
            paramPath[section][key] = value

    return paramPath

def getKeyandPosit(lines):
    """
    ---------------------
    input: 
        lines      : the cnt file lines
    output: 
        keyword    : the kew word list
        posit      : the key word line posit
    ---------------------
    """    
    keyword = []
    posit   = []
    
    k = 0
    for line in lines:
        if line[0] == '$':
            keyword.append(line[1:-1])
            posit.append(k)
        k = k + 1    
    
    return keyword, posit
