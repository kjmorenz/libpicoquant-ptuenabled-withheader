%% 5.38 URIECA Module 10
% Massachusetts Institute of Techonology
% Dylan Arias
% 17 November 2008
%
% Modified 19 January 2011
% Thomas Bischof
% 
% Given a video filename (with suffix), reads and displays the video. This
% script assumes your computer has enough memory to store the whole file,
% so make sure you do before loading anything large.
%
% If you want to adjust the framerate, store mymovie and play it using:
% >> movie(mymovie, repetitions, framerate)

function [mymovie] = QDmovie(filename)
video = readvideo(filename);
videosize = size(video);
nframes = videosize(3);

mymovie = moviein(nframes); % initialize the movie
figure
for j = 1:nframes
    frame = video(:,:,j);
    imagesc(frame)
    colormap(gray)
    mymovie(:,j) = getframe;
    clf
end