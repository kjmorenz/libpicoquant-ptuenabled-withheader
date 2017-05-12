function [ xOut, yOut] = MarkPlotPrep(DataIn, KinPickParam, varargin )

% A function to generate a pair of column vectors (xOut, yOut) that can be
% directly used in a 'plot' function, from a data structure (DataIn), given
% a user-selected curve (KinPickParam) and a set of flags, which can
% include:

% zeroT -- adjust the time-axis (xOut) for a pre-determined 'zero time'
% bkSub -- subtract a previously-calculated 'negative time' background from the data (yOut)
% norm -- normalize the data (yOut) to the peak
% mvAvg, SmoothNum -- apply a SmoothNum-point moving average filter to yOut
% rebin, BinDivisor -- rebin yOut to occupy 1/BinDivisor the number of timebins, and generate a new time axis (xOut) appropriately.

% Note, for now, the size of the re-binning or re-smoothing must be the
% last value in the function call, and must be a string: i.e. '16'

% Presently, I'm passing the whole data structure, as opposed to using a
% global, to avoid re-writing the data import code that sets this up. 

% For reference, usual function calls would look like:

% [xData,yData]=MarkPlotPrep(MainData{DataSelect(i),1},KinPickParam(i),'ZeroT','BkSub','Norm');
% [xData,yData]=MarkPlotPrep(MainData{DataSelect(i),1},KinPickParam(i),'ZeroT','BkSub','Norm','MvAvg','17');
% [xData,yData]=MarkPlotPrep(MainData{DataSelect(i),1},KinPickParam(i),'ZeroT','BkSub','Norm','Rebin','16');

% Also, this function relies on the MarkMovAvg.m function.

% -- M.W.B. Wilson, 2015-02-09


%% Parse varargin to obtain flags

isZeroT = ismember('ZeroT',varargin);
isBkSub = ismember('BkSub',varargin);
isNorm = ismember('Norm',varargin);
isMvAvg = ismember('MvAvg',varargin);

if isMvAvg

    [SmoothNum,status]=str2num(varargin{end});
    
    if ~status
        error(['No numeric input detected to set the size of the moving average filter.\n'...
            'Ensure that the ''smoothNum'' is the last entry in the MarkPlotPrep function call.\n'...
            'Program execution terminated...'],1);
    end
    
end

isReBin = ismember('ReBin',varargin);

if isReBin

    [BinDivisor,status]=str2num(varargin{end});
    
    if ~status
        error(['No numeric input detected to set the size of the moving average filter.\n'...
            'Ensure that the ''smoothNum'' is the last entry in the MarkPlotPrep function call.\n'...
            'Program execution terminated...'],1);
    end

end

if isMvAvg && isReBin
    error(['MarkPlotPrep was asked to both re-bin and smooth (moving average) the data. \n'...
        'This behaviour has not yet been implemented... (Sorry! 2015-02-09) \n'],1);
end

%% Confirm that the DataIn structure has the necessary properties

if ~isfield(DataIn, 'Data')
    error('*.Data field not detected in structure passed to MarkPlotPrep, program terminating');
end

if ~isfield(DataIn, 'ZeroTimeOffset')
    error('*.ZeroTimeOffset field not detected in structure passed to MarkPlotPrep, program terminating');
end

if ~isfield(DataIn, 'BkSub')
    error('*.BkSub field not detected in structure passed to MarkPlotPrep, program terminating');
end

%% Define 'starter' x- and y- vectors

% This function captures the default behaviour if no flags are passed.

xOut = DataIn.Data{KinPickParam}(:,1);
yOut = DataIn.Data{KinPickParam}(:,2);

%% Correct time axis for a 'zero time'

if isZeroT
    xOut = xOut-DataIn.ZeroTimeOffset(KinPickParam);
end

%% Perform background subtraction

if isBkSub
    yOut = yOut - DataIn.BkSub(KinPickParam);
end

%% Apply moving average filter

if isMvAvg
    yOut = MarkMovAvg(yOut,SmoothNum);
end

%% Re-bin data

if isReBin
    
    % Test to ensure that the requested number of bins equally divides the data
    if size(yOut,1)/BinDivisor ~= floor(size(yOut,1)/BinDivisor)
        error(['Rebinning of data by requested divisor leads to non-integer number of bins...\n'...
            'Program execution terminating.\n'],1);
    end
        % Could add to this to just truncate points from the 'end' until it
        % divides evenly in the future.
    
    % To generate the rebinned data, reshape the matrix, and then sum over the rows
    yOut=sum(reshape(yOut,[BinDivisor,size(yOut,1)/BinDivisor]),1)';
    
    % To generate the new time axis, we reshape the matrix as before, but
    % take the mean of each row so that the new bins are positioned at the
    % center of the time range. (...this could be done more efficiently,
    % particularly if the bins are equally-spaced, but this is unlikley to
    % matter)
    xOut=mean(reshape(xOut,[BinDivisor,size(xOut,1)/BinDivisor]),1)';
    
end

%% Nomalize Data to peak

if isNorm
    yOut=yOut/max(yOut);
end


%% xOut and yOut are then returned implicitly.

end

