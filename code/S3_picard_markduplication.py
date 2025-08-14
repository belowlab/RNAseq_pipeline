'''
Loop through the STAR output folder, and create files:
1. Commands to submit to Slurm
2. Slurm array submission

Then submit the slurm array

Usage:
python S3_picard_markduplication.py <picard_cmd> <project_folder> <pipeline_folder>
# picard_cmd: path to picard.jar
# project_folder: root folder to for the project
# pipeline_folder: root folder of the pipeline, eg: /data100t1/home/wanying/CCHC/RNAseq_pipeline

Example:
project_folder=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian/
pipeline_folder=/data100t1/home/wanying/CCHC/RNAseq_pipeline
picard_cmd=${pipeline_folder}/tools/picard/picard.jar
python ${pipeline_folder}/code/S3_picard_markduplication.py ${picard_cmd} ${project_folder} ${pipeline_folder}
'''

import os
import sys
import logging

# Path to picard.jar
picard_cmd = sys.argv[1]
# Project folder to save output results
project_folder = sys.argv[2]
# Path to the pipeline
pipeline_folder = sys.argv[3] # '/data100t1/home/wanying/CCHC/RNAseq_pipeline'

logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.info('# Create commands to run picard')
logging.info('# - Call used:')
logging.info('# python ' + ' '.join(sys.argv))

output_dir = f'{project_folder}/picard'

# Loop through the star output folder to create commands
# Use default for other settings
star_output_path = os.path.join(project_folder, 'star')
suffix = '.sortedByCoord.out.bam'
output_slurm_prefix = f'{project_folder}/code/slurm_submission/step03_run_picard'
cmd_fn = output_slurm_prefix + '.sh'
count = 0
with open(cmd_fn,'w') as fh_out:
    for fn in os.listdir(star_output_path):
        if fn.endswith(suffix):
            prefix = fn.split(suffix)[0]
            cmd = f'python {os.path.join(pipeline_folder, "code/utils", "step3_run_MarkDuplicates.py")}'
            cmd += f' {os.path.join(star_output_path, fn)}'
            cmd += f' {prefix}.Aligned.sortedByCoord.out.patched.md'
            cmd += f" --output_dir {os.path.join(project_folder, 'picard')}"
            cmd += f' --jar {picard_cmd}'
            fh_out.write(cmd+'\n')
            count += 1
logging.info('# - %s commands were written to output'%count)

# ##### Create slurm array submission #####
# STAR run takes about 40GB from a previous example
logging.info('# Create file for slurm array submission')
sumr_arry_fn = f'{output_slurm_prefix}.slurm_array'
with open(sumr_arry_fn, 'w') as fh_slurm_array:
    content = f'''#!/bin/bash
#SBATCH --job-name=RNAseq_picard
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=24:00:00
#SBATCH --mem=15G
#SBATCH --array=1-{count}
#SBATCH --output={project_folder}/code/slurm_logs/picard_%A_%a.out

echo "SLURM_JOBID: " $SLURM_JOBID
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
echo "SLURM_ARRAY_JOB_ID: " $SLURM_ARRAY_JOB_ID

COMMANDS_FILE={cmd_fn}
'''
    content += 'sed -n "${SLURM_ARRAY_TASK_ID}p" < ${COMMANDS_FILE} | bash'
    fh_slurm_array.write(content)




    