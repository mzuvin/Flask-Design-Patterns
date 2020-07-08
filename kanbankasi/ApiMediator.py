from abc import ABC
from kanbankasi.adaptor import rowsjson
from kanbankasi.sqlrun2 import sqlrun

class Mediator(ABC):
	#sender:object event:str
	def crud(self,sender,event):
		pass

class ConcreteMediator(Mediator):
	def __init__(self, donor, hasta):
	    self._component1 = donor
	    self._component1.mediator = self
	    self._component2 = hasta
	    self._component2.mediator = self
	
	def crud(self, sender, event, **param):
		if event == "list":
			if sender.name=="donor":
				return self._component1._list(param['offset'],param['limit'])
			if sender.name=="hasta":
				return self._component2._list(param['offset'],param['limit'])
		elif event == "create":
			if sender.name=="donor":
				data=param['data']
				return self._component1._create(data)				
			if sender.name=="hasta":
				data=param['data']
				return self._component2._create(data)
		elif event == "update":
			if sender.name=="donor":
				data=param['data']
				return self._component1._update(data)
			if sender.name=="hasta":
				data=param['data']
				return self._component2._update(data)
		elif event == "delete":
			if sender.name=='donor':
				data=param['data']
				return self._component1._delete(data)
			if sender.name=='hasta':
				data=param['data']
				return self._component2.delete(data)
				
class BaseComponent:
    def __init__(self, mediator = None):
        self._mediator = mediator
    @property
    def mediator(self):
        return self._mediator
    @mediator.setter
    def mediator(self, mediator):
    	self._mediator = mediator

class ComponentDonor(BaseComponent):
	def __init__(self,isim):
		self.name=isim
	def list(self,offset,limit):
		return self.mediator.crud(self, "list",offset=offset,limit=limit)
	def create(self,data):
		return self.mediator.crud(self, "create",data=data)
	def update(self,data):
		return self.mediator.crud(self, "update",data=data)
	def delete(self,data):
		return self.mediator.crud(self,"delete",data=data)
	def _list(self,offset,limit):
		sorgu="select * from donor offset "+ str(offset) +" rows fetch first "+str(limit)+" rows only"
		return rowsjson(sorgu)
	def _create(self,data):
		sorgu="insert into donor(d_name,d_surname,d_gender,d_email,d_address,d_phone,d_tc,h_id,kan_grubu) values('"+data['isim']+"','"+data['soyisim']+"','"+data['cinsiyet']+"','"+data['email']+"','"+data['adres']+"',"+str(data['tel'])+","+str(data['tc'])+",1,"+str(data['kan'])+")"
		sqlrun(sorgu)
		if str(data['ytc'])!="None":
			sorguyh="insert into dfriend(d_f_name, d_f_surname,d_f_tc,d_f_phone,d_f_address) values('"+data['yisim']+"','"+data['ysoyisim']+"',"+str(data['ytc'])+","+str(data['ytel'])+",'"+data['yadres']+"')"
			iliskisql="INSERT INTO \"DFRelative\" VALUES("+str(data['tc'])+","+str(data['ytc'])+");"
			sqlrun(sorguyh)
			sqlrun(iliskisql)
			return "yakin ile eklendi"
		else:
			return "Lütfen yakin tc numarası giriniz."
	def _update(self,data):
		sorgu="update donor set (d_name,d_surname,d_gender,d_email,d_address,d_phone,d_tc,h_id,kan_grubu) =('"+data['isim']+"','"+data['soyisim']+"','"+data['cinsiyet']+"','"+data['email']+"','"+data['adres']+"',"+data['tel']+","+str(data['tc'])+",1,"+str(data['kan'])+") where d_tc="+str(data['tc'])+";"
		sqlrun(sorgu)
		try:
			sorgupfriend="update dfriend set (d_f_name, d_f_surname,d_f_tc,d_f_phone,d_f_address)=('"+data['yisim']+"','"+data['ysoyisim']+"','"+data['ytc']+"',"+data['ytc']+",'"+data['yadres']+"') where d_f_tc="+str(data['ytc'])
			sqlrun(sorgupfriend)
		except:
			sorguyh="insert into dfriend(d_f_name, d_f_surname,d_f_tc,d_f_phone,d_f_address) values('"+data['yisim']+"','"+data['ysoyisim']+"',"+data['ytc']+","+data['ytel']+",'"+data['yadres']+"')"
			iliskisql="INSERT INTO \"DFRelative\" VALUES("+str(data['tc'])+","+str(data['ytc'])+");"
			sqlrun(sorguyh)
			sqlrun(iliskisql)
		return 'basarili'
	def _delete(self,data):
		sorgu="DELETE FROM donor WHERE d_tc="+str(int(data['d_tc']))
		sqlrun(sorgu)
		return str(data['d_tc'])

