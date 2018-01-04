#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.climber

import const



class Run_Climber( Command ):

	def __init__( self, robot, speed):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.climber )
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

		self.robot.climber.run_climber( self.speed )


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
		
		

class Stop_Climber( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.climber )
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

		self.robot.climber.run_climber( 0 )


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