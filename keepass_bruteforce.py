"""
KeePass brute forcing script
Based on another GitHub project by Raphael Vallat: https://gist.github.com/raphaelvallat/646bd1675f2dadff09c50ebc85f298b8
Author: Timo Sittig
Date: 17th March 2021
Python 3.8.2
"""

from pykeepass import PyKeePass
import sys

import string
from itertools import product
from time import time
from numpy import loadtxt

from datetime import datetime

def check_credentials(file, passwords):
    for current in passwords:
        kp = None
        current = ''.join(current)

        try:
            kp = PyKeePass(file, password=current)
        except:
            pass

        if isinstance(kp, PyKeePass):
            print('\nPassword for ', file, ' is  ', current)
            return current
    return False

def bruteforce(file, max_nchar=8):
    print('1) Digits cartesian product')
    for l in range(1, max_nchar + 1):
        current_passwords = product(string.digits, repeat=l)
        print("\t..%d digit" % l)
        p = check_credentials(file, current_passwords)
        if p is not False:
            return p

    print('2) Digits + ASCII lowercase')
    for l in range(1, max_nchar + 1):
        print("\t..%d char" % l)
        current_passwords = product(string.digits + string.ascii_lowercase,
                            repeat=l)
        p = check_credentials(file, current_passwords)
        if p is not False:
            return p

    print('3) Digits + ASCII lower / upper + punctuation')
    all_char = string.digits + string.ascii_letters + string.punctuation

    for l in range(1, max_nchar + 1):
        print("\t..%d char" % l)
        current_passwords = product(all_char, repeat=l)
        p = check_credentials(file, current_passwords)
        if p is not False:
            return p

def main():
    max_length = 8

    if 1 < len(sys.argv):
        file = str(sys.argv[1])
        
        if 2 < len(sys.argv):
            max_length = int(sys.argv[2])
        
        start = time()
        print('Starting bruteforce on ', file, ' at ', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        bruteforce(file, max_length)
        
        end = time()
        print('Total time: %.2f seconds' % (end - start))

if __name__=='__main__':
    main()
