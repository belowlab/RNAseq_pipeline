'''
Loop through the STAR output folder, and create files:
1. Commands to submit to Slurm
2. Slurm array submission

Then submit the slurm array

Usage:
python S5_run_rsem.py <rsem_cmd> <rsem_reference> <project_folder> <pipeline_folder>
# rsem_cmd: path to RSEM
# rsem_reference: folder to the rsem reference prepared by HH's: /vgipiper04/CCHC/GTEx_compare/GTEx_ref/RSEM_indx/
# project_folder: root folder to for the project
# pipeline_folder: root folder of the pipeline, eg: /data100t1/home/wanying/CCHC/RNAseq_pipeline

Example:
project_folder=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian
pipeline_folder=/data100t1/home/wanying/CCHC/RNAseq_pipeline
rsem_cmd=rsem-calculate-expression
rsem_ref=/vgipiper04/CCHC/GTEx_compare/GTEx_ref/RSEM_indx/
python ${pipeline_folder}/code/S5_run_rsem.py ${rsem_cmd} ${rsem_ref} ${project_folder} ${pipeline_folder}
'''

import os
import sys
import logging

# Path to rsem
rsem_cmd = sys.argv[1] # Included in the onda environment, but also available here: /data100t1/home/wanying/downloaded_tools/RSEM-1.3.3/
# rsem reference prepared by rsem-prepare-reference (keep using HH's files for now): /vgipiper04/CCHC/GTEx_compare/GTEx_ref/RSEM_indx/
rsem_reference = sys.argv[2]
# Project folder to save output results
project_folder = sys.argv[3]
# Path to the pipeline
pipeline_folder = sys.argv[4] # '/data100t1/home/wanying/CCHC/RNAseq_pipeline'

logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.info('# Create commands to run RSEM')
logging.info('# - Call used:')
logging.info('# python ' + ' '.join(sys.argv))

# ##### Create commands #####
star_output_path = os.path.join(project_folder, 'star')
output_dir = os.path.join(project_folder, 'RSEM')
suffix = '.Aligned.toTranscriptome.out.bam'
output_slurm_prefix = os.path.join(project_folder, 'code/slurm_submission/step05_run_rsem')
cmd_fn = output_slurm_prefix + '.sh'
count = 0
with open(cmd_fn,'w') as fh_out:
    for fn in os.listdir(star_output_path):
        if fn.endswith(suffix):
            prefix = fn.split(suffix)[0]
            bam_file = os.path.join(star_output_path, fn)
            cmd = f'python {os.path.join(pipeline_folder, "code/utils", "step5_run_RSEM.py")}'
            cmd += f' {rsem_reference} {bam_file} {prefix} --output_dir {output_dir} --rsem_cmd {rsem_cmd}'
            fh_out.write(cmd+'\n')
            count += 1
logging.info('# - %s commands were written to output'%count)


# ##### Create slurm array submission #####
logging.info('# Create file for slurm array submission')
sumr_arry_fn = f'{output_slurm_prefix}.slurm_array'
with open(sumr_arry_fn, 'w') as fh_slurm_array:
    content = f'''#!/bin/bash
#SBATCH --job-name=RNAseq_rnaseqc
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=2:00:00
#SBATCH --mem=10G
#SBATCH --array=1-{count}
#SBATCH --output={project_folder}/code/slurm_logs/rsem_%A_%a.out

echo "SLURM_JOBID: " $SLURM_JOBID
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
echo "SLURM_ARRAY_JOB_ID: " $SLURM_ARRAY_JOB_ID

COMMANDS_FILE={cmd_fn}
'''
    content += 'sed -n "${SLURM_ARRAY_TASK_ID}p" < ${COMMANDS_FILE} | bash'
    fh_slurm_array.write(content)