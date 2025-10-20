#!/usr/bin/env python3

import sys,time
import numpy as np
from scipy import sparse
from COMMON import *
from SOLVE.solve_other import *
from SOLVE.solve_constrain import *
        
def designMatrix(scanInfo, staObs, Param, stationInfo, sourceInfo, P_obs, oc_obs):
    """
    Design the matrix A
    ---------------------
    input: 
        filename    : the control file name
    output: 
        Param       : the class type, see class_all.py
    ---------------------
    """
    na = len(scanInfo.stationAll)
    nobs = sum(scanInfo.scanObsNum)
    mjd0 = np.floor(scanInfo.scanMJD[0])
    
    A = LABEL()
    H = LABEL()
    Ph = LABEL()
    och = LABEL()

    estParam = ESTPARAM()
    staNNRT = NNRNNT()
    # print(os.path.abspath(__file__))
    souNNR = NNRSOU()
    
    clk_flag = 0
    zwd_flag = 0
    grad_flag = 0
    xyz_flag = 0
    
    
    HnnrtSta = []
    for ista in range(na):
        mjdSta = staObs.mjd[ista]
        minute = (mjdSta - mjd0)*24*60
        
        
        # create clock matrix
        clk_flag = clkMatrix(scanInfo, ista, staObs, nobs, mjdSta, mjd0, Param, minute, A, H, Ph, estParam, clk_flag)
            
        # create zwd matrix
        zwd_flag = zwdMatrix(scanInfo, ista, staObs, nobs, mjdSta, mjd0, Param, minute, A, H, Ph, estParam, zwd_flag)
        
        # create gradient matrix
        grad_flag = gradMatrix(scanInfo, ista, staObs, nobs, mjdSta, mjd0, Param, minute, A, H, Ph, estParam, grad_flag)

        
        # create station coordinate matrix
        xyz_flag, HnnrtSta = xyzMatrix(scanInfo, Param, ista, staObs, nobs, A, H, Ph, estParam, staNNRT, xyz_flag, HnnrtSta)

    if Param.Flags.sou[0] == 'YES':
        souMatrix(scanInfo,sourceInfo,Param,nobs,A,H,Ph,och,souNNR,estParam)
    
    if Param.Flags.xyz[0] == 'YES':
        temp = sum(sum(HnnrtSta))
        if temp != 0:
            PnnrtSta = sparse.block_diag((np.eye(3)*1/Param.Const.sigma_nnr_nnt_sta[0]**2,\
                                         np.eye(3)*1/Param.Const.sigma_nnr_nnt_sta[1]**2))
            try:
                HnnrtSta = np.linalg.inv(HnnrtSta.T @ HnnrtSta) @ HnnrtSta.T
            except np.linalg.LinAlgError:
                print("Error: NNR/NNT constraints set！")
                sys.exit()
                
            H.xyz = sparse.vstack((H.xyz,HnnrtSta))
            Ph.xyz = sparse.block_diag((Ph.xyz,PnnrtSta))
        och.xyz = np.zeros(H.xyz.shape[0])
        # H.xyz,Ph.xyz,och.xyz = rmBlank(H.xyz, Ph.xyz, och.xyz)
        
    och.clk = np.zeros(H.clk.shape[0])
    if Param.Flags.zwd != 'NO':
        och.zwd = np.zeros(H.zwd.shape[0])
    
    if Param.Flags.gradient[0] == 'YES':
        och.ngr = np.zeros(H.ngr.shape[0])
        och.egr = np.zeros(H.egr.shape[0])
        
    # create eop matrix
    pEOP = np.array(scanInfo.pEOP)
    if Param.Flags.type == 'SEGMENT':
        segMode(pEOP.T, scanInfo.scanMJD, scanInfo.scanObsNum, Param, mjd0, A, H, Ph, och, estParam)
    if Param.Flags.type == 'POLY':
        polyMode(pEOP.T, Param, A, H, Ph, och, estParam)
        
    if len(scanInfo.blClkList) > 0 and Param.Flags.blClk == 'IN':
        blClkMatrix(scanInfo, staObs, nobs, A, H, Ph, och, estParam)
    
    Ablk = getattr(A, estParam.param[0])
    Hblk = getattr(H, estParam.param[0])
    Pblk = getattr(Ph, estParam.param[0])
    Oblk = getattr(och, estParam.param[0])
    
    for i in range(1,len(estParam.param)):
        if estParam.num[i] != 0:
            name = estParam.param[i]
            Ablk = sparse.hstack((Ablk, getattr(A, name)))
            try: 
                temp = len(getattr(H, name))
            except TypeError:
                temp = getattr(H, name).shape[0]
            if temp:
                Hblk = sparse.block_diag((Hblk, getattr(H, name)))
                Pblk = sparse.block_diag((Pblk, getattr(Ph, name)))
                Oblk = np.hstack((Oblk, getattr(och, name)))
            
    Hblk,Pblk,Oblk = rmBlank(Hblk, Pblk, Oblk)
    P_obs = sparse.block_diag((sparse.csr_matrix(P_obs), Pblk))
    oc = np.hstack((oc_obs, Oblk))
    
    # twin station
    if Param.Const.tie != 'NO':
        Htie,Phtie,OCtie = constrainTie(Ablk.shape[1], Param, scanInfo, stationInfo, estParam)
        if len(Htie.toarray()) != 0:
            Hblk = sparse.vstack((Hblk, Htie))
            P_obs = sparse.block_diag((P_obs, Phtie))
            oc = np.hstack((oc, OCtie))

    #print(Ablk.toarray())
    return estParam,Ablk,Hblk,P_obs,oc,staNNRT,souNNR

