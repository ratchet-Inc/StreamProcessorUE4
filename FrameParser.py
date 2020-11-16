#! C:/Python3
import numpy as NP

FrameWidth = 640
FrameHeight = 360
LossyFrame = 1


def ParseFrame(data: list, w = FrameWidth, h = FrameHeight, lossy = LossyFrame) -> list:
    arr = NP.zeros([h, w, 3], NP.uint8)
    byt = 0
    temp = []
    col = 0
    row = 0
    buf = ''
    while byt < len(data):
        buf += data[byt]
        if len(buf) > 1:
            temp.append(int(buf, 16))
            buf = ''
            pass
        if len(temp) == 3:
            #convert from RGB to BGR
            temp[0], temp[2] = temp[2], temp[0]
            arr[col][row] = temp
            temp = []
            row += lossy
            if row >= FrameWidth:
                col += 1
                row = 0
            pass
        byt += 1
        pass
    return arr