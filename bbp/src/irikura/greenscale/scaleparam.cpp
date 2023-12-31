#include "greenscale.h"

#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <string>
#include <complex>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void init( FLT *mfault, FLT *sbfault )
{

//	sbfault->LengthElement  =    2000;            // [m] vffw·³LS
//	sbfault->WidthElement   =    2000;            // [m] vffwWS 
//	sbfault->Ds             =    0.1790366;                     // [m] ÅI·×èÊ Ds
//	sbfault->myu            =    3.2323 * pow( 10.0, 10.0 );   // ¹ñf«¦[N/square m]
//	sbfault->M0s            =    2.3148 * pow( 10.0, 16.0 );  // [Nm] [g}Oj`[hM0s
//	sbfault->Beta_s         =    3460;                        // [m/sec] n`dSg¬x
	sbfault->Alpha_p        =    6620;                        // [m/sec] n`dPg¬x
//	sbfault->Sigma_s        =     10.0 * pow( 10.0,  6.0 );    // ÍÊÐs(MPa) 
//  sbfault->vr             =    2500;                        // jó`d¬x(m/sec)
//  sbfault->fmax           =     6.0;    // fmax
//  sbfault->Qdepend1       =   110.0;    // Ql
//  sbfault->Qdepend2       =    0.69;    // QlÌügÏ»Ìæ
//  sbfault->Qdepend3       =    1.00;    // «Eüg
//	sbfault->Qdepend4       =   110.0;    // »Ì¼ÌQl
    sbfault->Qp             =   200.0;
//	sbfault->offsettime     =     0.0;    // jóJnÔÌItZbgÔ(sec)
	
	return;

}

void MakeFaultPara( FLT *subf )
{

	double pi;
	pi = atan( 1.0 ) * 4.0;

	subf->EqMoment = subf->myu * subf->LengthElement * subf->WidthElement * subf->Ds;
	subf->lamda = sqrt( subf->LengthElement * subf->WidthElement / pi );
	subf->omegaCs = 2.0 * subf->Beta_s * sqrt( (pi * subf->lamda * subf->Sigma_s) / subf->EqMoment );
    subf->AomegaCs = 2.0 * subf->Alpha_p * sqrt( (pi * subf->lamda * subf->Sigma_s) / subf->EqMoment );
	subf->omegaSpq = 2.0 * subf->Beta_s / subf->lamda;
	return;

}

std::complex<double> ScaleFactorS( double omega, 
							      double Qvalue,
							      double EDpq,
							      double EomegaDpq,
							      double Rpq,
							      double Rs,
							      double Sigmapq,
							      FLT mf, 
							      FLT subf)
{

	std::complex<double> fpq,tmp1,tmp2,tmp3,tmp4,tmp5;
	std::complex<double> tj(0.0,1.0);
	FLT sf;
	sf = subf;

	tmp1 = EDpq / sf.Ds;
    tmp2 = ( 1.0 + (tj * omega) / sf.omegaCs ) * ( 1.0 + (tj * omega) / sf.omegaCs);	
	tmp3 = ( 1.0 + (tj * omega) / EomegaDpq  ) * ( 1.0 + (tj * omega) / sf.omegaSpq );
	tmp4 = Rs / Rpq;
	tmp5 = exp( ( omega / ( 2.0 * Qvalue * sf.Beta_s ) ) * ( Rs - Rpq ) );
	fpq =  tmp1 * ( tmp2 / tmp3 ) * tmp4 * tmp5; //XP[t@N^[Fpq
	return fpq;

}

std::complex<double> ScaleFactorP( double omega, 
							      double Qvalue,
							      double EDpq,
							      double EomegaDpq,
							      double Rpq,
							      double Rs,
							      double Sigmapq,
							      FLT mf, 
							      FLT subf)
{

	std::complex<double> fpq,tmp1,tmp2,tmp3,tmp4,tmp5;
	std::complex<double> tj(0.0,1.0);
	FLT sf;
	sf = subf;

	tmp1 = EDpq / sf.Ds;
    tmp2 = ( 1.0 + (tj * omega) / sf.AomegaCs) * ( 1.0 + (tj * omega) / sf.AomegaCs);	
	tmp3 = ( 1.0 + (tj * omega) / EomegaDpq  ) * ( 1.0 + (tj * omega) / sf.omegaSpq );
	tmp4 = Rs / Rpq;
	tmp5 = exp( ( omega / ( 2.0 * Qvalue * sf.Alpha_p ) ) * ( Rs - Rpq ) );
	fpq =  tmp1 * ( tmp2 / tmp3 ) * tmp4 * tmp5; //XP[t@N^[Fpq

	return fpq;

}
