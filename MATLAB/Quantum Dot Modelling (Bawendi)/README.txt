5.38 URIECA Module 10
Massachusetts Institute of Technology
Last updated 05 March 2011 by Thomas Bischof (tbischof@mit.edu)

Contained in this archive are all of the Matlab .m files needed for this
quantum dot module. Many of these files are used for subroutines, so unless 
you are digging into the methods themselves (which you are encouraged to do), 
you should focus your attention on the following files, which contain further 
documentation: 

QDtrace.m:
Acts as a front-end to the time-trace routines needed to study the blinking 
of single quantum dots. See also tracedot.m, dotsonoff.m, readvideo.m.

singletrace.m: 
Produces time traces for a single dot.

QDmovie.m: 
A simple video player suitable for the TIFF files produced by the instrument 
in the laboratory. Alternately, you can use (all free software):
> ImageJ (http://rsbweb.nih.gov/ij/): a versatile scientific image program.
> vlc (http://www.videolan.org/vlc/): a versatile video player (will not handle
                raw TIFF, so you will have to use...)
> ImageMagick (http://www.imagemagick.org): converter for image files; you can 
                use this to turn your TIFF into simple videos or single frames.
> ffmpeg (http://ffmpeg.org/): a general-purpose video converter. Has some 
                difficulty with TIFF files, but if you have individual frames 
                it is quite nice.
Keep in mind that the actual signal will be low in your data, so unless you 
choose good threshhold values you may just see a black screen. See also
readvideo.m.

QDmodel.m: 
Produces physical information about core-shell quantum dots via an 
infinite-well approximation. See also constants.m, infstepwell.m, 
parameters.m, wavefunctions.m.

QY.m:
Determines the quantum yield of a quantum dot sample, when given the absorbance
and fluorescence spectra for the sample and a reference sample of known quantum
yield.
See also read_ocean_optics.m
