"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition
Code for use on Raspberry Pi coprocessor
contact@team4096.org
"""

import sys
from exposure import Exposure

"""
Sets the exposure of /dev/video0 to the first arg passed or 10 if no args are passed
If 2 args are passed it sets the exposure of arg 2 to arg 1
"""
if len(sys.argv) < 3:
	print("Exposure is {0}".format(Exposure.getExposure()))
	Exposure.setExposure(10 if len(sys.argv) < 2 else sys.argv[1])
	print("Exposure is now {0}".format(Exposure.getExposure()))
else:
	print("Exposure is {0}".format(Exposure.getExposure()))
	Exposure.setExposure(10 if len(sys.argv) < 2 else sys.argv[1])
	print("Exposure is now {0}".format(Exposure.getExposure()))