def blClkMatrix(scanInfo, staObs, nobs, A, H, Ph, och, estParam):
    blclk = np.zeros((nobs, len(scanInfo.blClkList)))
    
    blPosit = np.where(scanInfo.Obs2Scan != 0)
    blList = scanInfo.Obs2Baseline[blPosit[0]]
    exclude = []
    
    num = 0
    for i in range(len(scanInfo.blClkList)):
        temp = np.sum(abs(blList - scanInfo.blClkList[i]),1)
        findPosit =  np.where(temp == 0)
        
        if len(findPosit[0])>0:
            blclk[findPosit[0],i] = 1
            num += 1
        else:
            exclude.append(i)
    
    if len(exclude):
        blclk = np.delete(blclk, exclude, axis=1)
    
    
    paramP = estParam.param.index('blclk')
    estParam.num[paramP] = num
    
    A.blclk = blclk
    
    H.blclk = np.zeros((num,num))
    Ph.blclk = np.zeros((num,num))
    och.blclk = np.zeros(num)
        

def clkMatrix(scanInfo, ista, staObs, nobs, mjdSta, mjd0, Param, minute, A, H, P, estParam, flag):
    """
    Get the A/H/P/och matrix of clock
    ---------------------
    input:
        scanInfo    : scan struct
        ista        :
        staObs      :
        nobs        :
        mjdSta      : epochs of the observations carried out by the station in mjd
        mjd0        : mjd of the first day of the session at 0:00 UTC
        Param       : 
        minute      :
    output: 
        A.clk, H.clk, P.clk, och.clk
    ---------------------
    """

    if (not scanInfo.stationAll[ista] == scanInfo.refclk) and (not scanInfo.stationAll[ista] in scanInfo.rmSta):
        order = Param.Flags.clk[1]
        obs_per_stat, n_unk, n_all, T_ = staWise(mjdSta, mjd0, Param, minute, 'clk')
        Aclk = apw_clk(obs_per_stat, T_, n_unk, n_all, minute, ista, staObs, nobs, order)
        const_clk = Param.Const.clk*1E-2 # [m]
        mat_clk = np.eye(n_unk+1) - np.eye(n_unk+1, k=1)
        mat_clk = sparse.csr_matrix(np.hstack((mat_clk,np.zeros((n_unk+1,order)))))
        
        if flag == 0:
            A.clk = Aclk
            H.clk = mat_clk[0:n_unk,:]
            P.clk = sparse.eye(n_unk)*1/const_clk**2
        else:
            A.clk = sparse.hstack((A.clk, Aclk))
            H.clk = sparse.block_diag((H.clk, mat_clk[0:n_unk,:]))
            P.clk = sparse.block_diag((P.clk, sparse.eye(n_unk)*1/const_clk**2))
            
        estParam.num[0] += Aclk.shape[1]
        estParam.clkinfo[0].append(scanInfo.stationAll[ista])
        estParam.clkinfo[1].append(Aclk.shape[1])
        estParam.tmjd[0].extend(T_)
        flag += 1
        
    return flag
        
