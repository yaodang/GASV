from COMMON import *
from GLOB_glob import *

Param = PARAMETER()
Param.Map.stationFile = '/home/GeoAS/Work/GASV/APRIORI/station.txt'
Param.Map.sourceFile = '/home/GeoAS/Work/GASV/APRIORI/souSort.txt'
Param.Out.snxPath = ['YES','/data/VLBI/SINEX/bkg2022a/']

#fid = open('/home/GeoAS/Work/GASV/ARC/glob_arc/bkg2022a_test.arc', 'r')
fid = open('/home/GeoAS/Work/GASV/ARC/glob_arc/bkg2022a_1996_2022.arc', 'r')

lines = fid.readlines()
fid.close()

for line in lines:
    if line[0] == '$':
        temp = list(filter(None, line.split(" ")))
        Param.Arcs.session.append(temp[0][1:])

Param.Flags.vel = ['YES']
Param.Global.station[0] = 'YES'
Param.Global.source[0] = 'YES'
Param.Const.nnr_nnt_sta[0][0] = 'NO'
Param.Const.nnr_nnt_sta[1][0] = 'NO'
Param.Const.nnr_sou[0] = 'NO'

fid = open('/home/GeoAS/Work/GASV/APRIORI/ITRF_NNRT.txt','r')
trfLines = fid.readlines()
fid.close()
fid = open('/home/GeoAS/Work/GASV/APRIORI/ICRF3_NNR.txt','r')
crfLines = fid.readlines()
fid.close()
fid = open('/home/GeoAS/Work/GASV/APRIORI/GLOB_rm_bkg2022a.txt','r')
rmStaLines = fid.readlines()
fid.close()
fid = open('/home/GeoAS/Work/GASV/APRIORI/GLOB_rm_sou_bkg2022a.txt','r')
rmSouLines = fid.readlines()
fid.close()

fid = open('/home/GeoAS/Work/GASV/APRIORI/tie.txt','r')
vlTieLine = fid.readlines()
fid.close()

Param.Const.nnr_nnt_sta[0].extend(getLine(True, trfLines, -1, 0))
Param.Const.nnr_nnt_sta[1].extend(getLine(True, trfLines, -1, 0))
Param.Const.nnr_sou.extend(getLine(True, crfLines, -1, 0))
Param.Global.station.extend(getLine(True, rmStaLines, -1, 0))
Param.Global.source.extend(getLine(True, rmSouLines, -1, 0))
velTie = []
for line in vlTieLine:
    temp = list(filter(None, line.split(" ")))

    if '\\\n' in line:
        velTie.append(temp[:-1])
    else:
        velTie.append(temp)
Param.Tie.velTie = velTie
#'''
GLOB(Param)

'''
NGlobc = np.loadtxt('NGlob.txt',delimiter=',')
bGlobc = np.loadtxt('bGlob.txt',delimiter=',')
Bcon = np.loadtxt('Bcon.txt',delimiter=',')

xout = np.linalg.inv(NGlobc) @ bGlobc
v = bGlobc - NGlobc @ xout
nall = np.hstack((NGlobc, bGlobc))
# print('R(N)=%d (n=%d)\nR(N,b)=%d (n=%d)'%(np.linalg.matrix_rank(NGlobc),NGlobc.shape[0],\
# np.linalg.matrix_rank(nall),nall.shape[0]))

helmert = np.linalg.inv(Bcon @ Bcon.T) @ Bcon @ xout[:Bcon.shape[1], :]
#'''
