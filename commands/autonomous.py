"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import wpilib

from wpilib.command.commandgroup import CommandGroup
from wpilib.command import WaitCommand

import const
import commands.drivetrain
import commands.gear_lexan
import commands.agitator
import commands.shooter

#Variables for Command "Move_To_Gear"
#CG_INITIAL_APPROACH_DISTANCE = 3.5

### CLASSES ###

class Shoot_From_Hopper( CommandGroup ):
	"""
	This autonomous mode does... wait for it... something.
	"""

	def __init__( self, robot, side_id ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( commands.drivetrain.Set_State_H_Drive( self.robot ) )
		self.addSequential( commands.gear_lexan.Set_Gear_Lexan_State( self.robot, const.ID_GEAR_LEXAN_OPEN ) )	
		if side_id == const.ID_AUTO_RED_SIDE:
			# Red Alliance
			# Initial forward driving
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 5.70, max_speed = 1.0 ), 3.5 ) #we want to go 6.5 + 1.5 feet
			
			self.addSequential( WaitCommand( 0.50 ) )
			self.addSequential( commands.drivetrain.Rotate_To_Angle( self.robot, 90 ), 3.0 )
			self.addSequential( commands.shooter.Run_Shooter_Wheel( self.robot ) )
			# Hitting the hopper
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 4.50, max_speed = 1.0 ), 3.0 ) #we want to go 8 feet
		else:
			# Blue Alliance
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, -5.65, max_speed = -1.0 ), 3.5 ) #we want to go 6.5 + 1.5 feet
			self.addSequential( WaitCommand( 0.50 ) )
			self.addSequential( commands.drivetrain.Rotate_To_Angle( self.robot, -90 ), 3.0 )
			self.addSequential( commands.shooter.Run_Shooter_Wheel( self.robot ) )
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, -4.50, max_speed = -1.0 ), 3.0 ) #we want to go 8 feet
	
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.drivetrain.Rotate_To_Boiler( self.robot ), 3.0 )
		self.addSequential( commands.drivetrain.Stop( self.robot ) )
		self.addSequential( commands.agitator.Run_Agitator( self.robot, 1.0 ) )
		#self.addSequential( WaitCommand( 15.00 ) )
		#self.addSequential( commands.agitator.Stop_Agitator( self.robot ) )
		#self.addSequential( commands.shooter.Stop_Shooter_Wheel( self.robot ) )
		

class Shoot_From_Start( CommandGroup ):
	"""
	This autonomous mode does... wait for it... something.
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot
		self.addSequential( commands.shooter.Run_Shooter_Wheel( self.robot ) )
		self.addSequential( WaitCommand( 2.0 ) )
		self.addSequential( commands.agitator.Run_Agitator( self.robot, 1.0 ) )
		self.addSequential( WaitCommand( 5.0 ) )
		self.addSequential( commands.drivetrain.Drive_Distance(self.robot, 7.0, max_speed = 0.4), 3.5 )
		
		        



class Do_Nothing( CommandGroup ):
	"""
	This autonomous mode does... wait for it... nothing.
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( commands.drivetrain.Stop( self.robot ) )


class Cross_Baseline( CommandGroup ):
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, .8, 0), 3.00 )
		self.addSequential( commands.drivetrain.Stop( self.robot ) )
		

class Center_Gear_Without_Camera( CommandGroup ):
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		# Align to gear target, drive up to it and deposit gear
		#self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 5 )
		#self.addSequential( commands.drivetrain.Drive_Distance_To_Gear( self.robot, 5.0, 3.0, 0.65 ), 5.0 )
		#self.addSequential( WaitCommand( 0.25 ) )
		#self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 5 )
		#self.addSequential( WaitCommand( 0.50 ) )

		#self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 5 ) #total was 4.777
		#self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 2.5 ), 3.0 )
		#self.addSequential( WaitCommand( 0.50 ) )
		#self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 5 )
		#self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 2.277 ), 7.0 )
		#self.addSequential( WaitCommand( 0.50 ) )

		self.addSequential( commands.drivetrain.Set_State_H_Drive( self.robot ) )
		#self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 6.55 ), 3.5 )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, .5, 0), 4.68 )
		
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0 , -.5 , 0 ), .20 )
		##self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot,  0, 0 , .4 ), .25 )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot,  0, .5 , 0 ), .35 )
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot,  0, 0 , -.4 ), .25 )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot,  0, .5 , 0 ), .35 )
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0 ,-.5 , 0 ), .30 )
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.gear_claw.Open_Container( self.robot ), timeout= .5 )



		#self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, .5 , 0 , 0 ), .50 )


		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, -.6, 0 ), timeout = 0.75 ) # usual timeout 0.75
		self.addSequential( commands.gear_claw.Close_Container( self.robot ) )


class Move_To_Gear_And_Shoot( CommandGroup ):
	def __init__( self, robot, side_id ):
		super( ).__init__( )

		self.robot = robot
		
		if side_id == const.ID_AUTO_RED_SIDE:
			# Red Alliance
			# First move to the correct peg and deposit gear
			self.addSequential( Move_To_Gear( self.robot, const.ID_AUTO_RIGHT_GEAR ) )			
			# Position to take 10-ball shot
			self.addSequential( commands.drivetrain.Rotate_To_Angle( self.robot, 100.0 ), timeout = 5 )
		else:
			# Blue Alliance
			# First move to the correct peg and deposit gear
			self.addSequential( Move_To_Gear( self.robot, const.ID_AUTO_LEFT_GEAR ) )			
			# Position to take 10-ball shot			
			self.addSequential( commands.drivetrain.Rotate_To_Angle( self.robot, 67.5 ), timeout = 5 )

		# Start shooter wheel
		self.addSequential( commands.shooter.Run_Shooter_Wheel( self.robot ) )
		
		# Strafe closer to boiler
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( commands.drivetrain.Rotate_To_Boiler( self.robot ), 3.0 )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, 0, -0.85 ), 0.90 ) #-0.85 for 1.5 seconds brings us 5 feet from the center of the boiler we want to be around 7 feet
		
		# Let GRIP values catch up
		self.addSequential( WaitCommand( 0.50 ) )
		# Rotate to face boiler			
		self.addSequential( commands.drivetrain.Rotate_To_Boiler( self.robot ), 3.0 )
		
		# Fire
		self.addSequential( commands.agitator.Run_Agitator( self.robot, 1.0 ) ) #-1.0 on the practice bot
		
			
