%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Code to Analyze the Vis-TCSPC Data from Dan Franke's SWIR dots (2015-08-28) %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% User-set parameters for partial program execution

% '0' --> All subunits
% '1' --> Generate one plot with all raw curves from each .phd file
% '2' --> Generate one plot with all curves (background-subtracted & normalized) from each .phd file

% '3' --> Run the 'Good Bits' --> generally the user-specified 'particular plots'


DoParam=0;

%%%%% User-set program execution parameters

%% User-set flag to trigger export of .fig and .png files for each figure

isSaveFigs=false; 
        
%% User-set home directory -- All .phd files in this directory will be loaded

PathD='D:\Dropbox (WilsonLab)\WilsonLab Team Folder\Programs\2016-12-21 - Mark''s Matlab Data Analysis Package';
PathD=[PathD '\'];
cd(PathD);

%% User-Set Parameter for Figure Background Colour

% Note that setting this to black ([0 0 0]) or white ([1 1 1]) is used as a
% flag to control program execution to generate white- or black-background 
% figures -- other values are not yet handled.

DefaultFigColour=[1 1 1]; 

%% Setting this flag to 'false' tells the program not to alter the size/position of the figures

ResetPlot=false; 

%% User-Set Parameters for figure size 

DefaultFigSize=[640 480];

ScreenSize=get(0,'ScreenSize');
DefaultFigPosn=[ScreenSize(3)-DefaultFigSize(1)-20 ScreenSize(4)-DefaultFigSize(2)-120];
if min(DefaultFigPosn)<=0
    error('Current display resolution too small to display standard figure');
end

%% User-set Parameters for Data Analysis

%BaselineFindParam=10; % This means that the 'find zero' routine will consider the signal before ten times the distance from the peak to the 50% point as 'background'
%TruncTime=-10; % Sets the value (in ns) beyond which there is 'real data' to speed background subtraction

% Background subtraction ranges presently handled manually --> search for #MWBW001

%% Create PathD/Analysis folder if necessary

% Switch depending on whether black figures or white

if sum(DefaultFigColour)==3
    [~,~,~]=mkdir('Analysis\White'); % Output is suppressed to avoid the 'directory already exists' warning
elseif sum(DefaultFigColour)==0
    [~,~,~]=mkdir('Analysis\Black'); % Output is suppressed to avoid the 'directory already exists' warning
else
    error('DefaultFigColour is neither white nor black -- this case is not yet handled by the program')
end

%% Disable 'Negative Data Ignored' Warning

warning('OFF','MATLAB:Axes:NegativeDataInLogAxis'); %Re-enabled at end

%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Load Data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Skip loding of the data if it's already in the memory

% Note that the program only checks that there is a variable named
% 'MainData' in the workspace, so this needs to be cleared if something is
% left over from an earlier run.

if  exist('MainData')~=0
    LoadSkip=true;
    disp(' ');
    disp('**************************************************************');
    disp('Data Detected in Memory - Skipping Data Load');
    disp('**************************************************************');

    dummy=input('Press <Enter> to Continue');
    
    clear dummy
    
    disp(' ');
    disp('Continuing Program Execution...');
    disp(' ');
else
    LoadSkip=false;
    disp(' ');
    disp('**************************************************************');
    disp('No Data Detected in Memory');
    disp('--> Proceeding to Load Data...');
    disp('**************************************************************');
end

%%%%% Clear memory

if ~LoadSkip
    clearvars -except LoadSkip DoParam PathD ResetPlot DefaultFigSize DefaultFigColour DefaultFigPosn isSaveFigs
end
 

%% Load standard .phd files

if ~LoadSkip
    
    MainData{1,1}.IsData=false; %Set flag to default
    
    disp(' ');
    disp('Loading data...');

    Files = ls;
    disp('Loading .phd files');

    %%%%% Count number of valid files and build list of filenames

    NumDataFiles=0;
    for i=1:size(Files,1)
        Name = strtrim(Files(i,:));
        if length(Name) >= 8 && strcmpi(Name(end-7:end), 'Data.phd')
            NumDataFiles=NumDataFiles+1;
            FileList{NumDataFiles,1}=Name;
        end
    end

    if NumDataFiles==0
        disp(' ');
        disp('No .phd files detected');
        disp('...continuing operation assuming that there are G1 files...')
        disp(' ');
        MainData{1,1}.IsData=true;
    else
    
        %%%%% Load Data

        for j=1:NumDataFiles

            MainData{j,1}=read_phd_mwbw(FileList{j});

            %%%%% Extract Plot Titles from Filenames

            MainData{j}.Date=FileList{j}(1:10); %regexp(FileList{j},'Data.phd','start')-2);

        end
    
    end