class ComponentHasta(BaseComponent):
	def __init__(self,isim):
		self.name=isim
	def list(self,offset,limit,search=""):
		return self.mediator.crud(self, "list",offset=offset,limit=limit,search=search)
	def create(self,data):
		return self.mediator.crud(self, "create",data=data)
	def update(self,data):
		return self.mediator.crud(self, "update",data=data)
	def delete(self,data):
		return self.mediator.crud(self,"delete",data=data)
	
	def _list(self,offset,limit,search=""):
		sorgu="select * from patient offset "+ str(offset) +" rows fetch first "+str(limit)+" rows only"
		return rowsjson(sorgu)
	def _create(self,data):
		sorgu="insert into patient(p_name,p_surname,p_gender,p_email,p_address,p_phone,p_tc,h_id,kan_grubu) values('"+data['isim']+"','"+data['soyisim']+"','"+data['cinsiyet']+"','"+data['email']+"','"+data['adres']+"',"+data['tel']+","+str(data['tc'])+",1,"+str(data['kan'])+")"
		sqlrun(sorgu)
		if str(data['ytc'])!="":
			sorguyh="insert into pfriend(pf_name, pf_surname,pf_tc,pf_phone,pf_address) values('"+data['yisim']+"','"+data['ysoyisim']+"',"+data['ytc']+","+data['ytel']+",'"+data['yadres']+"')"
			iliskisql="INSERT INTO \"PFRelative\" VALUES("+str(data['tc'])+","+str(data['ytc'])+");"
			sqlrun(sorguyh)
			sqlrun(iliskisql)
			return "yakin ile eklendi"
		else:
			return "Lütfen yakin tc numarası giriniz."
	def _update(self,data):
		sorgu="update patient set (p_name,p_surname,p_gender,p_email,p_address,p_phone,p_tc,h_id,kan_grubu) =('"+data['isim']+"','"+data['soyisim']+"','"+data['cinsiyet']+"','"+data['email']+"','"+data['adres']+"',"+data['tel']+","+str(data['tc'])+",1,"+str(data['kan'])+") where p_tc="+str(data['tc'])+";"
		sqlrun(sorgu)
		#yakin bilgisi girilmisse ve yeniden yakin bilgisi eklenmek isteniyorsa
		if str(data['ytc'])!="":
			sorgupfriend="update pfriend set (pf_name,pf_surname,pf_tc,pf_phone,pf_address)=('"+data['yisim']+"','"+data['ysoyisim']+"','"+data['ytc']+"',"+data['ytc']+",'"+data['yadres']+"') where pf_tc="+str(data['ytc'])
			sqlrun(sorgupfriend)
			try:
				sorguyh="insert into pfriend(pf_name, pf_surname,pf_tc,pf_phone,pf_address) values('"+data['yisim']+"','"+data['ysoyisim']+"',"+data['ytc']+","+data['ytel']+",'"+data['yadres']+"')"
				iliskisql="INSERT INTO \"PFRelative\" VALUES("+str(data['tc'])+","+str(data['ytc'])+");"
				sqlrun(sorguyh)
				sqlrun(iliskisql)
			except:
				return "zaten var"
		return ''
	def _delete(self,data):
		sorgu="DELETE FROM patient WHERE p_tc="+str(data[0]['p_tc'])
		sqlrun(sorgu)
		return str(data[0]['p_tc'])
