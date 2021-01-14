import Client_Package.CoreAPI as API

class DB(object):
    def __init__(self, host = "localhost", cname = "", creg = False, cinit = False):
        self.k = "Z4QC6KAM9WrXsm58jkXtoOfXVaN82LSrxtkJXzK0NP87nftNtGw2dieFJBDW99Ri"
        self.h = host
        self.cacheName = cname
        self.cacheReg = creg
        self.cacheInit = cinit
        API.SetAPI_Key(self.k)
        pass
    def Init(self):
        return API.InitAPI(self.h, self.cacheReg, self.cacheInit, self.cacheName)
    def SendData(self, msg: str, append: bool = False)->int:
        return API.SendToCache(msg, ip_addr = self.h, append = append)
    def Close(self):
        return API.CloseAPI()
    pass
