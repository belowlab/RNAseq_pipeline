'''
Using a sample list file, create files:
1. Commands to submit to Slurm
2. Slurm array submission

Then submit the slurm array

Usage:
python S2-2_setup_star_run_in_slurm.py <fastq_list> <project_folder>
# fastq_list: a file with column header and at least 2 columns (extra columns will be ignored): full_path, sample_name
# - full_path: full path of the fastq
# - sample_name: sample name is used as prefix to save STAR outputs
# project_folder: root folder to for the project

Example:
fastp_file_list=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian/data/fastp_cleaned_file_list.csv
project_folder=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian/
python S2-2_setup_star_run_in_slurm.py ${fastp_file_list} ${project_folder}
'''

import pandas as pd
import sys
import logging
import subprocess

# A file of fastqs
fn_fastq_list = sys.argv[1]

# Project folder to save output results
project_folder = sys.argv[2]


# ########## TODO: make these flexible ##########
# Path to the pipeline
pipeline_folder = '/data100t1/home/wanying/CCHC/RNAseq_pipeline'

# Path to STAR index (created by Hung-hsin)
star_index_folder = '/vgipiper04/CCHC/GTEx_compare/GTEx_ref/STAR_indx_2.7.9/'

# STAR command
# Or use STAR-2.7.9a: /data100t1/home/wanying/downloaded_tools/STAR-2.7.9a/source/STAR
star_tool = '/data100t1/home/wanying/CCHC/RNAseq_pipeline/tools/STAR-2.7.11b/source/STAR'

# ##############################

# Set output files
output_dir = f'{project_folder}/star'
slurm_output_dir = f'{project_folder}/code/slurm_submission'

logging.basicConfig(format='%(message)s', level=logging.INFO)

# ##### Load fastq file list #####
logging.info('# Load fastq file list %s' % fn_fastq_list)
if fn_fastq_list.endswith('.csv'):
    df_fastq = pd.read_csv(fn_fastq_list)
else:
    df_fastq = pd.read_csv(fn_fastq_list, sep='\t')
    
# Make sure no missing values
n_org = len(df_fastq)
df_fastq.dropna(subset=['sample_name', 'full_path'], inplace=True)
logging.info('# N rows with missing values dropped: %s' % (n_org-len(df_fastq)))

# Group dataframe by sample name to get paired fastq input
output_slurm_prefix = f'{slurm_output_dir}/step02_run_star'
cmd_fn = output_slurm_prefix + '.sh'
count = 0
with open(cmd_fn,'w') as fh_out:
    for sample_name, df in df_fastq.groupby('sample_name'):
        if len(df)==1:
            logging.info('# WARNING: single fastq file for sample %s' % sample_name)
    
        fastq_inputs = ' '.join(df['full_path'].values)
        cmd = f'python {pipeline_folder}/code/utils/step2_run_STAR.py'
        cmd += f' {star_index_folder}'
        cmd += f' {fastq_inputs}'
        cmd += f' {sample_name}'
        cmd += f' --output_dir {output_dir}'
        cmd += f' --STARalt {star_tool}'
        cmd += f' --threads 4' # Use too many threads might lead to failed run due to memory issue
        fh_out.write(cmd + '\n')
        count += 1
logging.info('# - %s commands were written to output'%count)

# ##### Create slurm array submission #####
# STAR run takes about 40GB from a previous example
logging.info('# Create file for slurm array submission')
sumr_arry_fn = f'{output_slurm_prefix}.slurm_array'
with open(sumr_arry_fn, 'w') as fh_slurm_array:
    content = f'''#!/bin/bash
#SBATCH --job-name=RNAseq_star
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=48:00:00
#SBATCH --mem=80G
#SBATCH --array=1-{count}
#SBATCH --output={project_folder}/code/slurm_logs/star_%A_%a.out

echo "SLURM_JOBID: " $SLURM_JOBID
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
echo "SLURM_ARRAY_JOB_ID: " $SLURM_ARRAY_JOB_ID

COMMANDS_FILE={cmd_fn}
'''
    content += 'sed -n "${SLURM_ARRAY_TASK_ID}p" < ${COMMANDS_FILE} | bash'
    fh_slurm_array.write(content)
        
