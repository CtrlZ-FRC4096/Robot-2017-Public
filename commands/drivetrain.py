"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import wpilib
from wpilib.command.commandgroup import Command, CommandGroup
from wpilib.command.waitcommand import WaitCommand

#import commands.drivetrain

import const
import subsystems.drivetrain


### CLASSES ###

#class Full_Speed_Ahead( Command ):

	#def __init__( self, robot ):
		#super( ).__init__( )

		#self.robot = robot

		#self.requires( self.robot.drive )


	#def initialize( self ):
		#pass


	#def execute( self ):
		#self.robot.drive.run_full_forward( 1.0 )


	#def isFinished( self ):
		#return True
	

#class Full_Speed_Back( Command ):

	#def __init__( self, robot ):
		#super( ).__init__( )

		#self.robot = robot

		#self.requires( self.robot.drive )


	#def initialize( self ):
		#pass


	#def execute( self ):
		#self.robot.drive.run_full_forward( -1.0 )


	#def isFinished( self ):
		#return True

#class Full_Speed_Stop( Command ):

	#def __init__( self, robot ):
		#super( ).__init__( )

		#self.robot = robot

		#self.requires( self.robot.drive )


	#def initialize( self ):
		#pass


	#def execute( self ):
		#self.robot.drive.run_full_forward( 0.0 )


	#def isFinished( self ):
		#return True
	
	
class Back_Up( CommandGroup ):
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot
		self.addSequential( Drive_Distance(self.robot, -0.20, max_speed = -0.65 ), timeout=2.0 ) #actually going around 0.3
		#self.addSequential( Drive_With_Tank_Values(self.robot, 0, 0, 0) , timeout = 0.0 )

class Spinmove( CommandGroup):
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot
		
		self.addSequential( Drive_With_Tank_Values(self.robot, 0, .8, 0), timeout=0.75 ) # usual timeout 0.75
		self.addSequential( Drive_With_Tank_Values(self.robot, .8, 1.0, 0), timeout=1.5 ) # usual timeout 0.75
		self.addSequential( Drive_With_Tank_Values(self.robot, 0, .8, 0), timeout=0.75 ) # usual timeout 0.75
	

class Drive_To_Gear( CommandGroup ):
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		#self.addSequential( Set_State_Tank( self.robot ), timeout=0.0 )
		#self.addSequential( Rotate_To_Gear( self.robot ), timeout=5 )
		#self.addSequential( Drive_Distance_To_Gear(robot, 4, 2.5, .60 ), 4.0)
		#self.addSequential( Rotate_To_Gear_And_Forward( self.robot ), 3.0)
		#self.addSequential( Drive_With_Tank_Values(self.robot, 0, 0, 0), .25 )
		#self.addSequential( Drive_With_Tank_Values(self.robot, 0, -.7, 0), timeout=0.75 ) # usual timeout 0.75		
		
		#self.addSequential( Set_State_Tank( self.robot ), timeout=0.0 )
		self.addSequential( Rotate_To_Gear( self.robot ), timeout=5 )
		self.addSequential( Drive_Distance_To_Gear( self.robot, 5.0, 3.0, 0.65 ), 5.0 )
		self.addSequential( WaitCommand( 0.25 ) )
		self.addSequential( Rotate_To_Gear( self.robot ), timeout=5 )
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( Drive_Distance_To_Gear( self.robot, 5.0, 0.0, 0.4 ), 3.0 )		
		self.addSequential( WaitCommand( 0.50 ) )
		self.addSequential( Drive_With_Tank_Values(self.robot, 0, -.7, 0), timeout=0.75 ) # usual timeout 0.75
		