def zwdMatrix(scanInfo, ista, staObs, nobs, mjdSta, mjd0, Param, minute, A, H, P, estParam, flag):
    """
    Get the A/H/P/och matrix of clock
    ---------------------
    input:
        scanInfo    : scan struct
        ista        :
        staObs      :
        nobs        :
        mjdSta      : epochs of the observations carried out by the station in mjd
        mjd0        : mjd of the first day of the session at 0:00 UTC
        Param       : 
        minute      :
    output: 
        A.clk, H.clk, P.clk, och.clk
    ---------------------
    """ 
    if Param.Flags.zwd != 'NO':
        if not scanInfo.stationAll[ista] in scanInfo.rmSta:
            #wet troposphere
            obs_per_stat, n_unk, n_all, T_ = staWise(mjdSta, mjd0, Param, minute, 'zwd')
            Azwd = apw_zwd(obs_per_stat, T_, n_unk, n_all, minute, ista, staObs, nobs)
            
            const_atm = Param.Const.atm*1E-2 # [m]
            mat_zwd = sparse.eye(n_unk+1) - sparse.eye(n_unk+1, k=1)
                
            if flag == 0:
                A.zwd = Azwd
                H.zwd = mat_zwd[0:n_unk,0:n_unk+1]
                P.zwd = sparse.eye(n_unk)*1/const_atm**2
                
            else:
                A.zwd = sparse.hstack((A.zwd, Azwd))
                H.zwd = sparse.block_diag((H.zwd, mat_zwd[0:n_unk,0:n_unk+1]))
                P.zwd = sparse.block_diag((P.zwd, sparse.eye(n_unk)*1/const_atm**2))
                
            temp = estParam.param.index('zwd')    
            estParam.num[temp] += Azwd.shape[1]
            estParam.zwdinfo[0].append(scanInfo.stationAll[ista])
            estParam.zwdinfo[1].append(Azwd.shape[1])
            estParam.tmjd[temp].extend(T_)
            
            flag += 1
    
    return flag


def gradMatrix(scanInfo, ista, staObs, nobs, mjdSta, mjd0, Param, minute, A, H, P, estParam, flag):
    """
    Get the A/H/P/och matrix of clock
    ---------------------
    input:
        scanInfo    : scan struct
        ista        :
        staObs      :
        nobs        :
        mjdSta      : epochs of the observations carried out by the station in mjd
        mjd0        : mjd of the first day of the session at 0:00 UTC
        Param       : 
        minute      :
    output: 
        A.clk, H.clk, P.clk, och.clk
    ---------------------
    """ 
    if Param.Flags.gradient[0] == 'YES':
        if not scanInfo.stationAll[ista] in scanInfo.rmSta:
            #wet troposphere
            obs_per_stat, n_unk, n_all, T_ = staWise(mjdSta, mjd0, Param, minute, 'grad')
            Angr,Aegr = apw_gradient(obs_per_stat, T_, n_unk, n_all, minute, ista, staObs, nobs)
            #mat_grad = sparse.eye(n_unk+1) - sparse.eye(n_unk+1, k=1)
            #mat_h = sparse.vstack((mat_grad[0:n_unk,0:n_unk+1],sparse.eye(n_unk+1)))

            #matRelP = sparse.eye(n_unk) * 1 / Param.Const.grad[0] ** 2
            #matAbsP = sparse.eye(n_unk + 1) * 1 / Param.Const.grad[1] ** 2
            #mat_p = sparse.block_diag((matRelP, matAbsP))


            mat_rel = sparse.eye(n_unk + 1) - sparse.eye(n_unk + 1, k=1)
            mat_abs = np.eye(n_unk + 1)[:n_unk]
            matRelP = sparse.eye(n_unk) * 1 / (Param.Const.grad[0]*1E-2) ** 2
            matAbsP = sparse.eye(n_unk) * 1 / (Param.Const.grad[1]*1E-2) ** 2

            # east gradient
            mat_egr_h = sparse.vstack((mat_rel[:n_unk], mat_abs))
            mat_egr_p = sparse.block_diag((matRelP,matAbsP))

            # north gradient
            mat_ngr_h = sparse.vstack((mat_rel[:n_unk], mat_abs))
            mat_ngr_p = sparse.block_diag((matRelP, matAbsP))

            if flag == 0:
                A.ngr = Angr
                A.egr = Aegr
                H.ngr = mat_ngr_h
                H.egr = mat_egr_h
                P.ngr = mat_ngr_p
                P.egr = mat_ngr_p
            else:
                A.ngr = sparse.hstack((A.ngr, Angr))
                H.ngr = sparse.block_diag((H.ngr, mat_ngr_h))
                P.ngr = sparse.block_diag((P.ngr, mat_ngr_p))
                
                A.egr = sparse.hstack((A.egr, Aegr))
                H.egr = sparse.block_diag((H.egr, mat_egr_h))
                P.egr = sparse.block_diag((P.egr, mat_egr_p))
            
            temp = estParam.param.index('ngr')
            estParam.num[temp] += Angr.shape[1]
            estParam.ngrinfo[0].append(scanInfo.stationAll[ista])
            estParam.ngrinfo[1].append(Angr.shape[1])
            estParam.tmjd[temp].extend(T_)
            
            temp = estParam.param.index('egr')    
            estParam.num[temp] += Aegr.shape[1]
            estParam.egrinfo[0].append(scanInfo.stationAll[ista])
            estParam.egrinfo[1].append(Aegr.shape[1])
            estParam.tmjd[temp].extend(T_)
            
            flag += 1
    
    return flag

