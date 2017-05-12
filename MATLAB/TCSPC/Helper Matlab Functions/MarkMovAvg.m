function DataOut=MarkMovAvg(DataIn,SmoothNum)

% This is a cheesy little function to do a symmetric moving average filter
% on a row-vector. The advantage is that it does not shift the data in
% time (which the normal 'filter' function seems to do, and handles the 
% 'edges' by padding the vector with copies of the first and last value, 
% running the filter, and then extracting the proper range at the end.

% Check for non-integer kernel sizes

if SmoothNum~=floor(SmoothNum)
    error('Function cannot accept non-integer filter kernel sizes')
end

% Reduce even 'SmoothNum's by one to ensure odd (symmetric) kernels

if SmoothNum/2==floor(SmoothNum/2)
    SmoothNum=SmoothNum-1;
end    

% Check if DataIn is a row or column Vector

if size(DataIn,1)~=1 && size(DataIn,2)~=1
    error('MarkMovAvg function can only handle vectors, check inputs');
end

if size(DataIn,2)==1
    DataIn=DataIn';
    IsCol=true;
else
    IsCol=false;
end

% Pad data

DataLength=length(DataIn);

FrontPad=repmat(DataIn(1),1,(SmoothNum-1)/2);
BackPad=repmat(DataIn(end),1,(SmoothNum-1)/2);

PaddedData=[FrontPad DataIn BackPad];

% Perform moving average

DataOut=zeros(1,DataLength);

for i=1:DataLength
    DataOut(i)=sum(PaddedData(i:i+(SmoothNum-1)))/SmoothNum;
end

% Re-transpose data if the input was a column

if IsCol
    DataOut=DataOut';
end

end

