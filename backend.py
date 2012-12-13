'''
class for populating and qurying the files DB
'''

import logging
import os
import sqlite3 as sq

class FileInfo:

	def __init__(self, path, size, date):
		self.path = path
		self.size = size
		self.date = date

class Backend:

	def __init__(self, dbname):
		self.dbname = dbname
		self.conn 	= None
		self.cur	= None

	def	get_file_list(self):
		'''run the query, return results'''
		self.cur.execute('select fpath from files')
		return self.cur.fetchall()

	def	get_file_info(self, fpath):
		'''run the query, return results'''
		sqry = "select * from files where fpath = '%s'" % fpath
		logging.info("invoking %s" % sqry)
		self.cur.execute(sqry)
		row = self.cur.fetchone()
		
		if row:
			filedata = FileInfo(row[0], row[1], row[2])
			return filedata
		else:
			return None

	def open_db(self):
		'''open a connection to the DB'''
		logging.info("tickstore: opening %s" % self.dbname)
		self.conn = sq.connect(self.dbname);
		self.cur = self.conn.cursor();

	def create_db(self):
		logging.info("creating %s" % self.dbname)
		self.conn = sq.connect(self.dbname)
		self.cur = self.conn.cursor()
		self.cur.execute("drop table if exists files")
		self.cur.execute("create table files (fpath text, fsize integer, fdate string)")

	def close_db(self):
		'''close connection to the DB'''
		self.conn.commit()
		self.conn.close()

	def write_file_data(self, filedata):
		'''issue a query to write file data'''
		self.cur.execute("insert into files values('%s', '%s', '%s')" %  (filedata.path, filedata.size, filedata.date) )

