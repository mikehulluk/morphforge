

#include <gsl/gsl_interp.h>
#include "gsl_wrapper.h"

typedef struct tag_IntWrapper
{
    gsl_interp* pInterpolator;
    gsl_interp_accel *acc;

    double* pX;
    double* pY;
    int nPts;
} IntWrapper;

void* makeIntWrapper( double* x, double* y, int nPts)
{
    IntWrapper* pNewWrapper = (IntWrapper*) malloc( sizeof(IntWrapper));

    pNewWrapper->pInterpolator = gsl_interp_alloc (gsl_interp_linear, nPts );
    gsl_interp_init(pNewWrapper->pInterpolator, x,y, nPts );
    pNewWrapper->acc = gsl_interp_accel_alloc ();

    //Copy the data:
    pNewWrapper->pX = (double*) malloc( sizeof(double) * nPts);
    pNewWrapper->pY = (double*) malloc( sizeof(double) * nPts);
    int i;
    for(i=0;i< nPts;i++)
    {
        pNewWrapper->pX[i] = x[i];
        pNewWrapper->pY[i] = y[i];
    }
    pNewWrapper->nPts = nPts;

    return pNewWrapper;
}

double interpolate2( double x0, void * pInterpolator)
{
     //printf("%lf\n",x0);
    IntWrapper* pInt = (IntWrapper*) pInterpolator;

    if(x0 <= pInt->pX[0])
        return pInt->pY[0];
    if(x0 >= pInt->pX[pInt->nPts-1])
        return pInt->pY[pInt->nPts-1];
    return gsl_interp_eval ( pInt->pInterpolator, pInt->pX, pInt->pY, x0, pInt->acc);
}


int hello()
{
    return 0;
}

float MyInf()
{
    return 0.5;
}





