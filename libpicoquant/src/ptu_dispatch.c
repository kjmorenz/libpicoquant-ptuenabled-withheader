/*
 * Copyright (c) 2011-2014, Thomas Bischof
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without 
 * modification, are permitted provided that the following conditions are met:
 * 
 * 1. Redistributions of source code must retain the above copyright notice, 
 *    this list of conditions and the following disclaimer.
 * 
 * 2. Redistributions in binary form must reproduce the above copyright notice, 
 *    this list of conditions and the following disclaimer in the documentation 
 *    and/or other materials provided with the distribution.
 * 
 * 3. Neither the name of the Massachusetts Institute of Technology nor the 
 *    names of its contributors may be used to endorse or promote products 
 *    derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <string.h>

#include "hydraharp.h"

#include "hydraharp/hh_v20.h"

//for when eventually we can also handle ptu from other hardware
#include "hydraharp/hh_v10.h"

#include "picoharp.h"
#include "picoharp/ph_v20.h"

#include "timeharp.h"
#include "timeharp/th_v20.h"
#include "timeharp/th_v30.h"
#include "timeharp/th_v50.h"
#include "timeharp/th_v60.h"

#include "error.h"


//from ptu demo:
#include  <windows.h>
#include  <ncurses.h>
#include  <stdio.h>

#include  <stddef.h>
#include  <stdlib.h>
#include  <time.h>


bool IsT2;
long long RecNum;
long long oflcorrection;
long long truensync, truetime;
int m, c;
double GlobRes = 0.0;
double Resolution = 0.0;
unsigned int dlen = 0;
unsigned int cnt_0=0, cnt_1=0;

/*void tttr_init(ptu_header_t *ptu_header, tttr_t *tttr) {
	tttr->sync_channel = ptu_header->InputChannelsPresent;
	tttr->origin = 0;
	tttr->overflows = 0;
  if isT2{
	  tttr->overflow_increment = HH_T2_OVERFLOW;
    tttr->resolution_float = HH_BASE_RESOLUTION;
  } else {
    tttr->overflow_increment = HH_T3_OVERFLOW;
    tttr->resolution_float = ptu_header->Resolution*1e-12;
  }//NOW THIS ONLY WORKS FOR HH
	tttr->sync_rate = tttr_header->SyncRate;
	
	tttr->resolution_int = floor(fabs(tttr->resolution_float*1e12));
}*/

// TDateTime (in file) to time_t (standard C) conversion



time_t TDateTime_TimeT(double Convertee){
    const int EpochDiff = 25569; // days between 30/12/1899 and 01/01/1970
    const int SecsInDay = 86400; // number of seconds in a day
    time_t Result; 
    Result = ((long)(((Convertee) - EpochDiff) * SecsInDay));
    return Result;
}


int ptu_dispatch(FILE *in_stream, FILE *out_stream, pq_header_t *pq_header, 
		options_t *options) {
	  int result;
    //reparse header as a ptu file
    ptu_header_t ptu_header;

    result = ptu_header_read(stream_in, &ptu_header)
    if ( result ) {
		  error("Could not read string header.\n");
    }
    //find hardware
    isT2 = get_recordtype(ptu_header->TTResultFormat_TTTRRecType);//need to define header, record type
    
    pq_header->FormatVersion = ptu_header.FormatVersion;
    
    //read it!
    if ( isT2 == NULL ) {
		  error("Board is not supported in ptu format: %s.\n", pq_header->Ident, pq_header->FormatVersion, ftell);
    } else if ( options->print_header ) {
			if ( options->binary_out ) {
				ptu_header_fwrite(stream_out, ptu_header);
			} else {
				pq_header_printf(stream_out, pq_header);
			}
	  } else if ( options->print_mode ) {
			if ( ptu_header->Measurement_Mode == HH_MODE_INTERACTIVE ) {
				fprintf(stream_out, "interactive\n");
			} else if ( ptu_header->Measurement_Mode == HH_MODE_T2 ) {
				fprintf(stream_out, "t2\n");
			} else if ( ptu_header->Measurement_Mode == HH_MODE_T3 ) {
				fprintf(stream_out, "t3\n");
			} else {
				error("Measurement mode not recognized: %"PRId32".\n",
						ptu_header->Measurement_Mode);
				return(PQ_ERROR_MODE);
			}
	  } else if ( isT2) { 
		  result = ptu_hh_V20_t2_stream(*in_stream, *out_stream, *ptu_header, *options);
	  } else {
      result = ptu_hh_V20_t3_stream(*in_stream, *out_stream, *ptu_header, *options);
    }                                     

	return(result);
}


int get_recordtype(int32_t RecordType){ //only hydraharp gives correct version
    // TTTR Record type
  switch (RecordType)
  {
    case rtHydraHarp2T2:
      return true;//DOES THIS WORK?
      //return ptu_hh_v20_t2_stream(FILE *stream_in, FILE *stream_out,
      // ptu_header_t *ptu_header, options_t *options) 
      //fprintf(fpout, "HydraHarp V2 T2 data\n");
      //fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      break;
    case rtHydraHarp2T3:
      return false;//DOES THIS WORK?
      //return ptu_hh_v20_t3_stream(FILE *stream_in, FILE *stream_out,
      // ptu_header_t *ptu_header, options_t *options)
      //fprintf(fpout, "HydraHarp V2 T3 data\n");
      //fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      break;
    
    //need to add errors

    /*
    
    //none of the rest of these are set up, only hydraharp
    case rtPicoHarpT2:
      fprintf(fpout, "PicoHarp T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      return(ph_dispatch);
      break;
    case rtPicoHarpT3:
      fprintf(fpout, "PicoHarp T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      return(ph_dispatch);
      break;
    case rtHydraHarpT2:
      fprintf(fpout, "HydraHarp V1 T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      return(hh_dispatch);
      break;
    case rtHydraHarpT3:
      fprintf(fpout, "HydraHarp V1 T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      return(hh_dispatch);
      break;
	case rtTimeHarp260NT3:
      fprintf(fpout, "TimeHarp260N T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      return(th_dispatch);
      break;
	case rtTimeHarp260NT2:
      fprintf(fpout, "TimeHarp260N T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      return(th_dispatch);
      break;
    case rtTimeHarp260PT3:
      fprintf(fpout, "TimeHarp260P T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      return(th_dispatch);
      break;
	case rtTimeHarp260PT2:
      fprintf(fpout, "TimeHarp260P T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      return(th_dispatch);
      break;*/
  default:
    error("Unknown record type: 0x%X\n 0x%X\n ", RecordType);
    return NULL;
  }
  
}
