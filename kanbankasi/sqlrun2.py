#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
#sql kodlarını çalıştıracak dosya
from flask import Flask, flash
import logging as log
import json

class MetaSingleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class Database(metaclass=MetaSingleton):
	def __init__(self):
		self.con=None
		if self.con is None:
			self.con = psycopg2.connect("host='ec2-54-228-252-67.eu-west-1.compute.amazonaws.com' dbname='d8q0af90g4n4du' user='hggpdxcwdtspnn' password=''")
			self.con.set_client_encoding('UTF8')
			self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

	def execute(self,sorgu):
		try:
			self.cur.execute(sorgu)
			self.con.commit()
			log.debug("sorgu"+sorgu)
			print(sorgu)
			#flash(f'Basarili !\n'+str(self.sorgu), 'success')
			while True:
				row = self.cur.fetchall()
				if row == None:
					break
				#print(row)
				return list(row)
		except psycopg2.DatabaseError as e:
			print(e)
			if self.con:
				self.con.rollback()
		finally:
			if self.con:
				#self.con.close()
				print()
				

#tek nesne
def sqlrun(sorgu):
	db1 = Database()
	return db1.execute(sorgu)


if __name__ == '__main__':
    sqlrun()
