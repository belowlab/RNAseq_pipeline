count=0
while IFS=$'\t' read -r col1 col2 col3
do
    count=$((count+1))
    echo ''
    echo "Processing sample # ${count}: ${col1}"
	/data100t1/home/wanying/downloaded_tools/gtex-pipeline/rnaseq/src/run_MarkDuplicates.py \
		/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/STAR_2.7.9a/$col1/$col1.Aligned.sortedByCoord.out.bam \
		$col1.Aligned.sortedByCoord.out.patched.md \
		--output_dir /data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/picard_2.27.4/ \
		--jar /data100t1/home/wanying/downloaded_tools/picard.jar	
done < $1
