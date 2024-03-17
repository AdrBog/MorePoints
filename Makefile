setup:
	python -m venv venv
	venv/bin/pip install flask flask-cors paramiko pyftpdlib pyopenssl pdoc webdavclient3 
	echo "Everything ready: run 'make run' or 'make debug'"

run:
	venv/bin/python3 -m flask run -p 5002

debug:
	venv/bin/python3 -m flask run --debug -p 5002

doc:
	pdoc app.py utils
