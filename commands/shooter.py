#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import wpilib
import wpilib.command
from wpilib.command.commandgroup import Command, CommandGroup

import const

import commands.agitator


### CLASSES ###

class Run_Shooter( CommandGroup ):
	"""
	"""

	def __init__( self, robot, shooter_speed ):
		super( ).__init__( )

		self.robot = robot
		self.shooter_speed = shooter_speed

		self.requires( self.robot.agitator )
		self.requires( self.robot.shooter )
		self.setInterruptible( True )

		# Run shooter wheel for 1 second before starting agitator
		#self.addSequential( commands.agitator.Run_Agitator( self.robot, -0.2 ), timeout=0.0 )
		#self.addSequential( Run_Shooter_Wheel( self.robot, self.shooter_speed ), timeout = 1.0 )
		self.addSequential( Run_Shooter_Wheel(self.robot), timeout=1.0)
		# Now start shooter wheel
		self.addParallel( commands.agitator.Run_Agitator( self.robot, 1.0 ) )
		#self.addSequential( Run_Shooter_Wheel( self.robot, self.shooter_speed ) )
		self.addSequential( Run_Shooter_Wheel(self.robot))

class Run_Shooter_Wheel_Full_Speed( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.shooter )
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
		#print( 'SHOOTING {0}'.format( self.speed ) )
		self.robot.shooter.run_shooter( 4200 )


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

class Run_Shooter_Wheel( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.shooter )
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
		#print( 'SHOOTING {0}'.format( self.speed ) )
		self.robot.shooter.run_shooter( const.SHOOTER_SPEED )


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
		

class Stop_Shooter( CommandGroup ):
	"""
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.agitator )
		self.requires( self.robot.shooter )
		self.setInterruptible( True )

		self.addParallel( commands.agitator.Stop_Agitator( self.robot ) )
		self.addSequential( Stop_Shooter_Wheel( self.robot ) )



class Stop_Shooter_Wheel( Command ):

	def __init__( self, robot ):

		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.shooter )
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

		self.robot.shooter.stop_shooter( )


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