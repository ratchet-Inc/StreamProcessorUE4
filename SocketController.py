import socket

class SocketController():
    """ A simple socket abstraction class to remove complexity elsewhere """
    def __init__(self, host, port, bufferLen = 1024):
        self.host = host
        self.port = port
        self.buffLen = bufferLen
        pass
    def InitSocket_Server(self):
        try:
            self.ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssocket.bind((self.host, self.port))
            pass
        except:
            return 1
        return 0
    def Listen(self):
        self.ssocket.listen()
        return self.ssocket.accept()
    def SendData(self, msg: str):
        return self.ssocket.send(msg)
    def RecvData(self, conn):
        return self.ssocket.recv(self.buffLen)
    pass