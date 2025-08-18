#!/bin/bash
##STAR --genomeLoad LoadAndExit --genomeDir /data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Sequence/STARIndex/
while IFS=' ' read -r col1 col2
do
	echo "$col1"
	echo "$col2"
	mkdir $col2
	~/tools/STAR-2.7.8a/bin/Linux_x86_64/STAR \
		--genomeDir /data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Sequence/STARIndex/ \
		--runThreadN 16 \
		--readFilesIn "/vgipiper02/CCHC_seq/covid19_RNAseq/fastp/fa_JB-5928/"$col1".R1.fa.gz" "/vgipiper02/CCHC_seq/covid19_RNAseq/fastp/fa_JB-5928/"$col1".R2.fa.gz" \
		--outFileNamePrefix $col2/$col2. \
		--twopassMode Basic \
		--outSAMtype BAM SortedByCoordinate \
		--outSAMunmapped Within \
		--readFilesCommand zcat
	rm -r $col2/$col2"._STARtmp"
done <$1

##STAR --genomeLoad Remove --genomeDir /data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Sequence/STARIndex/
