#!/usr/bin/env python2
"""Simple syntax checker for yaml."""


import sys
import yaml


def usage():
    """Usage.

    Use:
       find /path/to/yaml/files -name "*.yaml" -print0 | xargs -0 -r |yaml_syntax_check.py
    """


def main(files):
    """Looping thru a list of files and tries to load em."""
    exit_code = 0
    num_files = 0
    for f in files:
        num_files += 1
        try:
            yaml.safe_load(file(f))
        except yaml.reader.ReaderError:
            print "File: %s contains errors" % f
            exit_code = 1
            continue
        except yaml.parser.ParserError:
            print "File: %s parse errors" % f
            exit_code = 1
            continue
    print "Checked %d files for yaml syntax." % num_files
    sys.exit(exit_code)


if __name__ == '__main__':
    files = sys.stdin.readline()
    filelist = files.split()
    main(filelist)
