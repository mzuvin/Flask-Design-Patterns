import json

from kanbankasi.sqlrun2 import sqlrun
#from sqlrun2 import sqlrun
class Target:
	#interface default method
	def list2json(self,sorgu):
		return sqlrun(sorgu)

class JsonDict(Target):
    def __init__(self, sqlrun):
        self.sqlrun = sqlrun

    def list2json(self,sorgu):
    	rows=self.sqlrun(sorgu)
    	return json.dumps( [dict(ix) for ix in rows] )

def client_code(target,sorgu):
	print(target.list2json(sorgu))

def rowsjson(sorgu):
	adapter=JsonDict(sqlrun)
	return adapter.list2json(sorgu)
		
"""
target = Target()
client_code(target,"select * from user1")
adapter= JsonDict(sqlrun)
client_code(adapter,"select * from user1")
"""