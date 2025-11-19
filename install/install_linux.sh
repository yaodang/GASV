#!/bin/bash

CONDAENV="gasv"
CONDAINIT="$HOME/Software/miniconda3/etc/profile.d/conda.sh"
NAMER="GASVR"
NAMEG="GASVGUI"
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
SOFTRPATH="$SCRIPT_DIR/dist/$NAMER/"
SOFTGPATH="$SCRIPT_DIR/dist/$NAMEG/"
echo "$SOFTPATH"

if [ ! -f "$CONDAINIT" ]; then
	CONDAINIT="$HOME/anaconda3/etc/profile.d/conda.sh"
fi

if [ ! -f "$CONDAINIT" ]; then
	echo "Error: can't find conda initialization script, please check path."
	exit 1
fi

source "$CONDAINIT"
echo "Activate conda environment: $CONDAENV"
conda activate $CONDAENV

pyinstaller -n $NAMER -w --add-data "../source/EXTERNAL:./EXTERNAL" ../source/GASVR.py
pyinstaller -n $NAMEG --add-data "../source/EXTERNAL:./EXTERNAL" --add-data "../source/directory.ini:." ../source/GASVGUI.py

if grep -qxF "export PATH=\"\$PATH:$SOFTRPATH\"" ~/.bashrc; then
    echo "The path '$SOFTRPATH' already in .bashrc"
else
    echo "export PATH=\"\$PATH:$SOFTRPATH\"" >> ~/.bashrc
    echo "Add '$SOFTRPATH' to .bashrc."
    echo "Please 'source ~/.bashrc'"
    echo "Input '$NAMER' in terminal to check the software."
fi

if grep -qxF "export PATH=\"\$PATH:$SOFTGPATH\"" ~/.bashrc; then
    echo "The path '$SOFTGPATH' already in .bashrc"
else
    echo "export PATH=\"\$PATH:$SOFTGPATH\"" >> ~/.bashrc
    echo "Add '$SOFTGPATH' to .bashrc."
    echo "Please 'source ~/.bashrc'"
    echo "Input '$NAMEG' in terminal to check the software."
fi