class Drive_To_Gear_2( Command ):
	def __init__ ( self, robot ):
		super( ).__init__( )
		
		self.robot = robot
		
		self.check_alligned_timer = wpilib.Timer( )
		self.check_alligned_timer.start( )
		self.distance_to_gear = 0
		#self.speed = 0
		self.setInterruptible( True )
		self.setTimeout( 4.0 )
		
	def initialize( self ):
		self.distance_to_gear = 5.0
		#self.speed = 0

	def execute( self ):
		if(self.check_alligned_timer.hasPeriodPassed( 4.0 ) ):
			print( "resetting timer")
			self.robot.gyro.reset( )
			self.check_alligned_timer.reset( )
			self.distance_to_gear = self.robot.drive.calculate_distance( )
			#self.speed = 0.6 + ( (0.4) * self.distance_to_gear)
			#self.robot.drive.set_pid_forward_speed( self.speed )
			self.angle = self.robot.gear_camera.calculate_angle( )
			self.robot.drive.enable( )
			self.robot.drive.setSetpoint( self.angle )

	def isFinished( self ):
		if( self.distance_to_gear < 3.0 or self.isTimedOut( ) ):
			self.robot.drive.disable( )
			self.robot.drive.drive_with_tank_values( 0, 0, 0 )
			return True

	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		self.robot.drive.drive_with_tank_values( 0, 0, 0 )


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )		

class Drive_With_Tank_Values( Command ):

	def __init__( self, robot, get_r, get_y, get_x):
		'''
		initializes mecanum drive movement.
		:param robot: the robot object
		:param get_x: Used to get the x angle, function that determines y direction
		:param get_y: Used to get the y angle, function that determines the y value and direction
		:param get_z: Used to get the z angle, function that determines
		rotation and direction of rotation. Z value must be given if it separate from the joystick.
		'''
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )
		self.setInterruptible( True )

		self.get_r = get_r
		self.get_y = get_y
		self.get_x = get_x


	def initialize( self ):
		'''
		Called just before this Command runs the first time
		'''
		pass


	def execute( self ):
		'''
		Called repeatedly when this Command is scheduled to run
		'''

		# If in tank mode, still use mecanum drive code but force X/strafe to zero
		r = self.get_r( ) if callable( self.get_r ) else self.get_r
		y = self.get_y( ) if callable( self.get_y ) else self.get_y
		x = self.get_x( ) if callable( self.get_x ) else self.get_x

		# Not doing field-centric, so always pass 0 for gyro value
		self.robot.drive.drive_with_tank_values( r, y, x )


	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return False


	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		self.robot.drive.stop( )


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )
		
		
		
class Drive_With_Tank_And_Gear_Camera( Command ):

	def __init__( self, robot, get_r, get_y, get_x):
		'''
		initializes mecanum drive movement.
		:param robot: the robot object
		:param get_x: Used to get the x angle, function that determines y direction
		:param get_y: Used to get the y angle, function that determines the y value and direction
		:param get_z: Used to get the z angle, function that determines
		rotation and direction of rotation. Z value must be given if it separate from the joystick.
		'''
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )
		self.setInterruptible( True )

		self.get_r = get_r
		self.get_y = get_y
		self.get_x = get_x


	def initialize( self ):
		'''
		Called just before this Command runs the first time
		'''
		pass


	def execute( self ):
		'''
		Called repeatedly when this Command is scheduled to run
		'''

		# If in tank mode, still use mecanum drive code but force X/strafe to zero
		r = self.get_r( ) if callable( self.get_r ) else self.get_r
		y = self.get_y( ) if callable( self.get_y ) else self.get_y
		x = self.get_x( ) if callable( self.get_x ) else self.get_x

		# Not doing field-centric, so always pass 0 for gyro value
		self.robot.drive.drive_with_tank_and_gear_camera( r, y, x )


	def isFinished( self ):
		if self.robot.drive.calculate_distance( ) < 3.0:
			self.robot.drive.stop( )
			return True
		

	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		self.robot.drive.stop( )


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )
			
				