end


%% Create LegendHeaders

% This code has been re-written to operate on the 'Experimental Log' file
% directly, parsing out entries which start with '##-## - ' and using these
% as the legend headers. Previous documentation is below 2014-10-31

% This code loads in the strings specified in any file in the directory
% with the name in the form ***LegendHeaders.txt (Where * is a wildcard)

% The strings are stored in a two-level cell array. The top level has one 
% entry for each input data file, and each element is a cell sub-array
% filled with the strings corresponding to each run.

% Hence, to access the title for the 3rd run in the 2nd set of
% measurements, use PlotTitles{2}{3}

if ~(LoadSkip||~MainData{1,1}.IsData)
    
    disp('Generating LegendHeaders from *Experimental Log.txt');
    
    %%%%% Count number of valid files and build list of filenames

    NumTitleFiles=0;
    for i=1:size(Files,1)
        Name = strtrim(Files(i,:));
        if length(Name) >= 20 && strcmpi(Name(end-19:end), 'Experimental Log.txt')
            NumTitleFiles=NumTitleFiles+1;
            TitleList{NumTitleFiles,1}=Name;
        end
    end

    if exist('TitleList','var')==0
        disp(' ');
        disp('Warning: Could not detect any files in the form ''***Experimental Log.txt''');
        disp('At present, this is required for program execution, so the program will terminate:');
        error('Unable to generate LegendHeaders');        
    end
    
    if length(TitleList)~=length(FileList)
        disp('Warning: This folder contains a different number of Data and Experimental Log files');
        disp(' ');
        dummy=input('Press <Enter> to Continue, or Ctrl-C to quit');
        disp(' ');
        disp('Continuing Program Execution...');
        disp(' ');
    end

    %%%%% Imports the strings

    for i=1:length(TitleList)

        %%%# For the record, the 'temp' bodge is here because I the default
        %%%behaviour of textscan with the 'Collect Output' for strings
        %%%results in an annoying nested set of cells in a cell. It'd be
        %%%nice to have this happen more cleanly...
        
        fid=fopen(TitleList{i});
        temp=textscan(fid,'%s','Delimiter','\n','CollectOutput',1);
        temp=temp{1,1};
        
        % Strip out non-header entries, append all entries that begin with
        % two numbers to Data Object
        
        k=0; % Initialize counter
        for j=1:length(temp)
            if regexp(temp{j,1},'\d\d-\d\d\s-\s')
                k=k+1;
                MainData{i,1}.LegendHeaders{k,1}=temp{j,1};
            end
        end
        fclose(fid);

        % Ensure that there is one legend header for each curve
    
        if k ~= MainData{i,1}.NumCurves
            disp('**************************************************************');
            disp('It looks like there are a different number of curves and legend headers')
            disp('This usually causes problems...');
            [~]=input('Press <Enter> to Continue execution');
        
        end
        
    end
    
    clear temp fid i j k FileList TitleList NumTitleFiles Name Files NumDataFiles

    disp('LegendHeaders loading complete');
    
    
    
    
end