def polyMode(pEOP, Param, A, H, Ph, och, estParam):
    
    rad2mas = (180/np.pi)*3600*1000
    rad2ms = rad2mas/15
    if Param.Flags.ut1[0] == 'YES':
        estParam.num[estParam.param.index('ut1')] = 1
        temp = pEOP[2,:]*const.c*(1/rad2ms)
        A.ut1 = temp.reshape(temp.shape[0],1)
        
        if len(Param.Const.erp):
            H.ut1 = np.array([[1]])
            Ph.ut1 = np.array([[1/Param.Const.erp[1]**2]])
        else:
            H.ut1 = np.array([[0]])
            Ph.ut1 = np.array([[0]])
        
        och.ut1 = np.array([0])
        
    if Param.Flags.lod[0] == 'YES':
        estParam.num[estParam.param.index('lod')] = 1
        temp = pEOP[7,:]*const.c*(1/rad2ms)
        A.lod = temp.reshape(temp.shape[0],1)
        
        if len(Param.Const.erp):
            H.lod = np.array([[1]])
            Ph.lod = np.array([[1/Param.Const.erp[3]**2]])
        else:
            H.lod = np.array([[0]])
            Ph.lod = np.array([[0]])
        och.lod = np.array([0])
        
    if Param.Flags.pm[0] == 'YES':
        estParam.num[estParam.param.index('pmx')] = 1
        estParam.num[estParam.param.index('pmy')] = 1
        
        temp = pEOP[0,:]*const.c*(1/rad2mas)
        A.pmx = temp.reshape(temp.shape[0],1)
        
        temp = pEOP[1,:]*const.c*(1/rad2mas)
        A.pmy = temp.reshape(temp.shape[0],1)
        
        if len(Param.Const.erp):
            H.pmx = np.array([[1]])
            Ph.pmx = np.array([[1/Param.Const.erp[0]**2]])
            H.pmy = np.array([[1]])
            Ph.pmy = np.array([[1/Param.Const.erp[0]**2]])
        else:
            H.pmx = np.array([[0]])
            Ph.pmx = np.array([[0]])
            H.pmy = np.array([[0]])
            Ph.pmy = np.array([[0]])
        
        och.pmx = np.array([0])
        och.pmy = np.array([0])
        
    if Param.Flags.pmr[0] == 'YES':
        estParam.num[estParam.param.index('pmxr')] = 1
        estParam.num[estParam.param.index('pmyr')] = 1
        
        temp = pEOP[5,:]*const.c*(1/rad2mas)
        A.pmxr = temp.reshape(temp.shape[0],1)
        
        temp = pEOP[6,:]*const.c*(1/rad2mas)
        A.pmyr = temp.reshape(temp.shape[0],1)
        
        if len(Param.Const.erp):
            H.pmxr = np.array([[1]])
            Ph.pmxr = np.array([[1/Param.Const.erp[2]**2]])
            H.pmyr = np.array([[1]])
            Ph.pmyr = np.array([[1/Param.Const.erp[2]**2]])
        else:
            H.pmxr = np.array([[0]])
            Ph.pmxr = np.array([[0]])
            H.pmyr = np.array([[0]])
            Ph.pmyr = np.array([[0]])
            
        och.pmxr = np.array([0])
        och.pmyr = np.array([0])

    #if Param.Flags.nut[0] == 'YES':
    if Param.Flags.nut[0] == 'XY_OFFSET':
        estParam.num[estParam.param.index('nutx')] = 1
        estParam.num[estParam.param.index('nuty')] = 1
        
        temp = pEOP[3,:]*const.c*(1/rad2mas)
        A.nutx = temp.reshape(temp.shape[0],1)
        H.nutx = np.array([[0]])
        Ph.nutx = np.array([[0]])
        och.nutx = np.array([0])
        
        temp = pEOP[4,:]*const.c*(1/rad2mas)
        A.nuty = temp.reshape(temp.shape[0],1)
        H.nuty = np.array([[0]])
        Ph.nuty = np.array([[0]])
        och.nuty = np.array([0])
        
