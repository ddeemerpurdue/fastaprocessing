''' 
Author: Dane
Program that takes two fasta files that will be compared for matching
entries.
This was designed to track how many entries were removed from bin sets after
refinement, and then those removed contigs were compared to the original
bin sets to see how many were removed vs. how many were originally binned.

Example usage:
$ python count_same_fasta.py -1 <firstFile> -2 <secondFile> -o <outfile_name>
'''

import os
import sys
import argparse
from Bio import SeqIO

''' Initialize the arguments to be entered into program '''

parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-1", "--In1", help="One of two files to compare to one another",
                    required=True)
parser.add_argument("-2", "--In2", help="One of two files to compare to one another",
                    required=True)
parser.add_argument("-o", "--Output", help="Output file name",
                    required=True, default="")
parser.add_argument("-d", "--Different", help="Add flag is two bin sets use different labeling \
for the contigs but the number remains the same",
                    required=False, action="store_true")
argument = parser.parse_args()


def return_fasta_dic(file, different=False):
    """
    Open up a .fasta file and return the entries as a dictionary in the
    form of dic[defline]=seq
    """
    if different is True:
        seq_dict = {str(int(rec.id.split('-')[1])): rec.seq for rec in SeqIO.parse(file, "fasta")}
    else:
        seq_dict = {rec.id: rec.seq for rec in SeqIO.parse(file, "fasta")}
    return seq_dict


def compare_two_binsets(file1, file2, different=False):
    '''
    Compare how many shared entries there are between two binsets,
    along with differences
    '''
    bin1 = return_fasta_dic(file1, different)
    bin2 = return_fasta_dic(file2, different)
    shared_len = 0
    bin1_unique_len = 0
    bin2_unique_len = 0
    shared = list(bin1.keys() & bin2.keys())
    shared_quantity = len(shared)
    for value in shared:
        shared_len += len(bin1[value])
    # Difference: file1 but not file 2
    bin1_unique = list(bin1.keys() - bin2.keys())
    bin1_unique_quantity = len(bin1_unique)
    for value in bin1_unique:
        bin1_unique_len += len(bin1[value])
    # Difference: file 2 but not file 1
    bin2_unique = list(bin2.keys() - bin1.keys())
    bin2_unique_quantity = len(bin2_unique)
    for value in bin2_unique:
        bin2_unique_len += len(bin2[value])
    return [shared_quantity, shared_len,
            bin1_unique_quantity, bin1_unique_len,
            bin2_unique_quantity, bin2_unique_len]


def write_comparisons(file1, file2, output, different=False):
    stats = compare_two_binsets(file1, file2, different)
    print(stats)
    with open(output, 'w') as o:
        header = "\t".join(["SQuant", "SLen",
                            "Bin1_Quant", "Bin1_Len",
                            "Bin2_Quant", "Bin2_Len", "\n"])
        o.write(header)
        writeline = "\t".join(stat for stat in stats) + '\n'
        o.write(writeline)
    return 0


if __name__ == "__main__":
    if argument.Different:
        write_comparisons(argument.In1, argument.In2, argument.Output)
    else:
        write_comparisons(argument.In1, argument.In2,
                          argument.Output, different=True)
