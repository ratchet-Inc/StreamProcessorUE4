import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

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
        conn, addr = self.ssocket.accept()
        return conn, addr
    def SendData(self, msg):
        return 0
    def RecvData(self):
        return self.ssocket.recv(self.buffLen)
    pass