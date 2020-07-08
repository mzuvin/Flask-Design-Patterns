from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired('Kullanici adi gerekli'), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email('Email hata!')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Donor(FlaskForm):
    isim = StringField('isim',
                           validators=[DataRequired('isim gerekli'), Length(message="İsim Alanı 3 ile 20 Karakter olnak zorunda!",min=3, max=20)])
    soyisim = StringField('soyisim',
                           validators=[DataRequired('soyisim gerekli'), Length(message="İsim Alanı 3 ile 20 Karakter olnak zorunda!",min=3, max=20)])

    tel  = IntegerField('tel', validators=[DataRequired('tel gerekli')])
    #NumberRange(min=5, max=12, message="Telefon Numarası Hatası")

    adres = StringField('adres', validators=[DataRequired('adres gerekli')])

    tc = IntegerField('tc', validators=[DataRequired('tc hatali')])

    kan = RadioField('kan', validators=[DataRequired('Kan Grubu Girilmek Zorunda')], choices=[('1','A+'),('2','A-'),('3','B+'),('4','B-'),('5','AB+'),('6','AB-'),('7','0+'),('8','0-')])

    hastane = StringField('hastane')

    email = StringField('email',
                        validators=[DataRequired('Bu alan Zorunlu!'), Email('sallama email girmeyiniz.')])
    cinsiyet = RadioField('cinsiyet', validators=[DataRequired()], choices=[('e','erkek'),('k','kadin')])

    #HASTA YAKINI FORM ALANI
    yisim = StringField('yisim',
                           validators=[DataRequired('isim gerekli'), 
                           Length(message="İsim Alanı 3 ile 20 Karakter olnak zorunda!",min=3, max=20)])
    ysoyisim = StringField('ysoyisim',
                           validators=[DataRequired('soyisim gerekli'), Length(message="İsim Alanı 3 ile 20 Karakter olnak zorunda!",min=3, max=20)])

    ytel  = IntegerField('ytel', validators=[DataRequired('ytel gerekli')])

    yadres = StringField('yadres')

    ytc = IntegerField('ytc', validators=[DataRequired('Yakın Tc Numarası Girmek Zorunlu')])    

    submit = SubmitField('kaydet')