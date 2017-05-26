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
#include "hydraharp/hh_v10.h"
#include "hydraharp/hh_v20.h"

//for when eventually we can also handle ptu from other hardware
#include "picoharp.h"

#include "picoharp/ph_v20.h"

#include "timeharp.h"
#include "timeharp/th_v20.h"
#include "timeharp/th_v30.h"
#include "timeharp/th_v50.h"
#include "timeharp/th_v60.h"

#include "error.h"

FILE *fpin,*fpout;
bool IsT2;
long long RecNum;
long long oflcorrection;
long long truensync, truetime;
int m, c;
double GlobRes = 0.0;
double Resolution = 0.0;
unsigned int dlen = 0;
unsigned int cnt_0=0, cnt_1=0;

void tttr_init(ptu_header_t *ptu_header, tttr_t *tttr) {
	tttr->sync_channel = ptu_header->InputChannelsPresent;
	tttr->origin = 0;
	tttr->overflows = 0;
	tttr->overflow_increment = HH_T2_OVERFLOW;//NOW THIS ONLY WORKS FOR HH
	tttr->sync_rate = tttr_header->SyncRate;
	tttr->resolution_float = HH_BASE_RESOLUTION;
	tttr->resolution_int = floor(fabs(tttr->resolution_float*1e12));
}

int ptu_dispatch(FILE *in_stream, FILE *out_stream, pq_header_t *pq_header, 
		options_t *options) {
	int result;
//reparse header as a ptu file
    ptu_header = ptu_header_parse(in_stream, out_stream)//check that this is how you should send these

    //find hardware
    decode = get_recordtype(ptu_header->RecordType)//need to define header, record type
    pq_header.FormatVersion = ptu_header.FormatVersion
    
    //read it!
    if ( decode == NULL ) {
		error("Could not identify board %s.\n", pq_header.Ident, pq_header.FormatVersion, ftell);
    } else if ( isT2) { //need to define isT2?
        tttr_t tttr;//only for t2?
        tttr = tttr_init(ptu_header, &tttr);
		result = pq_t2_stream(in_stream, out_stream, decode, tttr, options)
	} else {
        result = pq_t3_stream(in_stream, out_stream, decode, tttr, options)//also needs fixing
    }                                     

	return(result);
}

