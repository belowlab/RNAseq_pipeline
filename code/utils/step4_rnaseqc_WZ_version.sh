count=0
genes_gtf=/vgipiper04/CCHC/GTEx_compare/GTEx_ref/gencode.v26.GRCh38.genes.gtf
picard_output_path=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/picard_2.27.4/
while IFS=$'\t' read -r col1 col2 col3
do
        count=$((count+1))
        echo ""
        echo "####################################################"
        echo "Processing sample # ${count}: ${col1}"
        /data100t1/home/wanying/downloaded_tools/gtex-pipeline/rnaseq/src/run_rnaseqc.py \
            ${genes_gtf} \
            ${picard_output_path}${col1}.Aligned.sortedByCoord.out.md.bam \
            ${col1} \
            --output_dir /data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/rnaseqc_test/ \
            --rnaseqc /data100t1/home/wanying/downloaded_tools/rnaseqc/rnaseqc-2.4.2/rnaseqc
done <$1