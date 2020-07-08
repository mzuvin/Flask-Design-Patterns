from kanbankasi.sqlrun import sqlrun
import time,json
from kanbankasi import app
from kanbankasi.adaptor import rowsjson

class kanver():

	def __init__(self, ptc,kanid,adet,stockid):
		self.tc=ptc
		self.zaman=time.strftime("%Y-%m-%d")
		self.kanid=kanid
		self.adet=adet
		self.stockid=stockid
		#self.islemitamamla()

	def donated(self,sid):
		app.logger.info('sid')
		app.logger.info(sid)
		sorgu="insert into donated (patient_tc,donated_date,blood_id,blood_adet,stock_id) values("+str(self.tc)+",'"+str(self.zaman)+"','"+str(self.kanid)+"','"+self.adet+"','"+str(sid)+"')"
		sqlrun(sorgu)
	def nekadarkanvar(self):
		sorgu="select sum(blood_adet) as adet ,blood_id from stock where blood_adet>0 and blood_id="+str(self.kanid)+" group by blood_id"
		a=sqlrun(sorgu)
		if (str(a)=='[]'):
			return 0
		else:
			return a[0][0]

	def stokidyegoregetir(self):
		sorgu="select stock_id, blood_adet as adet from stock where blood_id="+str(self.kanid)+" and blood_adet>0 and stock_id="+str(self.stockid)+" order by adet desc"
		a= sqlrun(sorgu)
		print(a)
		return a[0][1]

	def stokkanlarlistele(self):
		sorgu="select stock_id as id, blood_adet as adet from stock where blood_id="+str(self.kanid)+" and blood_adet>0 order by adet asc"
		a=rowsjson(sorgu)
		if (str(a)=='[]'):
			return 0
		else:
			return a

		