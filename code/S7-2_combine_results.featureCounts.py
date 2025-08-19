# Combine individual files from featureCounts into one
'''
Usage:
python S7-2_combine_results.featureCounts.py <input_path_with_featureCounts_files> <output_file_name>

Example call:
project_folder=/data100t1/home/wanying/CCHC/RNAseq_gtex_pipeline/202507_batch5_9560-JB_glp1_and_brazilian
pipeline_folder=/data100t1/home/wanying/CCHC/RNAseq_pipeline
featureCounts_path=${project_folder}/featureCounts
output_fn=${project_folder}/final_output/combined_featureCounts.counts
python ${pipeline_folder}/code/S7-2_combine_results.featureCounts.py ${featureCounts_path} ${output_fn}

'''

import sys
import pandas as pd
import glob
import os

# Path to featureCounts outputs
input_path = sys.argv[1] # Input path with featureCounts outputs
output_fn = sys.argv[2] # Output file name
suffix = '.featureCount.count.gz' # Gzipped output

dfs = []
count = 0
for fn in os.listdir(input_path):
    if not fn.endswith(suffix):
        continue
    # Extract sample name before ".featureCount.count"
    sample = fn.split(suffix)[0]
    
    # Skip comment lines starting with "#"
    df = pd.read_csv(os.path.join(input_path,fn), sep="\t", comment="#", compression='gzip')
    
    # Keep only geneid and count column (last column)
    df = df[["Geneid", df.columns[-1]]]
    
    # Rename count column to sample name
    df.rename(columns={df.columns[-1]: sample}, inplace=True)
    
    dfs.append(df)
    count += 1
    print(f'\r# Load {count} files', end='', sep='', flush=True)
print(f'\r# Load {count} files\n')

# Merge all dataframes on Geneid
print('# Combine all files\n')
count = 1
merged = dfs[0]
for df in dfs[1:]:
    merged = pd.merge(merged, df, on="Geneid", how="outer")
    count += 1
    if count%10==0:
        print(f'\r# Merged {count} files', end='', sep='', flush=True)
print(f'\r# Merged {count} files\n')

# Fill missing values with 0
merged = merged.fillna(0)

print('# Save to output:', output_fn)
# Save final matrix
merged.to_csv(output_fn, sep="\t", index=False)
print('# Done')
