%% 5.38 URIECA Module 10
% Massachusetts Institute of Techonology
% Thomas Bischof
% 19 January 2011
%
% Given the on times, off times, and the integration time, plot histograms
% with the distribution of times.
%
function plotonoff(ontimes, offtimes, dt)
% The times are reported as the number of frames, but we typically want to
% know the time in seconds. 
ontimes = ontimes * dt;
offtimes = offtimes * dt;

figure();
subplot(2,1,1);
title('Histogram of on times for all regions chosen');
hist(ontimes,30);
ylabel('counts');
xlabel('t/s');

subplot(2,1,2);
title('Histogram of off times for all regions chosen');
hist(offtimes,30);
ylabel('counts');
xlabel('t/s');