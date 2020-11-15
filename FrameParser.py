#! C:/Python3
import numpy as NP

FrameWidth = 600
FrameHeight = 480
LossyFrame = 2


def ParseFrame(data: list) -> list:
    arr = NP.zeros([FrameHeight, FrameWidth, 3], NP.uint8)
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
            temp[0], temp[2] = temp[2], temp[0]
            arr[col][row] = temp
            temp = []
            row += LossyFrame
            if row >= FrameWidth:
                col += 1
                row = 0
            pass
        byt += 1
        pass
    return arr