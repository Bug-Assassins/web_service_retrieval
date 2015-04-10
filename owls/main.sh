#!/bin/bash
input=$1;
output=$2;
theta=$3;

inp_vect=`bash index_unit.sh "$1" input`
out_vect=`bash index_unit.sh "$2" output`

python cosine.py $inp_vect $out_vect $3 > result.temp
