#!/usr/bin/env python3

import sys
import json as JSON
import threading
import cv2 as OPENCV
import numpy as NP
import SocketController
import FrameParser
import time
import StreamTest as ST

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

def ParseData():
    img = NP.zeros([480,600,3], NP.uint8)
    img[:,300:] = [255, 255, 0]
    img[:,:300] = [0, 255, 255]
    OPENCV.imshow("test image", img)
    OPENCV.waitKey(0)
    OPENCV.destroyAllWindows()
    return 0

def ParseData2(data):
    img = data
    OPENCV.imshow("test image", img)
    OPENCV.waitKey(0)
    OPENCV.destroyAllWindows()
    return 0

def main(args = None):
    if not args:
        args = ParseArgs()
        pass
    s = SocketController.SocketController(args['-host'], args['-port'])
    s.InitSocket_Server()
    print("listening...")
    conn, addr = s.Listen()
    print("Connected Address: ", addr)
    recv = conn.recv(4200000)
    de = recv.decode()
    #print("bytes recieved: %s\n\n" % (recv))
    conn.send(str("Hello World\0").encode())
    s.ssocket.close()
    print("buffer ending: %s\n" % (de[len(de) - 7:]))
    f = open("C:/UE4_Dumps/Streamed(HEX).txt", "w")
    f.write(de)
    f.close()
    #ParseData(JSON.loads(recv))
    r = FrameParser.ParseFrame(de, w = 1207, h = 572)
    res = ParseData2(r)
    return res

def TestFunc():
    print("Reading file...")
    #f = open("C:/UE4_Dumps/UE4_Frame(buffer).txt", "r")
    f = open("C:/UE4_Dumps/Streamed(HEX).txt", "r")
    data = f.read()
    f.close()
    print("parsing data")
    start = time.time()
    #r = FrameParser.ParseFrame(data, w = 1207, h = 572, lossy=1)
    #r = FrameParser.ParseFrame2(data, w = 1207, h = 572)
    r = FrameParser.ParseFrameFAST(data, w = 1207, h = 572)
    stop = time.time()
    print("Time taken: %s seconds" % (stop - start))
    FrameParser.ConvertIMG(r, True)
    ParseData2(r)
    return 0

if __name__ == "__main__":
    args = ParseArgs()
    #main()
    #TestFunc()
    #ParseData()
    ST.RunTest()