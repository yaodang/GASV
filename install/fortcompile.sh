cd ../source/EXTERNAL/IERS/solid_tidal
gfortran -shared -fPIC CAL2JD.F DAT.F DEHANTTIDEINEL.F NORM8.F SPROD.F ST1IDIU.F ST1ISEM.F ST1L1.F STEP2DIU.F STEP2LON.F ZERO_VEC8.F -o libstc.so
cd ../ocean_tidal
gfortran -shared -fPIC ADMINT.F ETUTC.F EVAL.F JULDAT.F LEAP.F MDAY.F OTC.F RECURS.F SHELLS.F SPLINE.F TDFRPH.F TOYMD.F -o libhardsip.so
cd ../gmf
gfortran -shared -fPIC GMF.F -o libgmf.so

