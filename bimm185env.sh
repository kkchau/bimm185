#!/usr/bin/env bash

# This shell script will create a python-3.4.2-64 virtual environment along with biopython in the specified directory
# For use on UCSD ieng6 server ONLY (the server contains the python-342-64 module)
# SPACE REQUIRED: at least 24MB
# Put this shell script into your bm185s directory (/home/linux/ieng6/bm185s/<username>);
# chmod +x bimm185env.sh to make this shell script executable
# ./bimm185env.sh to run

usage="$(basename "$0") [directory] -- Create a python-3.4.2-64 virtual environment with biopython in supplied directory"
caution='WARNING: Make sure you have enough space to create the environment!! (24MB)'

if [ -z $1 ]; then
    echo $usage >&2
    echo $caution >&2
    echo 'ERROR: Please supply a directory.' >&2
    exit
fi

if [ -d $1 ]; then
    echo $usage
    echo $caution
    echo 'ERROR: Directory already exists!!'
    exit
fi

# make the directory
mkdir $1

# load appropriate python interpreter and create venv
echo 'Making virtual environment'
module load python-342-64
python3 -m venv $1

# activate environment
echo 'Activating virtual environment'
source $1/bin/activate

# use appropriate gcc compiler since ieng6 is weird
export CC=/usr/bin/gcc

# install biopython
pip install biopython

# echo directions
echo -e "\n\n"\
"###############################################################################################\n"\
"To use your new virtual environment:                                                          #\n"\
"    Change to the top level of the directory with your virtual environment                    #\n"\
"    Type \"source ./bin/activate\" and hit enter                                                #\n"\
"                                                                                              #\n"\
"To deactivate your virtual environment:                                                       #\n"\
"    Type \"deactivate\" while the environment is active and hit enter                           #\n"\
"###############################################################################################\n"

