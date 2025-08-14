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
python ${pipeline_folder}/code/S4_run_rnaseqc.py ${picard_cmd} ${project_folder} ${pipeline_folder}
'''

import os
import sys
import logging