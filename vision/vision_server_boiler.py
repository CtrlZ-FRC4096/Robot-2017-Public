import cv2
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from networktables import NetworkTables
from grip_peg import GripPipeline as BoilerPipeline #temporary fix so we can test streams
from exposure import Exposure

boilerCapture = None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
		self.end_headers()
		table = NetworkTables.getTable('/vision/')
		while table.getNumber('shooter_camera_mode') == 1:
			boilerOk, boilerFrame = boilerCapture.read()
			if boilerOk:
				try:
					jpg = cv2.imencode('.jpeg', boilerFrame)[1]
					enc = bytearray(jpg)
					self.wfile.write(b"--jpgboundary")
					self.send_header(b'Content-type',b'image/jpeg')
					self.send_header(b'Content-length',len(enc))
					self.end_headers()
					self.wfile.write(enc)
				except (KeyboardInterrupt, BrokenPipeError):
					break
		return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def extra_processing(pipeline):
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

	# Publish to the '/vision/boiler_targets' network table
	table = NetworkTables.getTable('/vision/boiler_targets')
	table.putNumberArray('x', center_x_positions)
	table.putNumberArray('y', center_y_positions)
	table.putNumberArray('width', widths)
	table.putNumberArray('height', heights)

def main():
	print('Initializing NetworkTables for boiler')
	NetworkTables.setClientMode( )
	NetworkTables.setIPAddress( '10.40.96.2' )
	NetworkTables.initialize( )

	print('Creating boiler video capture ')
	global boilerCapture
	boilerCapture = cv2.VideoCapture("/dev/shooter_camera")
	boilerCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320) 
	boilerCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
	capture.set(cv2.CAP_PROP_FPS, 15)

	print('Creating boiler pipeline')
	boilerPipeline = BoilerPipeline()
	
	try:
		print("Starting boiler server")
		server = ThreadedHTTPServer(('0.0.0.0', 5801), CamHandler)
		
		print('Running boiler pipeline')
		table = NetworkTables.getTable('/vision/')
		while True:
			boilerOk, boilerFrame = boilerCapture.read()
			if boilerOk:
				print("ok")
				if table.getNumber('shooter_camera_mode') == 0:
					print('Switching boiler to GRIP mode')
					if Exposure.getExposure("/dev/shooter_camera") != 10:
						Exposure.setExposure(10, "/dev/shooter_camera")
					while table.getNumber('shooter_camera_mode') == 0:
						boilerPipeline.process(boilerFrame)
						extra_processing(boilerPipeline)
				else:
					print('Switching boiler to stream mode')
					if Exposure.getExposure("/dev/shooter_camera") != 100:
						Exposure.setExposure(100, "/dev/shooter_camera")
					while table.getNumber('shooter_camera_mode') == 1:
						server.handle_request()

	except KeyboardInterrupt:
		boilerCapture.release()
		server.socket.close()

if __name__ == '__main__':
	main()
