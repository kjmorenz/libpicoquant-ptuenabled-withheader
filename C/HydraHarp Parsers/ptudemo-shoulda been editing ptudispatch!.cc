/************************************************************************

  PicoQuant Unified TTTR (PTU)    File Access Demo in C/C++

  This is demo code. Use at your own risk. No warranties.

  Tested with MS Visual Studio 2010 and Mingw 4.5

  Marcus Sackrow, PicoQuant GmbH, December 2013
  Michael Wahl, PicoQuant GmbH, revised July 2014


************************************************************************/

#include  <windows.h>
#include  <ncurses.h>
#include  <stdio.h>

#include  <stddef.h>
#include  <stdlib.h>
#include  <time.h>

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

// TagTypes  (TTagHead.Typ)
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

#pragma pack(8) //structure alignment to 8 byte boundaries

// A Tag entry
struct TgHd{
  char Ident[32];     // Identifier of the tag
  int Idx;            // Index for multiple tags or -1
  unsigned int Typ;  // Type of tag ty..... see const section
    long long TagValue; // Value of tag.
} TagHead;


// TDateTime (in file) to time_t (standard C) conversion

const int EpochDiff = 25569; // days between 30/12/1899 and 01/01/1970
const int SecsInDay = 86400; // number of seconds in a day

time_t TDateTime_TimeT(double Convertee)
{
  time_t Result((long)(((Convertee) - EpochDiff) * SecsInDay));
  return Result;
}

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

// procedures for Photon, overflow, marker

//Got Photon
//  TimeTag: Raw TimeTag from Record * Globalresolution = Real Time arrival of Photon
//  DTime: Arrival time of Photon after last Sync event (T3 only) DTime * Resolution = Real time arrival of Photon after last Sync event
//  Channel: Channel the Photon arrived (0 = Sync channel for T2 measurements)
void GotPhoton(long long TimeTag, int Channel, int DTime)
{
  if(IsT2)
  {
      fprintf(fpout,"%I64u CHN %1x %I64u %8.0lf\n", RecNum, Channel, TimeTag, (TimeTag * GlobRes * 1e12));
  }
  else
  {
    fprintf(fpout,"%I64u CHN %1x %I64u %8.0lf %10u\n", RecNum, Channel, TimeTag, (TimeTag * GlobRes * 1e9), DTime);
  }
}

//Got Marker
//  TimeTag: Raw TimeTag from Record * Globalresolution = Real Time arrival of Photon
//  Markers: Bitfield of arrived Markers, different markers can arrive at same time (same record)
void GotMarker(long long TimeTag, int Markers)
{
  fprintf(fpout,"%I64u MAR %2x %I64u\n", RecNum, Markers, TimeTag);
}

//Got Overflow
//  Count: Some TCSPC provide Overflow compression = if no Photons between overflow you get one record for multiple Overflows
void GotOverflow(int Count)
{
  fprintf(fpout,"%I64u OFL * %2x\n", RecNum, Count);
}

// PicoHarp T3 input
void ProcessPHT3(unsigned int TTTRRecord)
{
  const int T3WRAPAROUND = 65536;
  union
  {
    unsigned int allbits;
    struct
    {
    unsigned numsync  :16;
    unsigned dtime    :12;
    unsigned channel  :4;
    } bits;
    struct
    {
    unsigned numsync  :16;
    unsigned markers  :12;
    unsigned channel  :4;
    } special;
  } Record;

  Record.allbits = TTTRRecord;
    if(Record.bits.channel==0xF) //this means we have a special record
  {
    if(Record.special.markers==0) //not a marker means overflow
    {
      GotOverflow(1);
      oflcorrection += T3WRAPAROUND; // unwrap the time tag overflow
    }
    else
    {
      truensync = oflcorrection + Record.bits.numsync;
      m = Record.special.markers;
      GotMarker(truensync, m);
    }
  } else
  {
    if(
        (Record.bits.channel==0) //Should never occur in T3 Mode
      ||(Record.bits.channel>4) //Should not occur with current routers
      )
    {
      printf("\nIllegal Channel: #%1d %1u",dlen,Record.bits.channel);
      fprintf(fpout,"\nillegal channel ");
    }

    truensync = oflcorrection + Record.bits.numsync;
    m = Record.bits.dtime;
    c = Record.bits.channel;
    GotPhoton(truensync, c, m);
    dlen++;
  }
};


