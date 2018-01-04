import sys
import cv2
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
capture=None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
		self.end_headers()
		while True:
			try:
				ok, img = capture.read()
				if not ok:
					continue
				jpg = cv2.imencode('.jpeg', img)[1]
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

def main():
	global capture
	if len(sys.argv) > 1:
		capture = cv2.VideoCapture(sys.argv[1])
	else:
		capture = cv2.VideoCapture("/dev/gear_camera")
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
	capture.set(cv2.CAP_PROP_FPS, 15)
	global img
	try:
		if len(sys.argv) > 2:
			server = ThreadedHTTPServer(('0.0.0.0', int(sys.argv[2])), CamHandler)
			print("serving on port {0}".format(sys.argv[2]))
		else:
			server = ThreadedHTTPServer(('0.0.0.0', 5800), CamHandler)
			print("serving on port 5800")
		server.serve_forever()
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()

if __name__ == '__main__':
	main()
