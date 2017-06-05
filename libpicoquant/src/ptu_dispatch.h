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

#include <stdio.h>
#include "picoquant.h"

#include  <windows.h>
#include  <ncurses.h>

#include  <stddef.h>
#include  <stdlib.h>
#include  <time.h>

// TagTypes  (TagHead.Typ)
#define tyEmpty8      0xFFFF0008
#define tyBool8       0x00000008
#define tyInt8        0x10000008
#define tyBitSet64    0x11000008
#define tyColor8      0x12000008
#define tyFloat8      0x20000008
#define tyTDateTime   0x21000008
#define tyFloat8Array 0x2001FFFF
#define tyAnsiString  0x4001FFFF
#define tyWideString  0x4002FFFF
#define tyBinaryBlob  0xFFFFFFFF

// RecordTypes
#define rtPicoHarpT3     0x00010303    // (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $03 (PicoHarp)
#define rtPicoHarpT2     0x00010203    // (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $03 (PicoHarp)
#define rtHydraHarpT3    0x00010304    // (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $04 (HydraHarp)
#define rtHydraHarpT2    0x00010204    // (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $04 (HydraHarp)
#define rtHydraHarp2T3   0x01010304    // (SubID = $01 ,RecFmt: $01) (V2), T-Mode: $03 (T3), HW: $04 (HydraHarp)
#define rtHydraHarp2T2   0x01010204    // (SubID = $01 ,RecFmt: $01) (V2), T-Mode: $02 (T2), HW: $04 (HydraHarp)
#define rtTimeHarp260NT3 0x00010305    // (SubID = $00 ,RecFmt: $01) (V2), T-Mode: $03 (T3), HW: $05 (TimeHarp260N)
#define rtTimeHarp260NT2 0x00010205    // (SubID = $00 ,RecFmt: $01) (V2), T-Mode: $02 (T2), HW: $05 (TimeHarp260N)
#define rtTimeHarp260PT3 0x00010306    // (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T3), HW: $06 (TimeHarp260P)
#define rtTimeHarp260PT2 0x00010206    // (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $06 (TimeHarp260P)

// some important Tag Idents (TagHead.Ident) that we will need to read the most common content of a PTU file
// check the output of this program and consult the tag dictionary if you need more
#define TTResultFormat_TTTRRecType "TTResultFormat_TTTRRecType"
#define TTResult_NumberOfRecords  "TTResult_NumberOfRecords"  // Number of TTTR Records in the File;
#define MeasDesc_Resolution         "MeasDesc_Resolution"       // Resolution for the Dtime (T3 Only)
#define MeasDesc_GlobalResolution     "MeasDesc_GlobalResolution" // Global Resolution of TimeTag(T2) /NSync (T3)
#define Header_End         "Header_End"                // Always appended as last tag (BLOCKEND)

// The rest of the Tag Idents: We do this so that if the name in the header given changes, you only 
// need to change it up here, not in the rest of the code
#define File_GUID "File_GUID" //tyAnsiString
#define File_AssuredContent "File_AssuredContent" //tyAnsiString
#define CreatorSW_ContentVersion "CreatorSW_ContentVersion" //tyAnsiString
#define CreatorSW_Name "CreatorSW_Name" //tyAnsiString 
#define CreatorSW_Version "CreatorSW_Version" //tyAnsiString
#define File_CreatingTime "File_CreatingTime" //tyTDateTime
#define File_Comment "File_Comment" //tyAnsiString
#define Measurement_Mode "Measurement_Mode" //tyInt8
#define Measurement_SubMode "Measurement_SubMode" //tyInt8
#define TTResult_StopReason "TTResult_StopReason" //tyInt8
#define Fast_Load_End "Fast_Load_End" //empty tag?