void ProcessPHT2(unsigned int TTTRRecord)
{
  const int T2WRAPAROUND = 210698240;
  union
  {
    unsigned int allbits;
    struct
    {
    unsigned time   :28;
    unsigned channel  :4;
    } bits;

  } Record;
  unsigned int markers;
  Record.allbits = TTTRRecord;
  if(Record.bits.channel==0xF) //this means we have a special record
  {
    //in a special record the lower 4 bits of time are marker bits
    markers=Record.bits.time&0xF;
    if(markers==0) //this means we have an overflow record
    {
      oflcorrection += T2WRAPAROUND; // unwrap the time tag overflow
      GotOverflow(1);
    }
    else //a marker
    {
      //Strictly, in case of a marker, the lower 4 bits of time are invalid
      //because they carry the marker bits. So one could zero them out.
      //However, the marker resolution is only a few tens of nanoseconds anyway,
      //so we can just ignore the few picoseconds of error.
      truetime = oflcorrection + Record.bits.time;
            GotMarker(truetime, markers);
    }
  }
  else
  {
    if((int)Record.bits.channel > 4) //Should not occur
    {
      printf(" Illegal Chan: #%I64u %1u\n",RecNum,Record.bits.channel);
      fprintf(fpout," illegal chan.\n");
    }
    else
    {
      if(Record.bits.channel==0) cnt_0++;
      if(Record.bits.channel>=1) cnt_1++;

      truetime = oflcorrection + Record.bits.time;
      m = Record.bits.time;
      c = Record.bits.channel;
      GotPhoton(truetime, c, m);
    }
  }
}

void ProcessHHT2(unsigned int TTTRRecord, int HHVersion)
{
  const int T2WRAPAROUND_V1 = 33552000;
  const int T2WRAPAROUND_V2 = 33554432;
  union{
    DWORD   allbits;
    struct{ unsigned timetag  :25;
        unsigned channel  :6;
        unsigned special  :1; // or sync, if channel==0
        } bits;
    } T2Rec;
  T2Rec.allbits = TTTRRecord;

  if(T2Rec.bits.special==1)
    {
      if(T2Rec.bits.channel==0x3F) //an overflow record
      {
    if(HHVersion == 1)
    {
      oflcorrection += (unsigned __int64)T2WRAPAROUND_V1;
      GotOverflow(1);
    }
    else
    {
      //number of overflows is stored in timetag
      if(T2Rec.bits.timetag==0) //if it is zero it is an old style single overflow
      {
          GotOverflow(1);
        oflcorrection += (unsigned __int64)T2WRAPAROUND_V2;  //should never happen with new Firmware!
      }
      else
      {
        oflcorrection += (unsigned __int64)T2WRAPAROUND_V2 * T2Rec.bits.timetag;
        GotOverflow(T2Rec.bits.timetag);
      }
    }
      }

      if((T2Rec.bits.channel>=1)&&(T2Rec.bits.channel<=15)) //markers
      {
        truetime = oflcorrection + T2Rec.bits.timetag;
        //Note that actual marker tagging accuracy is only some ns.
    m = T2Rec.bits.channel;
    GotMarker(truetime, m);
      }

      if(T2Rec.bits.channel==0) //sync
      {
        truetime = oflcorrection + T2Rec.bits.timetag;
    GotPhoton(truetime, 0, 0);
      }
    }
    else //regular input channel
    {
    truetime = oflcorrection + T2Rec.bits.timetag;
    c = T2Rec.bits.channel + 1;
    GotPhoton(truetime, c, 0);
    }

}