def segMode(pEOP, scanMJD, scanObsNum, Param, mjd0, A, H, Ph, och, estParam):
    """
    Design matrix for the EOP
    ---------------------
    input: 
        pEOP           : the EOP partial matrix 
        Param          : the 
        mjd0           : mjd of the first day of the session at 0:00 UTC
    output: 
        Param       : the class type, see cntparameter.py
    ---------------------
    """
    # create the ut1 matrix    
    if Param.Flags.ut1[0] == 'YES':
        #estParam.append('ut1')
        Apwdut1, Hdut1, Phdut1, oc_hdut1 = eopMatrix(pEOP, scanMJD, scanObsNum, Param, mjd0, 'ut1', estParam)
        A.ut1 = Apwdut1
        H.ut1 = Hdut1
        Ph.ut1 = Phdut1
        och.ut1 = oc_hdut1
        posit = estParam.param.index('ut1')
        estParam.num[posit] += A.ut1.shape[1]
        
    # create the pole matrix    
    if Param.Flags.pm[0] == 'YES':
        #estParam.append('pmx')
        Apwdpmx, Hdpmx, Phdpmx, oc_hdpmx = eopMatrix(pEOP, scanMJD, scanObsNum, Param, mjd0, 'pmx', estParam)
        A.pmx = Apwdpmx
        H.pmx = Hdpmx
        Ph.pmx = Phdpmx
        och.pmx = oc_hdpmx
        posit = estParam.param.index('pmx')
        estParam.num[posit] += A.pmx.shape[1]
        
        #estParam.append('pmy')
        Apwdpmy, Hdpmy, Phdpmy, oc_hdpmy = eopMatrix(pEOP, scanMJD, scanObsNum, Param, mjd0, 'pmy', estParam)
        A.pmy = Apwdpmy
        H.pmy = Hdpmy
        Ph.pmy = Phdpmy
        och.pmy = oc_hdpmy
        posit = estParam.param.index('pmy')
        estParam.num[posit] += A.pmy.shape[1]
        
    # create the nutation matrix    
    if Param.Flags.nut[0] == 'YES':
        #estParam.append('nutx')
        Apwdnutx, Hdnutx, Phdnutx, oc_hdnutx = eopMatrix(pEOP, scanMJD, scanObsNum, Param, mjd0, 'nutx', estParam)
        A.nutx = Apwdnutx
        H.nutx = Hdnutx
        Ph.nutx = Phdnutx
        och.nutx = oc_hdnutx
        posit = estParam.param.index('nutx')
        estParam.num[posit] += A.nutx.shape[1]
        
        #estParam.append('nuty')
        Apwdnuty, Hdnuty, Phdnuty, oc_hdnuty = eopMatrix(pEOP, scanMJD, scanObsNum, Param, mjd0, 'nuty', estParam)
        A.nuty = Apwdnuty
        H.nuty = Hdnuty
        Ph.nuty = Phdnuty
        och.nuty = oc_hdnuty
        posit = estParam.param.index('nuty')
        estParam.num[posit] += A.nuty.shape[1]
        
def xyzMatrix(scanInfo, Param, ista, staObs, nobs, A, H, P, estParam, aprSta, flag, Hnnrt):
    """
    Design matrix for the station coordinate
    ---------------------
    input: 
        scanInfo       : the 
        ista           : the
        staObs         :
        nobs           :
    output: 
        A.xyz
    ---------------------
    """
    
    if Param.Flags.xyz[0] == 'YES':
        station = scanInfo.stationAll[ista]
        if not station in Param.Flags.xyz:
            # get matrix
            Axyz = a_xyz(ista,staObs,nobs)
            flag_nnr,flag_nnt = False,False
            if station.strip() in Param.Const.nnr_nnt_sta[0]:
                if Param.Const.nnr_nnt_sta[0][0] == 'NO':
                    flag_nnr = True
            else:
                if Param.Const.nnr_nnt_sta[0][0] == 'YES':
                    flag_nnr = True
                    
            if station.strip() in Param.Const.nnr_nnt_sta[1]:
                if Param.Const.nnr_nnt_sta[1][0] == 'NO':
                    flag_nnt = True
            else:
                if Param.Const.nnr_nnt_sta[1][0] == 'YES':
                    flag_nnt = True
            
            staPosit = staObs.meanPosit[ista]
            H_sta = helmertTRF(flag_nnr, flag_nnt, staPosit)
            
            Pxyz = np.eye(3)*1/Param.Const.sta[1]**2
            if Param.Const.sta[0] == 'YES':
                Hxyz = np.eye(3)
            else:
                Hxyz = np.zeros((3,3))
                    
            if flag == 0:
                A.xyz = Axyz
                H.xyz = Hxyz
                P.xyz = Pxyz
                Hnnrt = H_sta
            else:
                A.xyz = sparse.hstack((A.xyz, Axyz))
                H.xyz = sparse.block_diag((H.xyz,Hxyz))
                P.xyz = sparse.block_diag((P.xyz,Pxyz))
                Hnnrt = np.vstack((Hnnrt,H_sta))
            
            posit = estParam.param.index('xyz')
            estParam.num[posit] += 3
            flag += 1
            

    return flag, Hnnrt
        
