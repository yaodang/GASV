#!/bin/bash
if ! which gfortran >/dev/null 2>&1; then
    echo "Error: gfortran not exists. Please install."
    exit
fi
