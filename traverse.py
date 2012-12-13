import logging
import os, os.path
import sys

import backend

# iterative breadth first search of root folder

g_lstfiles = []


#TODO: error handle for "permission denied"
#TODO: handle cycles due to hard links
def traverse(rootpath, dbname):

	global g_lstfiles

	queue = []
	queue.append(rootpath)

	numfiles = 0 
	numdirs = 1

	obackend = backend.Backend(dbname)
	obackend.create_db()

	while len( queue ) > 0:

		toppath = queue.pop()

		# hand off the listdir to celery workers

		try:
			files = os.listdir( toppath )
		except:
			logging.warning("ignoring %s, cannot access " % toppath)
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
				logging.debug(sfilepath)
				numfiles += 1
			# handle dir
			elif ( os.path.isdir( sfilepath ) ):
				queue.append( sfilepath )
				numdirs += 1 

	logging.info("traversed %s files and %s directories" % ( numfiles, numdirs ) )

	obackend.close_db()

if __name__ == "__main__":

	logging.basicConfig(level=logging.DEBUG)

	if ( len(sys.argv) < 2 ):
		logging.error( "usage : %s rootfolder" % sys.argv[0] )
		sys.exit(1)

	rootpath = sys.argv[1]

	logging.info("traversing from root path %s" % rootpath)

	traverse(rootpath, "kazapp.db")

