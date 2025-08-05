'''
Create a folder with the desired structure for RNAseq QC pipeline:
    project/
    ├── fastp/
    │   ├── reports/
    │   └── qced_files/
    ├── star/
    │   └── star_output/
    ├── post_pipeline_QC/
    ├── Picard/
    ├── RNAseqQC/
    └── RSEM/

Usage:
python create_folders.py RNAseq_batch5
'''

import os
import sys

root_folder = system.argv[1] # Name of the root folder
if os.path.isdir(root_folder):
    ans = -1
    while ans.lower()!='y' and ans.lower()!='n':
        ans = input('# Folder already exists. Do you want to continue? (y/n)')
    if ans=='n':
        print('# Exit')
        exit()
    else:
        print('# Create subfolders')

# Create subfolders
lst_subfolders = 

print('# Done')
    