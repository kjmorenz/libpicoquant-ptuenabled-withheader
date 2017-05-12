%% 5.38 URIECA Module 10
% Massachusetts Institutde of Technology
% Thomas Bischof
% 19 January 2011
%
% Given a greyscale video's filename, reads the video to memory and returns
% it as a three-dimensional array.
function [video] = readvideo(filename)
iminfo = imfinfo(filename);
nframes = length(iminfo);

video = zeros(iminfo(1).Height, iminfo(1).Width, nframes);

for j=1:nframes
    video(:,:,j) = imread(filename, j);
end