#!/bin/bash
if which gfortran >/dev/null 2>&1; then
    echo "Check gfortran: OK."
else
    echo "Check gfortran: not exists."
    exit
fi

echo "Start compile fortran file..."
# ocean tidal program compile
cd ../EXTERNAL/IERS/ocean_tidal
gfortran -shared -fPIC ADMINT.F ETUTC.F EVAL.F JULDAT.F LEAP.F MDAY.F OTC.F RECURS.F SHELLS.F SPLINE.F TDFRPH.F TOYMD.F -o libhardsip.so

echo "  Ocean tidal OK."


cd ../solid_tidal
gfortran -shared -fPIC CAL2JD.F DAT.F DEHANTTIDEINEL.F NORM8.F SPROD.F ST1IDIU.F ST1ISEM.F ST1L1.F STEP2DIU.F STEP2LON.F ZERO_VEC8.F -o libstc.so

echo "  Solid tidal OK."

echo "Modify bashrc file..."
cd ../../../

softpath=$(pwd)


TARGET_ALIAS="alias GASVR='python"
NEW_ALIAS="alias GASVR='python $softpath/run.py'"

if grep -q "$TARGET_ALIAS" ~/.bashrc; then
    sed -i "/$TARGET_ALIAS/d" ~/.bashrc
fi

echo "$NEW_ALIAS" >> ~/.bashrc

echo "  .bashrc updated."
source ~/.bashrc
