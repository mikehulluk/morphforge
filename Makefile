


.PHONY: clean test doc examples force_look

all:

examples:
	$(MAKE) -C src/morphforgeexamples/

doc: force_look
	python ./devscripts/MF_create_example_docs.py
	$(MAKE) -C doc/	all

clean:
	$(MAKE) -C src/morphforgeexamples/ clean
	$(MAKE) -C doc/	clean
	find . -name "*.pyc" -exec rm {} \;
	find . -name "*.bak" -exec rm {} \;
	find . -name "parser.out" -exec rm {} \;



test:
	rm -rf build/
	mkdir build
	nosetests  --with-xunit --xunit-file=build/xunit_out.xml --with-coverage --cover-package=morphforge --cover-erase --cover-tests  --cover-html --cover-html-dir=build/coveragehtml/ src/morphforgetest/morphforge/unittests/morphology/core/*.py
