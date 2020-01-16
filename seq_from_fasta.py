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
                            help='Target header')
    arg_parser.add_argument('-o', '--output', required=True,
                            help='Output filename')
    arg_parser.add_argument('-oh', '--output_header',
                            help='Name used in output header')
    arg_parser.add_argument('-U', '--uppercase', action='store_true',
                            help='Whether to convert lowercase to uppercase')
    arg_parser.add_argument('-s', '--start',
                            help='Start coordinate for splicing')
    arg_parser.add_argument('-e', '--end',
                            help='End coordinate for splicing')
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
                    fh.write(f'>{i}_{header}__{args.start}__{args.end}\n'
                             f'{seq[int(args.start):int(args.end)]}\n')
                else:
                    fh.write(f'>{i}_{header}\n{seq}\n')
                i += 1
            else:
                if args.start and args.end:
                    fh.write(f'>{header}__{args.start}__{args.end}\n'
                             f'{seq[int(args.start):int(args.end)]}\n')
                else:
                    fh.write(f'>{header}\n{seq}\n')

    print('[INFO] Done!')


if __name__ == '__main__':
    main()