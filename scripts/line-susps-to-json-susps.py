#!/usr/bin/python2.7

import argparse
import csv
import json
import operator

def line_to_class(line):
    classname, loc = line.rsplit('#',1)
    return classname, loc

parser = argparse.ArgumentParser()
parser.add_argument('--line-susps', required=True)
parser.add_argument('--test-failing', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

dic = {}
dic['failing'] = args.test_failing.rsplit('\n',1)

rankings = []
with open(args.line_susps) as fin:
    reader = csv.DictReader(fin)
    for row in reader:
        classname, loc = line_to_class(row['Line'])
        susps = float(row['Suspiciousness'])
        if susps != 0.0:
            rankings.append({
                'class': classname,
                'loc': loc,
                'score': susps
            })  
fin.close()

dic['rankings'] = sorted(rankings, key=lambda item: item['score'], reverse=True)

with open(args.output, 'w') as outfile:
    json.dump(dic, outfile,indent=4)