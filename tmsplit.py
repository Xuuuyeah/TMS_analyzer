#!/usr/bin/env python

import argparse
import sys
import tmsplitFunctions
import os


parser = argparse.ArgumentParser(description='Your program description here.')

parser.add_argument('-i', dest = 'ifile', type=str, help='Input file name (in fasta format).')
parser.add_argument('-T', dest = 'TMSinfo', type=str, help='Optional input file with TMS coordinates. TMSs in this file can be provided in either HMMTOP format or in a two-column format: Accesssion[\\t]ranges1,range2,etc. (e.g., P0AEP1[\\t]5-25,30-48,50-70). If this file is not provided, HMMTOP will be run to extract TMS coordinates.')
parser.add_argument('-s', dest = 'indiv_info', type=str, help='Optional input file with the index or group size wanted. Example format: Accesssion[\\t]range1,range2 or Accession[\\t]group_size')
parser.add_argument('-o', dest = 'ofile', type=str, help='Output file name.')

parser.add_argument('-m', dest = 'qmode', type=int, help='Set split mode. Acceptable values: 1 for "range of TMSs", 2 for "groups of TMSs". 3 for "range of amino acids". If mode is 1, provide the range (start-end) of TMSs with option (-r) or provied additional file (-s) to specifically extract TMS(s) in every sequences. If mode is 2, provide the number of TMSs within each group with option (-g) or provide additional file (-s) to customize group size of every sequence. If mode is 3, provide the region of desired amino acids (-r) or provide additional file (-s) to specifically extract certain region(s) in each sequences.')

parser.add_argument('-r', dest = 'region', type=str, help="region of TMSs, only allowed when mode (-m) = 1 or 3. ':', ',', '-' are allowed to separate start and stop position.")

parser.add_argument('-g', dest = 'group_size', type=str, help='Number of TMSs per group, only allowed when mode (-m) = 2.')
parser.add_argument('-c', dest = 'option', type=str, help='When the number of TMSs if not the multiple of the number of TMSs per group (-g), 1 for ignoring the last remaining TMSs, 2 for expanding the last group, 3 for creating a new groups. Default is 2')
# tail parameter
parser.add_argument('-t', dest = 'tail', type=str, nargs = "+", default=0, help='Optional tail length. Default value is 0.')
## standard amino acid
parser.add_argument('-a', dest = 'stan', type=str, help='Option to determine whether invalid amino acid (totally 22 different amino acids) is allowed. -a 1: non-standard amino acid is allowed, otherwise not allowed by default')





try: 
    args = parser.parse_args() 
    if not os.path.isfile(args.ifile):
        raise ValueError("Error: input file -i does not exist")
    elif args.TMSinfo != None and not os.path.isfile(args.TMSinfo):
        raise ValueError("Error: input file -T does not exist")
    elif args.indiv_info != None and not os.path.isfile(args.indiv_info):
        raise ValueError("Error: input file -s does not exist")
    if args.tail:  
        if len(args.tail) > 1:
            raise ValueError('Error: invalid tail length argument -t')
        else: 
            args.tail = int(args.tail[0])

    try:
        args.tail = int(args.tail)
        if args.tail < 0:
            raise ValueError("Error: tail length -t must be non-negative integer.")
    except:
        raise ValueError("Error: tail length -t must be non-negative integer.")
        
    if args.ifile:
        if not args.TMSinfo:
            if args.qmode != 3:
                args.TMSinfo = tmsplitFunctions.runHmm(args.ifile)
        tmsplitFunctions.TMScut(args.ifile, args.TMSinfo, args.indiv_info, args.qmode, args.tail, args.region, args.group_size, args.option, args.ofile, args.stan)
    else:
        raise ValueError('Error: input file -i is needed') 
except ValueError as e:
    print(str(e))
# if not args.TMSinfo:
#     if args.qmode != 3:
#         args.TMSinfo = tmsplitFunctions.runHmm(args.ifile)
# tmsplitFunctions.TMScut(args.ifile, args.TMSinfo, args.seq_range, args.qmode, args.tail, args.region, args.tnum, args.option, args.ofile, args.stan)
