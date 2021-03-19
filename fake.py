#!/usr/bin/env python3
import io
import sys
import os

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


# if __name__ == '__main__':
url = sys.argv[1]
print(url + " yay")
print(os.getcwd())
print(os.getuid())
