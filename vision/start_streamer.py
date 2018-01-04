"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition
Code for use on Raspberry Pi coprocessor
contact@team4096.org
"""

from streamer import Streamer

"""
Starts a default mjpg stream
"""

stream = Streamer()

print(stream.isRunning())
input()
stream.stop()
print(stream.isRunning())
input()
stream.kill()
print(stream.isRunning())
input()
print(stream.isRunning())