class Move_To_Center_Gear_And_Shoot( CommandGroup ):
	def __init__( self, robot, side_id ):
		super( ).__init__( )

		self.robot = robot
		
		if side_id == const.ID_AUTO_RED_SIDE:
			# Red Alliance
			# First move to the correct peg and deposit gear
			self.addSequential( Move_To_Gear( self.robot, const.ID_AUTO_CENTER_GEAR ) )
			# Position to take 10-ball shot
			self.addSequential( commands.drivetrain.Rotate_To_Angle( self.robot, 0.0 ), timeout = 5 )
		else:
			# Blue Alliance
			# First move to the correct peg and deposit gear
			self.addSequential( Move_To_Gear( self.robot,  const.ID_AUTO_CENTER_GEAR ) )
			# Position to take 10-ball shot			
			self.addSequential( commands.drivetrain.Rotate_To_Angle( self.robot, 180.0 ), timeout = 5 )

		# Start shooter wheel
		self.addSequential( commands.shooter.Run_Shooter_Wheel( self.robot ) )
		
		# Strafe closer to boiler
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, 0, -0.85 ), 0.80 ) #-0.85 for 1.5 seconds brings us 5 feet from the center of the boiler we want to be around 7 feet
	
		# Let GRIP values catch up
		self.addSequential( WaitCommand( 0.50 ) )
		# Rotate to face boiler			
		self.addSequential( commands.drivetrain.Rotate_To_Boiler( self.robot ), 3.0 )
		
		# Fire
		self.addSequential( commands.agitator.Run_Agitator( self.robot, 0.9 ) ) #-1.0 on the practice bot
		


class Move_To_Gear( CommandGroup ):
	def __init__( self, robot, gear_id ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( commands.drivetrain.Set_State_H_Drive( self.robot ) )
		self.addSequential( commands.drivetrain.Set_Gear_State_Low( self.robot ) )
		#self.addSequential( commands.drivetrain.Set_State_Tank( self.robot ) )


		if gear_id == const.ID_AUTO_CENTER_GEAR:
			# Center gear
			# Vision align (1 of 2)
			self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 5 )

			# Initial approach
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 3.3, max_speed = 1.0 ), 3.70 ) #currently goes 4' 8"
			self.addSequential( WaitCommand( 0.50 ) )			
			
		else:								
			# One of the side gears, so start by driving forward and turning left or right
			# Initial approach
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 6.25, max_speed = 1.0 ), 3.5 ) #we want 90"
			self.addSequential( WaitCommand( 0.50 ) )			
			
			if gear_id == const.ID_AUTO_RIGHT_GEAR:
				# Gear on right of airship
				turn_degrees = -55 #was 68
			else:
				# Gear on left of airship
				turn_degrees = 55

			# Do the turn
			self.addSequential( WaitCommand( 0.50 ) )
			self.addSequential( commands.drivetrain.Rotate_To_Angle( self.robot, turn_degrees ), timeout = 5 )
			self.addSequential( WaitCommand( 0.75 ) )
			#self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 5 )

		# Drive_With_Tank_Values
		# x = rotate
		# y = forward/back  + = forward, - = backward
		# z = strafe

		# Vision align (2 of 2)
		self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 3 )
		self.addSequential( commands.drivetrain.Rotate_To_Gear( self.robot ), timeout = 3 )

		# Final approach
		if gear_id == const.ID_AUTO_CENTER_GEAR:
			# Center peg
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 4.0, max_speed = 0.65 ), 2.0 )
		else:
			# Side peg
			self.addSequential( commands.drivetrain.Drive_Distance( self.robot, 4.0, max_speed = 0.65 ), 2.0 )

		# Strafe jiggle to make sure gear is speared
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, 0.7, .60 ), .1 )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, 0.7, -.60 ), .2 )
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, 0.7, .60 ), .1 )

		# Reverse a little to give gear room to eject onto peg
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, -.5, 0 ), .30 )

		# Eject
		self.addSequential( commands.gear_claw.Open_Container( self.robot ), timeout= .2 )
		self.addSequential( WaitCommand( 0.25 ) )
		self.addSequential( commands.gear_claw.Close_Container( self.robot ) )
		self.addSequential( WaitCommand( 0.25 ) )
		self.addSequential( commands.gear_claw.Open_Container( self.robot ) )
		self.addSequential( WaitCommand( 0.50 ) )
		#self.addSequential( commands.gear_claw.Close_Container( self.robot ), timeout = .1 )
		#self.addSequential( commands.gear_claw.Open_Container( self.robot ), timeout= .2 )

		# Pull back and close claw
		self.addSequential( commands.drivetrain.Drive_With_Tank_Values( self.robot, 0, -.6, 0 ), 1.30 ) # currently goes 41"
		self.addSequential( commands.gear_claw.Close_Container( self.robot ) )
		

