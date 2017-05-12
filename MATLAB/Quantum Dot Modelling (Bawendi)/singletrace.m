%% 5.38 URIECA Module 10
% Massachusetts Institute of Technology
% Dylan Arias
% October 27 2008
% Function that finds a single trace of a single dot

function [t, timetrace] = singletrace(filename,frames,dt,N)
% Current directory must contain the m file and image file
% filename - case-sensitive name of the image file
% frames - number of frames in the file
% N - number of frames to use for averaging
% dt - integration time used in winspec in seconds

%% Initial image to find appropriate dot
for i=1:N % Average first N frames to find reliable dot positions
    initialimage(:,:,i)=imread([filename '.tif'],i);
end
initialimage=sum(initialimage,3)/N; % average of first N frames
figure(1)
imagesc(initialimage), colormap gray % plot the image
title(['Average of first ' num2str(N) ' frames to find reliable dot positions'])
xlabel('Pixel'), ylabel('Strip')
disp('Click on the dot you want to trace and press enter')
position=ginput;  position=round(position); % the user-selected position to trace

%% Load the timetrace
timetrace=[];
for j=1:frames
    v1=imread([filename '.tif'],j); % Load the jth frame into matlab
    timetrace(j)=v1(position(2),position(1)); % Add the jth frame to the time trace
end

%% plot the time trace
t=linspace(0,dt*frames,frames); % make a time vector
figure(2)
plot(t,timetrace,'.-'), title(['Time trace of QD at pixel ' num2str(position(1)) ', strip ' num2str(position(2))]), xlabel('t/s'), ylabel('Intensity')

%% smoothing
smtrace=smooth(timetrace,3);
figure(3)
plot(t,smtrace,'.-'), title('Smoothed time trace'), xlabel('t/s'), ylabel('intensity')