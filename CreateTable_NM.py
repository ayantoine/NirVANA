# coding: utf-8
"""Python3.6"""
# compatibility: python2.7, python2.6

import time
from optparse import OptionParser

sCurrentVersionScript="v1"
iTime1=time.time()
########################################################################
'''
V2-2020/02/14
Adapt to Diamond and no multiplexing

V1-2019/11/06
Create tsv bilan from Blast data

python CreateTable.py -i JOBS -p PID
JOBS: jobs number
PID: Plaque Id
'''
########################################################################
#CONSTANT
HEADER_LIST=["Hit rank","Query Seq-Id","Read quantity","Sequence length",
"Subject Seq-Id","Organism","SuperKingdom","Taxonomy","Hit definition","% Fragment","Identity",
"Query cover","Alignment length","Mismatches","Gap opening","Start alignment query","End alignment query",
"Start alignment subject","End alignment subject","E-value","Bit score","Query sequences"]
HEADER="\t".join(HEADER_LIST)+"\n"

BEST_HIT="Best hit"
HIT="."

REPLACEME="REPLACE-ME"
SAMPLE_SEPARATOR="-"
CONTIG="Contig"

BLAST_QUERYIDCOl=0
BLAST_SUBJECTIDCOl=1
BLAST_IDENTITYCOl=2
BLAST_LENGTHCOl=3
BLAST_MISMATCHCOl=4
BLAST_GAPOPENCOl=5
BLAST_QUERYSTARTCOl=6
BLAST_QUERYENDCOl=7
BLAST_SUBJECTSTARTCOl=8
BLAST_SUBJECTENDCOl=9
BLAST_EVALUECOl=10
BLAST_BITSCORECOl=11

TAXO_ACCCOL=0
TAXO_ORGANISMCOL=1
TAXO_SUPKINGDOMCOL=2
TAXO_LINEAGECOL=3
TAXO_DEFCOL=4

DEFAULT="."

EMPTY=""
DIESE="#"
EQUAL="="
OPEN_PARENTHESIS="("
CLOSE_PARENTHESIS=")"
SPACE=""

########################################################################
#Options
if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-j","--jobs", dest="jobs")
	parser.add_option("-p","--pid", dest="pid")
	parser.add_option("-l","--length", dest="length")
	parser.add_option("-d","--data", dest="data")

	(options, args) = parser.parse_args()

	sJobs=options.jobs
	if not sJobs:
		exit("Error : no jobs -j defined, process broken")
	try:
		iJobs=int(sJobs)
	except KeyError:
		exit("Error : jobs -j must be an integer, process broken")
		
	sPID=options.pid
	if not sPID:
		exit("Error : no pid -p defined, process broken")

	sLengthFile=options.length
	if not sLengthFile:
		exit("Error : no length -l defined, process broken")
	
	sData=options.data
	if not sData:
		exit("Error : no data -d defined, process broken")

	#Half-constant
	BLAST_OUTPUT=sPID+"_Diamond_results.tab"
	BLAST_FOLDER=sPID+"_Diamond"
	BLAST_INPUT=sPID+"_All.fa."+REPLACEME+".keeped"
	BLAST_FILE=sPID+"_All.fa."+REPLACEME+".Diamond_2.tab"
	TAXO_FILE=sPID+"_All.fa."+REPLACEME+".Diamond_2.tab.taxo"
	SHORTSPADES=sPID+"_All.Megahit.contigs2sample.tsv"
	SHORTFLASH=sPID+"_All.FLASH.contigs2sample.tsv"

########################################################################
#Function 	
def LoadContigs(sFile,dRef,dDict={}):
	print("Loading file "+str(sFile))
	for sNewLine in open(sFile):
		sLine=sNewLine.strip()
		tLine=sLine.split("\t")
		sName=tLine[0]
		try:
			oCrash=dRef[sName]
			dDict[sName]=tLine[1].split(SAMPLE_SEPARATOR)
		except KeyError:
			continue
	return dDict

