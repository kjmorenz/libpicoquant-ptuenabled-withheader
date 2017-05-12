%% 5.38 URIECA Module 10
% Massachusetts Institute of Techonology
% Dylan Arias
% 27 October 2008
%
% Thomas Bischof
% 19 January 2011
% 
% This routine implements the selection, thresholding, and tracing
% capabilities needed in QDtrace. It requires:
% video: a three-dimensional array representing the movie of interest.
% t: the time vector (1xN array), representing the time each frame 
%    is associated with.
% positionfig: the figure with the averaged image displayed. This is used
%    to find particles of interest.
% tracefig: a figure which can hold the time traces for the particles
%    chosen.
%
% This routine returns:
% timetrace: the intensity at the selection for each frame.
% threshold: the intensity which divides dots from their on and off states.
% position: the [x, y, width, height] for the selected dot

function [timetrace, threshold, position] = ...
    tracedot(video, t, positionfig, tracefig)
% Select a region of interest. For now, this is a pixel, but later we
% should allow selection of a rectangle using getrect
figure(positionfig)
disp('Select a rectangular region of interest, then press enter')
% position = ginput;  
% position = round(position);
nframes = length(video(1,1,:));
% For whatever reason, [a,b,c,d] = getrect will not work.
rect = getrect(1);
rawx = round(rect(1));
rawy = round(rect(2));
rawwidth = round(rect(3));
rawheight = round(rect(4));
position = [rawx rawy rawwidth rawheight]';
% Make X and Y contain all pixel indices for the region of interest
X = rawx:(rawx+rawwidth);
Y = rawy:(rawy+rawheight);

% Retrieve the intensity of the selected pixels from the video.
timetrace = zeros(nframes, 1);
for i=1:nframes
    timetrace(i) = sum(sum(video(Y,X,i)));
end

threshold = set_threshold(t, timetrace, tracefig);