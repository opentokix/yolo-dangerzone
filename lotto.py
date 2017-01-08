#!/usr/bin/env pypy
import random
import sys
import time

def main():
    count = 0
    start_time = time.time()
    while 1:
        count += 1
        row = [1, 2, 3, 4, 5, 6, 7]
        numbers = []
        drawn = []
        for i in range(1,36):
            numbers.append(i)
        for i in range(0,7):
            selection = random.choice(numbers)
            numbers.remove(selection)
            drawn.append(selection)
        drawn.sort()
        if drawn == row:
            end_time = time.time()
            t = end_time - start_time
            print drawn
            print "Win, %d iteration in %s s" % (count, t)
            sys.exit(0)
if __name__ == '__main__':
    main()
