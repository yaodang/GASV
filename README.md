# GASV
Software for VLBI analysis. The VLBI baseline delays and rates data in format of HOPS outputs and NGS card files are used as the inputs to estimate geodetic and astrometric parameters including the station coordinates, EOP parameters, source coordinates, clock and atmospheric models.

required packages: python(>=3.8), numpy, matplotlib, scipy, netcdf4, jplephem

run:
python GASVGUI.py
or python GASVR.py /path/to/cnt_file

for single session analysis, it can using some IERS modules write in Fortran by Ctype to improve the compute speed.