class Get_Distance( Command ):
	def __init__( self, robot ):

		super( ).__init__( )
		self.robot = robot		
		self.requires( self.robot.drive )
		#self.setTimeout( 1 )
		self.setInterruptible( True )

	def initialize( self ):
		Drive_Distance( self.robot, self.robot.drive.calculate_distance( ) )

	def execute( self ):
		pass

	def isFinished( self ):
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


class Drive_Distance( Command ):
	def __init__ ( self, robot, distance, max_speed = 0.4 ):
		super( ).__init__( )
		
		self.robot = robot
		
		self.requires( self.robot.drive )
		self.distance = distance
		self.max_speed = max_speed
		
		self.driving_straight = (distance > 0) # true if distance is positive
		self.distance_remaining = distance
		self.distance_traveled = 0.0
		self.setTimeout( 6 )
		
		
	def initialize( self ):
		print("resetting")
		self.robot.drive_encoder_left.reset( )
		self.robot.drive_encoder_right.reset( )

	def execute( self ):
		self.distance_traveled = (self.robot.drive_encoder_left.getDistance( ) + self.robot.drive_encoder_right.getDistance( )) / 2
		self.distance_remaining = self.distance - self.distance_traveled
		
		#curr_speed = 0.40 + (.06 * self.distance_remaining)
		percent_distance = self.distance_traveled / self.distance
		half_speed = self.max_speed / 2.0
		
		curr_speed = half_speed + half_speed * 0.333 + half_speed * 0.666 * ( 1.0 - percent_distance )
		
		self.robot.drive.drive_with_tank_values( 0, curr_speed, 0 )


	def isFinished( self ):
		if self.driving_straight:
			if self.distance_remaining < 0.0 or self.isTimedOut( ):
				self.robot.drive.drive_with_tank_values( 0, 0, 0 )
				return True
		else:
			if (self.distance_remaining > 0.0 or self.isTimedOut( ) ):
				self.robot.drive.drive_with_tank_values( 0, 0, 0)
				return True			

	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		self.robot.drive.stop( )


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )	 	
		

class Drive_Distance_To_Gear( Command ):
	def __init__ ( self, robot, est_distance, subtract, speed ):
		super( ).__init__( )
		
		self.robot = robot
		self.est_distance = est_distance;
		self.requires( self.robot.drive )
		self.distance = 0
		self.distance_remaining = 0
		self.distance_traveled = 0.0
		self.subtract = subtract
		self.speed = speed
		self.setTimeout( 5.0 )	
		
	def initialize( self ):
		print("resetting")
		self.distance = self.robot.drive.calculate_distance( )
		if ( self.distance == 0.0 ):
			self.distance = self.est_distance
		self.distance = self.distance - self.subtract
		self.distance_remaining = self.distance
		self.robot.drive_encoder_left.reset( )
		self.robot.drive_encoder_right.reset( )

	def execute( self ):
		self.distance_traveled = (self.robot.drive_encoder_left.getDistance( ) + self.robot.drive_encoder_right.getDistance( )) / 2
		self.distance_remaining = self.distance - self.distance_traveled
		#print("distance Remaining: ", self.distance_remaining )
		self.curr_speed = self.speed + ( (0.1 - (self.speed / 10)) * self.distance_remaining)
		#self.curr_speed = 0.5 + ( 0.05 * self.distance_remaining)
		self.robot.drive.drive_with_tank_values( 0, self.curr_speed, 0)

	def isFinished( self ):
		if (self.distance_remaining < 0.0 or self.isTimedOut( ) or self.robot.gear_switch.get( ) ):
			self.robot.drive.drive_with_tank_values( 0, 0, 0)
			return True

	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		self.robot.drive.stop( )


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )


class Rotate_To_Angle( Command ):
	def __init__( self, robot, angle ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )
		self.angle = angle
		self.setTimeout( 10 )

		#print( 'rotating to {0:.2f}'.format( self.angle ))


	def initialize( self ):
		self.robot.drive.set_pid_forward_speed( 0.0 )
		self.robot.gyro.reset( )
		#print( 'gyro start = {0:.2f}'.format( self.robot.gyro.getAngle( )))
		self.robot.drive.enable( )
		self.robot.drive.setSetpoint( self.angle )


	def execute( self ):
		"""Called repeatedly"""


	def isFinished( self ):
		on_target = self.robot.drive.onTarget( )
		#timed_out = self.isTimedOut( )

		#if timed_out:
			#print( 'Timed out!' )
		if on_target:
			print( 'On Target! {0:.2f}'.format( self.robot.gyro.getAngle( ) ) )

		finished = self.robot.drive.onTarget( ) or self.isTimedOut( )

		#wpilib.SmartDashboard.putString( 'Feeder Lift PID Finished: ', '{0}'.format( finished ) )
		return finished


	def end( self ):
		"""
		Called once after isFinished returns true
		"""
		#print( 'gyro end = {0:.2f}'.format( self.robot.gyro.getAngle( )))
		self.robot.drive.disable( )
		#not sure if this can just be self.robot.drive.stop()


	def interrupted( self ):
		"""
		Called when another thing which requires one or more of the same subsystem is scheduled to run
		"""
		self.end( )
		


class Rotate_To_Angle_And_Forward( Command ):
	def __init__( self, robot, angle ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )
		self.angle = angle
		self.setTimeout( 10 )

		#print( 'rotating to {0:.2f}'.format( self.angle ))


	def initialize( self ):
		self.robot.drive.set_pid_forward_speed( 0.53 )
		self.robot.gyro.reset( )
		#print( 'gyro start = {0:.2f}'.format( self.robot.gyro.getAngle( )))
		self.robot.drive.enable( )
		self.robot.drive.setSetpoint( self.angle )


	def execute( self ):
		"""Called repeatedly"""


	def isFinished( self ):
		on_target = self.robot.drive.onTarget( )
		#timed_out = self.isTimedOut( )

		#if timed_out:
			#print( 'Timed out!' )
		if on_target:
			print( 'On Target! {0:.2f}'.format( self.robot.gyro.getAngle( ) ) )

		finished = self.robot.drive.onTarget( ) or self.isTimedOut( )

		#wpilib.SmartDashboard.putString( 'Feeder Lift PID Finished: ', '{0}'.format( finished ) )
		return finished


	def end( self ):
		"""
		Called once after isFinished returns true
		"""
		#print( 'gyro end = {0:.2f}'.format( self.robot.gyro.getAngle( )))
		self.robot.drive.disable( )
		#not sure if this can just be self.robot.drive.stop()


	def interrupted( self ):
		"""
		Called when another thing which requires one or more of the same subsystem is scheduled to run
		"""
		self.end( )


class Rotate_To_Gear( Rotate_To_Angle ):
	def __init__( self, robot ):

		self.robot = robot

		angle = 0	# gets set for real in initialize below

		super( ).__init__( self.robot, angle )


	def initialize( self ):
		angle = self.robot.gear_camera.calculate_angle( )

		distance = self.robot.drive.calculate_distance( )
		print("distance in rotation code: ", distance)
		if (distance < const.MIN_DISTANCE_FROM_PEG):
			angle = 0

		self.angle = angle

		super( ).initialize( )


	def execute( self ):
		pass


	def isFinished( self ):
		return super( ).isFinished( )
	

class Rotate_To_Boiler( Rotate_To_Angle ):
	def __init__( self, robot ):

		self.robot = robot

		angle = 0	# gets set for real in initialize below

		super( ).__init__( self.robot, angle )


	def initialize( self ):
		angle = self.robot.shooter_camera.calculate_shooter_angle( )

		self.angle = angle

		super( ).initialize( )


	def execute( self ):
		pass


	def isFinished( self ):
		return super( ).isFinished( )
	
	

