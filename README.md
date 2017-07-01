# Synthetic Aperture Radar Calibration Using Snappy
---
This is a SAR Calibration tool made on top of SNAP (Sentinel Application Platform).
This tool is written in Python and uses the snappy module that comes with SNAP. 

#### Follow these instructions to configure snappy https://senbox.atlassian.net/wiki/display/SNAP/How+to+use+the+SNAP+API+from+Python 

---
How to use:
-------------------------

* First input the basic details of your data, like Frequency, Length of arm of reflector, etc. All this info is available in the metadata of your dataset. 
* Now it asks for the number of corner reflectors that were used for calibration. Also, it asks for the X and Y coordinates of the reflectors.
* Now the background processes will make calculations for Background Corrected Intensity, Subset means, and Bandmaths.
* The calculated value of the Calibration Constant for that band will be displayed in the console.
* A new window will contain all the plots of intensity around corner reflectors.
* Also a log file is generated in the project folder which contains all the parameter values.

Working Example
------------------------
###### 1)Open the program 
![open program](https://github.com/WVik/snappy-sar-calibration/blob/master/Pics/Screen%20Shot%202017-07-01%20at%201.19.57%20pm.png?raw=true)


