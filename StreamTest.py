import socket
import base64
import testFrame
import Client_Package.CoreAPI as GUC
import time
import math
import json as JSON

fName = "C:/UE4_Dumps/rendered(TCP).jpg"

def RunTestTCP(isFile = True):
    print("***Starting test stream...\n\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 8000))
    print("*Server is listening...")
    sock.listen()
    conn, addr = sock.accept()
    print("Connected Address: ", addr)
    recv = conn.recv(45000)
    if not isFile:
        print("recieved: %s\nsending response." % (base64.b64encode(recv)))
    else:
        print("attempting to write to disk")
        try:
            f = open(fName, "wb")
            f.write(recv)
            f.close()
            print("File created and written to.")
        except:
            print("Disk writing failed.")
            pass
        pass
    s = "Closing connection.\0".encode()
    conn.send(s)
    sock.close()
    return 0

def EncodeTestFunc():
    f = open(fName, "rb")
    fData = f.read()
    f.close()
    enc = base64.b16encode(fData)
    print(enc.decode())
    return 0

def StreamTestFunc():
    def CalcSegments(msgLen):
        data = [1, 0.3334, msgLen]
        maxSegLen = 31 * 1024
        quotient = math.ceil(msgLen / maxSegLen)
        if quotient > 1:
            data[2] = maxSegLen
            pass
        data[0] = quotient
        data[1] = data[1] / quotient
        return data
    GUC.SetAPI_Key("Z4QC6KAM9WrXsm58jkXtoOfXVaN82LSrxtkJXzK0NP87nftNtGw2dieFJBDW99Ri")
    res = GUC.InitAPI(regToCache = True, initCache = True, cacheName = "stream")
    if(res != 0):
        print("*failed to connect to database.")
        return 1
    frameCounter = 1
    while(True):
        time.sleep(0.41667)
        recv = testFrame.GetSampleFrame()
        recvLen = len(recv)
        #print("recieved: %s | bytes: %s." % (recv, recvLen))
        segData = CalcSegments(recvLen)
        print("segment info: %s" % segData)
        for x in range(segData[0]):
            lowerBound = segData[2] * x
            upperBound = segData[2] * (x + 1)
            if x == (segData[0] - 1):
                upperBound = recvLen
                pass
            obj = JSON.loads('{}')
            obj['_'] = frameCounter
            obj['seg'] = x
            obj['frm'] = recv[lowerBound:upperBound]
            d = JSON.dumps(obj)
            print("segment[%s:%s]: %s" % (lowerBound, upperBound, d))
            GUC.SendToCache(d, append = True)
            time.sleep(segData[1])
            pass
        obj = JSON.loads('{}')
        obj['_'] = frameCounter
        obj['frm'] = "END FRAME"
        obj['seg'] = segData[0]
        GUC.SendToCache(JSON.dumps(obj), append = True)
        frameCounter += 1
        break
        pass
    GUC.CloseAPI()
    return 0

def RunTest():
    reval = 1
    #reval = EncodeTestFunc()
    reval = StreamTestFunc()
    #reval = RunTestTCP(False)
    return reval