#!/usr/bin/env python3

import sys
import json as JSON
import threading
import SocketController

def ParseArgs():
    args = JSON.loads('{"-host": "localhost", "-port":8000 }') # default arguments
    for i in range(1, len(sys.argv)):
        if('-host' == sys.argv[i].lower()):
            args['-host'] = sys.argv[i+1].strip()
            pass
        if('-port' == sys.argv[i].lower()):
            args['-port'] = sys.argv[i+1].strip()
            pass
        pass
    return args

def main():
    args = ParseArgs()

    return 0

if __name__ == "name":
    main()