
import cscore as cs
import time

gear_cam = cs.UsbCamera("gear","/dev/gear_camera")
shooter_cam = cs.UsbCamera("shooter","/dev/shooter_camera")

gear_cam.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 15)
shooter_cam.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 15)

gear_server = cs.MjpegServer("gear_http_server", 5800)
shooter_server = cs.MjpegServer("shooter_http_server", 5801)

gear_server.setSource(gear_cam)
shooter_server.setSource(shooter_cam)

print("Server started on ports 5800 and 5801")
while True:
	time.sleep(0.1)