def staWise(mjdSta, mjd0, Param, minute, paramName):
    """
    Get the information of pwl
    ---------------------
    input: 
        mjdSta      : epochs of the observations carried out by the station in mjd
        mjd0        : mjd of the first day of the session at 0:00 UTC
        Param       : 
        minute      :
        paramName   : 'clk' or 'zwd' or 'grad'
    output: 
        Param       : the class type, see cntparameter.py
    ---------------------
    """
    n_unk = []
    n_all = []
    obs_per_stat = np.zeros(len(minute), dtype=int)
    
    mjd1 = min(mjdSta)
    mjd2 = max(mjdSta)
    
    t1 = (mjd1 - mjd0)*24*60
    t2 = (mjd2 - mjd0)*24*60

    if paramName == 'grad':
        est_len = float(Param.Flags.gradient[1])*60
    elif paramName == 'clk':
        est_len = float(Param.Flags.clk[0])
    else:
        est_len = getattr(Param.Flags, paramName)
    t1_ = np.floor(t1/est_len)*est_len
    t2_ = np.ceil(t2/est_len)*est_len
    n_unk = int((t2_-t1_)/est_len)
    T_ = np.linspace(t1_, t2_, n_unk+1)
    

    for inter in range(n_unk):
        if inter == n_unk - 1:
            tst = np.where((minute >= T_[inter]) & (minute <= T_[inter+1]))
        else:
            tst = np.where((minute >= T_[inter]) & (minute < T_[inter+1]))
        
        obs_per_stat[tst[0]]  = inter
        n_all.append(len(tst[0]))
        
    return obs_per_stat, n_unk, n_all, T_
    
def apw_clk(num, T_, n_unk, n_all, minute, ista, staObs, nobs, order):
    """
    Design matrix for the clocks as piecewise linear offsets.
    ---------------------
    input: 
        num         : the s
        T_          : the 
        n_unk       : 
        n_all       :
        minute      :
        ista        : the station index
        staObs      : the station observe class
        nobs        : the all observe number
        order       : the number of polynomials
    output: 
        Aclk        : the matrix of clock. (nobs, n_unk+1+order)
    ---------------------
    """
    first = staObs.first[ista]
    
    Apwclk = np.zeros((nobs, n_unk+1))
    Arqclk = np.zeros((nobs, order))
    
    k = 0
    for inter in range(n_unk):
        for iobs in range(n_all[inter]):
            Apwclk[staObs.oc_nob[ista][k],inter] = first[k]*(1 - (minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]]))
            Apwclk[staObs.oc_nob[ista][k],inter+1] = first[k]*(minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]])
            
            for io in range(order):
                Arqclk[staObs.oc_nob[ista][k],io] = first[k]*((minute[k]-T_[num[0]])/60/24)**(io+1)
            k += 1
    
    Aclk = np.hstack((Apwclk, Arqclk))
    # return sparse.csr_matrix(Apwclk),sparse.csr_matrix(Arqclk)
    return sparse.csr_matrix(Aclk)

def apw_zwd(num, T_, n_unk, n_all, minute, ista, staObs, nobs):
    """
    Design matrix for the wet tropsphere as piecewise linear ofsets
    ---------------------
    input: 
        istat       : the s
        staObs      : the 
        mjdSta      : epochs of the observations carried out by the station in mjd
        mjd0        : mjd of the first day of the session at 0:00 UTC 
    output: 
        Azwd        : design matrix for pwlo zwd estimates
    ---------------------
    """
    mf = staObs.mf[ista]
    first = staObs.first[ista]
    
    Azwd = np.zeros((nobs, n_unk+1))
    
    k = 0
    for inter in range(n_unk):
        for iobs in range(n_all[inter]):
            Azwd[staObs.oc_nob[ista][k],inter] = first[k]*(1 - (minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]]))*mf[k]
            Azwd[staObs.oc_nob[ista][k],inter+1] = first[k]*(minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]])*mf[k]
            
            k += 1
    #print(mf,Azwd)
    return sparse.csr_matrix(Azwd)

def apw_gradient(num, T_, n_unk, n_all, minute, ista, staObs, nobs):
    """
    Design matrix for the gradients as piecewise linear ofsets
    ---------------------
    input: 
        istat       : the s
        staObs      : the 
        mjdSta      : epochs of the observations carried out by the station in mjd
        mjd0        : mjd of the first day of the session at 0:00 UTC 
    output: 
        Angr        : design matrix for pwlo north gradient estimates
        Aegr        : design matrix for pwlo east gradient estimates
    ---------------------
    """
    mge = staObs.mge[ista]
    mgn = staObs.mgn[ista]
    first = staObs.first[ista]
    
    Angr = np.zeros((nobs, n_unk+1))
    Aegr = np.zeros((nobs, n_unk+1))
    
    k = 0
    for inter in range(n_unk):
        for iobs in range(n_all[inter]):
            Angr[staObs.oc_nob[ista][k],inter] = first[k]*(1 - (minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]]))*mgn[k]
            Angr[staObs.oc_nob[ista][k],inter+1] = first[k]*(minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]])*mgn[k]
            Aegr[staObs.oc_nob[ista][k],inter] = first[k]*(1 - (minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]]))*mge[k]
            Aegr[staObs.oc_nob[ista][k],inter+1] = first[k]*(minute[k]-T_[num[k]])/(T_[num[k]+1]-T_[num[k]])*mge[k]
            
            k += 1

    return sparse.csr_matrix(Angr),sparse.csr_matrix(Aegr)

