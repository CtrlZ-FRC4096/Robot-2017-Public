#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.feeder

import const


class Run_Feeder( Command ):

	def __init__( self, robot, speed):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.feeder )
		self.setInterruptible( True )

		self.speed = speed


	def initialize( self ):
		'''
		Called just before this Command runs the first time
		'''
		pass


	def execute( self ):
		'''
		Called repeatedly when this Command is scheduled to run
		'''

		self.robot.feeder.run_feeder( self.speed )


	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True


	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		pass


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	
		

class Stop_Feeder( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.feeder )
		self.setInterruptible( True )

		self.speed = 0


	def initialize( self ):
		'''
		Called just before this Command runs the first time
		'''
		pass


	def execute( self ):
		'''
		Called repeatedly when this Command is scheduled to run
		'''

		self.robot.feeder.run_feeder( 0 )


	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True


	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		pass


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	
		

class Toggle_Feeder_Engaged( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.feeder )
		self.setInterruptible( True )

	def initialize( self ):
		'''
		Called just before this Command runs the first time
		'''
		pass


	def execute( self ):
		'''
		Called repeatedly when this Command is scheduled to run
		'''

		self.robot.feeder.toggle_feeder_state( )


	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True


	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		pass


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	
		
		

class Toggle_Feeder_Running( Command ):

	def __init__( self, robot,speed ):
		super( ).__init__( )

		self.robot = robot
		self.speed = speed
		self.requires( self.robot.feeder )


	def initialize( self ):
		pass


	def execute( self ):
		new_state = self.robot.feeder.toggle_feeder_running(self.speed)


	def isFinished( self ):
		return True
	


class Set_Feeder_State( Command ):

	def __init__( self, robot, state ):
		super( ).__init__( )

		self.robot = robot
		self.state = state
		
		self.requires( self.robot.feeder )


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.feeder.set_feeder_solenoid( self.state )


	def isFinished( self ):
		return True
	