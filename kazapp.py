'''web app that exposes REST API endpoints'''

import json
import logging, sys
from flask import Flask, request
import backend
from tasks import traverse
from celery.result import AsyncResult

app = Flask(__name__)
obackend = backend.Backend("kazapp.db")

g_taskid = None

#TODO: bettererror handling
#TODO: return task completion percent if in scanning state

@app.route('/get_file_list')
def get_file_list():

	global g_taskid
	ar = AsyncResult(g_taskid)
	if ( not ar.ready() ):
		ret = { "status" : "scanning", "data":  [] }
		return json.dumps(ret)

	lstfiles = obackend.get_file_list()
	ret = { "status" : "success", "data":  lstfiles  }
	return json.dumps( ret )
    #return render_template('get_file_list.html', name=name)

@app.route('/get_file_info')
def get_file_info():

	global g_taskid
	ar = AsyncResult(g_taskid)
	if ( not ar.ready() ):
		ret = { "status" : "scanning", "data":  [] }
		return json.dumps(ret)

	filepath = request.args.get('path', '')
	logging.info("serving file info for %s" % filepath )

	filedata = obackend.get_file_info(filepath)

	if filedata:
		ret = { "status" : "success", "data":  filedata.__dict__  }
	else:
		ret = { "status" : "error", "data":  {} }

	return json.dumps(ret)

if __name__ == '__main__':

	logging.basicConfig(level=logging.INFO)

	if (len(sys.argv) < 2 ):
		logging.error("usage: %s rootpath" % sys.argv[0] )
		sys.exit(1)
		
	rootpath = sys.argv[1]

	obackend.open_db()

	# kick off scanning tasks
	res = traverse.delay(rootpath, "kazapp.db")
	g_taskid = res.task_id
	logging.info("traverse running on %s" % g_taskid)

	# run webservice
	app.run(port=5001)

