import Client_Package.CoreAPI as API

class DB(object):
    def __init__(self, host = "localhost", cname = "", creg = False, cinit = False):
        return API.InitAPI(host, creg, cinit, cname)
    def SendData(self, msg: str)->int:
        return API.SendToCache(msg)
    def Close(self):
        return API.CloseAPI()
    pass
