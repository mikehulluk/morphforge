#if!defined __GSL_HEADER_H__
#define __GSL_HEADER_H__

int hello();
float MyInf();


//typedef struct IntWrapper;
void* makeIntWrapper(double* x, double* y, int nPts);
double interpolate2(  double x0, void*  );


#endif