def eopMatrix(pEOP, scanMJD, scanObsNum, Param, mjd0, paramName, estParam):
    """
    Design matrix for the eop
    ---------------------
    input: 
        pEOP           : the EOP partial matrix
        scanMJD        : the MJD of earch scan
        scanObsNum     : the observe number of earch scan
        Param          : the 
        mjd0           : mjd of the first day of the session at 0:00 UTC
        paramName      : the estimate parameter name
    output: 
        Param       : the class type, see cntparameter.py
    ---------------------
    """
    if paramName == 'ut1':
        rad2mas = (180 / np.pi) * 3600 * 1000 / 15 # rad to ms
    else:
        rad2mas = (180 / np.pi) * 3600 * 1000 # rad to ms
    mjd1 = min(scanMJD)
    mjd2 = max(scanMJD)
    
    t1 = (mjd1 - mjd0) * 24 * 60
    t2 = (mjd2 - mjd0)* 24 * 60
    
    t_mjd = []
    for iscan in range(len(scanMJD)):
        for iobs in range(scanObsNum[iscan]):
            t_mjd.append((scanMJD[iscan] - mjd0)*24*60)
    
    if paramName == 'ut1':
        est_len = float(Param.Flags.ut1[1])
        coef_eop = Param.Flags.segConstr[1]
        deop = pEOP[2,:]
        #flag = 2
    elif paramName == 'pmx':
        est_len = float(Param.Flags.pm[1])
        coef_eop = Param.Flags.segConstr[0]
        deop = pEOP[0,:]
        #flag = 3
    elif paramName == 'pmy':
        est_len = float(Param.Flags.pm[1])
        coef_eop = Param.Flags.segConstr[0]
        deop = pEOP[1,:]
        #flag = 4
    elif paramName == 'nutx':
        est_len = float(Param.Flags.ut1[1])
        coef_eop = Param.Const.nut
        deop = pEOP[3,:]
        #flag = 5    
    elif paramName == 'nuty':
        est_len = float(Param.Flags.ut1[1])
        coef_eop = Param.Const.nut
        deop = pEOP[4,:]
        #flag = 5
     
    flag = estParam.param.index(paramName)
    t1_eop = np.floor(t1/est_len)*est_len
    t2_eop = np.ceil(t2/est_len)*est_len
    num = int((t2_eop-t1_eop)/est_len)
    
    inter_eop = np.linspace(t1_eop, t2_eop, num+1)
    estParam.tmjd[flag].extend(inter_eop)
    
    stm_eop = np.zeros(num, dtype=int)
    for inter in range(num):
        if inter == num-1:
            tst = np.where((t_mjd >= inter_eop[inter]) & (t_mjd <= inter_eop[inter+1]))
        else:
            tst = np.where((t_mjd >= inter_eop[inter]) & (t_mjd < inter_eop[inter+1]))
        stm_eop[inter] = len(tst[0])
        
    Apwdeop = np.zeros((len(t_mjd),num+1))
    k = 0
    for inter in range(num):
        for iobs in range(stm_eop[inter]):
            #Apwdeop[k,inter] = (1-(t_mjd[k]-inter_eop[inter])/(inter_eop[inter+1]-inter_eop[inter]))*\
            #                    deop[k]*const.c*100*(1/rad2mas) #[sec/rad -- cm/mas]
            #Apwdeop[k,inter+1] = (t_mjd[k]-inter_eop[inter])/(inter_eop[inter+1]-inter_eop[inter])*\
            #                    deop[k]*const.c*100*(1/rad2mas)
            Apwdeop[k, inter] = (1 - (t_mjd[k] - inter_eop[inter]) / (inter_eop[inter + 1] - inter_eop[inter])) * \
                                deop[k] * const.c * (1 / rad2mas)  # [sec/rad -- m/mas]
            Apwdeop[k, inter + 1] = (t_mjd[k] - inter_eop[inter]) / (inter_eop[inter + 1] - inter_eop[inter]) * \
                                    deop[k] * const.c * (1 / rad2mas) # [sec/rad -- m/mas]

            k += 1
    
    
    mat = np.eye(num+1) - np.eye(num+1, k=1)
    Hdeop = mat[0:num, 0:num+1]
    Phdeop = np.eye(num)*1/coef_eop**2
    oc_hdeop = np.zeros(len(Hdeop))
       
    return Apwdeop, Hdeop, Phdeop, oc_hdeop
    
