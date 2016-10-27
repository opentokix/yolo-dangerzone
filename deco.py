#!/usr/bin/env python
from functools import wraps
import time

global DEBUG
DEBUG = True

def verbose(func):
    wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        t = (time.time() - start_time)
        if DEBUG  == True:
            print "%s took %fs" % (func.__name__, t)
        return res
    return wrapper


@verbose
def arccot(x, unity):
    sum = xpower = unity // x
    n = 3
    sign = -1
    while 1:
        xpower = xpower // (x*x)
        term = xpower // n
        if not term:
            break
        sum += sign * term
        sign = -sign
        n += 2
    return sum

@verbose
def pi(digits):
    unity = 10**(digits + 10)
    pi = 4 * (4*arccot(5, unity) - arccot(239, unity))
    return pi // 10**10

def main():
    p = pi(32423)

if __name__ == "__main__":
    main()
