"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition
Code for use on Raspberry Pi coprocessor
contact@team4096.org
"""

import subprocess

class Exposure:
	"""
	Used to control the exposure of webcams
	Only tested with Logitech C920 HD PRO
	Requires uvcdynctrl
	"""

	@staticmethod
	def setExposure(value, cam='/dev/video0'):
		"""
		Sets the exposure of a camera using uvcdynctrl.
		:param value: the exposure value to set to
		:param cam (optional): camera to control, default /dev/video0
		"""
		try:
			subprocess.call( 'uvcdynctrl -d $(realpath {0}) -s "Exposure, Auto" 1'.format(cam), shell=True)
			subprocess.call( 'uvcdynctrl -d $(realpath {0}) -s "Exposure, Auto Priority" 0'.format(cam), shell=True)
			subprocess.call( 'uvcdynctrl -d $(realpath {0}) -s "Exposure (Absolute)" {1}'.format(cam, value), shell=True)
			print('Set exposure of {0} to {1}'.format(cam, value))
		except (subprocess.CalledProcessError) as e:
			print('Failed to set exposure of {0} to {1}:\n{2}'.format(cam, value, e.output))
	
	@staticmethod
	def setExposureAuto(cam='/dev/video0'):
		"""
		Sets the exposure of a camera to auto mode using uvcdynctrl.
		:param cam (optional): camera to control, default /dev/video0
		"""
		try:
			subprocess.call( 'uvcdynctrl -d $(realpath {0}) -s "Exposure, Auto" 3'.format(cam), shell=True)

			print('Set exposure of {0} to auto mode'.format(cam))
		except (subprocess.CalledProcessError) as e:
			print('Failed to set exposure of {0} to auto mode:\n{1}'.format(cam, e.output))

	@staticmethod
	def getExposure(cam='/dev/video0'):
		"""
		Gets the exposure of a camera using uvcdynctrl.
		:param cam (optional): camera to query, default /dev/video0
		:return: the current exposure
		"""
		try:
			exposure = int(subprocess.check_output('uvcdynctrl -d $(realpath {0}) -g "Exposure (Absolute)"'.format(cam), shell=True))
			return exposure
		except (subprocess.CalledProcessError) as e:
			print('Failed to get exposure of {0}:\n{1}'.format(cam, e.output))
