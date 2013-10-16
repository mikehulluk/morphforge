
srcs := $(wildcard *.py)
outputs := $(patsubst %.py,%.py.out,$(srcs))



all: $(outputs)

clean:
	rm -rf *.out output/

%.py.out: %.py
	export MREORG_CONFIG="BATCHRUN"; python $< > $@ 2>&1