#define TTResultFormat_BitsPerRecord "TTResultFormat_BitsPerRecord" //tyInt8
#define MeasDesc_BinningFactor "MeasDesc_BinningFactor" //tyInt8
#define MeasDesc_Offset "MeasDesc_Offset" //tyInt8
#define MeasDesc_AcquisitionTime "MeasDesc_AcquisitionTime" //tyInt8
#define MeasDesc_StopAt "MeasDesc_StopAt" //tyInt8
#define MeasDesc_StopOnOvfl "MeasDesc_StopOnOvfl" //tyBool8
#define MeasDesc_Restart "MeasDesc_Restart" //tyBool8
#define CurSWSetting_DispLog "CurSWSetting_DispLog" //tyBool8
#define CurSWSetting_DispAxisTimeFrom "CurSWSetting_DispAxisTimeFrom" //tyInt8
#define CurSWSetting_DispAxisTimeTo "CurSWSetting_DispAxisTimeTo" //tyInt8
#define CurSWSetting_DispAxisCountFrom "CurSWSetting_DispAxisCountFrom" //tyInt8
#define CurSWSetting_DispAxisCountTo "CurSWSetting_DispAxisCountTo" //tyInt8
#define CurSWSetting_DispCurves "CurSWSetting_DispCurves" //tyInt8
#define CurSWSetting_DispCurve_MapTo0 "CurSWSetting_DispCurve_MapTo(0)" //tyInt8
#define CurSWSetting_DispCurve_Show0 "CurSWSetting_DispCurve_Show(0)" //tyBool8
#define CurSWSetting_DispCurve_MapTo1 "CurSWSetting_DispCurve_MapTo(1)" //tyInt8
#define CurSWSetting_DispCurve_Show1 "CurSWSetting_DispCurve_Show(1)" //tyBool8
#define CurSWSetting_DispCurve_MapTo2 "CurSWSetting_DispCurve_MapTo(2)" //tyInt8
#define CurSWSetting_DispCurve_Show2 "CurSWSetting_DispCurve_Show(2)" //tyBool8
#define CurSWSetting_DispCurve_MapTo3 "CurSWSetting_DispCurve_MapTo(3)" //tyInt8
#define CurSWSetting_DispCurve_Show3 "CurSWSetting_DispCurve_Show(3)" //tyBool8
#define CurSWSetting_DispCurve_MapTo4 "CurSWSetting_DispCurve_MapTo(4)" //tyInt8
#define CurSWSetting_DispCurve_Show4 "CurSWSetting_DispCurve_Show(4)" //tyBool8
#define CurSWSetting_DispCurve_MapTo5 "CurSWSetting_DispCurve_MapTo(5)" //tyInt8
#define CurSWSetting_DispCurve_Show5 "CurSWSetting_DispCurve_Show(5)" //tyBool8
#define CurSWSetting_DispCurve_MapTo6 "CurSWSetting_DispCurve_MapTo(6)" //tyInt8
#define CurSWSetting_DispCurve_Show6 "CurSWSetting_DispCurve_Show(6)" //tyBool8
#define CurSWSetting_DispCurve_MapTo7 "CurSWSetting_DispCurve_MapTo(7)" //tyInt8
#define CurSWSetting_DispCurve_Show7 "CurSWSetting_DispCurve_Show(7)" //tyBool8
#define HW_Type "HW_Type" //tyAnsiString
#define HW_PartNo "HW_PartNo" //tyAnsiString
#define HW_Version "HW_Version" //tyAnsiString
#define HW_SerialNo "HW_SerialNo" //tyAnsiString
#define HW_Modules "HW_Modules" //tyInt8
#define HWModule_TypeCode0 "HWModule_TypeCode(0)" //tyInt8
#define HWModule_VersCode0 "HWModule_VersCode(0)" //tyInt8
#define HWModule_TypeCode1 "HWModule_TypeCode(1)" //tyInt8
#define HWModule_VersCode1 "HWModule_VersCode(1)" //tyInt8
#define HWModule_TypeCode2 "HWModule_TypeCode(2)" //tyInt8
#define HWModule_VersCode2 "HWModule_VersCode(2)" //tyInt8
#define HW_BaseResolution "HW_BaseResolution" //tyFloat8
#define HW_InpChannels "HW_InpChannels" //tyInt8
#define HW_ExternalRefClock "HW_ExternalRefClock" //tyBool8
#define HW_ExternalDevices "HW_ExternalDevices" //tyInt8
#define HWSync_Divider "HWSync_Divider" //tyInt8
#define HWSync_CFDLevel "HWSync_CFDLevel" //tyInt8
#define HWSync_CFDZeroCross "HWSync_CFDZeroCross" //tyInt8
#define HWSync_Offset "HWSync_Offset" //tyInt8
#define HWInpChan_ModuleIdx0 "HWInpChan_ModuleIdx(0)" //tyInt8
#define HWInpChan_CFDLevel0 "HWInpChan_CFDLevel(0)" //tyInt8
#define HWInpChan_CFDZeroCross0 "HWInpChan_CFDZeroCross(0)" //tyInt8
#define HWInpChan_Offset0 "HWInpChan_Offset(0)" //tyInt8
#define HWInpChan_Enabled0 "HWInpChan_Enabled(0)" //tyBool8
#define HWInpChan_ModuleIdx1 "HWInpChan_ModuleIdx(1)" //tyInt8
#define HWInpChan_CFDLevel1 "HWInpChan_CFDLevel(1)" //tyInt8
#define HWInpChan_CFDZeroCross1 "HWInpChan_CFDZeroCross(1)" //tyInt8
#define HWInpChan_Offset1 "HWInpChan_Offset(1)" //tyInt8
#define HWInpChan_Enabled1 "HWInpChan_Enabled(1)" //tyBool8

