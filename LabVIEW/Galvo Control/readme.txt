2017-02-07
This script enables both scanning the laser the spot across a sample, and holding the laser spot steady at a user defined position.
Either of these options can be selected by clicking on the appropriate radio button within the program.

In "Scan" mode, the user will define a range of voltages through which they wish to scan.  At the moment (2017-02-07), 1.5<V<-1.5 for both axes is more than enough
to cover the entirety of the objective.  To scan in the "X" direction, set the upper option to "Dev2/ao1" and select your voltage range.  To scan in the "Y" direction, set the upper
option to "Dev2/ao0".  The wait time defines how long the laser spot will be held at a given position before moving onto the next position.  100ms is default, and should be sufficient
to distinguish between signal and noise.  The lower device output should be set to the opposite of the scanning direction, i.e. if you have chosen to scan in "X" (Dev2/ao1), set the 
lower option to "Dev2/ao0".  The voltage range here is not as important, just make sure it covers the entirety of the objective, and in general selecting the same range as your scanning voltage will suffice.  The wait time should be chosen to match the wait time of the scanning axis.  The voltage step option allows for choice of discrete voltage increments.  The default value is 0.1V.

Once parameters are set, press the arrow button in the top left corner of the window, to be found under the "Edit" menu option.  The mirrors will begin to scan across the sample.  Once the scan is complete, you will receive a message informing you the program executed correctly.



In "Hold" mode, the user will first run the program by clicking the arrow button as above.  The positions of the mirrors can then by dynamically updated by inputting the desired voltage.  Type in the desired voltages value into the "Output Voltage" boxes available on the screen.  Press <Enter>.  The mirrors will move to the position corresponding to the voltage value.  Do not select the same analog outputs for both top and bottom dropdown boxes, i.e. if the top box reads "Dev2/ao0" ensure that the bottom dropdown box reads "Dev2/ao1".  "Dev2/ao0" corresponds to "Y"-axis control, and "Dev2/ao1" corresponds to "X"-axis control. The order is irrelevant, as long as the two values are not the same.  Do not change the max/min voltages in "Hold" mode.  These are set so that the mirrors do not receive a signal larger than they can handle.  For the time being (2017-02-07), use the stop button found to the right of the run program button, to be found under the "Project" menu option.  The program will exit, however the mirrors will stay at the last updated position.  In "Hold" mode, no message will be seen if the program executed correctly.  

Troubleshooting:

