"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.gear_funnel
import const

class Set_Gear_Funnel_State( Command ):

	def __init__( self, robot, state ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_funnel )

		self.state = state


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.gear_funnel.set_gear_funnel_state( self.state )


	def isFinished( self ):
		return True
	
	
class Toggle_Gear_Funnel_State( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_funnel )


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.gear_funnel.toggle_gear_funnel_state( )


	def isFinished( self ):
		return True