#define HW_Markers "HW_Markers" //tyInt8
#define HWMarkers_RisingEdge0 "HWMarkers_RisingEdge(0)" //tyBool8
#define HWMarkers_RisingEdge1 "HWMarkers_RisingEdge(1)" //tyBool8
#define HWMarkers_RisingEdge2 "HWMarkers_RisingEdge(2)" //tyBool8
#define HWMarkers_RisingEdge3 "HWMarkers_RisingEdge(3)" //tyBool8
#define HWMarkers_Enabled0 "HWMarkers_Enabled(0)" //tyBool8
#define HWMarkers_Enabled1 "HWMarkers_Enabled(1)" //tyBool8
#define HWMarkers_Enabled2 "HWMarkers_Enabled(2)" //tyBool8
#define HWMarkers_Enabled3 "HWMarkers_Enabled(3)" //tyBool8
#define WMarkers_HoldOff "HWMarkers_HoldOff" //tyInt8

#define TTResult_SyncRate "TTResult_SyncRate" //tyInt8
#define TTResult_InputRate0 "TTResult_InputRate(0)" //tyInt8
#define TTResult_InputRate1 "TTResult_InputRate(1)" //tyInt8
#define TTResult_StopAfter "TTResult_StopAfter" //tyInt8

// A Tag entry
typedef struct {
  char Ident[32];     // Identifier of the tag
  int Idx;            // Index for multiple tags or -1
  unsigned int Typ;  // Type of tag ty..... see const section
    long long TagValue; // Value of tag.
} TagHead_t;

typedef struct {
	char CreatorName[18];
	char CreatorVersion[12];
	char FileTime[18];
	char CRLF[2];
	char Comment[256];
	int32_t NumberOfCurves;

	/* Note that Records is the only difference between interactive and 
	 * tttr main headers. Interactive calls this BitsPerHistogBin.
	 */

	 //booleans
	 MeasDesc_StopOnOvfl;
	 MeasDesc_Restart; 
	 CurSWSetting_DispLog;
	 CurSWSetting_DispCurve_Show0;
	 CurSWSetting_DispCurve_Show1;
	 CurSWSetting_DispCurve_Show2; 
	 CurSWSetting_DispCurve_Show3; 
	 CurSWSetting_DispCurve_Show4; 
	 CurSWSetting_DispCurve_Show5;
	 CurSWSetting_DispCurve_Show6;
	 CurSWSetting_DispCurve_Show7;
	 HW_ExternalRefClock;
	 HWInpChan_Enabled0;
	 HWInpChan_Enabled1;
	 HWMarkers_RisingEdge0;
	 HWMarkers_RisingEdge1;
	 HWMarkers_RisingEdge2;
	 HWMarkers_RisingEdge3;
	 HWMarkers_Enabled0;
	 HWMarkers_Enabled1;
	 HWMarkers_Enabled2;
	 HWMarkers_Enabled3;

	 //int8
	 Measurement_Mode;
	 Measurement_SubMode;
	 TTResult_StopReason;
	 TTResultFormat_TTTRRecType;
	 TTResultFormat_BitsPerRecord;
	 MeasDesc_BinningFactor;
	 MeasDesc_Offset;
	 MeasDesc_AcquisitionTime;
	 MeasDesc_StopAt;
	 CurSWSetting_DispAxisTimeFrom;
	 CurSWSetting_DispAxisTimeTo;
	 CurSWSetting_DispAxisCountFrom;
	 CurSWSetting_DispAxisCountTo;
	 CurSWSetting_DispCurves;
	 CurSWSetting_DispCurve_MapTo0;
	 CurSWSetting_DispCurve_MapTo1;
	 CurSWSetting_DispCurve_MapTo2;
	 CurSWSetting_DispCurve_MapTo3;
	 CurSWSetting_DispCurve_MapTo4;
	 CurSWSetting_DispCurve_MapTo5;
	 CurSWSetting_DispCurve_MapTo6;
	 CurSWSetting_DispCurve_MapTo7;
	 HW_Modules;
	 HWModule_TypeCode0;
	 HWModule_TypeCode1;
	 HWModule_TypeCode2;
	 HWModule_VersCode0;
	 HWModule_VersCode1;
	 HWModule_VersCode2;
	 HW_InpChannels;
	 HW_ExternalDevices;
	 HWSync_Divider;
	 HWSync_CFDLevel;
	 HWSync_CFDZeroCross;
	 HWSync_Offset;
	 HWInpChan_ModuleIdx0;
	 HWInpChan_ModuleIdx1;
	 HWInpChan_CFDLevel0;
	 HWInpChan_CFDLevel1;
	 HWInpChan_CFDZeroCross0;
	 HWInpChan_CFDZeroCross1;
	 HWInpChan_Offset0;
	 HWInpChan_Offset1;
	 HW_Markers;
	 HWMarkers_HoldOff;
	 TTResult_SyncRate;
	 TTResult_InputRate0;
	 TTResult_InputRate1;
	 TTResult_StopAfter;
	 TTResult_NumberOfRecords;

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
	hh_v20_input_channel_t *InpChan;
	int32_t *InputRate;
} ptu_header_t;

int ptu_dispatch(FILE *in_stream, FILE *out_stream, pq_header_t *pq_header,
		options_t *options);

time_t TDateTime_TimeT(double Convertee);

void tttr_init(ptu_header_t *ptu_header, tttr_t *tttr) ;

#endif
