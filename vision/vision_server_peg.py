import cv2
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from networktables import NetworkTables
from grip_peg import GripPipeline as PegPipeline
from exposure import Exposure

pegCapture = None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
		self.end_headers()
		table = NetworkTables.getTable('/vision/')
		while table.getNumber('gear_camera_mode') == 1:
			pegOk, pegFrame = pegCapture.read()
			if pegOk:
				try:
					jpg = cv2.imencode('.jpeg', pegFrame)[1]
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

	# Publish to the '/vision/peg_targets' network table
	table = NetworkTables.getTable('/vision/peg_targets')
	table.putNumberArray('x', center_x_positions)
	table.putNumberArray('y', center_y_positions)
	table.putNumberArray('width', widths)
	table.putNumberArray('height', heights)

def main():
	print('Initializing NetworkTables for peg')
	NetworkTables.setClientMode( )
	NetworkTables.setIPAddress( '10.40.96.2' )
	NetworkTables.initialize( )

	print('Creating peg video capture ')
	global pegCapture
	pegCapture = cv2.VideoCapture("/dev/gear_camera")
	pegCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
	pegCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
	capture.set(cv2.CAP_PROP_FPS, 15)

	print('Creating peg pipeline')
	pegPipeline = PegPipeline()
	
	try:
		print("Starting peg server")
		server = ThreadedHTTPServer(('0.0.0.0', 5800), CamHandler)
		
		print('Running peg pipeline')
		table = NetworkTables.getTable('/vision/')
		while True:
			pegOk, pegFrame = pegCapture.read()
			if pegOk:
				print("ok")
				if table.getNumber('gear_camera_mode') == 0:
					print('Switching peg to GRIP mode')
					if Exposure.getExposure("/dev/gear_camera") != 10:
						Exposure.setExposure(10, "/dev/gear_camera")
					while table.getNumber('gear_camera_mode') == 0:
						pegPipeline.process(pegFrame)
						extra_processing(pegPipeline)
				else:
					print('Switching peg to stream mode')
					if Exposure.getExposure("/dev/gear_camera") != 100:
						Exposure.setExposure(100, "/dev/gear_camera")
					while table.getNumber('gear_camera_mode') == 1:
						server.handle_request()

	except KeyboardInterrupt:
		pegCapture.release()
		server.socket.close()

if __name__ == '__main__':
	main()
