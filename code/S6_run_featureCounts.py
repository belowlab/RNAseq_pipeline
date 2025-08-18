# For DESeq pipeline
'''
Loop through the STAR output folder, and create files:
1. Commands to submit to Slurm
2. Slurm array submission

Then submit the slurm array

Usage:
python S6_run_featureCounts.py <featureCounts_cmd> <gene_annotation_reference> <project_folder> <pipeline_folder>
# featureCounts_cmd: path to featureCounts
# gene_annotation_reference: folder to the gene annotation reference prepared by HH's: /data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Annotation/Genes/genes.gtf
# project_folder: root folder to for the project
# pipeline_folder: root folder of the pipeline, eg: /data100t1/home/wanying/CCHC/RNAseq_pipeline

Example:
project_folder=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian
pipeline_folder=/data100t1/home/wanying/CCHC/RNAseq_pipeline
featureCounts_cmd=featureCounts
gene_annotation_reference=/data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Annotation/Genes/genes.gtf
python ${pipeline_folder}/code/S6_run_featureCounts.py ${featureCounts_cmd} ${gene_annotation_reference} ${project_folder} ${pipeline_folder}
'''


import os
import sys
import logging

# Path to rsem
featureCounts_cmd = sys.argv[1] # Included in the conda environment
# featureCounts reference used by HH in the past: /data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Annotation/Genes/genes.gtf
featureCounts_reference = sys.argv[2]
# Project folder to save output results
project_folder = sys.argv[3]
# Path to the pipeline
pipeline_folder = sys.argv[4] # '/data100t1/home/wanying/CCHC/RNAseq_pipeline'

logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.info('# Create commands to run featureCounts')
logging.info('# - Call used:')
logging.info('# python ' + ' '.join(sys.argv))

# ##### Create commands #####
star_output_path = os.path.join(project_folder, 'star')
output_dir = os.path.join(project_folder, 'featureCounts')
suffix = '.Aligned.sortedByCoord.out.bam'
output_slurm_prefix = os.path.join(project_folder, 'code/slurm_submission/step06_run_featureCounts')
cmd_fn = output_slurm_prefix + '.sh'
count = 0
with open(cmd_fn,'w') as fh_out:
    for fn in os.listdir(star_output_path):
        if fn.endswith(suffix):
            prefix = fn.split(suffix)[0]
            bam_file = os.path.join(star_output_path, fn)
            cmd = f'python {os.path.join(pipeline_folder, "code/utils", "step6_run_featureCounts.py")}'
            cmd += f' --input_files {bam_file}'
            cmd += f' --prefix {prefix}'
            cmd += f' --output_dir {output_dir}'
            cmd += f' --annotation_ref {featureCounts_reference}'
            cmd += f' --paired_end true'
            cmd += f' --threads 16'
            cmd += f' --featureCounts_cmd {featureCounts_cmd}'
            fh_out.write(cmd+'\n')
            count += 1
logging.info('# - %s commands were written to output'%count)


# ##### Create slurm array submission #####
logging.info('# Create file for slurm array submission')
sumr_arry_fn = f'{output_slurm_prefix}.slurm_array'
with open(sumr_arry_fn, 'w') as fh_slurm_array:
    content = f'''#!/bin/bash
#SBATCH --job-name=RNAseq_featureCounts
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=2:00:00
#SBATCH --mem=5G
#SBATCH --array=1-{count}
#SBATCH --output={project_folder}/code/slurm_logs/featureCounts_%A_%a.out

echo "SLURM_JOBID: " $SLURM_JOBID
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
echo "SLURM_ARRAY_JOB_ID: " $SLURM_ARRAY_JOB_ID

COMMANDS_FILE={cmd_fn}
'''
    content += 'sed -n "${SLURM_ARRAY_TASK_ID}p" < ${COMMANDS_FILE} | bash'
    fh_slurm_array.write(content)
    