void ProcessHHT3(unsigned int TTTRRecord, int HHVersion)
{
  const int T3WRAPAROUND = 1024;
  union {
    DWORD allbits;
    struct  {
      unsigned nsync    :10;  // numer of sync period
      unsigned dtime    :15;    // delay from last sync in units of chosen resolution
      unsigned channel  :6;
      unsigned special  :1;
    } bits;
  } T3Rec;
  T3Rec.allbits = TTTRRecord;
  if(T3Rec.bits.special==1)
  {
    if(T3Rec.bits.channel==0x3F) //overflow
    {
      //number of overflows is stored in nsync
      if((T3Rec.bits.nsync==0) || (HHVersion==1)) //if it is zero or old version it is an old style single oferflow
      {
        oflcorrection += (unsigned __int64)T3WRAPAROUND;
        GotOverflow(1); //should never happen with new Firmware!
      }
      else
      {
        oflcorrection += (unsigned __int64)T3WRAPAROUND * T3Rec.bits.nsync;
        GotOverflow(T3Rec.bits.nsync);
      }
    }
    if((T3Rec.bits.channel>=1)&&(T3Rec.bits.channel<=15)) //markers
    {
      truensync = oflcorrection + T3Rec.bits.nsync;
      //the time unit depends on sync period which can be obtained from the file header
      c = T3Rec.bits.channel;
      GotMarker(truensync, c);
    }
  }
  else //regular input channel
    {
      truensync = oflcorrection + T3Rec.bits.nsync;
      //the nsync time unit depends on sync period which can be obtained from the file header
      //the dtime unit depends on the resolution and can also be obtained from the file header
      c = T3Rec.bits.channel;
      m = T3Rec.bits.dtime;
      GotPhoton(truensync, c, m);
    }
}


