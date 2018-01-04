#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import wpilib
import time
from wpilib.command.commandgroup import CommandGroup, Command
from wpilib.command.waitcommand import WaitCommand

import commands.feeder

import const


### CLASSES ###

class Claws_Quick_Toggle( CommandGroup ):
	"""
	This autonomous mode moves backwards, lowering the feeder as it
	approaches the low bar, goes under the low bar, then turns
	to face the tower.  It used to also take an auto shot but that's
	currently commented out.
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( Open_Gear_Claws( self.robot ) )
		self.addSequential( WaitCommand( 0.04 ) )
		self.addSequential( Close_Gear_Claws( self.robot ) )
		


class Close_Gear_Claws( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_claw )
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
		self.robot.gear_claw.close_gear_claws( )

	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True


	def end( self ):
		pass

	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	
		


class Close_Gear_Punch( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_claw )
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
		self.robot.gear_claw.close_gear_punch( )

	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True


	def end( self ):
		pass

	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	
		

class Open_Gear_Claws( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_claw )
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
		self.robot.gear_claw.open_gear_claws( )

	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True


	def end( self ):
		pass

	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	
		


class Open_Gear_Punch( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_claw )
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
		self.robot.gear_claw.open_gear_punch( )

	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True


	def end( self ):
		pass

	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	
		

class Punch_Quick_Toggle( CommandGroup ):
	"""
	This autonomous mode moves backwards, lowering the feeder as it
	approaches the low bar, goes under the low bar, then turns
	to face the tower.  It used to also take an auto shot but that's
	currently commented out.
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( Open_Gear_Punch( self.robot ) )
		self.addSequential( WaitCommand( 0.08 ) )
		self.addSequential( Close_Gear_Punch( self.robot ) )



class Toggle_Gear_Release( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_claw )
		self.requires( self.robot.feeder )


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.gear_claw.toggle_gear_container_state( )
		self.robot.feeder.toggle_feeder_state( )

	def isFinished( self ):
		return True

		
class Open_Container( CommandGroup ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_claw )
		self.requires( self.robot.feeder )
		
		self.addParallel( commands.feeder.Set_Feeder_State( self.robot, const.ID_FEEDER_DISENGAGED ) )
		self.addSequential( Open_Gear_Claws( self.robot ) )
		self.addSequential( WaitCommand( 0.06 ) )
		self.addSequential( Open_Gear_Punch( self.robot ) )
		

class Close_Container( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.gear_claw )
		self.requires( self.robot.feeder )


	def initialize( self ):
		pass

	def execute( self ):
		self.robot.gear_claw.close_gear_punch( )
		self.robot.gear_claw.close_gear_claws( )
		self.robot.feeder.set_feeder_solenoid( const.ID_FEEDER_ENGAGED )

	def isFinished( self ):
		return True
		

class Delayed_Close( CommandGroup ):
	
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( WaitCommand( 2.0 ) )
		self.addSequential( Close_Container( self.robot ) )
		

		
