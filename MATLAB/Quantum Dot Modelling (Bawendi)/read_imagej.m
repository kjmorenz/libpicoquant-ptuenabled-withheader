%% 5.38 URIECA Module 10
% Massachusetts Institute of Technology
% Thomas Bischof
% 18 February 2011
%
% This function reads in data from the ImageJ Multi Measure routine. The
% first row consists of labels, and each row after that (one per frame) has
% an entry numbering it and then the values for each measurement, delimited
% by spaces. We need to remove the first row and column, which we can then
% return a the data.
%
% As far as arguments, filename is a string with the name of the file of
% interest.
%
function data = read_imagej(filename)
data = textread(filename, '%s', 'delimiter', '\n');

% This next line is a serious kuldge, but the general idea is that we need
% to find out how wide the file is, in terms of columns. We can do this by
% counting the number of delimiting characters, in this case tabs, and
% adding one to account for the fact that we have a column after the last
% one:
% '1\t2\t3' (2 \t, 3 columns)
% So, we take the second row (first data row), find the locations of all
% delimiting characters, and count the number of these locations.
width = length(regexp(char(data(2)), '\t')) + 1;
height = length(data);

% Now we know the width, so read everything in.
data = dlmread(filename, '', [1, 1, height-1, width-1]);