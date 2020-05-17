'''
Program that takes a numeric value n and the name of a fasta
file and returns the top n largest sequences
'''

import sys


def read_fasta(file):
    """ Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values """
    fasta_dict = {}
    with open(file) as f:
        line = f.readline()
        while line:
            if line.startswith('>') or line.startswith('NODE'):
                header = line.strip()
                line = f.readline()
                nucleotides = ''
            else:
                nucleotides = nucleotides + line.strip()
                line = f.readline()
                fasta_dict[header] = nucleotides
    fasta_dict = {y:x for x,y in fasta_dict.items()}
    return fasta_dict


def return_largest_seqs(file, n):
    d = read_fasta(file)
    top_n = {}
    for i in range(n):
        largest = max(d.keys(), key=len)
        top_n[d[largest]] = largest
        print(top_n.keys())
        d.pop(largest)
    return top_n


def write_largest_fastas(file, n, output):
    top_n = return_largest_seqs(file, int(n))
    with open(output, 'w') as o:
        for key, value in top_n.items():
            o.write(key)
            o.write('\n')
            o.write(value)
            o.write('\n')
    return 'Complete'


if __name__ == "__main__":
    file = sys.argv[1]
    n = sys.argv[2]
    output = sys.argv[3]
    write_largest_fastas(file, n, output)