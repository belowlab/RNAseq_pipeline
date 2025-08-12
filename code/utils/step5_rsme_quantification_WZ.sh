count=0
genes_gtf=/vgipiper04/CCHC/GTEx_compare/GTEx_ref/gencode.v26.GRCh38.genes.gtf
picard_output_path=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/picard_2.27.4/

while IFS=$'\t' read -r col1 col2 col3
do
    count=$((count+1))
    echo ""
    echo "####################################################"
    echo "Processing sample # ${count}: ${col1}"
    /data100t1/home/wanying/downloaded_tools/gtex-pipeline/rnaseq/src/run_RSEM.py \
        /vgipiper04/CCHC/GTEx_compare/GTEx_ref/RSEM_indx/ \
        /data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/STAR_2.7.9a/${col1}/${col1}.Aligned.toTranscriptome.out.bam \
        /data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/RSEM-1.3.3/${col1} \
        --rsem /data100t1/home/wanying/downloaded_tools/RSEM-1.3.3/rsem-calculate-expression \
        --threads 16
done < $1