%% Put the first block of g1 code here if required (Load g2 data) #MWBW


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% %%%%%%%%%%%%%%%%%% Plot Raw Kinetics for .phd data %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if DoParam==1||DoParam==0||DoParam==9

    disp('Plotting individual raw kinetics for .phd-style data...');

    if ~MainData{1,1}.IsData
        disp(' ');
        disp(['DoParam has been set to: ' num2str(DoParam) ', which plots .phd-style data']);
        disp('However, no .phd-style data is detected');
        disp('Either change mode of operation (i.e. value of DoParam)')
        disp('...or ensure the .phd file(s) are in the directory specified in PathD');
        error('No .phd-style data detected');
    end
    
    %%%%% Generate Colourset

    for j=1:size(MainData,1)
        ColourSet{j}=varycolour(MainData{j,1}.NumCurves); % The '+1' is to generate enough colours to avoid the use of a black trace
        %ColourSet(1,:)=[]; % Removes black trace
        %ColourSet=flipud(ColourSet);
    end
    
    %%%%% Create figure
    
    for j=1:size(MainData,1)
        
        figure(100+j*10)
        clf;
        set(gcf,'color',DefaultFigColour);

        for i=1:MainData{j,1}.NumCurves
            semilogy(MainData{j,1}.Data{i}(:,1),MainData{j,1}.Data{i}(:,2),'color',ColourSet{j}(i,:),'LineWidth',2);
            if i==1
                hold on
            end
        end

        % Control Plot Style
        box on
        FigPosn(1,1:2)=DefaultFigPosn;
        FigPosn(1,3:4)=DefaultFigSize;
        set(gcf,'Position',FigPosn);
        clear FigPosn;
        
        set(gca,'FontSize',15);
        axis tight
        title([MainData{j}.Date ' - Raw Data']);
        xlabel('Time (ns)');
        ylabel('PL Intensity (Counts)');
        % xlim([800 1600]);
        %set(gca,'LooseInset',get(gca,'TightInset'));
%        ylim([1 100000]);

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%% Add Legend
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        % BuildLocalLegend
        
        LocalLegendHeaders=cell(MainData{j,1}.NumCurves,1);
        
        for i=1:MainData{j,1}.NumCurves
            
            LocalLegendHeaders{i}= MainData{j,1}.LegendHeaders{i}(1:5);

        end
            
        % Add Legend

        L=legend(LocalLegendHeaders,'Location','NorthEast','FontSize',8);
        % LT=get(L,'title');
        % set(LT,'string',{'Pump Power'},'FontSize',15);
        % % Shift the legend down to accommodate the title
        % LP=get(L,'position');
        % LP(1)=LP(1)+(LP(3)/NumPlots);
        % set(L,'position',LP);
        % % Shift the legend horizontally if necessary
        % LP=get(L,'position');
        % LP(1)=LP(1)-(LP(3))*0.3; %This specifies the shift (left) in fractions-of-the-width -of-the-legend-box
        % set(L,'position',LP);

        % Re-Size Figure to adjust to the size of the legend (Use for 'Legend Outside' Placement Option)
        % LP=get(L,'position'); % Note that the legend size is specific relative to the Figure Size
        % FigPosn=[DefaultFigPosn-[(LP(1,3)*FigPosn(1,3)) 0] DefaultFigSize+[(LP(1,3)*FigPosn(1,3)) 0]];
        % set(gcf,'Position',FigPosn);

        clear LocalLegendHeaders i j L
        
    end
      
else disp('Individual plots of raw .phd-type data skipped')
    
end

%% %%%%%%%%%%%%%%%%%%%%%%% Determine Zero Offset %%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% For now, I just set the time offset by hand. This is because even though 
% it's straightforward to write code that seeks out the half-max point on 
% the rise, or the time index of the global peak, the reality is that, 
% without quite a biit of work, this won't always handle cases where
% there is a delayed rise in the measurement, or the 'negative-time'
% background is still decaying, or the particular run is (purposefully)
% just noise. Better still, with our measurements, the 'zero time point'
% should be the same for all measurements made with the same
% detector/laser/diode-current, so it's really quite reasonable to just set
% it by hand... it's nice to think that there are still some jobs left for
% we humans...

% When analyzing new data, I'd recommend to first run this script with the
% DoParam flag set to 1, which generates a plot where it's easy to see
% where 'zero time' should be set.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% 'ZeroTimeOffset' are the possible values of zero time offsets 
% (...allowing for more than one if it changed during the experiment)

ZeroTimeOffset(1)=117.1;
%ZeroTimeOffset(2)=127.88;

% This object (PickParam) assigns which curves get which offsets. 
% It's constructed as a cell array so that the different data files don't 
% have to have the same number of curves

% Here's a straightforward example where all curves in the data file parsed
% into MainData{1,1} have the same 'zero time'.

PickParam{1}=ones(1,MainData{1,1}.NumCurves);

% here's an example where the elements of a single .phd file (which has 14
% curves, have one of two different 'zero times'.
%PickParam{1}=[1,1,1,1,1,2,2,2,2,2,2,2,2,2];