ptu_header_t ptu_header_parse(FILE *in_stream, File *out_stream){
  ptu_header_t ptu_header
  char Magic[8];
  char Version[8];
  char Buffer[40];
  char* AnsiBuffer;
  WCHAR* WideBuffer;
  int Result;

  long long NumRecords = -1;
  long long RecordType = 0;

  TagHead_t TagHead;
  fseek(in_stream, sizeof(Magic)+sizeof(Version), SEEK_SET)//make sure we start at the right place
  // read tagged header
  do
  {
    // This loop is very generic. It reads all header items and displays the identifier and the
    // associated value, quite independent of what they mean in detail.
    // Only some selected items are explicitly retrieved and kept in memory because they are 
    // needed to subsequently interpret the TTTR record data.

    Result = fread( &TagHead, 1, sizeof(TagHead) ,fpin);
    if (Result!= sizeof(TagHead))
    {
        error("Incomplete file in header of ptu")
    }

    strcpy(Buffer, TagHead.Ident);
    if (TagHead.Idx > -1)
    {
      sprintf(Buffer, "%s(%d)", TagHead.Ident,TagHead.Idx);//puts formatted output into buffer
    }
    fprintf(fpout, "\n%-40s", Buffer);
    switch (TagHead.Typ)
    {
      case tyEmpty8:
        fprintf(fpout, "<empty Tag>");
        break;
      case tyBool8:
        fprintf(fpout, "%s", bool(TagHead.TagValue)?"True":"False");
        fprintf(fpout, "  tyBool8");
        break;
      case tyInt8:
        fprintf(fpout, "%lld", TagHead.TagValue);
        fprintf(fpout, "  tyInt8");
        // get some Values we need to analyse records
        if (strcmp(TagHead.Ident, TTTRTagNumRecords)==0) // Number of records
          NumRecords = TagHead.TagValue;
        if (strcmp(TagHead.Ident, TTTRTagTTTRRecType)==0) // TTTR RecordType
          RecordType = TagHead.TagValue;
        break;
      case tyBitSet64:
        fprintf(fpout, "0x%16.16X", TagHead.TagValue);
        fprintf(fpout, "  tyBitSet64");
        break;
      case tyColor8:
        fprintf(fpout, "0x%16.16X", TagHead.TagValue);
        fprintf(fpout, "  tyColor8");
        break;
      case tyFloat8:
        fprintf(fpout, "%E", *(double*)&(TagHead.TagValue));
        fprintf(fpout, "  tyFloat8");
        if (strcmp(TagHead.Ident, TTTRTagRes)==0) // Resolution for TCSPC-Decay
          Resolution = *(double*)&(TagHead.TagValue);
        if (strcmp(TagHead.Ident, TTTRTagGlobRes)==0) // Global resolution for timetag
          GlobRes = *(double*)&(TagHead.TagValue); // in ns
        break;
      case tyFloat8Array:
        fprintf(fpout, "<Float Array with %d Entries>", TagHead.TagValue / sizeof(double));
        fprintf(fpout, "  tyFloat8Array");
        // only seek the Data, if one needs the data, it can be loaded here
        fseek(fpin, (long)TagHead.TagValue, SEEK_CUR);
        break;
      case tyTDateTime:
        time_t CreateTime;
        CreateTime = TDateTime_TimeT(*((double*)&(TagHead.TagValue)));
        fprintf(fpout, "%s", asctime(gmtime(&CreateTime)), "\0");
        fprintf(fpout, "  tyTDateTime");
        break;
      case tyAnsiString:
        AnsiBuffer = (char*)calloc((size_t)TagHead.TagValue,1);
        Result = fread(AnsiBuffer, 1, (size_t)TagHead.TagValue, fpin);
        if (Result!= TagHead.TagValue){
          printf("\nIncomplete File.");
          free(AnsiBuffer);
          goto close;
        }
        fprintf(fpout, "%s", AnsiBuffer);
        fprintf(fpout, "  tyAnsiString");
        free(AnsiBuffer);
        break;
      case tyWideString:
        WideBuffer = (WCHAR*)calloc((size_t)TagHead.TagValue,1);
        Result = fread(WideBuffer, 1, (size_t)TagHead.TagValue, fpin);
        if (Result!= TagHead.TagValue){
          printf("\nIncomplete File.");
          free(WideBuffer);
          goto close;
        }
        //fwprintf(fpout, L"%s", WideBuffer);
        fprintf(fpout, "  tyWideString");
        free(WideBuffer);
        break;
      case tyBinaryBlob:
        fprintf(fpout, "<Binary Blob contains %d Bytes>", TagHead.TagValue);
        fprintf(fpout, "  tyBinaryBlob");
        // only seek the Data, if one needs the data, it can be loaded here
        fseek(fpin, (long)TagHead.TagValue, SEEK_CUR);
        break;
      default:
        printf("Illegal Type identifier found! Broken file?");
        goto close;
    }
  }
  while((strncmp(TagHead.Ident, FileTagEnd, sizeof(FileTagEnd))));

  return ptu_header
// End Header loading
}

pq_dispatch_t get_recordtype(long long RecordType){ //only hydraharp gives correct version
    // TTTR Record type
  switch (RecordType)
  {
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
    case rtHydraHarp2T2:
      fprintf(fpout, "HydraHarp V2 T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      return(hh_v20_tttr_stream);
      break;
    case rtHydraHarp2T3:
      fprintf(fpout, "HydraHarp V2 T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      return(hh_v20_tttr_stream);
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
      break;
  default:
    fprintf(fpout, "Unknown record type: 0x%X\n 0x%X\n ", RecordType);
    return NULL;
  }
  
}
