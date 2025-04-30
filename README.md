# GASV
Software for VLBI analysis. The VLBI baseline delays and rates data in format of HOPS outputs and NGS card files are used as the inputs to estimate geodetic and astrometric parameters including the station coordinates, EOP parameters, source coordinates, clock and atmospheric models.

required packages: python(>=3.8), numpy, matplotlib, scipy, netcdf4, jplephem

run:
python GASV_GUI.py
or python run.py /path/to/cnt_file

the software will optimize performance-critical functions by rewriting them in Cython, to further improve the single session analysis speed
