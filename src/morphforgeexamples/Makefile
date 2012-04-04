

.PHONY: examples morphologies singlecell multicell


examples: morphologies singlecell multicell


morphologies: 
	export MF_PLOT="OFF"
	python morphology/morphology010.py > out1.txt
	python morphology/morphology020.py > out2.txt
	python morphology/morphology030.py > out3.txt
	python morphology/morphology040.py > out4.txt
	python morphology/morphology050.py > out5.txt
	python morphology/morphology060.py > out6.txt
	python morphology/morphology070.py > out7.txt
	python morphology/morphology080.py > out8.txt

singlecell: 
	export MF_PLOT="OFF"
	python singlecell_simulation/singlecell_simulation010.py > out1.txt
	python singlecell_simulation/singlecell_simulation020.py > out1.txt
	python singlecell_simulation/singlecell_simulation030.py > out1.txt
	python singlecell_simulation/singlecell_simulation040.py > out1.txt
	python singlecell_simulation/singlecell_simulation050.py > out1.txt
	python singlecell_simulation/singlecell_simulation060.py > out1.txt
	python singlecell_simulation/singlecell_simulation070.py > out1.txt
	python singlecell_simulation/singlecell_simulation080.py > out1.txt
	python singlecell_simulation/singlecell_simulation090.py > out1.txt
	python singlecell_simulation/singlecell_simulation100.py > out1.txt
	python singlecell_simulation/singlecell_simulation110.py > out1.txt
	python singlecell_simulation/singlecell_simulation120.py > out1.txt

multicell: 
	export MF_PLOT="OFF"
	python multicell_simulation/multicell_simulation010.py > out1.txt
	python multicell_simulation/multicell_simulation020.py > out2.txt
	python multicell_simulation/multicell_simulation030.py > out3.txt


clean:
	rm out*.txt
