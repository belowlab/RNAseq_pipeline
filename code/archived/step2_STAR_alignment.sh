# STAR alignment
# Usage:
# bash step2_STAR_alignment.sh <input_fastq1> <input_fastq2> 


# STAR --genomeLoad LoadAndExit --genomeDir GTEx_ref/STAR_indx_2.7.9/

# Input fastq 1 and 2
fastq_input1=$1
fastq_input2=$2

# Prefix and folder for output files
output_prefix=$3
output_dir=$4

# ########## TODO: make these flexible ##########
# Path to the pipeline
pipeline_folder=/data100t1/home/wanying/CCHC/RNAseq_pipeline

# Path to STAR index (created by Hung-hsin)
star_index_folder=/vgipiper04/CCHC/GTEx_compare/GTEx_ref/STAR_indx_2.7.9/

# STAR command
# Or use STAR-2.7.9a: /data100t1/home/wanying/downloaded_tools/STAR-2.7.9a/source/STAR
star_tool=/data100t1/home/wanying/CCHC/RNAseq_pipeline/tools/STAR-2.7.11b/source/STAR

# ##############################


echo -e "Run STAR alignment for ${output_prefix}\n"
python ${pipeline_folder}/code/utils/run_STAR.py \
${star_index_folder} \
${fastq_input1} ${fastq_input2} \
${output_prefix} \
--threads 16 \
--output_dir ${output_dir} \
--STARalt ${star_tool}



