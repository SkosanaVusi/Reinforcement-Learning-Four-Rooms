install: venv
	. venv/bin/activate;pip install -Ur requirements.txt
venv:
	test -d venv || virtualenv -p python3 venv
run1:
	. venv/bin/activate;python3 Scenario1.py
run2:
	. venv/bin/activate;python3 Scenario2.py
run3:
	. venv/bin/activate;python3 Scenario3.py 
run4:
	. venv/bin/activate;python3 Scenario4.py –stochastic

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
