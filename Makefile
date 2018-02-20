.PHONY: clear build test pypi

clear:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	find . -name "*pycache*" | xargs rm -rf

build:
	python setup.py install

test:
	python -m unittest -v somecommand/tests/*.py

pypi:
	python setup.py register
	python setup.py sdist bdist bdist_egg upload
