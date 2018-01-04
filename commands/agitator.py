#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.agitator

import const


class Run_Agitator( Command ):

	def __init__( self, robot, speed ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.agitator )
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

		self.robot.agitator.run_agitator( self.speed )


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



class Stop_Agitator( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.agitator )
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

		self.robot.agitator.stop_agitator( )


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
		
		
class Toggle_Agitator( Command ):

	def __init__( self, robot, speed ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.agitator )
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

		self.robot.agitator.toggle_agitator( self.speed )


	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return False


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