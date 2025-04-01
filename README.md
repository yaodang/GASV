# GASV
Software for VLBI analysis. The VLBI baseline delays and rates data in format of HOPS outputs and NGS card files are used as the inputs to estimate geodetic and astrometric parameters including the station coordinates, EOP parameters, source coordinates, clock and atmospheric models.

required packages:numpy, matplotlib, scipy, netcdf4, jplephem, pyside2(currently, next version will change pyqt)

run:
python GASV_GUI.py
or python run.py /path/to/cnt_file
