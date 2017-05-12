%% 5.38 URIECA Module 10
% Massachusetts Institute of Technology
% Dylan Arias and Daniel Turner
% October 27 2008
%
% Thomas Bischof
% 19 January 2011
%
% This routine implements the indexing routines needed for QDtrace.m. Here,
% we take the time trace and the threshold value and determine the number 
% of frames for which the dot is on or off, starting a new count each time
% the state changes.
%
% This function requires:
% timetrace: 1xN array containing the intensity at each frame
% threshold: the intensity dividing on and off states.
%
% This function returns:
% ontimes, offtimes: 1xM arrays containing the number of frames for which
%    the dot was on or off, respectively.
function [ontimes, offtimes] = dotsonoff(timetrace, threshold)

%% Re-arrange timetrace into ones and zeros
TRUE = 1;
FALSE = 0;
ontimes = [];
offtimes = [];

if (timetrace(1) > threshold)
    dot_on = TRUE;
else
    dot_on = FALSE;
end

% Keep track of whether we have been through the first region. See below
% for a further explanation.
past_first = FALSE;

current_time = 0;

for i=1:length(timetrace)
% We want to move along the trace and keep track of how long we remain
% either on or off. So, we have four possibilities:
% dot on, currently known as on
% dot off, currently known as on
% dot on, currently known as off
% do off, currently known as off
% If we are in a region and find ourselves still in that region, we
% increment and move on. If we are in a region and found ourselves in the
% other region, we must have moved across the border, so we add the length
% of our stay in the old region to the appropriate count, reset the
% counter, and record ourselves as being in the new region.
%
% We do not record the first or last regions; we do not know when they
% started or ended, so their statistics should be discarded.
    if timetrace(i) > threshold
        if dot_on == TRUE
            current_time = current_time + 1;
        else
            if past_first == TRUE
                offtimes = [offtimes current_time];
            else
                past_first = TRUE;
            end
            current_time = 1;
            dot_on = TRUE;
        end
    else
        if dot_on == FALSE
            current_time = current_time + 1;
        else
            if past_first == TRUE
                ontimes = [ontimes current_time];
            else
                past_first = TRUE;
            end
            current_time = 1;
            dot_on = FALSE;
        end
    end
end