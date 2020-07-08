from kanbankasi.sqlrun import sqlrun
import time,json
from kanbankasi import app
from kanbankasi.adaptor import rowsjson

class kanal():
	def __init__(self,dtc,kanid,adet):
		self.tc=dtc
		self.zaman=time.strftime("%Y-%m-%d")
		self.kanid=kanid
		self.adet=adet

	def donate(self):
		sorgu = "insert into donate (donor_tc,donate_date,donor_blood_id,blood_miktar) values ("+str(self.tc)+",'"+str(self.zaman)+"',"+str(self.kanid)+","+str(self.adet)+")"
		print(sorgu)
		a=sqlrun(sorgu)

	def listegetir(self,offset,limit):
		sorgu="select tip, rh, isim, soyisim, tc, kanid from kanverenlist offset "+ str(offset) +" rows fetch first "+str(limit)+" rows only"
		a = rowsjson(sorgu)
		return a