def LoadTaxo(sFile):
	print("Loading file "+str(sFile))
	dDict={}
	for sNewLine in open(sFile):
		sLine=sNewLine.strip()
		tLine=sLine.split("\t")
		if len(tLine)!=5:
			continue
		
		# print(sFile)
		# print(tLine)
		sOrganism=DEFAULT
		if tLine[TAXO_ORGANISMCOL]!="":
			sOrganism=tLine[TAXO_ORGANISMCOL]
		sSuperkingdom=DEFAULT
		if tLine[TAXO_SUPKINGDOMCOL]!="":
			sSuperkingdom=tLine[TAXO_SUPKINGDOMCOL]
		sLineage=DEFAULT
		if tLine[TAXO_LINEAGECOL]!="":
			sLineage=tLine[TAXO_LINEAGECOL]
		sDefinition=DEFAULT
		if tLine[TAXO_DEFCOL]!="":
			sDefinition=tLine[TAXO_DEFCOL]
		
		
		dDict[tLine[TAXO_ACCCOL]]={
			"Organism":sOrganism,
			"Superkingdom":sSuperkingdom,
			"Lineage":sLineage,
			"Definition":sDefinition
			}
			
	return dDict

def LoadBlast(sFile):
	print("Loading file "+str(sFile))
	dDict={}
	for sNewLine in open(sFile):
		sLine=sNewLine.strip()
		tLine=sLine.split("\t")
		sQueryId=tLine[BLAST_QUERYIDCOl]
		try:
			oCrash=dDict[sQueryId]
		except KeyError:
			dDict[sQueryId]={}
		
		sSubjectId=DEFAULT
		if tLine[BLAST_SUBJECTIDCOl]!="":
			sSubjectId=tLine[BLAST_SUBJECTIDCOl]
			tSubjectId=sSubjectId.split("|")
			sSubjectId=tSubjectId[3]
			if sSubjectId==EMPTY:
				continue
		sIdentity=DEFAULT
		if tLine[BLAST_IDENTITYCOl]!="":
			sIdentity=tLine[BLAST_IDENTITYCOl]
		sLength=DEFAULT
		if tLine[BLAST_LENGTHCOl]!="":
			sLength=tLine[BLAST_LENGTHCOl]
		sMismatch=DEFAULT
		if tLine[BLAST_MISMATCHCOl]!="":
			sMismatch=tLine[BLAST_MISMATCHCOl]
		sGapOpen=DEFAULT
		if tLine[BLAST_GAPOPENCOl]!="":
			sGapOpen=tLine[BLAST_GAPOPENCOl]
		sQueryStart=DEFAULT
		if tLine[BLAST_QUERYSTARTCOl]!="":
			sQueryStart=tLine[BLAST_QUERYSTARTCOl]
		sQueryEnd=DEFAULT
		if tLine[BLAST_QUERYENDCOl]!="":
			sQueryEnd=tLine[BLAST_QUERYENDCOl]
		sSubjectStart=DEFAULT
		if tLine[BLAST_SUBJECTSTARTCOl]!="":
			sSubjectStart=tLine[BLAST_SUBJECTSTARTCOl]
		sSubjectEnd=DEFAULT
		if tLine[BLAST_SUBJECTENDCOl]!="":
			sSubjectEnd=tLine[BLAST_SUBJECTENDCOl]
		sEvalue=DEFAULT
		if tLine[BLAST_EVALUECOl]!="":
			sEvalue=tLine[BLAST_EVALUECOl]
		sBitScore=DEFAULT
		if tLine[BLAST_BITSCORECOl]!="":
			sBitScore=tLine[BLAST_BITSCORECOl]
					
		dDict[sQueryId][len(dDict[sQueryId])+1]={
			"SubjectId":sSubjectId,
			"Identity":sIdentity,
			"Length":sLength,
			"Mismatch":sMismatch,
			"GapOpen":sGapOpen,
			"QueryStart":sQueryStart,
			"QueryEnd":sQueryEnd,
			"SubjectStart":sSubjectStart,
			"SubjectEnd":sSubjectEnd,
			"Evalue":sEvalue,
			"BitScore":sBitScore
			}
	return dDict

def LoadQuery(sFile):
	print("Loading file "+str(sFile))
	dDict={}
	sSeqContent=""
	sSeqName=""
	for sNewLine in open(sFile):
		if ">"==sNewLine[0]:
			if sSeqName!="":
				dDict[sSeqName]=sSeqContent
			sSeqName=sNewLine[1:-1]
			sSeqContent=""
		else:
			sSeqContent+=sNewLine[:-1] #:-1, for \n char
	if sSeqName!="":
		dDict[sSeqName]=sSeqContent
	return dDict

