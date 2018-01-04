"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition
Code for use on Raspberry Pi coprocessor
contact@team4096.org
"""

from networktables import NetworkTables
from grip_peg import GripPipeline as GearPipeline
from grip_boiler import GripPipeline as ShooterPipeline
from exposure import Exposure
import cscore as cs
import numpy as np
import cv2
import time

#EXPOSURE_DEFAULT = 5

def gear_extra_processing(pipeline):
	"""
	Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
	:param pipeline: the pipeline that just processed an image
	:return: None
	"""
	center_x_positions = []
	center_y_positions = []
	widths = []
	heights = []

	# Find the bounding boxes of the contours to get x, y, width, and height
	for contour in pipeline.filter_contours_output:
		x, y, w, h = cv2.boundingRect(contour)
		center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
		center_y_positions.append(y + h / 2)
		widths.append(w)
		heights.append(h)

	# Publish to the '/vision/peg_targets' network table
	table = NetworkTables.getTable('/vision/peg_targets')
	table.putNumberArray('x', center_x_positions)
	table.putNumberArray('y', center_y_positions)
	table.putNumberArray('width', widths)
	table.putNumberArray('height', heights)

def shooter_extra_processing(pipeline):
	"""
	Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
	:param pipeline: the pipeline that just processed an image
	:return: None
	"""
	center_x_positions = []
	center_y_positions = []
	widths = []
	heights = []

	# Find the bounding boxes of the contours to get x, y, width, and height
	for contour in pipeline.filter_contours_output:
		x, y, w, h = cv2.boundingRect(contour)
		center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
		center_y_positions.append(y + h / 2)
		widths.append(w)
		heights.append(h)

	# Publish to the '/vision/peg_targets' network table
	table = NetworkTables.getTable('/vision/boiler_targets')
	table.putNumberArray('x', center_x_positions)
	table.putNumberArray('y', center_y_positions)
	table.putNumberArray('width', widths)
	table.putNumberArray('height', heights)
	
def main():
	
	#print('Setting Exposures to 10')
	#Exposure.setExposure(10, '/dev/gear_camera')
	#Exposure.setExposure(10, '/dev/shooter_camera')
	
	print('Initializing NetworkTables')
	# Server is the roborio, ip 10.40.96.2
	NetworkTables.setClientMode()
	NetworkTables.setIPAddress('10.40.96.2')
	NetworkTables.initialize()
	
	# Start with vision
	#table = NetworkTables.getTable('SmartDashboard')
	#table.putBoolean('Gear Camera Stream', False)
	#table.putBoolean('Shooter Camera Stream', False)
	#table.putNumber('Cam Exposure', EXPOSURE_DEFAULT)

	print('Creating pipelines')
	gearPipeline = GearPipeline()
	shooterPipeline = ShooterPipeline()
	
	print('Starting servers')
	gear_cam = cs.UsbCamera('shooter','/dev/gear_camera')
	shooter_cam = cs.UsbCamera('gear','/dev/shooter_camera')

	gear_cam.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 15)
	shooter_cam.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 15)
	
	gear_cam.setExposureManual(0);
	shooter_cam.setExposureManual(0);
	
	gear_cam.setExposureHoldCurrent();
	shooter_cam.setExposureHoldCurrent();

	gear_server = cs.MjpegServer('gear_http_server', 5800)
	shooter_server = cs.MjpegServer('shooter_http_server', 5801)

	gear_server.setSource(gear_cam)
	shooter_server.setSource(shooter_cam)

	gear_sink = cs.CvSink('gear_sink')
	shooter_sink = cs.CvSink('shooter_sink')
	
	gear_sink.setSource(gear_cam)
	shooter_sink.setSource(shooter_cam)
	
	# initialize frames to save time later
	gear_frame = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
	shooter_frame = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
	
	#expo = EXPOSURE_DEFAULT
	#prev_expo = EXPOSURE_DEFAULT
	while True:
		#if table.getBoolean('Gear Camera Stream', False):
			#Exposure.setExposure(15, '/dev/gear_camera')
		#else:
			#Exposure.setExposure(70, '/dev/gear_camera')
		#if table.getBoolean('Shooter Camera Stream', False):
			#Exposure.setExposure(15, '/dev/shooter_camera')
		#else:
			#Exposure.setExposure(70, '/dev/shooter_camera')
		#if table.containsKey('Cam Exposure'):
			#expo = table.getNumber('Cam Exposure')
			#if expo != prev_expo:
				#Exposure.setExposure(expo, '/dev/gear_camera')
				#Exposure.setExposure(expo, '/dev/shooter_camera')
				#prev_expo = expo
		
		time, gear_frame = gear_sink.grabFrame(gear_frame)
		if time == 0: # Timeout
			print("error:", cvsink.getError())
		else:
			gearPipeline.process(gear_frame)
			gear_extra_processing(gearPipeline)
		time, shooter_frame = shooter_sink.grabFrame(shooter_frame)
		if time == 0: # Timeout
			print("error:", cvsink.getError())
		else:
			shooterPipeline.process(shooter_frame)
			shooter_extra_processing(shooterPipeline)

if __name__ == '__main__':
	main()