int main(int argc, char* argv[])
{
  char Magic[8];
  char Version[8];
  char Buffer[40];
  char* AnsiBuffer;
  WCHAR* WideBuffer;
  int Result;

  long long NumRecords = -1;
  long long RecordType = 0;


  printf("\nPicoQuant Unified TTTR (PTU) Mode File Demo");
  printf("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");

  if((argc<3)||(argc>3))
  {
   printf("usage: ht2demo infile oufile\n");
   printf("infile is a Unified TTTR ptu file (binary)\n");
   printf("outfile is ASCII\n");
   getch();
   exit(-1);
  }
  if((fpin=fopen(argv[1],"rb"))==NULL)
      {printf("\n ERROR! Input file cannot be opened, aborting.\n"); goto ex;}


  if((fpout=fopen(argv[2],"w"))==NULL)
   {printf("\n ERROR! Output file cannot be opened, aborting.\n"); goto ex;}

  printf("\n Loading data from %s \n", argv[1]);
  printf("\n Writing output to %s \n", argv[2]);

  Result = fread( &Magic, 1, sizeof(Magic) ,fpin);
  if (Result!= sizeof(Magic))
  {
    printf("\nerror reading header, aborted.");
      goto close;
  }
  Result = fread(&Version, 1, sizeof(Version) ,fpin);
  if (Result!= sizeof(Version))
    {
    printf("\nerror reading header, aborted.");
      goto close;
  }
  if (strncmp(Magic, "PQTTTR", 6))
  {
    printf("\nWrong Magic, this is not a PTU file.");
    goto close;
  }
  fprintf(fpout, "Tag Version: %s \n", Version);

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
        printf("\nIncomplete File.");
          goto close;
    }

    strcpy(Buffer, TagHead.Ident);
    if (TagHead.Idx > -1)
    {
      sprintf(Buffer, "%s(%d)", TagHead.Ident,TagHead.Idx);
    }
    fprintf(fpout, "\n%-40s", Buffer);
    switch (TagHead.Typ)
    {
      case tyEmpty8:
        if (strcmp(TagHead.Ident, FastLoadEnd)==0){
          ptu_header.Fast_Load_End = TagHead.TagValue ;//just kept everything  
        }
        //fprintf(fpout, "<empty Tag>");
        break;
      case tyBool8:
        if (strcmp(TagHead.Ident, MeasDesc_StopOnOvfl)==0){
          ptu_header.MeasDesc_StopOnOvfl = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, MeasDesc_Restart)==0){
          ptu_header.MeasDesc_Restart = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispLog)==0){
          ptu_header.CurSWSetting_DispLog = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show0)==0){
          ptu_header.CurSWSetting_DispCurve_Show0 = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show1)==0){
          ptu_header.CurSWSetting_DispCurve_Show1 = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show2)==0){
          ptu_header.CurSWSetting_DispCurve_Show2 = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show3)==0){
          ptu_header.CurSWSetting_DispCurve_Show3 = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show4)==0){
          ptu_header.CurSWSetting_DispCurve_Show4 = TagHead.TagValue  ; 
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show5)==0){
          ptu_header.CurSWSetting_DispCurve_Show5 = TagHead.TagValue   
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show6)==0){
          ptu_header.CurSWSetting_DispCurve_Show6 = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_Show7)==0){
          ptu_header.CurSWSetting_DispCurve_Show7 = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, HW_ExternalRefClock)==0){
          ptu_header.HW_ExternalRefClock = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, HWInpChan_Enabled0==0){
          ptu_header.HWInpChan_Enabled0 = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, HWInpChan_Enabled1==0){
          ptu_header.HWInpChan_Enabled1 = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, HWMarkers_RisingEdge0==0){
          ptu_header.HWMarkers_RisingEdge0 = TagHead.TagValue  ; 
        } else if (strcmp(TagHead.Ident, HWMarkers_RisingEdge1==0){
          ptu_header.HWMarkers_RisingEdge1 = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, HWMarkers_RisingEdge2==0){
          ptu_header.HWMarkers_RisingEdge2 = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, HWMarkers_RisingEdge3==0){
          ptu_header.HWMarkers_RisingEdge3 = TagHead.TagValue;   
        } else if (strcmp(TagHead.Ident, HWMarkers_Enabled0==0){
          ptu_header.HWMarkers_Enabled0 = TagHead.TagValue  ; 
        } else if (strcmp(TagHead.Ident, HWMarkers_Enabled1==0){
          ptu_header.HWMarkers_Enabled1 = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, HWMarkers_Enabled2==0){
          ptu_header.HWMarkers_Enabled2 = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, HWMarkers_Enabled3==0){
          ptu_header.HWMarkers_Enabled3 = TagHead.TagValue;   
        }
        //fprintf(fpout, "%s", bool(TagHead.TagValue)?"True":"False");
        //fprintf(fpout, "  tyBool8");
        break;
      case tyInt8:
        if (strcmp(TagHead.Ident, Measurement_Mode)==0){
          ptu_header.Measurement_Mode = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, Measurement_SubMode)==0){
          ptu_header.Measurement_SubMode = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResult_StopReason)==0){
          ptu_header.TTResult_StopReason = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResultFormat_TTTRRecType)==0){
          ptu_header.TTResultFormat_TTTRRecType = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResultFormat_BitsPerRecord)==0){
          ptu_header.TTResultFormat_BitsPerRecord = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, MeasDesc_BinningFactor)==0){
          ptu_header.MeasDesc_BinningFactor = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, MeasDesc_Offset)==0){
          ptu_header.MeasDesc_Offset = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, MeasDesc_AcquisitionTime)==0){
          ptu_header.MeasDesc_AcquisitionTime = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, MeasDesc_StopAt)==0){
          ptu_header.MeasDesc_StopAt = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispAxisTimeFrom)==0){
          ptu_header.CurSWSetting_DispAxisTimeFrom = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispAxisTimeTo)==0){
          ptu_header.CurSWSetting_DispAxisTimeTo = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispAxisCountFrom)==0){
          ptu_header.CurSWSetting_DispAxisCountFrom = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispAxisCountTo)==0){
          ptu_header.CurSWSetting_DispAxisCountTo = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurves)==0){
          ptu_header.CurSWSetting_DispCurves = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo0)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo1)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo2)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo2 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo3)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo3 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo4)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo4 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo5)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo5 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo6)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo6 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CurSWSetting_DispCurve_MapTo7)==0){
          ptu_header.CurSWSetting_DispCurve_MapTo7 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_Modules )==0){
          ptu_header.HW_Modules  = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWModule_TypeCode0)==0){
          ptu_header.HWModule_TypeCode0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWModule_TypeCode1)==0){
          ptu_header.HWModule_TypeCode1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWModule_TypeCode2)==0){
          ptu_header.HWModule_TypeCode2 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWModule_VersCode0)==0){
          ptu_header.HWModule_VersCode0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWModule_VersCode1)==0){
          ptu_header.HWModule_VersCode1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWModule_VersCode2)==0){
          ptu_header.HWModule_VersCode2 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_InpChannels)==0){
          ptu_header.HW_InpChannels = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_ExternalDevices)==0){
          ptu_header.HW_ExternalDevices = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWSync_Divider)==0){
          ptu_header.HWSync_Divider = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWSync_CFDLevel)==0){
          ptu_header.HWSync_CFDLevel = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWSync_CFDZeroCross)==0){
          ptu_header.HWSync_CFDZeroCross = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWSync_Offset)==0){
          ptu_header.HWSync_Offset = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_ModuleIdx0)==0){
          ptu_header.HWInpChan_ModuleIdx0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_ModuleIdx1)==0){
          ptu_header.HWInpChan_ModuleIdx1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_CFDLevel0)==0){
          ptu_header.HWInpChan_CFDLevel0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_CFDLevel1)==0){
          ptu_header.HWInpChan_CFDLevel1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_CFDZeroCross0)==0){
          ptu_header.HWInpChan_CFDZeroCross0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_CFDZeroCross1)==0){
          ptu_header.HWInpChan_CFDZeroCross1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_Offset0)==0){
          ptu_header.HWInpChan_Offset0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWInpChan_Offset1)==0){
          ptu_header.HWInpChan_Offset1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_Markers)==0){
          ptu_header.HW_Markers = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HWMarkers_HoldOff )==0){
          ptu_header.HWMarkers_HoldOff = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResult_SyncRate)==0){
          ptu_header.TTResult_SyncRate = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResult_InputRate0)==0){
          ptu_header.TTResult_InputRate0 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResult_InputRate1)==0){
          ptu_header.TTResult_InputRate1 = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResult_StopAfter)==0){
          ptu_header.TTResult_StopAfter = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, TTResult_NumberOfRecords)==0){
          ptu_header.TTResult_NumberOfRecords = TagHead.TagValue;
        }
        /*fprintf(fpout, "%lld", TagHead.TagValue);
        fprintf(fpout, "  tyInt8");
        // get some Values we need to analyse records
        if (strcmp(TagHead.Ident, TTTRTagNumRecords)==0) // Number of records
          NumRecords = TagHead.TagValue;
        if (strcmp(TagHead.Ident, TTTRTagTTTRRecType)==0) // TTTR RecordType
          RecordType = TagHead.TagValue;*/ 
        break;
      /*case tyBitSet64: //not sure when this is used
        //fprintf(fpout, "0x%16.16X", TagHead.TagValue);
        //fprintf(fpout, "  tyBitSet64");
        break;*/
      /*case tyColor8:
        fprintf(fpout, "0x%16.16X", TagHead.TagValue);
        fprintf(fpout, "  tyColor8");
        break;*/
      case tyFloat8:
        if (strcmp(TagHead.Ident, HW_BaseResolution)==0){ //this one probs not needed
          ptu_header.HW_BaseResolution = *(double*)&(TagHead.TagValue);   
        } else if (strcmp(TagHead.Ident, MeasDesc_Resolution)==0){
          ptu_header.MeasDesc_Resolution = *(double*)&(TagHead.TagValue);
        } else if (strcmp(TagHead.Ident, MeasDesc_GlobalResolution)==0){
          ptu_header.MeasDesc_GlobalResolution = *(double*)&(TagHead.TagValue);//in ns
        }/*
        fprintf(fpout, "%E", *(double*)&(TagHead.TagValue));
        fprintf(fpout, "  tyFloat8");
        if (strcmp(TagHead.Ident, TTTRTagRes)==0) // Resolution for TCSPC-Decay
          Resolution = *(double*)&(TagHead.TagValue);
        if (strcmp(TagHead.Ident, TTTRTagGlobRes)==0) // Global resolution for timetag
          GlobRes = *(double*)&(TagHead.TagValue); // in ns*/
        break;
      /*case tyFloat8Array: //is this used when there are multiple records in one file?
        fprintf(fpout, "<Float Array with %d Entries>", TagHead.TagValue / sizeof(double));
        fprintf(fpout, "  tyFloat8Array");
        // only seek the Data, if one needs the data, it can be loaded here
        fseek(fpin, (long)TagHead.TagValue, SEEK_CUR);
        break;*/
      case tyTDateTime:
        time_t CreateTime;
        ptu_header.File_CreatingTime = TDateTime_TimeT(*((double*)&(TagHead.TagValue)));
        //fprintf(fpout, "%s", asctime(gmtime(&CreateTime)), "\0");
        //fprintf(fpout, "  tyTDateTime");
        break;
      case tyAnsiString:
        AnsiBuffer = (char*)calloc((size_t)TagHead.TagValue,1);
        Result = fread(AnsiBuffer, 1, (size_t)TagHead.TagValue, fpin);
        if (Result!= TagHead.TagValue){
          printf("\nIncomplete File at AnsiBuffer.");
        } else if (strcmp(TagHead.Ident, File_GUID)==0){
          ptu_header.File_GUID = TagHead.TagValue ;  
        } else if (strcmp(TagHead.Ident, File_AssuredContent)==0){
          ptu_header.File_AssuredContent = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CreatorSW_ContentVersion)==0){
          ptu_header.CreatorSW_ContentVersion = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CreatorSW_Name)==0){
          ptu_header.CreatorSW_Name = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, CreatorSW_Version)==0){
          ptu_header.CreatorSW_Version = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, File_Comment)==0){//T2 Mode!!!!!!!!!
          ptu_header.File_Comment = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_Type)==0){//HydraHarp400!!!!!!!!
          ptu_header.HW_Type = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_PartNo)==0){
          ptu_header.HW_PartNo = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_Version)==0){//Version 2.0!!!!!!!
          ptu_header.HW_Version = TagHead.TagValue;
        } else if (strcmp(TagHead.Ident, HW_SerialNo)==0){
          ptu_header.HW_SerialNo = TagHead.TagValue;
        }
        //fprintf(fpout, "%s", AnsiBuffer);
        //fprintf(fpout, "  tyAnsiString");
        free(AnsiBuffer);
        break;
      /*case tyWideString:
        WideBuffer = (WCHAR*)calloc((size_t)TagHead.TagValue,1);
        Result = fread(WideBuffer, 1, (size_t)TagHead.TagValue, fpin);
        if (Result!= TagHead.TagValue){
          printf("\nIncomplete File at WideBuffer");
        }
        //fwprintf(fpout, L"%s", WideBuffer);
        fprintf(fpout, "  tyWideString");
        free(WideBuffer);
        break;*/
      /*case tyBinaryBlob:
        fprintf(fpout, "<Binary Blob contains %d Bytes>", TagHead.TagValue);
        fprintf(fpout, "  tyBinaryBlob");
        // only seek the Data, if one needs the data, it can be loaded here
        fseek(fpin, (long)TagHead.TagValue, SEEK_CUR);
        break;*/
      default:
        error  ("Illegal Type identifier found! Broken file?");
        break;
    }
  }
  while((strncmp(TagHead.Ident, Header_End, sizeof(Header_End))));
  fprintf(fpout, "\n-----------------------\n");
