function index = nearest_index(data, x)
%% 5.38 Module 10
% Massachusetts Institute of Technology
% Thomas Bischof
% 18 February 2011
%
% Given a array of values data and some single value x, determines the
% index of data which contains the value closest to x.

difference = abs(data - x);
index = 0;
mymin = difference(1);
for i=1:length(difference)
    if difference(i) < mymin
        index = i;
        mymin = difference(i);
    end
end