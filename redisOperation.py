#-*-coding:utf-8-*-
import redis
import pickle 
import datetime
import time

class redisOperation(redis.Redis):

    def __init__(self, host='172.18.47.100', port=6379, db=3, station_name='station1'):
        self.database = redis.Redis(host=host, port=port, db=db)
        print("Successfully connect to Redis Server.")
        # 这里先进行一部分的初始化：
        key = bytes(datetime.datetime.now().strftime('%Y-%m-%d')+"_"+station_name,"utf8")
        
        if key in self.database.keys():
            pass
        else:
            start_time = datetime.datetime.now().strftime('%Y-%m-%d').split('-')+[0,0]
            start_time = list(map(lambda i: int(i),start_time))
            value = pickle.dumps({
                'data':[],
                'start_time': time.mktime(datetime.datetime(start_time[0],start_time[1],start_time[2],start_time[3],start_time[4]).timetuple())
                # 'start_time': time.mktime(datetime.datetime(2019,6,14,15,0).timetuple())
                # 'start_time': time.mktime(datetime.datetime.now().strftime('%Y-%m-%d').split('-')+[0,0])
            },protocol=2)
            self.database.set(key,value)

            index_key = key+bytes("_index","utf8")
            self.database.set(index_key,pickle.dumps(0,protocol=2))

    def setData(self, key, value):
        value = pickle.dumps(value,protocol=2)
        self.database.set(key, value)
 
    def getData(self, key):
        data = self.database.get(key)
        if data is None:
            return None
        else:
            return pickle.loads(data)
 
    def getKeys(self):
        byteKeys = self.database.keys()
        rawKeys = []
        for key in byteKeys:
            # rawKeys.append(key.decode())
            rawKeys.append(key)
        return rawKeys

    def delKeys(self,key):
        self.database.delete(key)
