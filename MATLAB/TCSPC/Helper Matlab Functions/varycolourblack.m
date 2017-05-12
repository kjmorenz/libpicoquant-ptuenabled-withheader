function ColorSet=varycolourblack(NumberOfPlots)

% This function is designed to produce a pleasing reasonably rainbow-ish
% array of colours for a black-background plot. It is modified from
% 'varycolour' (documentation below), which is in turn modified from
% VARYCOLOR.
%   - Mark W.B. Wilson, 2015-03-12

% This function is modified from the original (see below) so that colors
% range from a minimum of 'red' to a maximum of 'purple', passing through
% 'green'. The idea is to create a series of colours that works well from
% plots where temperature, or wavelength is the indpendent variable.
%   - Mark W.B. Wilson, 2012-03-11

    % The re-mapping of the colour spectrum to run from red to blue is
    % simply accomplished by resetting the vectors so they run from
    % black-->red-->yellow-->green-->cyan-->blue
    
    % Also, we include a scaling factor to avoid over-saturating the
    % yellow-->green-->cyan leg of the map, as well as a MagentaScale to
    % avoid having the 'ultra-blue' bit get all the way to magenta, which
    % could be construed as 'red-ish'.
       
    GreenScale=0.6;
    MagentaScale=0.7;

%%%%% Original Documentation

% VARYCOLOR Produces colors with maximum variation on plots with multiple
% lines.
%
%     VARYCOLOR(X) returns a matrix of dimension X by 3.  The matrix may be
%     used in conjunction with the plot command option 'color' to vary the
%     color of lines.  
%
%     Yellow and White colors were not used because of their poor
%     translation to presentations.
% 
%     Example Usage:
%         NumberOfPlots=50;
%
%         ColorSet=varycolor(NumberOfPlots);
% 
%         figure
%         hold on;
% 
%         for m=1:NumberOfPlots
%             plot(ones(20,1)*m,'Color',ColorSet(m,:))
%         end

%Created by Daniel Helmick 8/12/2008


error(nargchk(1,1,nargin))%correct number of input arguements??
error(nargoutchk(0, 1, nargout))%correct number of output arguements??

%Take care of the 'degenerate cases'
% --> where we have enough vectors to go around

if NumberOfPlots<1
    ColorSet=[];
elseif NumberOfPlots==1
    ColorSet=[1 1 1];
elseif NumberOfPlots==2
    ColorSet=[1 1 1; 1 0 0];
elseif NumberOfPlots==3
    ColorSet=[1 1 1; 1 0 0 ; 0 GreenScale 0];
elseif NumberOfPlots==4
    ColorSet=[1 1 1; 1 0 0 ; 0 GreenScale 0 ; 0 0 1];
elseif NumberOfPlots==5
    ColorSet=[1 1 1; 1 0 0 ; 1 GreenScale 0 ; 0 GreenScale 0 ; 0 0 1];
elseif NumberOfPlots==6
    ColorSet=[1 1 1; 1 0 0 ; 1 GreenScale 0 ; 0 GreenScale 0 ; 0 0 1 ; MagentaScale 0 1];
elseif NumberOfPlots==7
    ColorSet=[1 1 1; 1 0 0 ; 1 GreenScale 0 ; 0 GreenScale 0 ; 0 GreenScale 1 ; 0 0 1 ; MagentaScale 0 1];

else %default and where this function has an actual advantage
 
    %initialize our vector
    ColorSet=zeros(NumberOfPlots,3);
    
    %we have 6 segments to distribute the plots (--> from 7 'fencepost' vectors)
    EachSec=floor(NumberOfPlots/6); 
    
    %how many extra lines are there? 
    ExtraPlots=mod(NumberOfPlots,6); 
    
    %Distribute the 'remainder' plots into the bins for each segment
    Adjust=zeros(1,6);
    Adjust(1:ExtraPlots)=1;
    
    SecOne   =EachSec+Adjust(1);
    SecTwo   =EachSec+Adjust(2);
    SecThree =EachSec+Adjust(3);
    SecFour  =EachSec+Adjust(4);
    SecFive  =EachSec+Adjust(5);
    SecSix   =EachSec;
   
    % Generate sufficient colours by moving through each 'leg' of the
    % colourmap
    
    for m=1:SecOne
        ColorSet(m,:)=[(m-1)/(SecOne-1) 0 0];
        %   ColorSet(m,:)=[0 1 (m-1)/(SecOne-1)];
    end

    for m=1:SecTwo
        ColorSet(m+SecOne,:)=[1 ((m)/(SecTwo))*GreenScale 0];
        %   ColorSet(m+SecOne,:)=[0 (SecTwo-m)/(SecTwo) 1];
    end
    
    for m=1:SecThree
        ColorSet(m+SecOne+SecTwo,:)=[(SecThree-m)/(SecThree) GreenScale 0];
        %   ColorSet(m+SecOne+SecTwo,:)=[(m)/(SecThree) 0 1];
    end
    
    for m=1:SecFour
        ColorSet(m+SecOne+SecTwo+SecThree,:)=[0 GreenScale (m)/(SecFour)];
        %   ColorSet(m+SecOne+SecTwo+SecThree,:)=[1 0 (SecFour-m)/(SecFour)];
    end

    for m=1:SecFive
        ColorSet(m+SecOne+SecTwo+SecThree+SecFour,:)=[0 ((SecFive-m)/(SecFive))*0.8 1];
        %   ColorSet(m+SecOne+SecTwo+SecThree+SecFour,:)=[(SecFive-m)/(SecFive) 0 0];
    end
    
    for m=1:SecSix
        ColorSet(m+SecOne+SecTwo+SecThree+SecFour+SecFive,:)=[((m)/SecSix)*MagentaScale 0 1];
    end
    
end