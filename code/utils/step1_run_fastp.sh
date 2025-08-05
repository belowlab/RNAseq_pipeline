# Activate the conda environment or install fastp first: RNAseq_gtex_pipeline

# Goal:
# 1. Run fastp on a list of raw fastq files
# 2. Save the QCed outputs to a new place for the next step
# 3. Rename QCed files as needed

# Input files are raw fastq such as in.R1.fq.gz and in.R2.fq.gz
# Usage:
# bash step0_fastp.sh <raw_fastq1> <raw_fastq2> <output_fn1> <output_fn1> <report_prefix>


in_file1=$1 # Input fastq file 1
in_file2=$2 # Input fastq file 2
out_file1=$3 # Output QCed file 1
out_file2=$4 # Output QCed file 3
report_prefix=$5 # Report file name without suffix

fastp -i ${in_file1} \
-I ${in_file2} \
-o ${out_file1} \
-O ${out_file2} \
-A -V \
-w 16 \
-j ${report_prefix}.json \
-h ${report_prefix}.html
