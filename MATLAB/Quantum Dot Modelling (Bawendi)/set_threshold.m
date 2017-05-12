%% 5.38 URIECA Module 10
% Massachusetts Institute of Techonology
% Thomas Bischof
% 19 January 2011
% 
% This function implements the threshold-finding for tracing dots.
% Currently, it is not automated, and prompts the user to set the value.
% 
% It requires:
% t: the time vector (1xN array), representing the time each frame 
%    is associated with.
% positionfig: the figure with the averaged image displayed. This is used
%    to find particles of interest.
% tracefig: a figure which can hold the time traces for the particles
%    chosen.
%
% This routine returns the threshold value dividing on and off dots.
function threshold = set_threshold(t, timetrace, tracefig)
% Capture attention and draw the time trace.
figure(tracefig);
%clf();
subplot(121);
plot(t, timetrace);
xlabel('t/s');
ylabel('Intensity/counts');

subplot(122);
[n, x] = hist(timetrace,100);
plot(n, x)


% Set the on/off threshold
disp('Click the on/off threshold height on the plot')
g = ginput(1); 
threshold = g(2);