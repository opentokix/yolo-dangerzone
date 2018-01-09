#!/usr/bin/env python2

import sys
import yaml


def main(files):
    for f in files:
        try:
            yaml.safe_load(file(f))
        except yaml.reader.ReaderError:
            print "File: %s contains errors" % f
            continue
        except yaml.parser.ParserError:
            print "File: %s parse errors" % f
            continue

if __name__ == '__main__':
    files = sys.stdin.readline()
    filelist = files.split()
    main(filelist)