def WriteData(FILE,dBlast,dTaxo,dContigs,dContent,dLength):
	for sQuery in dBlast:
		for iRank in dBlast[sQuery]:
			
			if iRank==1:
				sRank=BEST_HIT
			else:
				sRank=HIT
			
			iQuerySize=len(dContent[sQuery])
			iCoverSize=int(dBlast[sQuery][iRank]["QueryEnd"])-int(dBlast[sQuery][iRank]["QueryStart"])
			fCover=round(float(iCoverSize)/iQuerySize*100,2)
				
			if CONTIG in sQuery:
				sReadQuantity=sQuery.split("(")[-1].split(")")[0]
			else:
				sReadQuantity="1"
			sSubjectId=dBlast[sQuery][iRank]["SubjectId"]
			
			sTaxo=dTaxo[sSubjectId]["Lineage"]
			tTaxo=sTaxo.replace("; ",";").split(";")
			iMinSize=0
			for oTaxo in tTaxo:
				try:
					iMinSize=dLength[oTaxo]
				except KeyError:
					continue
			if iMinSize==0:
				fFragment="N/A"
			else:
				fFragment=round(float(iQuerySize)/iMinSize*100,2)
				
			tLine=[sRank,sQuery,sReadQuantity,str(iQuerySize),
			sSubjectId,
			dTaxo[sSubjectId]["Organism"],dTaxo[sSubjectId]["Superkingdom"],
			dTaxo[sSubjectId]["Lineage"],dTaxo[sSubjectId]["Definition"],str(fFragment),
			dBlast[sQuery][iRank]["Identity"],
			str(fCover),dBlast[sQuery][iRank]["Length"],dBlast[sQuery][iRank]["Mismatch"],
			dBlast[sQuery][iRank]["GapOpen"],dBlast[sQuery][iRank]["QueryStart"],
			dBlast[sQuery][iRank]["QueryEnd"],dBlast[sQuery][iRank]["SubjectStart"],
			dBlast[sQuery][iRank]["SubjectEnd"],dBlast[sQuery][iRank]["Evalue"],
			dBlast[sQuery][iRank]["BitScore"],dContent[sQuery]
			]
			FILE.write("\t".join(tLine)+"\n")
						
# HEADER_LIST=["Hit rank","Query Seq-Id","Sample","Read quantity","Sequence length","Location","Date","Host",
# "Individual","Weight(mg)","Subject Seq-Id","Organism","SuperKingdom","Taxonomy","Hit definition","% Fragment","Identity",
# "Query cover","Alignment length","Mismatches","Gap opening","Start alignment query","End alignment query",
# "Start alignment subject","End alignment subject","E-value","Bit score","Query sequences"]

def LoadLength(sFile):
	print("Loading file "+str(sFile))
	dDict={}
	for sNewLine in open(sFile):
		sLine=sNewLine.strip()
		tLine=sLine.split()
		sFamily=tLine[0]
		iMinSize=int(tLine[1])
		dDict[sFamily]=iMinSize
	return dDict

########################################################################
#MAIN
if __name__ == "__main__":
	dLength=LoadLength(sLengthFile)
	FILE=open(BLAST_OUTPUT,"w")
	FILE.write(HEADER)
	for iIndex in range(1,iJobs+1):
		print("Working on index "+str(iIndex))
		dQuery2Content=LoadQuery(BLAST_FOLDER+"/"+BLAST_INPUT.replace(REPLACEME,str(iIndex)))
		dContigs2Sample=LoadContigs(SHORTSPADES,dQuery2Content)
		dContigs2Sample=LoadContigs(SHORTFLASH,dQuery2Content,dContigs2Sample)
		dTaxo=LoadTaxo(BLAST_FOLDER+"/"+TAXO_FILE.replace(REPLACEME,str(iIndex)))
		dBlast=LoadBlast(BLAST_FOLDER+"/"+BLAST_FILE.replace(REPLACEME,str(iIndex)))
		WriteData(FILE,dBlast,dTaxo,dContigs2Sample,dQuery2Content,dLength)
	FILE.close()
	
########################################################################    
iTime2=time.time()
iDeltaTime=iTime2-iTime1
print("Script done: "+str(iDeltaTime))

