#!/usr/bin/env python
from subprocess import call

def main():
    output = call(['ls', '-l', '-a'])
    print output


if __name__ == '__main__':
    main()
