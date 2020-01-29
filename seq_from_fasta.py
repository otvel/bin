#!/bin/python3

import gzip
from argparse import ArgumentParser


def extract_sequence(fh, target_header, uppercase):
    seq = ''
    header = ''
    fasta_dict = {}
    for line in fh:
        if line.startswith('>'):
            if target_header in header:
                yield (header, seq)
            header = line.strip()[1:]
            seq = ''
        else:
            if uppercase:
                seq += line.strip().upper()
            else:
                seq += line.strip()
    if target_header in header:
        yield (header, seq)


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-i', '--input', required=True,
                            help='FASTA to parse')
    arg_parser.add_argument('-t', '--target', required=True,
                            help="Target sequence's header")
    arg_parser.add_argument('-o', '--output', required=True,
                            help='Output filename')
    arg_parser.add_argument('-s', '--start',
                            help='Start coordinate for splicing (0-index) (optional)')
    arg_parser.add_argument('-e', '--end',
                            help='End coordinate for splicing (0-index) (optional)')
    arg_parser.add_argument('-c', '--coordinates', action='store_true',
                            help='Include coordinates in output header (optional)')
    arg_parser.add_argument('-U', '--uppercase', action='store_true',
                            help='Convert all characters to uppercase (optional)')
    arg_parser.add_argument('-oh', '--output_header',
                            help='Text used in output header (optional)')
    args = arg_parser.parse_args()
    print('[INFO] Working...')
    try:
        with gzip.open(args.input, 'rt') as fh:
            seqs = [pair for pair in extract_sequence(fh, args.target, args.uppercase)]
    except OSError:
        with open(args.input) as fh:
            seqs = [pair for pair in extract_sequence(fh, args.target, args.uppercase)]

    with open(args.output, 'w') as fh:
        i = 1
        for header, seq in seqs:
            if args.output_header:
                header = args.output_header
            if args.start and args.end:
                seq = seq[int(args.start):int(args.end)]
            elif args.start:
                seq = seq[int(args.start):]
            elif args.end:
                seq = seq[:int(args.end)]
            if args.coordinates:
                if args.start:
                    start = args.start
                else:
                    start = 0
                if args.end:
                    end = args.end
                else:
                    end = len(seq)
                fh.write(f'>{header}_{start}_{end}\n')
            else:
                fh.write(f'>{header}\n')
            fh.write(f'{seq}\n')

    print('[INFO] Done!')


if __name__ == '__main__':
    main()
