from abc import ABCMeta, abstractmethod
from flask import Flask,session, render_template, url_for, flash, redirect,request,jsonify
from kanbankasi.forms import RegistrationForm, LoginForm, Donor
from kanbankasi import app
from functools import wraps
from kanbankasi.sqlrun import sqlrun

class UserSystem(metaclass=ABCMeta):
	@abstractmethod
	def register(self):
		pass
	@abstractmethod
	def login(self):
		pass


class islem(UserSystem):
	def __init__(self,isim):
		self.isim=isim

	def login_required(f):
		@wraps(f)
		def wrap(*args, **kwargs):
			if 'logged_in' in session:
				return f(*args, **kwargs)
			else:
				flash('Giriş Yapın!')
				return redirect(url_for('login'))
		return wrap


	@app.route("/cikis/")
	def logout():
		session.clear()
		#session.pop('username', None)
		flash('cikis yaptiniz.')
		return redirect(url_for('login'))


	@app.route("/register", methods=['GET', 'POST'])
	def register():
		if 'logged_in' in session:
			return redirect(url_for('home'))
		form = RegistrationForm()
		if form.validate_on_submit():
			email=form.email.data
			username=form.username.data
			password=form.password.data
			sqlrun("insert into user1(username,password,email) values('"+username+"','"+password+"','"+email+"')")
			flash(f'Account created for {form.username.data}!', 'success')
			return redirect(url_for('home'))
		return render_template('register.html', title='Register', form=form)

	
	@app.route("/login", methods=['GET', 'POST'])
	def login():
		if 'logged_in' in session:
			return redirect(url_for('home'))
		form = LoginForm()
		if form.validate_on_submit():
			a=sqlrun("select user_id as id from user1 where email='"+form.email.data+"' and password='"+form.password.data+"'")
			try:
				userid=a[0][0]
			except:
				userid=-2
			if userid>-1:
				session['logged_in']=True
				session['email'] = form.email.data
				flash('You have been logged in!', 'success')
				return redirect(url_for('home'))
			else:
				flash('Giriş Başarısız. Lütfen Email ve Şifrenizi kontrol ediniz.', 'danger')
		return render_template('login.html', title='Login', form=form)


