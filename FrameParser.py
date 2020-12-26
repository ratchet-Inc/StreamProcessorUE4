#! C:/Python3
import numpy as NP
from PIL import Image
import StreamProcessor_PY as SP_FAST

FrameWidth = 640
FrameHeight = 360
LossyFrame = 1


def ParseFrame(data: list, w = FrameWidth, h = FrameHeight, lossy = LossyFrame) -> list:
    arr = NP.zeros([h, w, 3], order = "C", dtype = NP.uint8)
    temp = []
    col = 0
    row = 0
    buf = []
    append1 = temp.append
    append2 = buf.append
    for byt in data:
        append2(byt)
        if len(buf) > 1:
            append1(int("".join(buf), 16))
            buf.clear()
            if len(temp) > 2:
                #convert from RGB to BGR
                #temp[0], temp[2] = temp[2], temp[0]
                arr[col][row] = temp
                temp.clear()
                row += lossy
                if row >= w:
                    col += 1
                    row = 0
                pass
            pass
        pass
    return arr

def ParseFrame2(data: list, w = FrameWidth, h = FrameHeight) -> list:
    sink = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    arr = NP.zeros([h, w, 3], order = "C", dtype = NP.uint8)
    index = 0
    for i in range (len(arr)):
        for j in range(len(arr[i])):
            arr[i][j][2] = (sink[data[index+0]] * 16) + sink[data[index+1]]
            arr[i][j][1] = (sink[data[index+2]] * 16) + sink[data[index+3]]
            arr[i][j][0] = (sink[data[index+4]] * 16) + sink[data[index+5]]
            index += 6
            pass
        pass
    return arr

def FromHex(val: str) -> int:
    sink = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    value = sink[val[0]]*16 + sink[val[1]]
    return value

def ParseFrameFAST(data: list, w = FrameWidth, h = FrameHeight) -> list:
    arr = NP.zeros([h, w, 3], order = "C", dtype = NP.uint8)
    SP_FAST.ParseFrame(data, arr)
    return arr

def ConvertIMG(numpyArr: list, saveFlag=False):
    img = Image.fromarray(numpyArr)
    if saveFlag:
        img.save('rendered.jpg', 'jpeg')
        pass
    return 0
