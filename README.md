kazapp
======

sample python/flask/sqlite app

== Release Notes

* Tested with the following configuration
python 2.66 on Ubuntu 10.10
celery 3.0 over rabbitmq
broker configured as in appconfig.py
* The traverse code ignores symlinks and will probably fail in the presence of hard links with cycles
* The tests assume presence of a populated /usr/share/locale and /usr/share/locale/all_languages

== Run the app and test suite

Configure broker in appconfig.py

1. Terminal 1: Start the workers
$python tasks.py worker -l info

2. Terminal 2:Start the web app with the root path to scan
$ python kazapp.py /usr/share/locale

where the argument is the full path to the root folder to traverse.
This kicks off the worker to populate the SQLite DB kazapp.db with file info, and starts the flask loop

3. Terminal 3:Run the tests 
$ python testall.py

Manually, you can test as:

$wget 127.0.0.1:5001/get_file_list -O t1
$wget 127.0.0.1:5001/get_file_info?path=/usr/share/locale/all_languages -O t2


== REST API Documentation

1. get_file_list

returns a list of files as a map in the format { "status" : "" , "data": [] }
status = success or scanning of error


2. get_file_info 

returns a dict of file metadata as a map in the format { "status" : "" , "data": { }  }
status = success or scanning of error
metadata has date, path, size

== TODO 

1. use batch inserts and commit after each batch 
2. the error handling is weak. 

