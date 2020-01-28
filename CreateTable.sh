#! /bin/bash

datetime1=$(date +%s)

ARG=$1
source $ARG
source $CONF

task=$2
nb_jobs=$3

echo "python ${SDIR}/CreateTable.py -t ${task} -j ${nb_jobs} -p ${PID} -m ${META} -l ${VIRMINLEN}"
python ${SDIR}/CreateTable.py -t ${task} -j ${nb_jobs} -p ${PID} -m ${META} -l ${VIRMINLEN}

touch ${PID}.creation${task}.ok
