#!/usr/bin/env python2
"""Simple syntax checker for yaml."""

import sys
import yaml

# FLAGS
exit_code = 0


def main(files):
    """Looping thru a list of files and tries to load em."""
    for f in files:
        try:
            yaml.safe_load(file(f))
        except yaml.reader.ReaderError:
            print "File: %s contains errors" % f
            continue
        except yaml.parser.ParserError:
            print "File: %s parse errors" % f
            exit_code = 1
            continue
    sys.exit(exit_code)


if __name__ == '__main__':
    files = sys.stdin.readline()
    filelist = files.split()
    main(filelist)
