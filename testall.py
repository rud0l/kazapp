'''
Create test fixture
	- directory structure and files
	- populate test db

Invoke method get_all_files, check count
Invoke method get_file_info, check file info
Send web request for REST Api get_all_files, check count
Send web request for REST Api get_file_info, check file info
'''

import urllib
import json
import logging
import sys
import unittest
import subprocess
from threading import Thread

# app modules
import kazapp
import backend
import traverse

FULLSETUP = False

class KazappTest(unittest.TestCase):

	testfile 		= "/usr/share/locale/all_languages"
	testfile_size 	= 0
	testfile_date 	= 0

	testfiles_count	= 0

	bobj = backend.Backend("test.db")

	def setUp(self):
		'''setUp: creating test db'''

		global FULLSETUP
		if FULLSETUP == True:
			traverse.traverse("/usr/share/locale", "test.db")

		# get file count from bash
		cmd = "find /usr/share/locale -not -type d -not -type l"
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
		sret = process.communicate()[0]
		retcount  = len( sret.split() )
		self.testfiles_count = retcount

		# get a file size
		cmd = "stat -c %s " + self.testfile
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
		self.testfile_size = int( process.communicate()[0] )

		# get a file date
		cmd = "stat -c %Y " + self.testfile
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
		self.testfile_date = int( process.communicate()[0] )

		self.bobj.open_db()


	def tearDown(self):
		'''tearDown: closing db'''
		self.bobj.close_db()

	def testBackendGetFileList(self):
		'''query the DB for all files'''
		logging.info( "testBackendGetFileList" )
		# get file count from DB 
		lstfiles = self.bobj.get_file_list()
		logging.info("backend says db has %s files" % len(lstfiles) )
		logging.info("bash says %s files" % self.testfiles_count)

		self.assertEqual(len(lstfiles), int(self.testfiles_count))

	def testBackendGetFileInfo(self):
		'''query the DB and get info for a single file'''
		logging.info( "testBackendGetFileInfo: %s" % self.testfile )
		filedata = self.bobj.get_file_info(self.testfile)

		logging.info( "testBackendGetFileInfo: %s %s" % (filedata.size, filedata.date) )
		self.assertEqual(filedata.size, self.testfile_size)
		self.assertEqual(filedata.date, self.testfile_date)

	def testWebGetFileList(self):
		'''test REST api to  get all  files'''

		surl = "http://127.0.0.1:5001/get_file_list"

		ret = json.loads( urllib.urlopen(surl).readline() )
		self.assertTrue(ret['retcode'] == 0)

		logging.info("webapp says db has %s files" % len( ret['data'] ) )
		logging.info("bash says %s files" % self.testfiles_count)

		self.assertEqual( len( ret['data'] ),  self.testfiles_count)

	def testWebGetFileInfo(self):
		'''test REST api to get info for a single file'''

		surl = urllib.urlencode( {"path":self.testfile} )
		surl = "http://127.0.0.1:5001/get_file_info?" + surl

		logging.info( "testWebGetFileInfo: %s" % surl )

		ret = json.loads( urllib.urlopen(surl).readline() )
		self.assertTrue(ret['retcode'] == 0)
		
		logging.info( "testWebGetFileInfo: %s %s" % (ret['data']['size'], ret['data']['date']) )
		self.assertEqual(ret['data']['size'], self.testfile_size)
		self.assertEqual(ret['data']['date'], self.testfile_date)

		pass

if __name__ == "__main__":

	logging.basicConfig(level=logging.INFO)

	# run tests
	unittest.main()

