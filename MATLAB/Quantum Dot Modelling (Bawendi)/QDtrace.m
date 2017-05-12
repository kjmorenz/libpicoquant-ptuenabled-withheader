%% 5.38 URIECA Module 10
% Massachusetts Institute of Technology
% Dylan Arias
% October 27 2008
% 
% Thomas Bischof
% 19 January 2011
%
% This function is designed as a simple way to study the blinking
% statistics of quantum dots in videos taken by the fluorescence
% microscope. Given a filename and the integration time, this function will
% walk you through the selection of dots to study, present you with their
% Z-axis profile (intensity over time), create a threshhold for on/off
% differentiation, and create histograms of the distribution for later
% study.
% 
% Function arguments are:
% filename: string containing the name of the video file (greyscale)
% dt: integration time (seconds)
%
% Function returns:
% t: a 1xN array with the times associated with each frame.
% positions: 1x4xM array containing the [x,y,width,height] information for
%            the particles that were chosen.
% timetrace: an NxM array with the intensity for each selected region at
%            each frame
% threshold: the threshold value for each region of interest, which
%            defines the division between an off and an on dot.
% ontimes, offtimes: 1xP vectors with on and off times for the regions

function [t, positions, timetrace, threshold, ontimes, offtimes] = ...
    QDtrace(filename, dt)

% Load the image into memory
video = readvideo(filename); 
[height, width, nframes] = size(video);

% Create an image which averages all frames. This more clearly defines the
% particles, although with a large number of frames with high intensity
% this might run into an integer overflow error. If you find the averaged
% image is washed out, try increasing the integer size to 64-bit.
%
% There is probably a nicer way to express this flattening, but for now a
% simple for loop does the trick.
zaverage = zeros(height, width); 
N = nframes; % Number of frames to use for the average.
for i=1:N
    zaverage = zaverage + video(:,:,i);
end
zaverage = zaverage / N;

% Now that we have the averaged image, get some feedback from the user as
% to which dots we want to study.
positionfig = figure; 
imagesc(zaverage);
colormap gray;
title(['Average of first ' num2str(N) ' frames.']);

% For however many dots the user wants to look at, collect statistics.
%
% To do: turn the timetrace and histogram routines into their own
% subroutines. This would be the first step toward allowing users to load
% their own particle selections, useful if we want to restart data analysis
% from a previous run, or if we want to export/import particle definitions
% to/from another program, such as ImageJ.
t = linspace(0, dt*nframes, nframes);
do_more = 1;
i = 1;
tracefig = figure; % a figure to plot the time traces on
timetrace = [];
threshold = [];
positions = [];
while do_more == 1
    [timetrace(i,:), threshold(i), positions(i,:)] = ...
        tracedot(video, t, positionfig, tracefig); 
    do_more = input('Another trace? 1-yes 0-no ');
    i = i+1;
end

% We have the time traces, so determine the on/off times and create the
% histograms. 
ontimes = [];
offtimes = [];
for j=1:length(threshold) % statistics for the dot labeled j
    [myontimes, myofftimes] = dotsonoff(timetrace(j,:), threshold(j));
    ontimes = [ontimes myontimes]; 
    offtimes = [offtimes myofftimes];
end

% Now, plot the results to show them off.
plotonoff(ontimes, offtimes, dt);