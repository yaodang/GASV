gfortran -shared -fPIC ADMINT.F ETUTC.F EVAL.F JULDAT.F LEAP.F MDAY.F OTC.F RECURS.F SHELLS.F SPLINE.F TDFRPH.F TOYMD.F -o libhardsip.so
gfortran -shared -fPIC GMF.F -o libgmf.so
