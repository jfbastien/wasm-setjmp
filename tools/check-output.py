#!/usr/bin/env python

import argparse
import difflib
import subprocess
import sys


def ParseArgs():
  parser = argparse.ArgumentParser(
      description='Run program and check its output against golden file')
  parser.add_argument('--program', required=True, help='Program to execute')
  parser.add_argument('--gold', required=True, help='Golden output file')
  return parser.parse_args()


def munge(string):
  return [l + '\n' for l in string.strip().splitlines()]


def run(program):
  return subprocess.check_output([program])


def compare(out, gold, fromfile, tofile):
  diff = list(difflib.unified_diff(out, gold,
                                   fromfile=fromfile, tofile=tofile))
  for line in diff:
    sys.stdout.write(line)
  return len(diff)


if __name__ == '__main__':
  options = ParseArgs()
  with open(options.gold, 'r') as gold_file:
    gold = munge(gold_file.read())
  out = munge(run(options.program))
  sys.exit(compare(out, gold, options.program, options.gold))
