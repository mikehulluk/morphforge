
srcs := $(wildcard *.py)
outputs := $(patsubst Figure%.py,Figure%.py.out,$(srcs))



all: $(outputs)

clean:
	rm -rf *.out _output/*
	

%.py.out: %.py
	export MF_PLOT="OFF"; python $< > $@ 2>&1


