while IFS= read -r line; do 


	rnaseqc \
		/vgipiper04/CCHC/GTEx_compare/GTEx_ref/gencode.v26.GRCh38.genes.gtf \
		/vgipiper04/CCHC/GTEx_compare/picard/$line.Aligned.sortedByCoord.out.md.bam \
		/vgipiper04/CCHC/GTEx_compare/RNA-SeQC_1.1.9 \
		-s $line -vv --legacy
	gzip /vgipiper04/CCHC/GTEx_compare/RNA-SeQC_1.1.9/$line.exon_reads.gct \
		/vgipiper04/CCHC/GTEx_compare/RNA-SeQC_1.1.9/$line.gene_tpm.gct \
		/vgipiper04/CCHC/GTEx_compare/RNA-SeQC_1.1.9/$line.gene_reads.gct
	rnaseqc \
		/vgipiper04/CCHC/GTEx_compare/GTEx_ref/gencode.v26.GRCh38.genes.gtf \
		/vgipiper04/CCHC/GTEx_compare/picard/$line.Aligned.sortedByCoord.out.md.bam \
		/vgipiper04/CCHC/GTEx_compare/RNA-SeQC_2.3.5 \
		-s $line -vv 
	gzip /vgipiper04/CCHC/GTEx_compare/RNA-SeQC_2.3.5/$line.exon_reads.gct \
		/vgipiper04/CCHC/GTEx_compare/RNA-SeQC_2.3.5/$line.gene_tpm.gct \
		/vgipiper04/CCHC/GTEx_compare/RNA-SeQC_2.3.5/$line.gene_reads.gct
done < $1


