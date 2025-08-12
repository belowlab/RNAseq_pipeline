# Create a list of fastp QCed files to run STAR
'''
Usage:
python S2-1_get_list_of_files_to_run_star.py <project_folder>

Example call:
project_folder=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian
python ./code/S2-1_get_list_of_files_to_run_star.py ${project_folder}
'''

import os
import sys

project_folder = sys.argv[1]
fastp_path = f'{project_folder}/fastp'

output_fn = f'{project_folder}/data/fastp_cleaned_file_list.csv'

# Find all fastp cleaned files and output to a list to run STAR alignment
c = 0
with open(output_fn, 'w') as fh:
    fh.write('full_path,file_name,sample_name\n')
    for fn in os.listdir(fastp_path):
        if fn.endswith('.fastq.gz'):
            c += 1
            # fastp cleaned files created from previous steps should end with '.R1.fastq.gz' or '.R2.fastq.gz'
            if fn.endswith('.R1.fastq.gz'):
                sample_name = fn.split('.R1.fastq.gz')[0]
            elif fn.endswith('.R2.fastq.gz'):
                sample_name = fn.split('.R2.fastq.gz')[0]
            else:
                print("# ERROR: FASTQ file does not end with '.R1.fastq.gz'. Cannot create list of files to run STAR")
                print('# Exit')
                exit()
            fh.write(f'{fastp_path}/{fn},{fn},{sample_name}\n')
print('# Done creating list of fastp files: %s' % c)
