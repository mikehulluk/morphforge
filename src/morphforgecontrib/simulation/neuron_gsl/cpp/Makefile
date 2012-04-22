
libgslwrapper.so.1.0.1: gsl_wrapper.o
	gcc -shared -Wl,-soname,libgslwrapper.so.1 -o libgslwrapper.so.1.0.1  gsl_wrapper.o
	rm -rf libgslwrapper.so libgslwrapper.so.1
	ln -s libgslwrapper.so.1.0.1 libgslwrapper.so
	ln -s libgslwrapper.so.1.0.1 libgslwrapper.so.1


gsl_wrapper.o: gsl_wrapper.c gsl_wrapper.h
	gcc -c -fPIC gsl_wrapper.c -o gsl_wrapper.o
