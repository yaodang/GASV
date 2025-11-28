# GASV
Software for VLBI analysis. The VLBI baseline delays and rates data in format of HOPS outputs and NGS card files are used as the inputs to estimate geodetic and astrometric parameters including the station coordinates, EOP parameters, source coordinates, clock and atmospheric models.

required packages: python(>=3.7), numpy, matplotlib, scipy, netcdf4, jplephem, cartopy

*Requirement Install:
Install python (Version≥3.7) and pip on Debian/Ubuntu System:
    >sudo apt update
    >sudo apt install python3 python3-pip python3-venv

Install python (Version≥3.7) and pip on CentOS/RHEL System:
    >sudo yum install python3 python3-pip

Create and activate the virtual environment:
    >python3 -m venv gasv
    *Linux/macOS
    >source gasv/bin/activate
    *Windows
    >gasv\Scripts\activate.bat
Install dependencies:
    >pip install -r requirements.txt

If the package installation via the default mirror source is slow, you may switch to the
Tsinghua University Open Source Mirror Source.
For Linux/macOS systems:
    >mkdir -p /.pip
    >vi /.pip/pip.conf

Write the following content, and save the file:
    [global]
    index-url = https://pypi.tuna.tsinghua.edu.cn/simple
    [install]
    trusted-host = pypi.tuna.tsinghua.edu.cn

for single session analysis, it can using some IERS modules write in Fortran by Ctype to improve the compute speed. compile the fortran:
    >bash path/software/install/fortcompile.sh

Then you can run the software as following:
    >cd path/software/source
    *pipeline process
    >python GASVR.py --help
    *GUI interface process
    >python GASVGUI.py


If you want to generate an executable file, follow the steps below:
• pyinstaller -n GASVGUI –add-data "path/software/source/directory.ini:." –add-data
"path/software/source/EXTERNAL:./EXTERNAL" path/software/source/GASVGUI.py
• pyinstaller -n GASVR -w –add-data "path/software/source/EXTERNAL:./EXTERNAL"
path/software/source/GASVR.py