%%%%% Loop over the elements in Main Data (i.e., each sepearate .phd file and apply the specified offsets

for h=1:size(MainData,1)

    % Loop over the individual curves
    
    if MainData{h,1}.IsData % This flag allows the program to run if there are more g2-style data files than .phd files
        
        disp(['Applying manual zero-time offsets to .phd data set #' num2str(h)]);
        
        for j=1:MainData{h,1}.NumCurves
            MainData{h,1}.ZeroTimeOffset(j,1)=ZeroTimeOffset(PickParam{h}(j));
        end
        
    end

end

% Cleaning

clear h i j ZeroTimeOffset PickParam

%% %%%%%%%%%%%%% Determine Value for Background Subtraction %%%%%%%%%%%%%%%

% Right now, this is implemented with a single pair of pre-set 'start' and 
% 'stop' times for the averaging of the negative-time background. These 
% should eventually be replaced with an array of values, or, better yet, a
% dynamically-set range using a modified 'FindZeroTimePlusPeak' routine. 
% This was not done at the time because the data in some traces is not flat
% in the negative-time region.

% % Legacy code
% for i=1:NumPlots
%     [HalfMaxIndices(i),PeakIndices(i),Baselines(i)]=FindZeroTimePlusPeak(MainData(:,2,i),BaselineFindParam);
%     MainDataBkSub(:,2,i)=MainData(:,2,i)-Baselines(i);
% end

%%%#MWBW001

if MainData{1,1}.IsData

    disp('Determining values for background subtraction for .phd data...');

    for j=1:size(MainData,1)
        
        BkSubStartTime=-MainData{1,1}.ZeroTimeOffset(j); % Along with the next value, sets the value (in ns) at which the 'negative time' data is averaged to be subtracted
        BkSubStopTime=-2; %Time point at which to stop averaging in the 'negative time' background
        
        MainData{j,1}.BkSub=zeros(MainData{j,1}.NumCurves,1);

        for i=1:MainData{j,1}.NumCurves
            MainData{j,1}.BkSub(i)=mean(...
                MainData{j,1}.Data{i}(...
                find((MainData{j,1}.Data{i}(:,1)-MainData{j,1}.ZeroTimeOffset(i))>BkSubStartTime,1,'first'):...
                find((MainData{j,1}.Data{i}(:,1)-MainData{j,1}.ZeroTimeOffset(i))>BkSubStopTime,1,'first')...
                ,2) );
        end
    end

end

clear BkSubStartTime BkSubStopTime NumDataFiltes

%% Put the second block of G1 code here if required #MWBW




%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Quick Check Plot - All Curves, Zero-Timed, Bk-Subbed & Normalized Data %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if DoParam==2||DoParam==0||DoParam==9
    
    for h=1:size(MainData,1)  % (Loop over all .phd-type data sets)
        
        %%%%% Choose which block to use: plot all traces, or plot designated traces
        
        DataSelect   = h*ones(MainData{h,1}.NumCurves,1);
        KinPickParam = [1:MainData{h,1}.NumCurves]';
        
        if length(DataSelect)~=length(KinPickParam)
            error('The data set and KinPickParam values don''t match... this is usually a typo');
        end
        
        %%%%% Generate Colour Set
        
        LocalColourSet=varycolour(size(KinPickParam,1));
        
        %%%%% Create Figure
        
        figure(200+h*10)
        clf;
        set(gcf,'color',DefaultFigColour);
        
        for i=1:length(KinPickParam)
            
            [xData,yData]=MarkPlotPrep(MainData{DataSelect(i),1},KinPickParam(i),'ZeroT','BkSub','Norm');
            
            semilogy(xData,yData,'.','color',LocalColourSet(i,:));
            if i==1
                hold on
            end
        end
        
        % Cleaning
        
        clear xData yData
        
        %%%%% Control Plot Style
        box on
        FigPosn(1,1:2)=DefaultFigPosn;
        FigPosn(1,3:4)=DefaultFigSize;
        set(gcf,'Position',FigPosn);
        clear FigPosn
        
        set(gca,'FontSize',15);
        axis tight
        title([MainData{DataSelect(h)}.Date ' - All Data (ZeroT, BkSub, Norm)']);
        xlabel('Time (ns)');
        ylabel('PL Intensity (Counts per Bin)');
        %xlim([-50 400]);
        %set(gca,'LooseInset',get(gca,'TightInset'));
        %ylim([20 60000]);
        
        %%%%% Build LocalLegendHeaders
        
        LocalLegendHeaders=cell(length(KinPickParam),1);
        
        for i=1:length(KinPickParam)
            LocalLegendHeaders{i}=MainData{DataSelect(i),1}.LegendHeaders{KinPickParam(i)};
            % Truncate Comments
            %        TruncStart=regexpi(LocalLegendHeaders{i},' ]','end')+1;
            TruncEnd=5; %Preserve only the ##-## run number
            LocalLegendHeaders{i}=LocalLegendHeaders{i}(1:TruncEnd);
            %         TruncStart=regexpi(LocalLegendHeaders{i},'@','end');
            %         TruncEnd=regexpi(LocalLegendHeaders{i},'Hz','end')+1;
            %         LocalLegendHeaders{i}=[LocalLegendHeaders{i}(1:TruncStart) LocalLegendHeaders{i}(TruncEnd:end)];
        end
        
        %%%%% Add, shape, and position Legend
        
        L=legend(LocalLegendHeaders,'Location','NorthEast','FontSize',8);
        % LT=get(L,'title');
        % set(LT,'string',{'Pump Power'},'FontSize',15);
        % % Shift the legend down to accommodate the title
        % LP=get(L,'position');
        % LP(1)=LP(1)+(LP(3)/NumPlots);
        % set(L,'position',LP);
        % % Shift the legend horizontally if necessary
        % LP=get(L,'position');
        % LP(1)=LP(1)-(LP(3))*0.3; %This specifies the shift (left) in fractions-of-the-width -of-the-legend-box
        % set(L,'position',LP);
        
        % Re-Size Figure to adjust to the size of the legend (Use for 'Legend Outside' Placement Option)
        % LP=get(L,'position'); % Note that the legend size is specific relative to the Figure Size
        % FigPosn=[DefaultFigPosn-[(LP(1,3)*FigPosn(1,3)) 0] DefaultFigSize+[(LP(1,3)*FigPosn(1,3)) 0]];
        % set(gcf,'Position',FigPosn);
        
        %%%%% Additional Text
        
        %text(0.6,0.73,'"Low" Rep Rate','Fontsize',12,'Units','Normalized');
        
    end
    
    % Cleaning
    
    clear h i j KinPickParam L LocalColourSet LocalLegendHeaders TruncEnd
    
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%% Plot Particular Curves %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if DoParam==3||DoParam==0||DoParam==9
    
 
   
    %% %%% Generate Plots

    % Loop over the number of particular plots to generate
    
    for g=1

        % This switch statement is used to manually set which curves to put on each plot
        % Other cases can be added as desired...
        
        switch g
            case 1 % e.g. Compare the four curves we took from the phosphorous acid-treated sample
                DataSelect    = [ 1; 1; 1;]; % Selects the matched Data Sets (first row)
                KinPickParam  = [ 5; 9;13;]; %  and Individual Curves (second row) to be plotted
                MicroSecScale = false;    % A flag to plot the time axis in microseconds (...as opposed to nanoseconds, which is the default)
        end
        
        if length(DataSelect)~=length(KinPickParam)
            error('The DataSelect and KinPickParam dimensions don''t match... this is usually a typo');
        end
        
        %%%%% Generate Colour Set
        
        % Switch depending on whether black figures or white
        
        if sum(DefaultFigColour)==3
            switch g

                otherwise
                    LocalColourSet=varycolour(size(KinPickParam,1));
            end
        elseif sum(DefaultFigColour)==0
            switch g
                
                otherwise
                    LocalColourSet=varycolourblack(size(KinPickParam,1));
            end
            
        else
            error('DefaultFigColour is neither white nor black -- this case is not yet handled by the program')
        end
        
        %end
        
        
        
        %%%%% Set h=1:2 to loop to make an 'animated' set of figures,
            % for example, one with the data, and then one with the data+fit
            % Setting h=1 will produce only the data, and h=2 will only
            % make the plot with the data+fit.

        for h=1:2
            
            %%%%% Create Figure
            
            F=figure(300+10*(g-1)+h);
            clf;
            whitebg(F,DefaultFigColour)
            F.Color=DefaultFigColour; %set(gcf,'color',DefaultFigColour);
            
            for i=1:size(KinPickParam,1)
                
                % Generate data vectors from raw data
                
                switch h
                    otherwise
                        [xData,yData]=MarkPlotPrep(MainData{DataSelect(i),1},KinPickParam(i),'ZeroT','BkSub','Norm','ReBin','8');  %
                end
                
%                 % Truncate ends of data sets if necessary
%                 
%                 yData(find(xData>9900,1,'first'):end)=[];
%                 xData(find(xData>9900,1,'first'):end)=[];
                
                % Scale to us from ns if desired
                
                if MicroSecScale
                    xData=xData.*1e-3;
                end
                
                % Add curve to plote
                
                % Switch statement to allow the use of different markers
                % for each data set
                
                switch i
%                     case {1,2}
%                         semilogy(xData,yData,'o','color',LocalColourSet(i,:),'MarkerSize',3); %'LineWidth',2
                    otherwise
                        semilogy(xData,yData,'.','color',LocalColourSet(i,:)); %'LineWidth',2
                end
                        
                if i==1
                    hold on
                end
                
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %%%%% Fit data
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
                % Example: fitting of a monoexponential to the long-time data
                
                
                %%%%% Define function handel
                
                monoexp=@(param,t) param(2).*exp(-t./param(1));
                
                
                %%%%% Define fitting range (in the time units of the data)
                
                StartIndex=find(xData>200,1); 
                StopIndex=find(xData>500,1);
                
                
                %%%%% Determine initial parameters
                                
                % We guess the size of the residual decay as the data value
                % at the StartIndex of the fitting window
                
                InitParams(2)=yData(StartIndex);
                
                % We guess the first time constant as the e-folding time from
                % the start
                if isempty(find(yData(StartIndex:StopIndex)<(yData(StartIndex)*exp(-1)),1))
                    % Handle the case where there isn't sufficient decay for
                    % there to be data less than 1/e of the start point
                    InitParams(1)=xData(mean(StartIndex:StopIndex)); %xData(find(yData<(yData(LongTimeStartIndex)*exp(-1)),1));
                else
                    InitParams(1)=xData(StartIndex+find(yData(StartIndex:StopIndex)<(yData(StartIndex)*exp(-1)),1)); %xData(find(yData<(yData(LongTimeStartIndex)*exp(-1)),1));
                end
                
                
                %%%%% Run the fit
                
                [FittedParams{i},R,J,~,~,~] = nlinfit(xData(StartIndex:StopIndex),yData(StartIndex:StopIndex),monoexp,InitParams);
                
                
                %%%%% Determine error in the fit
                
                ErrorInFit{i}=nlparci(FittedParams{i},R,'jacobian',J);
            
            end
            
            % This break in the loop means that all of the fitted curves
            % are plotted after all of the data curves, so that the legend 
            % looks sensible. It also helps the generation of a series of
            % 'animated' plots work well.
            
            for i=1:size(KinPickParam,1)
                
                switch h
                    case {2}
                        %%%%% Add fitted curve to graph
                        
                        % Switch depending on whether black figures or white
                        if sum(DefaultFigColour)==3
                            semilogy(xData(xData>0),monoexp(FittedParams{i},xData(xData>0)),'color',[0.7 0.7 0.7],'LineWidth',1);
                        elseif sum(DefaultFigColour)==0
                            semilogy(xData(xData>0),monoexp(FittedParams{i},xData(xData>0)),'color',[0.7 0.7 0.7],'LineWidth',1);
                        end
                        
                        %%%% Add dot lifetime & error to graph
                        
                        % Set position depending on figure
                        
                        posnX(1)=0.1;
                        posnY(1)=0.3;
                        
                        % Add text
                        if MicroSecScale
                            text(posnX(1),posnY(1),{['\tau_{mono(1)} = ' ...
                                num2str(FittedParams{1}(1),'%.2f') '\pm' ...
                                num2str((ErrorInFit{1}(1,2)-ErrorInFit{1}(1,1))/2,'%.2f') '\mus'],...
                                ['\tau_{mono(2)} = ' ...
                                num2str(FittedParams{2}(1),'%.2f') '\pm' ...
                                num2str((ErrorInFit{2}(1,2)-ErrorInFit{2}(1,1))/2,'%.2f') '\mus'],...
                                ['\tau_{mono(3)} = ' ...
                                num2str(FittedParams{3}(1),'%.2f') '\pm' ...
                                num2str((ErrorInFit{2}(1,2)-ErrorInFit{2}(1,1))/2,'%.2f') '\mus']},...
                                'Fontsize',11,'Units','Normalized');
                        else
                            text(posnX(1),posnY(1),{['\tau_{mono(1)} = ' ...
                                num2str(FittedParams{1}(1),'%.0f') '\pm' ...
                                num2str((ErrorInFit{1}(1,2)-ErrorInFit{1}(1,1))/2,'%.0f') 'ns'],...
                                ['\tau_{mono(2)} = ' ...
                                num2str(FittedParams{2}(1),'%.0f') '\pm' ...
                                num2str((ErrorInFit{2}(1,2)-ErrorInFit{2}(1,1))/2,'%.0f') 'ns'],...
                                ['\tau_{mono(3)} = ' ...
                                num2str(FittedParams{3}(1),'%.0f') '\pm' ...
                                num2str((ErrorInFit{1}(1,2)-ErrorInFit{1}(1,1))/2,'%.0f') 'ns']},...
                                'Fontsize',11,'Units','Normalized');
                        end
                        
                        clear posnX posnY
                    otherwise
                        % No fitted curves added to the plot
                end
            end
            
            
            
            
            clear StartIndex StopIndex ErrorInFit FittedParams InitParams xData yData monoexp J R
            
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%% Control Plot Style
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            
            box on
            FigPosn(1,1:2)=DefaultFigPosn;
            FigPosn(1,3:4)=DefaultFigSize;
            set(gcf,'Position',FigPosn);
            clear FigPosn
            
            set(gca,'FontSize',18,'LineWidth',2);
            axis tight
            
            if MicroSecScale
                xlabel('Time (\mu{}s)');
            else
                xlabel('Time (ns)');
            end
            
            switch h
                otherwise
                    ylabel('PL Intensity (Norm.)');
            end
            
            xlim([-100 1500]);
            switch g
                case 1
                    ylim([0.0001 1.1]);
            end
            
            %%%%% Add Title
            
            switch g
                
                case {1}
                    % Generate title from folder name
                    LocalTitle=PathD(regexpi(PathD,'TCSPC - ','end')+1:end-1);
                    LocalTitle=[MainData{DataSelect(h)}.Date ' - ' LocalTitle ' - Solvent Dep'];
                
            end
            
            % Create title
            
            title(LocalTitle,'FontSize',18)
            
            
            %%%%% Tighten Figure
            
            %set(gca,'LooseInset',get(gca,'TightInset'));
            
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%% Add Legend
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            
            %%%%% BuildLocalLegend
            
            LocalLegendHeaders=cell(length(KinPickParam),1);

            for i=1:length(KinPickParam)
                
                LocalLegendHeaders{i}= MainData{DataSelect(i),1}.LegendHeaders{KinPickParam(i)};
                
                % Add legend entries for fitted data
                
                switch g
                    case {1}
                        
                        % Define truncation points for the legend headers
                        
                        TruncStart(1)=1;
                        TruncEnd(1)=5; 
                        
                        TruncStart(2)=regexpi(LocalLegendHeaders{i},'=>','end')+1;
                        TruncEnd(2)=regexpi(LocalLegendHeaders{i},'<900','start')-1; 
                        
                        % Construct Legend Label
                        
                        LocalLegendHeaders{i}=[LocalLegendHeaders{i}(TruncStart(1):TruncEnd(1)) ': ' LocalLegendHeaders{i}(TruncStart(2):TruncEnd(2))];
                    otherwise
                        % The default case isn't handled here, as the
                        % desired outcome will vary dramatically depending
                        % on what is desired.
                end
                
            end
            
            clear TruncStart TruncEnd;
            
            %%%%% Add additional legend entries for fitted curves
            
            switch h
                case {2}
                    LocalLegendHeaders{length(LocalLegendHeaders)+1}='Fits';
                otherwise
                    % No additional fitted curves added to legend
            end

            % Create Legend Object
            
            switch g

                otherwise
                    L=legend(LocalLegendHeaders,'Location','NorthEast','FontSize',18);
                    legend('boxoff');
            end
            
            % Set Legend Title
            % Deprecated code from MATLAB 2008a
            %     LT=get(L,'title');
            %     set(LT,'string',{'Sample'},'FontSize',15);
            
            %LT = legendTitle(L,{'Pump Power'},'FontWeight','bold');
            
            % Shift the legend as necessary
            %
            %         switch h
            %             case 1
            %         LP=get(L,'position');
            %         LP(2)=LP(2)+(LP(4)/20); %shift up/down
            %         %    LP(1)=LP(1)-(LP(3)/4);  %Shift right/left
            %         set(L,'position',LP);
            %
            %             otherwise
            %         LP=get(L,'position');
            %         LP(2)=LP(2)+(LP(4)/10); %shift up/down
            %         %    LP(1)=LP(1)-(LP(3)/4);  %Shift right/left
            %         set(L,'position',LP);
            %
            %         end
            
            % Re-Size Figure to adjust to the size of the legend
            
            % switch g
            %    case 1
            %        LP=get(L,'position'); % Note that the legend size is specific relative to the Figure Size
            %        FigPosn=[DefaultFigPosn-[(LP(1,3)*FigPosn(1,3)) 0] DefaultFigSize+[(LP(1,3)*FigPosn(1,3)) 0]];
            %        set(gcf,'Position',FigPosn);
            %        clear FigPosn
            %    otherwise
            %        %disp('Figure not resized, legend is internal.');
            % end
            

            % Cleaning

            clear L LP
            
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%% Additional Text
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            % Note: we parse the LegendHeader of the first curve in the 
            % figure obtain the experimental conditions, assuming that all
            % the curves are consistent. This would have to be extended if
            % this wasn't the case.
            
            i=1; % Sets which LegendHeader (specified by the KinPickParam) gets parsed
            
            % Obtain Laser Wavelength
            
            LocalLegendHeaders=MainData{DataSelect(i),1}.LegendHeaders{KinPickParam(i),1};
            
            TruncPoints=regexpi(LocalLegendHeaders,'@');
            TruncPoints(1)=TruncPoints(1)+1;
            TruncPoints(2)=TruncPoints(2)-1;
            LaserWavelength=LocalLegendHeaders(TruncPoints(1):TruncPoints(2));
            
            % Obtain RepRate
            
            TruncPoints(3)=regexpi(LocalLegendHeaders,'(')-1;
            RepRate=LocalLegendHeaders((TruncPoints(2)+2):TruncPoints(3));
            
            % Obtain Intrinsic Resolution
            
            IntrinsicRes=MainData{DataSelect(i),1}.TimeStep(KinPickParam(i));
            IntrinsicRes=num2str(round(IntrinsicRes*1e3)); % Convert to picoseconds, round, then cast to a string.
            
            % Manually record the degree of re-binning (or smoothing
            
            RebinText='Rebinned 8-fold';
            % SmoothText='12-point smoothed';
            
            switch g
                otherwise
                    text(0.1,0.08,{['Ex: ' LaserWavelength '@' RepRate ];...
                        [IntrinsicRes 'ps Intrinsic Resolution, ' RebinText];...
                        ['Background-Subtracted, Normalized']},...
                        'Fontsize',9,'Units','Normalized');
                    
            end
            
            %Cleaning
            
            clear LocalLegendHeaders TruncPoints LaserWavelength RepRate IntrinsicRes RebinText SmoothText
            
            
            %%%%% Export Figures
            
            if isSaveFigs
                if sum(DefaultFigColour)==0
                    set(gcf, 'InvertHardCopy', 'off');
                    savefig(gcf,[PathD '\Analysis\Black\Fig' num2str(F.Number) '-' LocalTitle]);
                    print(gcf,'-dpng',[PathD '\Analysis\Black\Fig' num2str(F.Number) '-' LocalTitle]);
                elseif sum(DefaultFigColour)==3
                    savefig(gcf,[PathD '\Analysis\White\Fig' num2str(F.Number) '-' LocalTitle]);
                    print(gcf,'-dpng',[PathD '\Analysis\White\Fig' num2str(F.Number) '-' LocalTitle]);
                end
            end
            
            
        end

        clear LocalColourSet LocalTitle
        
    end
    
    clear F g h i j KinPickParam DataSelect MicroSecScale
 

end


% Optional cleaning of flags and Defauls
% -- leave these in if using cell mode execution (i.e. Ctrl-Enter) to 
% ensure that the program flows sensibly.

% clear PathD
% clear ResetPlot LoadSkip isSaveFigs DoParam
% clear DefaultFigColour DefaultFigPosn DefaultFigSize ScreenSize









%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Cleaning %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


warning('on','all'); %Re-enable 'Negative Data Ignored' warning