class Rotate_To_Gear_And_Forward( Rotate_To_Angle_And_Forward ):
	def __init__( self, robot ):

		self.robot = robot

		angle = 0	# gets set for real in initialize below
		#self.distance_remaining = 0.0
		#self.distance = 0.0
		super( ).__init__( self.robot, angle )


	def initialize( self ):
		angle = self.robot.gear_camera.calculate_angle( )
		self.angle = angle

		#self.distance = self.robot.drive.calculate_distance( ) - 1.0
		#self.distance_remaining = self.distance 
		#self.robot.drive_encoder_left.reset( )
		#self.robot.drive_encoder_right.reset( )		

		super( ).initialize( )


	def execute( self ):
		#self.distance_traveled = (self.robot.drive_encoder_left.getDistance( ) + self.robot.drive_encoder_right.getDistance( )) / 2
		#self.distance_remaining = self.distance - self.distance_traveled
		#self.curr_speed = 0.4 + .06 * self.distance_remaining
		#self.robot.drive.set_pid_forward_speed( self.curr_speed )
		pass

	def isFinished( self ):
		return  self.robot.gear_switch.get( )
		#return super( ).isFinished( )

		

class Set_Gear_State_High( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		new_state = self.robot.drive.set_gear_state( const.ID_HIGH_GEAR )


	def isFinished( self ):
		return True
	
	
class Set_Gear_State_Low( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		new_state = self.robot.drive.set_gear_state( const.ID_LOW_GEAR )


	def isFinished( self ):
		return True
	

class Set_Rotation_Angle( Command ):

	def __init__( self, robot, angle ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive ) 
		self.angle = angle
		self.setTimeout( 10 )

		#print( 'rotating to {0:.2f}'.format( self.angle ))


	def initialize( self ):
		self.robot.gyro.reset( )
		#self.robot.navx.reset( )
		#print( 'gyro start = {0:.2f}'.format( self.robot.gyro.getAngle( )))
		self.robot.drive.enable( )
		self.robot.drive.setSetpoint( self.angle )


	def execute( self ):
		"""Called repeatedly"""


	def isFinished( self ):
		on_target = self.robot.drive.onTarget( )
		#timed_out = self.isTimedOut( )

		#if timed_out:
			#print( 'Timed out!' )
		if on_target:
			print( 'On Target! {0:.2f}'.format( self.robot.gyro.getAngle( ) ) )
			#print( 'On Target! {0:.2f}'.format( self.robot.navx.getAngle( ) ) )

		finished = self.robot.drive.onTarget( ) or self.isTimedOut( ) 

		#wpilib.SmartDashboard.putString( 'Feeder Lift PID Finished: ', '{0}'.format( finished ) )
		return finished


	def end( self ):
		"""
		Called once after isFinished returns true
		"""
		#print( 'gyro end = {0:.2f}'.format( self.robot.gyro.getAngle( )))
		self.robot.drive.disable( )
		#not sure if this can just be self.robot.drive.stop()


	def interrupted( self ):
		"""
		Called when another thing which requires one or more of the same subsystem is scheduled to run
		"""
		self.end( )
		

class Set_Sensitivity_High( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.drive.set_sensitivity( 1.0 )


	def isFinished( self ):
		return True
	


class Set_Sensitivity_Low( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.drive.set_sensitivity( const.ID_LOW_SENSITIVITY )


	def isFinished( self ):
		return True
	
	

class Set_State_H_Drive( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		new_state = self.robot.drive.set_drive_state( const.ID_H_DRIVE )


	def isFinished( self ):
		return True
	
	
	
class Set_State_Tank( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		new_state = self.robot.drive.set_drive_state( const.ID_TANK )


	def isFinished( self ):
		return True
	
	

class Stop( Command ):

	def __init__( self, robot ):
		'''
		'''
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )
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
		self.robot.drive.drive_with_tank_values( 0, 0, 0 )


	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True



class Toggle_Drive_State( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.drive.toggle_drive_state( )


	def isFinished( self ):
		return True
	
	
	
class Toggle_Gear_State( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		self.robot.drive.toggle_gear_state( )


	def isFinished( self ):
		return True