.PHONY  : run runclient runserver venv

PEMKEY  = key.pem
TESTURL = 'http://127.0.0.1:8080/dynenc/helloworld'

run runserver: | $(PEMKEY) venv
	venv/bin/python server.py $(PEMKEY)

runclient: | $(PEMKEY) venv
	venv/bin/python client.py $(TESTURL) $(PEMKEY)

$(PEMKEY):
	@ python -c 'from Crypto.PublicKey import RSA; print RSA.generate(1024).exportKey()' | tee $@

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
