


.PHONY: clean test doc examples force_look env env_NEURON_GSL

all: 



# Some things that need to be built for the environment:
env: env_NEURON_GSL

env_NEURON_GSL: force_look
	$(MAKE) -C src/morphforgecontrib/simulation/neuron_gsl/cpp/


lint: force_look
	pylint  --output-format=html --include-ids=y --disable='C0301,C0111,W0142,R0904,R0903,C0103,W0404,R0914,R0902,R0913'  --max-args=7 src/morphforge/ > pylint_out.html
	#pylint -E --output-format=html --include-ids=y --disable='C0301,C0111,W0142,R0904,R0903,C0103,W0404,R0914,R0902,R0913'  --max-args=7 src/morphforgecontrib/ > pylint_out.html
	# C0301 - long lines
	# C0111 - 
	# W0142 'Used * or ** magic'
	# R0903/4 are too many or too few methods in class
	# C0103
	# W0404 - Reimports
	# R0914 - Too many local variables:
	# R0902 - Too many instance attributes
	# R0913 - Too many arguments


examples:
	$(MAKE) -C src/morphforgeexamples/

doc: force_look
	python ./devscripts/MF_create_example_docs.py
	$(MAKE) -C doc/ all

clean:
	$(MAKE) -C src/morphforgeexamples/ clean
	$(MAKE) -C doc/ clean
	$(MAKE) -C src/morphforgecontrib/simulation/neuron_gsl/cpp clean
	find . -name "*.pyc" -exec rm {} \;
	find . -name "*.swp" -exec rm {} \;
	find . -name "*.swo" -exec rm {} \;
	find . -name "*~" -exec rm {} \;
	find . -name "*.bak" -exec rm {} \;
	find . -name "*.new" -exec rm {} \;
	find . -name "parser.out" -exec rm {} \;
	rm -rf dist/



test:
	rm -rf build/
	mkdir build
	nosetests  --with-xunit --xunit-file=build/xunit_out.xml --with-coverage --cover-package=morphforge --cover-erase --cover-tests  --cover-html --cover-html-dir=build/coveragehtml/ src/morphforgetest/morphforge/unittests/morphology/core/*.py
