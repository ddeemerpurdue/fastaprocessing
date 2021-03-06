'''
Author: Dane
Date: NA
Purpose: Program designed to take in 1+ multifasta files and outputting a tab-delimited
file recording the total nucleotide length, total fasta entries (e.g., contigs), and
the file name. For example, the output would be formatted:
Nucleotides\tContigs\tFile
120000\t10\tSampleA.fasta
80000\t6\tSampleB.fasta

Example usage:
$ python calcBinsetLengths.py -b MySampleBins/*.fasta -o mySampleBinsSizes.txt
'''
import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser


def CalcBinSizeLength(file):
    '''
    Calculate total length of multi-fasta file and how many
    sequences are in it.
    '''
    length = 0
    count = 0
    with open(file) as f:
        for values in SimpleFastaParser(f):
            length += len(values[1])
            count += 1
    return length, count


def loopCalcs(files, output):
    '''
    Extend CalcBinSizeLength to multiple fastas
    '''
    with open(output, 'w') as o:
        o.write(f"Nucleotides\tContigs\tFile\n")
        for file in files:
            name = os.path.basename(file)
            length, count = CalcBinSizeLength(file)
            o.write(f"{length}\t{count}\t{name}\n")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--BinFiles", help="Bin files (1+)",
                        required=True, nargs="*")
    parser.add_argument("-o", "--Output", help="Output file",
                        required=True)
    argument = parser.parse_args()
    loopCalcs(argument.BinFiles, argument.Output)
