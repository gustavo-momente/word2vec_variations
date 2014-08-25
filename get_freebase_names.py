#!/usr/bin/python

__author__ = 'vilelag'

from apiclient.discovery import build
import json
import argparse
import unicodedata
import sys


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Convert mids from a Freebase triplets files to theirs names')
    parser.add_argument('-i', '-input', metavar='<file>', required=True,
                        help='Input file in FB15k format')
    parser.add_argument('-o', '-output', metavar='<file>', default='freabase_names.txt',
                        help='Output file in FB15k format')
    parser.add_argument('-k', '-key', required=True,
                        help='Developer key to access the Freebase api')
    parser.add_argument('-s', '-start', default=0, type=int,
                        help="Line to start in the input file (default = 0), it will append to the output file")
    return parser


def load_freebase_triplets(fin, fout, key, start):
    with open(fin, 'r') as f:
        content = f.read().splitlines()

    n_lines = len(content)
    count = 0
    #Starting freebase service
    service = build('freebase', 'v1',  developerKey=key)

    know_entries = dict()
    if start <= 0:
        _ty = 'w'
    else:
        count = start
        _ty = 'a'
    with open(fout, _ty) as f:
        for line in content[start:]:
            try:
                count += 1
                if count % 50 == 0:
                    sys.stdout.write("\r{0:3.3f}".format(float(100*count)/(float (n_lines))))
                    sys.stdout.flush()

                data = line.split(' ')
                if len(data) != 3:
                    continue
                mids = [data[0], data[2]]
                rel = data[1]
                names = []
                for mid in mids:
                    try:
                        name = know_entries[mid]
                    except KeyError:
                        name = get_freebase_name(mid, service)
                        know_entries[mid] = name
                    if name is None:
                        break
                    names.append(name)

                if len(names) != 2:
                    continue
                f.write('{} {} {}\n'.format(names[0], rel, names[1]))
            except:
                print ' '
                print count-1
                print line
                exit(1)

def get_freebase_name(mid, service):
    response = service.search(mid=mid, exact=True, indent=False, limit=1).execute()

    tmp = json.loads(response)

    status = tmp['status']
    if status != "200 OK":
        print "{}: {}".format(mid, status)
        return None
    else:
        try:
            name = tmp['result'][0]['name']
        except:
            print "\n{} name not found!".format(mid)
            return None
        if len(name.split(' ')) != 1:
            return None
        else:
            return remove_accents(name)


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())
    fin = args['i']
    fout = args['o']
    key = args['k']
    start = args['s']

    load_freebase_triplets(fin, fout, key, start)

main()