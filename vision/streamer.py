"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition
Code for use on Raspberry Pi coprocessor
contact@team4096.org
"""

import subprocess
import signal

class Streamer:
	"""
	Update: this class is useless, just use cscore
	
	Used to start and interact with mpjg http camera streams
	Requires mjpg_streamer
	If ip and port are 10.40.96.18:5800, then the stream can be found at 10.40.96.18:5800/?action=stream
	"""

	def __init__(self, cam=0, res="320x240", fps=30, port=5800):
		"""
		Starts a stream with the currently defined settings
		"""
		
		self.cam = cam
		self.res = res
		self.fps = fps
		self.port = port
		
		self.process = subprocess.Popen(("mjpg_streamer "
				"-i \"input_uvc.so -d /dev/video{0} -r {1} -f {2}\" "
				"-o \"output_http.so -p {3}\"").format(
				self.cam, self.res, self.fps, self.port), shell=True)
	
	"""
	Checks if the stream is currently running
	"""
	def isRunning(self):
		return self.process.poll() == None
	
	"""
	Stops the stream gracefully
	"""
	def stop(self):
		self.process.send_signal(signal.SIGTERM)
			   
	"""
	Instantly kills the stream
	"""
	def kill(self):
		self.process.send_signal(signal.SIGKILL)