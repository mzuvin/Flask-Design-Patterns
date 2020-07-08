from flask import Flask, render_template, url_for, flash, redirect,request,jsonify
from kanbankasi.forms import RegistrationForm, LoginForm, Donor
from kanbankasi.sqlrun2 import sqlrun
from kanbankasi.kanalver import kanver
from kanbankasi.kanAl import kanal
import logging,json
from functools import wraps
from kanbankasi import app
from kanbankasi.userroute import islem 
from kanbankasi.adaptor import rowsjson
import kanbankasi.ApiMediator as api
donorApi=api.ComponentDonor('donor')
hastaApi=api.ComponentHasta('hasta')
api.ConcreteMediator(donorApi, hastaApi)

@app.route("/kanveren/json/datatable",methods=['GET', 'POST'])
@islem.login_required
def kanverenlist():
	offset = request.values.get('offset')
	limit = request.values.get('limit')
	if str(offset)=="None":
		offset=0
	if str(limit)=="None":
		limit=2

	ka1=kanal(0,0,0)
	return ka1.listegetir(offset,limit)

@app.route("/kanveren/json",methods=['GET', 'POST'])
@islem.login_required
def kanveren():
	tc=request.values.get('tc')
	id=request.values.get('kid')
	adet=request.values.get('adet')
	if int(adet)>0:
		ka=kanal(tc,id,adet)
		ka.donate()
		return 'tamam..'
	else:
		return 'adet girilmedi..'

@app.route("/stokkan/json",methods=['GET', 'POST'])
@islem.login_required
def stockkan():
	tc=request.values.get('tc')
	id=request.values.get('kid')
	adet=request.values.get('adet')
	stockid=request.values.get('stokid')
	if int(adet)>0:
		kv1=kanver(tc,id,adet,stockid)
		kv1.donated(stockid)
		return 'tamam..'
	else:
		kv=kanver(tc,id,adet,stockid)
		return str(kv.stokkanlarlistele())
	
@app.route("/hastakan/json",methods=['GET', 'POST'])
@islem.login_required
def homehastakanjson():
	offset = request.values.get('offset')
	limit = request.values.get('limit')
	if str(offset)=="None":
		offset=0
	if str(limit)=="None":
		limit=2
	id=request.values.get('kid')
	#where kan_grubu="+str(id)+
	sorgu="select p_name as isim, p_surname as soyisim, p_tc as tc,kan_grubu as kanid from patient offset "+ str(offset) +" rows fetch first "+str(limit)+" rows only"
	rows=rowsjson(sorgu)
	return rows

@app.route("/stok/json",methods=['GET', 'POST'])
@islem.login_required
def homejson():
	sorgu="select b.blood_type as tip, b.blood_rh as rh, sum(blood_adet) as tane from stock s join blood b on s.blood_id=b.blood_id group by b.blood_type, b.blood_rh"
	rows=rowsjson(sorgu)
	return rows

@app.route("/donoryakini/json",methods=['GET', 'POST'])
@islem.login_required
def donoryakini():
	a=request.values.get('tc')
	hastayakinibul="select d_friend_tc from \"DFRelative\" where donor_tc="+str(a)
	hastayakinibul=sqlrun(hastayakinibul)
	if str(hastayakinibul)=='[]':
		return '[]'
	else:
		pftc=hastayakinibul[0][0]
		hastabilgi="select * from dfriend where d_f_tc="+str(pftc)
		rows=rowsjson(hastabilgi)
		return rows 

@app.route("/hastayakini/json",methods=['GET', 'POST'])
@islem.login_required
def hastaYakini():
	a=request.values.get('tc')
	hastayakinibul="select p_frient_tc from \"PFRelative\" where patient_tc="+str(a)
	hastayakinibul=sqlrun(hastayakinibul)
	if str(hastayakinibul)=='[]':
		return '[]'
	else:
		pftc=hastayakinibul[0][0]
		hastabilgi="select * from pfriend where pf_tc="+str(pftc)
		rows=rowsjson(hastabilgi)
		return rows 

@app.route("/hasta/json",methods=['GET', 'POST'])
@islem.login_required
def hastajson():
	a=request.values.get('a')
	search = request.values.get('search')
	offset = request.values.get('offset')
	limit = request.values.get('limit')
	app.logger.error(search)
	try:
		kan = request.values.get('kan')
		sorgu="select * from patient where kan_grubu="+str(kan)
		rows=rowsjson(sorgu)
		return rows
	except:
		app.logger.error('kan yok.')

	if str(offset)=="None":
		offset=0
	if str(limit)=="None":
		limit=2
	if a=='list':
		if str(search)=="":
			return hastaApi.list(offset,limit)
		else:
			sorgu="select * from patient where p_tc="+str(search)+" offset "+ str(offset) +" rows fetch first "+str(limit)+" rows only"
			rows=rowsjson(sorgu)
			return rows
	if a=='create':
		data =request.data
		data=json.loads(data)
		return hastaApi.create(data)

	if a=='update':
		data =request.data
		data=json.loads(data)
		return hastaApi.update(data)

	if a=='delete':
		data =request.data
		data=json.loads(data)
		return hastaApi.delete(data)

@app.route("/donor/json",methods=['POST','GET'])
@islem.login_required
def donorjson():
	a=request.values.get('a')
	offset = request.values.get('offset')
	limit = request.values.get('limit')
	if str(offset)=="None":
		offset=0
	if str(limit)=="None":
		limit=2
	if a=='list':
		return donorApi.list(offset,limit)
	if a=='create':
		form = Donor()
		if form.validate_on_submit():
			data=form.data
			return donorApi.create(data)
		else:
			return jsonify(form.errors),500
	if a=='update':
		data =request.data
		data=json.loads(data)
		return donorApi.update(data)
	if a=='delete':
		data =request.data
		data=json.loads(data)
		return donorApi.delete(data)

@app.route("/hasta")
@islem.login_required
def hasta():
	return render_template('hasta.html')

@app.route("/donor")
@islem.login_required
def donor():
	form = Donor()	
	return render_template('donor.html',form=form)

@app.route("/")
@app.route("/home")
@islem.login_required
def home():
    return render_template('home.html')

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/kanver")
@islem.login_required
def kanverhtml():
    return render_template('kanver.html', title='Hastaya Kan Ver')

@app.route("/kanal")
@islem.login_required
def kanalhtml():
    return render_template('kanal.html', title='Kan Al')
