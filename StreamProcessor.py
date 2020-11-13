#!/usr/bin/env python3

import sys
import json as JSON
import threading
import SocketController
import cv2 as OPENCV
import numpy as NP

def ParseArgs():
    args = JSON.loads('{"-host": "192.168.100.64", "-port":8000 }') # default arguments
    for i in range(1, len(sys.argv)):
        if('-host' == sys.argv[i].lower()):
            args['-host'] = sys.argv[i+1].strip()
            pass
        if('-port' == sys.argv[i].lower()):
            args['-port'] = sys.argv[i+1].strip()
            pass
        pass
    return args

def ParseData(data):
    img = NP.zeros([600,480,3], NP.uint8)
    offset = 0
    for i in range(12):
        counter = 0
        for j in range(12):
            img[i][j] = data['pl'][offset + counter]
            counter += 1
            pass
        offset += 12
        pass
    OPENCV.imshow("test image", img)
    OPENCV.waitKey(0)
    OPENCV.destroyAllWindows()
    return 0

def main():
    args = ParseArgs()
    s = SocketController.SocketController(args['-host'], args['-port'])
    s.InitSocket_Server()
    print("listening...")
    conn, addr = s.Listen()
    print("Connected Address: ", addr)
    recv = conn.recv(517803)
    de = recv.decode()
    print("bytes recieved: %s\n\n" % (recv))
    print("buffer: %s\n" % (de))
    f = open("C:/users/denir/onedrive/desktop/tempColors.txt", "w+")
    f.write(de)
    f.close()
    conn.send(str("Hello World\0").encode())
    s.ssocket.close()
    #ParseData(JSON.loads(recv))
    return 0

if __name__ == "__main__":
    main()