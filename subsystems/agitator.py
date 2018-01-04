#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import math
import sys

import wpilib
import ctre
import wpilib.command
import networktables

import const
import time

class Agitator( wpilib.command.Subsystem ):
	def __init__( self, robot ):
		super( ).__init__( 'agitator' )
		self.robot = robot

		# The climber has two motors, but they are connected to one pwm because of a y cable
		self.agitator_motor_1 = wpilib.VictorSP( const.ID_AGITATOR_MOTOR_1 )
		self.agitator_motor_1.setInverted( True ) #true on practice robot
		
		self.speed = 0

	def toggle_agitator( self, value ):
		if self.speed == 0:
			self.run_agitator( value )
		else:
			self.run_agitator( 0.0 )
		return

	def run_agitator( self, value ):
		#print( 'running agitator {0}'.format( value ) )
		self.speed = value
		self.agitator_motor_1.set( value )

	def stop_agitator(self):
		self.agitator_motor_1.set( 0.0 )

	def log( self ):
		pass

