


.PHONY: clean test doc examples force_look env env_NEURON_GSL

all: 



# Some things that need to be built for the environment:
env: env_NEURON_GSL

env_NEURON_GSL: force_look
	$(MAKE) -C src/morphforgecontrib/simulation/neuron_gsl/cpp/




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
	find . -name "*.bak" -exec rm {} \;
	find . -name "parser.out" -exec rm {} \;
	rm -rf dist/



test:
	rm -rf build/
	mkdir build
	nosetests  --with-xunit --xunit-file=build/xunit_out.xml --with-coverage --cover-package=morphforge --cover-erase --cover-tests  --cover-html --cover-html-dir=build/coveragehtml/ src/morphforgetest/morphforge/unittests/morphology/core/*.py
