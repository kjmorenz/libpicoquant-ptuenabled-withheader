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

#ifndef HEADER_H_
#define HEADER_H_

#include <stdio.h>
#include "picoquant.h"


// Enforce byte alignment to ensure cross-platform compatibility.
//#pragma pack(4)

// Define the common file header.
typedef struct {
	char Ident[16];
	char FormatVersion[6];
} pq_header_t;

typedef struct {
	char CreatorName[18];
	char CreatorVersion[12];
	char FileTime[18];
	//char CRLF[2];//seems to be unused for everyone, what does this even stand for?
	char Comment[256];
	int32_t NumberOfCurves;



	/* Note that Records is the only difference between interactive and 
	 * tttr main headers. Interactive calls this BitsPerHistogBin.
	 */

	 //booleans
	 unsigned int MeasDesc_StopOnOvfl;
	 unsigned int MeasDesc_Restart; 
	 unsigned int CurSWSetting_DispLog;
	 unsigned int CurSWSetting_DispCurve_Show0;
	 unsigned int CurSWSetting_DispCurve_Show1;
	 unsigned int CurSWSetting_DispCurve_Show2; 
	 unsigned int CurSWSetting_DispCurve_Show3; 
	 unsigned int CurSWSetting_DispCurve_Show4; 
	 unsigned int CurSWSetting_DispCurve_Show5;
	 unsigned int CurSWSetting_DispCurve_Show6;
	 unsigned int CurSWSetting_DispCurve_Show7;
	 unsigned int HW_ExternalRefClock;
	 unsigned int HWInpChan_Enabled0;
	 unsigned int HWInpChan_Enabled1;
	 unsigned int HWMarkers_RisingEdge0;
	 unsigned int HWMarkers_RisingEdge1;
	 unsigned int HWMarkers_RisingEdge2;
	 unsigned int HWMarkers_RisingEdge3;
	 unsigned int HWMarkers_Enabled0;
	 unsigned int HWMarkers_Enabled1;
	 unsigned int HWMarkers_Enabled2;
	 unsigned int HWMarkers_Enabled3;

	 //int8
	 int32_t Measurement_Mode;
	 int32_t Measurement_SubMode;
	 int32_t TTResult_StopReason;
	 int32_t TTResultFormat_TTTRRecType;
	 int32_t TTResultFormat_BitsPerRecord;
	 int32_t MeasDesc_BinningFactor;
	 int32_t MeasDesc_Offset;
	 int32_t MeasDesc_AcquisitionTime;
	 int32_t MeasDesc_StopAt;
	 int32_t CurSWSetting_DispAxisTimeFrom;
	 int32_t CurSWSetting_DispAxisTimeTo;
	 int32_t CurSWSetting_DispAxisCountFrom;
	 int32_t CurSWSetting_DispAxisCountTo;
	 int32_t CurSWSetting_DispCurves;
	 int32_t CurSWSetting_DispCurve_MapTo0;
	 int32_t CurSWSetting_DispCurve_MapTo1;
	 int32_t CurSWSetting_DispCurve_MapTo2;
	 int32_t CurSWSetting_DispCurve_MapTo3;
	 int32_t CurSWSetting_DispCurve_MapTo4;
	 int32_t CurSWSetting_DispCurve_MapTo5;
	 int32_t CurSWSetting_DispCurve_MapTo6;
	 int32_t CurSWSetting_DispCurve_MapTo7;
	 int32_t HW_Modules;
	 int32_t HWModule_TypeCode0;
	 int32_t HWModule_TypeCode1;
	 int32_t HWModule_TypeCode2;
	 int32_t HWModule_VersCode0;
	 int32_t HWModule_VersCode1;
	 int32_t HWModule_VersCode2;
	 int32_t HW_InpChannels;
	 int32_t HW_ExternalDevices;
	 int32_t HWSync_Divider;
	 int32_t HWSync_CFDLevel;
	 int32_t HWSync_CFDZeroCross;
	 int32_t HWSync_Offset;
	 int32_t HWInpChan_ModuleIdx0;
	 int32_t HWInpChan_ModuleIdx1;
	 int32_t HWInpChan_CFDLevel0;
	 int32_t HWInpChan_CFDLevel1;
	 int32_t HWInpChan_CFDZeroCross0;
	 int32_t HWInpChan_CFDZeroCross1;
	 int32_t HWInpChan_Offset0;
	 int32_t HWInpChan_Offset1;
	 int32_t HW_Markers;
	 int32_t HWMarkers_HoldOff;
	 int32_t TTResult_SyncRate;
	 int32_t TTResult_InputRate0;
	 int32_t TTResult_InputRate1;
	 int32_t TTResult_StopAfter;
	 int32_t TTResult_NumberOfRecords;

	 //Float8
	 float64_t HW_BaseResolution;
	 float64_t MeasDesc_Resolution;
	 float64_t MeasDesc_GlobalResolution; 

	 //AnsiStrings not in general part
	 char File_GUID[40];
	 char File_AssuredContent[32];
	 char CreatorSW_ContentVersion[4];
	 char HW_Type[15];
	 char HW_PartNo[8];
	 char HW_Version[5];
	 char HW_SerialNo[8];

/*
	int32_t BitsPerRecord;

	int32_t ActiveCurve;
	int32_t MeasurementMode;
	int32_t SubMode;
	int32_t Binning;
	float64_t Resolution;
	int32_t Offset;
	int32_t AcquisitionTime;
	int32_t StopAt;
	int32_t StopOnOvfl;
	int32_t Restart;
	int32_t DisplayLinLog;
	uint32_t DisplayTimeAxisFrom;
	uint32_t DisplayTimeAxisTo;
	uint32_t DisplayCountAxisFrom;
	uint32_t DisplayCountAxisTo;
	hh_v20_display_curve_t DisplayCurve[8];
	hh_v20_param_t Param[3];
	int32_t RepeatMode;
	int32_t RepeatsPerCurve;
	int32_t RepeatTime;
	int32_t RepeatWaitTime;
	char ScriptName[20];
	char HardwareIdent[16];
	char HardwarePartNo[8];
	int32_t HardwareSerial;
	int32_t NumberOfModules;
	hh_v20_module_t ModuleInfo[10];
	float64_t BaseResolution;
	int64_t InputsEnabled;
	int32_t InputChannelsPresent;
	int32_t RefClockSource;
	int32_t ExtDevices;
	int32_t MarkerSettings;
	int32_t SyncDivider;
	int32_t SyncCFDLevel;
	int32_t SyncCFDZeroCross;
	int32_t SyncOffset;

	//whats up with this??? Why only point?? *******************************************
	hh_v20_input_channel_t *InpChan;
	int32_t *InputRate;*/
} ptu_header_t;


int pq_header_read(FILE *in_stream, pq_header_t *pq_header);
void pq_header_printf(FILE *out_stream, pq_header_t *pq_header);
void pq_header_fwrite(FILE *out_stream, pq_header_t *pq_header);
void ptu_header_fwrite(FILE *stream_out, ptu_header_t *ptu_header);

#endif 
