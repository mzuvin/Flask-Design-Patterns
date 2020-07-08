#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
#sql kodlarını çalıştıracak dosya
from flask import Flask, flash
import logging as log
#log.debug("sorgu"+sorgu)
con = None

def sqlrun(sorgu):
	try:
		con = psycopg2.connect("host='ec2-54-228-252-67.eu-west-1.compute.amazonaws.com' dbname='d8q0af90g4n4du' user='hggpdxcwdtspnn' password=''")
		con.set_client_encoding('UTF8')
		cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute(sorgu)
		con.commit()

		flash(f'Basarili !\n'+str(sorgu), 'success')
		#global col_names
		#col_names = [i[0] for i in cur.description]
		#for n, name in enumerate(col_names):
		#    print name
		#    self.tree.heading('#'+str(i), text=str(name), anchor=W)
		#    self.tree.column('#'+str(i), stretch=True, minwidth=80, width=85)
		while True:
			row = cur.fetchall()

			if row == None:
				break
			return list(row)

	except psycopg2.DatabaseError as e:
		flash(f'sorgu: !\n'+str(e), 'error')
		return str(e)
		if con:
			con.rollback()

        #log.debug(str(e))
        #print 'Error %s' % e
        #self.message['text']=e
        #sys.exit(1)

	finally:
		flash(f'sorgu: !\n'+str(sorgu), 'error')   
		if con:
			con.close()
        


if __name__ == '__main__':
	sqlrun()


"""
sorgu="select * from user1 u where u.username='admin' and u.password='admin'"
a=sqlrun(sorgu)
print (a)
"""
