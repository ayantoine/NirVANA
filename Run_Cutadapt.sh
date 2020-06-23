#! /bin/bash

datetime1=$(date +%s)

ARG=$1
source $ARG
source $CONF
source $DATA

echo "------ Get Subsample list ------"
declare -a SAMPLE_LIST
for VARNAME in "${PLATE[@]}"; do
	VAR_SAMPLE_FILE="${VARNAME}[3]"
	#echo "${!VAR_SAMPLE_FILE}"
	while read c1 leftovers; do
		SAMPLE_LIST+=(${VARNAME}${c1})
	done < ${!VAR_SAMPLE_FILE}
done
echo "${SAMPLE_LIST[@]}"
echo "------ /Get Subsample list ------"

echo "------ Launch Trim array ------"
nb_jobs=${#SAMPLE_LIST[@]} #$(cut -f1 ${DODE} | wc -l)
if [ ! -d "TrimReads_Ok" ] ; then mkdir "TrimReads_Ok" ; fi
if [ ! -d ${PID}"_log_TrimReads" ] ; then mkdir ${PID}"_log_TrimReads" ; fi
echo $SCALL $SPARAM_MULTICPU $SRENAME ${PID}_Cutadapt ${STASKARRAY}1-${nb_jobs}${SMAXTASK}${SMAXSIMJOB} -e ${PID}"_log_TrimReads"/${PID}_Cutadapt.e${SPSEUDOTASKID} -o ${PID}"_log_TrimReads"/${PID}_Cutadapt.o${SPSEUDOTASKID} ${SDIR}/LaunchCutadapt.sh $ARG
$SCALL $SPARAM_MULTICPU $SRENAME ${PID}_Cutadapt ${STASKARRAY}1-${nb_jobs}${SMAXTASK}${SMAXSIMJOB} -e ${PID}"_log_TrimReads"/${PID}_Cutadapt.e${SPSEUDOTASKID} -o ${PID}"_log_TrimReads"/${PID}_Cutadapt.o${SPSEUDOTASKID} ${SDIR}/LaunchCutadapt.sh $ARG
while true ; do
	if [ $(ls TrimReads_Ok/ | wc -l) -eq 0 ]
		then
		nbr_ok=0
	else
		nbr_ok=$(ls TrimReads_Ok/*.TrimReads.ok | wc -l)
	fi
	if [ "${nbr_ok}" -eq "${nb_jobs}" ]
		then
		rm -r TrimReads_Ok
		break
	fi
	sleep 60
done
echo "------ /Launch Trim array ------"

touch ${PID}.CutAdapt.ok

datetime2=$(date +%s)
delta=$((datetime2 - datetime1))
echo "Time Trimming: "$delta > Time04.txt
