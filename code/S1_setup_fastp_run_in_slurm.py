'''
Using a sample list file, create files:
1. Commands to submit to Slurm
2. Slurm array submission

Then submit the slurm array

Usage:
python S1_setup_fastp_run_in_slurm.py <sample_list> <project_folder>

Example:
sample_list=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian/data/sample_list.csv
project_folder=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian/
python S1_setup_fastp_run_in_slurm.py ${sample_list} ${project_folder}
'''

import pandas as pd
import sys
import logging
import subprocess

fn_sample_list = sys.argv[1]
project_folder = sys.argv[2]

# ########## TODO: make these flexible ##########
# Path to the pipeline
pipeline_folder = '/data100t1/home/wanying/CCHC/RNAseq_pipeline'
# ##############################


logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.info('# Load file names and sample names from %s' % fn_sample_list)

if fn_sample_list.endswith('csv'):
    df_sample_list = pd.read_csv(fn_sample_list)
else:
    df_sample_list = pd.read_csv(fn_sample_list, sep='\t')

# ##### Create bash commands #####
# bash step0_fastp.sh <raw_fastq1> <raw_fastq2> <output_fn1> <output_fn1> <report_prefix>
output_path = f'{project_folder}/fastp'

logging.info('# Create commands for to run in slurm')
code_prefix = 'step01_run_fastp'
cmd_fn = f'{project_folder}/code/slurm_submission/{code_prefix}.sh'
count = 0 # Count total number of commands
with open(cmd_fn, 'w') as fh_bash_cmds:
    for i, row in df_sample_list.iterrows():
        in_fn1 = row['in_fn1']
        in_fn2 = row['in_fn2']
        sample_name = row['sample_name']
        
        # The order of R1 and R2 in does not really matter
        out_fn1 = f'{output_path}/{sample_name}.R1.fastq.gz'
        out_fn2 = f'{output_path}/{sample_name}.R2.fastq.gz'
    
        report_prefix = f'{output_path}/report/{sample_name}'
        
        cmd = f'bash {pipeline_folder}/code/utils/step1_run_fastp.sh'
        cmd += f' {in_fn1} {in_fn2} {out_fn1} {out_fn2} {report_prefix}'
        fh_bash_cmds.write(cmd+'\n')
        count += 1
logging.info('# - %s commands were written to output'%count)

# ##### Create slurm array submission #####
logging.info('# Create file for slurm array submission')
sumr_arry_fn = f'{project_folder}/code/slurm_submission/{code_prefix}.slurm_array'
with open(sumr_arry_fn, 'w') as fh_slurm_array:
    content = f'''#!/bin/bash
#SBATCH --job-name=RNAseq_fastp
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=24:00:00
#SBATCH --mem=15G
#SBATCH --array=1-{count}
#SBATCH --output={project_folder}/code/slurm_logs/fastp_%A_%a.out

echo "SLURM_JOBID: " $SLURM_JOBID
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
echo "SLURM_ARRAY_JOB_ID: " $SLURM_ARRAY_JOB_ID

COMMANDS_FILE={cmd_fn}
'''
    content += 'sed -n "${SLURM_ARRAY_TASK_ID}p" < ${COMMANDS_FILE} | bash'
    fh_slurm_array.write(content)
    
