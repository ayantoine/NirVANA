#! /bin/bash

datetime1=$(date +%s)

ARG=$1
source $ARG
source $CONF

echo "------ Create Kmer library ------"
python ${SDIR}/CreateKmerList.py -m ${DODE} -o ${DODE}.kmer.tsv -p ${PID}
echo "------ /Create Kmer library ------"

echo "------ Count sequences ------"
NB_SEQ=$(($(sed -n '$=' ${PID}_R1.fastq)/4))
echo ${NB_SEQ} " present in ${PID}_R1.fastq"
echo "------ /Count sequences ------"

mkdir ${PID}_Demultiplexing

echo "------ Make assignation ------"
echo "python ${SDIR}/QsubAssignation.py -a ${ARG} -s ${SDIR} -k ${DODE}.kmer.tsv -d ${PID}_Demultiplexing -o QsubAssignation.sh -c ${CONF} -q ${NB_SEQ} -p ${PID}"
python ${SDIR}/QsubAssignation.py -a ${ARG} -s ${SDIR} -k ${DODE}.kmer.tsv -d ${PID}_Demultiplexing -o QsubAssignation.sh -c ${CONF} -q ${NB_SEQ} -p ${PID}
cat ./QsubAssignation.sh
bash ./QsubAssignation.sh
echo "------ /Make assignation ------"

sleep 60

echo "------ Merge subdata ------"
cat ${PID}_Demultiplexing/*_Hyper_Identified* > ${PID}_Hyper_Identified.tsv
cat ${PID}_Demultiplexing/*_Hypo_1_Identified* > ${PID}_Hypo_1_Identified.tsv
cat ${PID}_Demultiplexing/*_Hypo_2_Identified* > ${PID}_Hypo_2_Identified.tsv
cat ${PID}_Demultiplexing/*_Ambiguous_1* > ${PID}_Ambiguous_1.tsv
cat ${PID}_Demultiplexing/*_Ambiguous_2* > ${PID}_Ambiguous_2.tsv
cat ${PID}_Demultiplexing/*_Unidentified* > ${PID}_Unidentified.tsv
echo "------ /Merge subdata ------"

rm -r ${PID}_Demultiplexing/
rm ./QsubAssignation.sh

echo "------ Write output ------"
#cat ${PID}_Hyper_Identified.tsv ${PID}_Hypo_1_Identified.tsv ${PID}_Ambiguous_1.tsv ${PID}_Unidentified.tsv > ${PID}_Demultiplexing_Global.tsv
echo "python ${SDIR}/ConcatenateFile.py -o ${PID}_Demultiplexing_Global.tsv -l ${PID}_Hyper_Identified.tsv,${PID}_Hypo_1_Identified.tsv,${PID}_Ambiguous_1.tsv,${PID}_Unidentified.tsv"
python ${SDIR}/ConcatenateFile.py -o ${PID}_Demultiplexing_Global.tsv -l ${PID}_Hyper_Identified.tsv,${PID}_Hypo_1_Identified.tsv,${PID}_Ambiguous_1.tsv,${PID}_Unidentified.tsv
#cut -f2 ${PID}_Demultiplexing_Global.tsv | sort | uniq -c | awk '{print $2"\t"$1}' > ${PID}_Demultiplexing_Global_Distribution.tsv
echo "python ${SDIR}/CountDistribution.py -i ${PID}_Demultiplexing_Global.tsv -o ${PID}_Demultiplexing_Global_Distribution.tsv"
python ${SDIR}/CountDistribution.py -i ${PID}_Demultiplexing_Global.tsv -o ${PID}_Demultiplexing_Global_Distribution.tsv

gzip -f ${PID}_Demultiplexing_Global.tsv > ${PID}_Demultiplexing_Global.tsv.gz

#cat ${PID}_Hyper_Identified.tsv ${PID}_Hypo_2_Identified.tsv ${PID}_Ambiguous_2.tsv ${PID}_Unidentified.tsv > ${PID}_Demultiplexing_Hyper.tsv
echo "python ${SDIR}/ConcatenateFile.py -o ${PID}_Demultiplexing_Hyper.tsv -l ${PID}_Hyper_Identified.tsv,${PID}_Hypo_2_Identified.tsv,${PID}_Ambiguous_2.tsv,${PID}_Unidentified.tsv"
python ${SDIR}/ConcatenateFile.py -o ${PID}_Demultiplexing_Hyper.tsv -l ${PID}_Hyper_Identified.tsv,${PID}_Hypo_2_Identified.tsv,${PID}_Ambiguous_2.tsv,${PID}_Unidentified.tsv
#cut -f2 ${PID}_Demultiplexing_Hyper.tsv | sort | uniq -c | awk '{print $2"\t"$1}' > ${PID}_Demultiplexing_Hyper_Distribution.tsv
echo "python ${SDIR}/CountDistribution.py -i ${PID}_Demultiplexing_Hyper.tsv -o ${PID}_Demultiplexing_Hyper_Distribution.tsv"
python ${SDIR}/CountDistribution.py -i ${PID}_Demultiplexing_Hyper.tsv -o ${PID}_Demultiplexing_Hyper_Distribution.tsv
echo "------ /Write output ------"

echo "------ Bilan ------"
wc -l ${PID}_Hyper_Identified.tsv ${PID}_Hypo_1_Identified.tsv ${PID}_Ambiguous_1.tsv ${PID}_Unidentified.tsv ${PID}_Demultiplexing_Hyper.tsv | head -n -1
echo $(expr $(cat ${PID}_R1.fastq ${PID}_R2.fastq | wc -l | cut -d " " -f1) / 4 )" sequences in "${R1}" and "${R2}
echo "------ /Bilan ------"

echo "------ Store supplementary data ------"
gzip -f ${PID}_Hypo_1_Identified.tsv > ${PID}_Hypo_1_Identified.tsv.gz
gzip -f ${PID}_Hypo_2_Identified.tsv > ${PID}_Hypo_2_Identified.tsv.gz
gzip -f ${PID}_Ambiguous_1.tsv > ${PID}_Ambiguous_1.tsv.gz
gzip -f ${PID}_Ambiguous_2.tsv > ${PID}_Ambiguous_2.tsv.gz
gzip -f ${PID}_Unidentified.tsv > ${PID}_Unidentified.tsv.gz
echo "------ /Store supplementary data ------"

> ${PID}.Demultiplexing.ok

datetime2=$(date +%s)
delta=$((datetime2 - datetime1))
echo "Time Demultiplexing: "$delta > Time02.txt

