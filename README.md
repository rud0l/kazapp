kazapp
======

sample python/flask/sqlite app

== Release Notes

* Tested with the following configuration
python 2.66 on Ubuntu 10.10
celery 3.0 over rabbitmq
* The traverse code ignores symlinks and will probably fail in the presence of hard links with cycles
* The tests assume presence of a populated /usr/share/locale and /usr/share/locale/all_languages

== Run the app

1. Populate DB 

$python traverse.py [rootfolder]

where rootfolder is the full path to the root folder to traverse.
This populates the SQLite DB kazapp.db with file info. 

2. Query the web app

$python kazapp.py

$wget 127.0.0.1:5001/get_all_files

$wget 127.0.0.1:5001/get_file_info?path=path/to/file

== Run the tests

3. Run the test suite

$python testall.py

(ensure the web app kazapp.py is running first)

== REST API Documentation

== File layout

