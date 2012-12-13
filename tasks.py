'''iterative breadth first search of root folder'''

import logging
import os, os.path
import sys
from celery import Celery
from appconfig import BROKER
from celery.utils.log import get_task_logger
import backend


#TODO: handle cycles due to hard links

celery = Celery('tasks', backend='amqp', broker=BROKER)
logger = get_task_logger(__name__)


@celery.task()
def traverse(rootpath, dbname):

	queue = []
	queue.append(rootpath)

	numfiles = 0 
	numdirs = 1

	obackend = backend.Backend(dbname)
	obackend.create_db()

	while len( queue ) > 0:

		toppath = queue.pop()

		try:
			files = os.listdir( toppath )
		except:
			logger.warning("ignoring %s, cannot access " % toppath)
			continue

		# add dirs to queue, write files to output
		for afile in files:
			sfilepath = os.path.join(toppath, afile)
			# handle file
			if ( os.path.islink( sfilepath ) ):
				continue
			elif ( os.path.isfile( sfilepath ) ):
				fsize = os.path.getsize(sfilepath)
				fmtime = os.path.getmtime(sfilepath)
				filedata = backend.FileInfo(sfilepath, fsize, fmtime)
				obackend.write_file_data(filedata)
				logger.debug(sfilepath)
				numfiles += 1
			# handle dir
			elif ( os.path.isdir( sfilepath ) ):
				queue.append( sfilepath )
				numdirs += 1 

	logger.info("traversed %s files and %s directories" % ( numfiles, numdirs ) )

	obackend.close_db()

if __name__ == '__main__':

	celery.start()

