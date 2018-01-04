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

class Climber( wpilib.command.Subsystem ):
	def __init__( self, robot ):
		super( ).__init__( 'climber' )
		self.robot = robot

		# The climber has two motors, but they are connected to one pwm because of a y cable
		self.climber_motor_1 = wpilib.VictorSP( const.ID_CLIMBER_MOTOR_1 )

	def run_climber( self, value ):
		self.climber_motor_1.set( value )

	def stop_climber(self):
		self.climber.run_climber( 0.0 )

	def end( self ):
		self.stop_climber( )
		
	def cancel( self ):
		"""
		If bound to a button using whileHeld, will be called once when button is released
		"""
		self.end( )
		super( ).cancel( )		

		
	def log( self ):
		pass

