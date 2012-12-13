'''web app that exposes REST API endpoints'''

import json
import logging
from flask import Flask, render_template, request

import backend

app = Flask(__name__)

obackend = backend.Backend("kazapp.db")

@app.route('/get_file_list')
def get_file_list():

	lstfiles = obackend.get_file_list()
	ret = { "retcode" : 0, "data":  lstfiles  }
	return json.dumps( ret )
    #return render_template('get_file_list.html', name=name)

@app.route('/get_file_info')
def get_file_info():

	#TODO: error handling
	filepath = request.args.get('path', '')
	logging.info("serving file info for %s" % filepath )

	filedata = obackend.get_file_info(filepath)
	
	if filedata:
		ret = { "retcode" : 0, "data":  filedata.__dict__  }
	else:
		ret = { "retcode" : -1, "data":  {}  }

	return json.dumps( ret )

def start():

	obackend.open_db()
	app.run(port=5001)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)	
	start()