// End Header loading
}
  
  // TTTR Record type
  switch (ptu_header.TTResultFormat_TTTRRecType)
  {
    case rtHydraHarp2T2:
      return ptu_hh_v20_t2_stream(FILE *stream_in, FILE *stream_out,
       ptu_header_t *ptu_header, options_t *options) 
      //fprintf(fpout, "HydraHarp V2 T2 data\n");
      //fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      break;
    case rtHydraHarp2T3:
      return ptu_hh_v20_t3_stream(FILE *stream_in, FILE *stream_out,
       ptu_header_t *ptu_header, options_t *options)
      //fprintf(fpout, "HydraHarp V2 T3 data\n");
      //fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      break;
    
    case rtPicoHarpT2:
      fprintf(fpout, "PicoHarp T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      break;
    case rtPicoHarpT3:
      fprintf(fpout, "PicoHarp T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      break;
    case rtHydraHarpT2:
      fprintf(fpout, "HydraHarp V1 T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      break;
    case rtHydraHarpT3:
      fprintf(fpout, "HydraHarp V1 T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      break;
    
	  case rtTimeHarp260NT3:
      fprintf(fpout, "TimeHarp260N T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      break;
	  case rtTimeHarp260NT2:
      fprintf(fpout, "TimeHarp260N T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      break;
    case rtTimeHarp260PT3:
      fprintf(fpout, "TimeHarp260P T3 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ns dtime\n");
      break;
	  case rtTimeHarp260PT2:
      fprintf(fpout, "TimeHarp260P T2 data\n");
      fprintf(fpout,"\nrecord# chan   nsync truetime/ps\n");
      break;
    default:
      fprintf(fpout, "Unknown record type: 0x%X\n 0x%X\n ", RecordType);
      break;
  }

  unsigned int TTTRRecord;
  for(RecNum=0;RecNum<NumRecords;RecNum++)
    {
        Result = fread(&TTTRRecord, 1, sizeof(TTTRRecord) ,fpin);
    if (Result!= sizeof(TTTRRecord))
      {
        printf("\nUnexpected end of input file!");
        break;
      }
        switch (RecordType)
    {
    case rtPicoHarpT2:
      IsT2 = true;
      ProcessPHT2(TTTRRecord);
      break;
    case rtPicoHarpT3:
      IsT2 = false;
      ProcessPHT3(TTTRRecord);
      break;
    case rtHydraHarpT2:
      IsT2 = true;
      ProcessHHT2(TTTRRecord, 1);
      break;
    case rtHydraHarpT3:
      IsT2 = false;
      ProcessHHT3(TTTRRecord, 1);
      break;
	case rtHydraHarp2T2:
	case rtTimeHarp260NT2:
	case rtTimeHarp260PT2:
      IsT2 = true;
      ProcessHHT2(TTTRRecord, 2);
      break;
	case rtHydraHarp2T3:
	case rtTimeHarp260NT3:
	case rtTimeHarp260PT3:
      IsT2 = false;
      ProcessHHT3(TTTRRecord, 2);
      break;
    default:

      goto close;
    }
  }

close:
  fclose(fpin);
  fclose(fpout);

ex:
  printf("\n any key...");
  getch();
  exit(0);
  return(0);
}