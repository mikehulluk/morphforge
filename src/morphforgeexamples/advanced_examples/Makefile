
srcs := $(wildcard *.py)
outputs := $(patsubst %.py,%.py.out,$(srcs))



all: $(outputs)

clean:
	rm -rf *.out output/
	

%.py.out: %.py
	export MF_PLOT="OFF"; python $< > $@ 2>&1


