'''
Create a folder with the desired structure for RNAseq QC pipeline:
    project/
    ├── code/
    │   ├── slurm_submission/
    │   └── slurm_logs/
    ├── data/
    ├── fastp/
    │   └── report/
    ├── star/
    ├── picard/
    ├── RNAseqQC/
    ├── RSEM/
    └── post_pipeline_QC/

Usage:
python S0_create_folders.py <root_folder_of_the_project>

Example call:
python S0_create_folders.py RNAseq_batch5
'''

import os
import sys

root_folder = sys.argv[1] # Name of the root folder
if os.path.isdir(root_folder):
    ans = ''
    while ans.lower()!='y' and ans.lower()!='n':
        ans = input('# Folder already exists. Do you want to continue? (y/n)')
    if ans=='n':
        print('# Exit')
        exit()
    else:
        print('# Create subfolders')

# Create subfolders
lst_subfolders = [root_folder, f'{root_folder}/code', f'{root_folder}/data',
                  f'{root_folder}/fastp/report/', f'{root_folder}/star',
                  f'{root_folder}/picard', f'{root_folder}/RNAseqQC',
                  f'{root_folder}/RSEM', f'{root_folder}/slurm_submission',
                  f'{root_folder}/slurm_logs']
for folder in lst_subfolders:
    try:
        os.makedirs(folder)
    except:
        print(f'# Failed to create folder: {folder}')
print('# Done')
    