#!/bin/bash

while IFS=' ' read -r col1 col2
do
	echo "$col1"
	echo "$col2"
	fastp -i "/vgipiper02/CCHC_seq/covid19_RNAseq/RNAseq_0621/"$col1"_S1_L005_R1_001.fastq.gz" \
		-I "/vgipiper02/CCHC_seq/covid19_RNAseq/RNAseq_0621/"$col1"_S1_L005_R2_001.fastq.gz" \
		-o fa_JB-5928/$col1.R1.fa.gz \
		-O fa_JB-5928/$col1.R2.fa.gz \
		-w 6 -A -V \
		-h html_JB-5928/$col2.html \
		-j json_JB-5928/$col2.json
done <$1
