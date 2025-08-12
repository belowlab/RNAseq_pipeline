while IFS= read -r line; do
	echo $line
	python ~/tools/gtex-pipeline/rnaseq/src/process_star_junctions.py -o STAR_junction /vgipiper04/CCHC/GTEx_compare/STAR_2.7.9a/$line/$line.SJ.out.tab.gz /vgipiper04/CCHC/GTEx_compare/GTEx_ref/gencode.v26.GRCh38.junctions.txt $line	
done < $1


