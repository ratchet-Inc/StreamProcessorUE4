import socket
import base64
import testFrame

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

def StreamTestFunc():
    f = open(fName, "rb")
    fData = f.read()
    f.close()
    enc = base64.b16encode(fData)
    print(enc.decode())
    return 0

def RunTest():
    return RunTestTCP(False)#StreamTestFunc()