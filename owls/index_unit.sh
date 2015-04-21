#!/bin/bash
# The path to the folder which has the *.data files of all the categories
DATA_PATH="./keywords/$2";

sen=$1;
sen="`echo $sen | tr -s ' ' | tr ' ' '\n' | sort | uniq | tr '\n' ' '`"
i=0;

for fp in `ls $DATA_PATH`
do
    vector[$i]=`echo $sen | grep -oi -f $DATA_PATH/$fp | wc -l`;
    i=`expr $i + 1`;

done

for i in {0..5..1}
do
    echo -e "${vector[$i]} \c";
done
echo -e "${vector[6]}\c";
