

all: morphology assorted multicell_simulation singlecell_simulation advanced_examples
clean: morphology_clean assorted_clean multicell_simulation_clean singlecell_simulation_clean advanced_examples_clean


.PHONY: force_look
	
# Builing all the examples
###########################

morphology: force_look
	$(MAKE) -C morphology/ 

assorted: force_look
	#$(MAKE) -C assorted/ 

multicell_simulation: force_look
	$(MAKE) -C multicell_simulation/ 

singlecell_simulation: force_look
	$(MAKE) -C singlecell_simulation/ 

advanced_examples: force_look
	$(MAKE) -C advanced_examples/ 



# Cleaning:
############

morphology_clean: force_look
	$(MAKE) -C morphology/ clean	
	
assorted_clean: force_look
	$(MAKE) -C assorted/ clean
	
multicell_simulation_clean: force_look
	$(MAKE) -C multicell_simulation/ clean
	
singlecell_simulation_clean: force_look
	$(MAKE) -C singlecell_simulation/ clean
	
advanced_examples_clean: force_look
	$(MAKE) -C advanced_examples/ clean
	
	

	
