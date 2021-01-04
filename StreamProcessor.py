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
import DatabaseInterface
import math

def ParseArgs():
    args = JSON.loads('{"-host": "127.0.0.1", "-port":8000 }') # default arguments
    args['-bsize'] = 34 * 1024   # 34 kb approximate default 480p stream size
    for i in range(1, len(sys.argv)):
        if('-host' == sys.argv[i].lower()):
            args['-host'] = sys.argv[i+1].strip()
            pass
        if('-port' == sys.argv[i].lower()):
            args['-port'] = sys.argv[i+1].strip()
            pass
        if('-bsize' == sys.argv[i].lower()):
            args['-bsize'] = sys.argv[i+1].strip()
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

def CalcSegments(msgLen):
    # base segment is 1 | base sleep time is 16.667 ms
    # since maximum UDP packet includes header data I'm using
    # 32000 bytes as divisor instead of the full 32Kb
    data = [1, 0.1667, msgLen]
    quotient = math.ceil(msgLen / 32000)
    if quotient > 1:
        data[2] = 32000
        pass
    data[0] = quotient
    data[1] = data[1] // quotient   # get the lower bound
    return data

def main_JPEG_Stream(args):
    db = DatabaseInterface.DB(cname = "stream", creg = True, cinit = True)
    res = db.Init()
    if(res != 0):
        print("*failed to connect to database.")
        return 1
    print('RCVBUF={}'.format(
        DatabaseInterface.API.UDP_Socket.getsockopt(
            SocketController.socket.SOL_SOCKET,
            SocketController.socket.SO_RCVBUF
            )
        )
    )
    sock = SocketController.SocketController(args['-host'], args['-port'], args['-bsize'])
    sock.InitSocket_Server()
    print("*stream processor is listening..")
    conn, addr = sock.Listen()
    print("Connected by Address: ", addr)
    frameCounter = 0
    while(True):
        # caviot: appearantly my encryption method increases the size of the messages
        # so my UDP messages end up being larger than 64Kb, so I have to send the message in segments
        recv = sock.RecvData(conn)
        recvLen = len(recv)
        print("recieved: %s | bytes: %s." % (recv, recvLen))
        segData = CalcSegments(recvLen)
        for x in range(segData[0]):
            lowerBound = segData[2] * x
            upperBound = segData[2] * x + 1
            if x == (segData[0] - 1):
                upperBound = recvLen
                pass
            print("segment[%s:%s]: %s" % (lowerBound, upperBound, recv[lowerBound:upperBound]))
            db.SendData(recv[lowerBound:upperBound])
            time.sleep(segData[1])
            pass
        db.SendData("END FRAME:{}".format(frameCounter))
        break
        frameCounter += 1
        pass
    sock.Close()
    db.Close()
    return 0

def main_MP4_Stream(args):
    return 0

if __name__ == "__main__":
    args = ParseArgs()
    #main()
    #TestFunc()
    #ParseData()
    #ST.RunTest()
    main_JPEG_Stream(ParseArgs())