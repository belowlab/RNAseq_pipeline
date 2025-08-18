# Author: Wanying Zhu
# Call featureCounts: featureCounts [options] -a annotation.gtf -o counts.txt sample1.bam sample2.bam ...
'''
Usage:
python step6_run_featureCounts.py --input_files <input_files> \
                                --prefix <prefix> \
                                --output_dir <output_dir> \
                                --annotation_ref <annotation_ref> \
                                --paired_end <paired_end> \
                                --threads <threads> \
                                --featureCounts_cmd <featureCounts_cmd>

Example call:
python step6_run_featureCounts.py --input_files ... \
--prefix xxx \
--output_dir xxx \
--annotation_ref /data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Annotation/Genes/genes.gtf \
--paired_end true \
--threads 16 \
--featureCounts_cmd featureCounts

'''


import argparse
import os.path
import subprocess
from datetime import datetime
import contextlib

@contextlib.contextmanager
def cd(cd_path):
    saved_path = os.getcwd()
    os.chdir(cd_path)
    yield
    os.chdir(saved_path)

parser = argparse.ArgumentParser(description='Run featureCounts')

parser.add_argument('--input_files', type=str, help='Sorted BAM or SAM files, ', nargs='+')
parser.add_argument('--prefix', help='Prefix for output file names')
parser.add_argument('-o', '--output_dir', default='.', help='Output directory')
parser.add_argument('--annotation_ref', type='str',
                    default='/data100t1/share/reference_data/Homo_sapiens/UCSC/hg38/Annotation/Genes/genes.gtf',
                    help="Annotation file in GTF format. Default uses HH's version created in 2015, may need to update in the future")
parser.add_argument('--paired_end', type=str.lower, choices=['true', 'false'], default='true', help='Paired-end protocol')
parser.add_argument('-t', '--threads', default='8', help='Number of threads')
parser.add_argument('--featureCounts_cmd', type=str, default='featureCounts',
                    help="User supplied path to featureCounts")
args = parser.parse_args()

output_fn = os.path.join(args.output_dir, args.prefix+'.featureCount.count')
print('['+datetime.now().strftime("%b %d %H:%M:%S")+'] Running featureCounts', flush=True)
with cd(args.output_dir):
    if args.paired_end=='true':
        cmd = f'{args.featureCounts_cmd} -a {args.annotation_ref} -o {output_fn} -p -T {args.threads} ' + ' '.join({args.input_files})
    else:
        cmd = f'{args.featureCounts_cmd} -a {args.annotation_ref} -o {output_fn} -T {args.threads} ' + ' '.join({args.input_files})

    # run featureCounts
    print('  * command: '+cmd, flush=True)
    subprocess.check_call(cmd, shell=True, executable='/bin/bash')

print('['+datetime.now().strftime("%b %d %H:%M:%S")+'] Finished featureCounts', flush=True)
