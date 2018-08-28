help:
	cat Makefile

init:
	pip install -r requirements.txt
	pip install nosetests Twine pypinfo

pypinfo:
	pypinfo pymtst 

test:
	nosetests tests

clean:
	python setup.py clean
	rm -r pymtst.egg-info build

sdist:
	python setup.py sdist

pypi:
	twine upload dist/*.tar.gz -r pypi --skip-existing
testpypi:
	twine upload dist/*.tar.gz -r testpypi --skip-existing