def souMatrix(scanInfo,sourceInfo,Param,nobs,A,H,Ph,och,souNNR,estParam):
       
    psou = np.array(scanInfo.psou)
    scanSouP = np.where(scanInfo.Obs2Source!=0)
    Obs2Source = scanInfo.Obs2Source[scanSouP[0]]-1
    
    if len(Param.Flags.sou) >= 3:
        estSouNum = len(scanInfo.sourceAll)-len(Param.Flags.sou[2:])
    elif len(Param.Flags.sou) == 1:
        estSouNum = len(scanInfo.sourceAll)
    
    Asou = np.zeros((nobs,2*estSouNum))
    
    Psou = np.eye(2) * 1/Param.Const.sou[1]**2
    PnnrSou = np.eye(3) * 1/Param.Const.sigma_nnr_sou**2
    
    flag = 0
    HnnrSou = []
    for i in range(len(scanInfo.sourceAll)):
        if scanInfo.sourceAll[i] not in Param.Flags.sou:
            souName = scanInfo.sourceAll[i].strip()
            sp = np.where(Obs2Source==i)

            Asou[sp[0],2*flag] = psou[sp[0],0]
            Asou[sp[0],2*flag+1] = psou[sp[0],1]
    
            ra = sourceInfo.rade[i][0]
            de = sourceInfo.rade[i][1]
            
            
            if Param.Const.sou[0] == 'YES':
                Hsou = np.eye(2)
            else:
                Hsou = np.zeros((2,2))
            
            flag_nnr = False
            if souName in Param.Const.nnr_sou:
                if Param.Const.nnr_sou[0] == 'NO':
                    flag_nnr = True
            else:
                if Param.Const.nnr_sou[0] == 'YES':
                    flag_nnr = True
            
            Hnnr = helmertCRF(flag_nnr, ra, de)
                
                        
            if flag == 0:
                HnnrSou = Hnnr
                H.sou = Hsou
                Ph.sou = Psou
            else:
                HnnrSou = np.hstack((HnnrSou, Hnnr))
                H.sou = sparse.block_diag((H.sou,Hsou))
                Ph.sou = sparse.block_diag((Ph.sou,Psou))
            flag += 1
            
    H.sou = sparse.vstack((H.sou, HnnrSou))
    Ph.sou = sparse.block_diag((Ph.sou,PnnrSou))
    och.sou = np.zeros(H.sou.shape[0])
    
    H.sou,Ph.sou,och.sou = rmBlank(H.sou, Ph.sou, och.sou)
            
    estp = estParam.param.index('sou')
    estParam.num[estp] = 2*estSouNum
    
    A.sou = Asou 

def a_xyz(ista, staObs, nobs):
    """
    Design matrix for the station coordinate
    ---------------------
    input: 
        ista        : the position of station
        staObs      : the struct of station
        nobs        : the all observation
    output: 
        Axyz        : the matrix of station coordinate
    ---------------------
    """
    Axyz = np.zeros((nobs,3))
    
    for i in range(len(staObs.oc_nob[ista])):
        Axyz[staObs.oc_nob[ista][i],:] = staObs.pcoor[ista][i]
        
    return sparse.csr_matrix(Axyz)

def rmBlank(H, P, O):
    temp_h = H.toarray()
    p = []
    for i in range(temp_h.shape[0]):
        if np.all(temp_h[i,:]==0):
            p.append(i)
            
    temp_h = np.delete(temp_h, p, axis=0)
    O = np.delete(O, p, axis=0)
    
    temp_p = P.toarray()
    # p = []
    # for i in range(temp_p.shape[0]):
    #     if np.all(temp_p[i,:]==0):
    #         p.append(i)
            
    temp_p = np.delete(temp_p, p, axis=0) 
    p = []
    for i in range(temp_p.shape[1]):
        if np.all(temp_p[:,i]==0):
            p.append(i)
    temp_p = np.delete(temp_p, p, axis=1)
    
    return sparse.csr_matrix(temp_h),sparse.csr_matrix(temp_p), O

def rebuildMatrix(matrix, delP):
    
    outlier = 1*delP
    for i in range(outlier.shape[0]):
        shape = matrix.shape
        matrix[:, outlier[i]] = matrix[:, shape[1] - 1]
        matrix = matrix[:, :shape[1] - 1]
        matrix[outlier[i], :] = matrix[shape[1]-1, :]
        matrix = matrix[:shape[1] - 1, :]
        if i != outlier.shape[0]:
            outlier[i+1:] -= 1
    
    return matrix
            
