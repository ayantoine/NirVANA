#! /bin/bash

datetime1=$(date +%s)

ARG=$1
source $ARG
source $CONF

echo "------ Launch Trim array ------"
nb_jobs=$(cut -f1 ${DODE} | wc -l)
if [ ! -d "TrimReads_Ok" ] ; then mkdir "TrimReads_Ok" ; fi
if [ ! -d ${PID}"_log_TrimReads${PAIR}" ] ; then mkdir ${PID}"_log_TrimReads${PAIR}" ; fi
echo $SCALL $SPARAM $SRENAME ${PID}_Cutadapt ${STASKARRAY}1-${NumberPairFile}${SMAXTASK}${SMAXSIMJOB} -e ${PID}"_Cleaning"/${PID}_Cutadapt.e${SPSEUDOTASKID} -o ${PID}"_Cleaning"/${PID}_Cutadapt.o${SPSEUDOTASKID} ${SDIR}/LaunchCutadapt.sh $ARG
$SCALL $SPARAM $SRENAME ${PID}_Cutadapt ${STASKARRAY}1-${NumberPairFile}${SMAXTASK}${SMAXSIMJOB} -e ${PID}"_Cleaning"/${PID}_Cutadapt.e${SPSEUDOTASKID} -o ${PID}"_Cleaning"/${PID}_Cutadapt.o${SPSEUDOTASKID} ${SDIR}/LaunchCutadapt.sh $ARG
while true ; do
	if [ $(ls TrimReads_Ok/ | wc -l) -eq 0 ]
		then
		nbr_ok=0
	else
		nbr_ok=$(ls TrimReads_Ok/*.TrimReads.ok | wc -l)
	fi
	echo ${nbr_ok}
	echo ${nb_jobs}
	if [ "${nbr_ok}" -eq "${nb_jobs}" ]
		then
		rm -r TrimReads_Ok
		break
	fi
	sleep 60
done
echo "------ /Launch Trim array ------"

touch ${PID}.fastq.trim.ok

datetime2=$(date +%s)
delta=$((datetime2 - datetime1))
echo "Time Trimming: "$delta > Time04.txt
