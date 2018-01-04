"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017
Code for robot "Nona Drive"
contact@team4096.org
"""

import math
import sys

import wpilib
import wpilib.command
import networktables


import const
import time


### CONSTANTS ###

#ID_MOTOR_FRONT_LEFT		= 2
#ID_MOTOR_REAR_LEFT			= 3
#ID_MOTOR_FRONT_RIGHT		= 0
#ID_MOTOR_REAR_RIGHT		= 1

# Old Values from CIR:
#DEFAULT_KP = 0.009
#DEFAULT_KI = 0.00
#DEFAULT_KD = 0.02

# New aggressive rotate PID from MWR
#DEFAULT_KP = 0.025
#DEFAULT_KI = 0.00
#DEFAULT_KD = 0.04

## New less aggressive rotate PID from MWR
DEFAULT_KP = 0.013
DEFAULT_KI = 0.00
DEFAULT_KD = 0.025

### CLASSES ###

class Drivetrain( wpilib.command.PIDSubsystem ):

	def __init__( self, robot ):

		super( ).__init__( DEFAULT_KP, DEFAULT_KI, DEFAULT_KD, name = 'drive' )

		self.robot = robot

		self.default_kP = DEFAULT_KP
		self.default_kI = DEFAULT_KI
		self.default_kD = DEFAULT_KD

		self.kP = DEFAULT_KP
		self.kI = DEFAULT_KI
		self.kD = DEFAULT_KD

		# Configure PID stuff
		self.setAbsoluteTolerance( 1.0 )
		self.getPIDController( ).setContinuous( False )

		self.drive = wpilib.RobotDrive( frontLeftMotor = const.ID_DRIVE_MOTOR_FRONT_LEFT,
		                                rearLeftMotor = const.ID_DRIVE_MOTOR_REAR_LEFT,
										frontRightMotor = const.ID_DRIVE_MOTOR_FRONT_RIGHT,
										rearRightMotor = const.ID_DRIVE_MOTOR_REAR_RIGHT )

		# Invert motors
		self.drive.setInvertedMotor( const.ID_DRIVE_MOTOR_FRONT_LEFT, True )
		self.drive.setInvertedMotor( const.ID_DRIVE_MOTOR_REAR_LEFT, True )
		self.drive.setInvertedMotor( const.ID_DRIVE_MOTOR_FRONT_RIGHT, True )
		self.drive.setInvertedMotor( const.ID_DRIVE_MOTOR_REAR_RIGHT, True )
		
		# Strafe
		self.strafe_wheel_1 = wpilib.VictorSP( const.ID_STRAFE_WHEEL_1 )
		self.strafe_wheel_2 = wpilib.VictorSP( const.ID_STRAFE_WHEEL_2 )
		
		#self.frontLeftMotor = wpilib.VictorSP(const.ID_DRIVE_MOTOR_FRONT_LEFT)
		#self.rearLeftMotor = wpilib.VictorSP(const.ID_DRIVE_MOTOR_REAR_LEFT)
		#self.frontRightMotor = wpilib.VictorSP(const.ID_DRIVE_MOTOR_FRONT_RIGHT)
		#self.rearRightMotor = wpilib.VictorSP(const.ID_DRIVE_MOTOR_REAR_RIGHT)

		self.drive_state = const.ID_TANK
		self.gear_state = const.ID_LOW_GEAR

		self.shift_solenoid_1 = wpilib.Solenoid( const.ID_PCM_1, const.ID_DRIVE_SOLENOID_SHIFTER_1 )
		self.shift_solenoid_2 = wpilib.Solenoid( const.ID_PCM_1, const.ID_DRIVE_SOLENOID_SHIFTER_2 )

		self.actuate_solenoid_1 = wpilib.Solenoid( const.ID_PCM_1, const.ID_DRIVE_SOLENOID_ACTUATOR_1 )
		self.actuate_solenoid_2 = wpilib.Solenoid( const.ID_PCM_1, const.ID_DRIVE_SOLENOID_ACTUATOR_2 )
		
		self.strafe_wheel_solenoid_1 = wpilib.Solenoid( const.ID_PCM_1, const.ID_STRAFE_WHEEL_SOLENOID_1 )
		self.strafe_wheel_solenoid_2 = wpilib.Solenoid( const.ID_PCM_1, const.ID_STRAFE_WHEEL_SOLENOID_2 )

		self.r = 0.0
		self.corrected_rotation = 0.0
		self.y = 0.0
		self.x = 0.0
		self.sensitivity = 1.0
		
		self.pid_forward_speed = 0.0
		
		self._was_correcting = False	
		self._correction_start_angle = None


	def set_pid_forward_speed( self, speed ):
		self.pid_forward_speed = speed

	def returnPIDInput( self ):
		return self.robot.gyro.getAngle( )


	def usePIDOutput( self, output ):
		# invert it
		output = -float( output )

		# Reduce the max output to 50%
		#output = output / 2.0
		min_output = const.DRIVE_MIN_ROTATION_OUTPUT_OMNI if (self.drive_state == const.ID_H_DRIVE) else const.DRIVE_MIN_ROTATION_OUTPUT_TANK
		#min_output = wpilib.SmartDashboard.getNumber( 'PID Tank Min Rotation Threshold: ' )

		# Make sure we're outputing at least enough to move the robot at all
		if output < 0:
			output = min( output, -min_output )
		elif output > 0:
			output = max( output, min_output )

		#wpilib.SmartDashboard.putString( 'Drive Rotate PID Output: ', '{0:.3f}'.format( output ) )
		if( self.onTarget( ) ):
			output = 0
			
		self.drive_with_tank_values( output, self.pid_forward_speed, 0)
		#self.drive_with_tank_values( output, 0, 0)
		
	def run( self, rotation ):
		self.drive_with_tank_values( rotation, 0, 0)


	def update_pid( self, p = None, i = None, d = None ):
		'''
		Updates the PID coefficients
		'''
		if p:
			self.kP = p
		if i:
			self.kI = i
		if d:
			self.kD = d

		self.getPIDController( ).setPID( self.kP, self.kI, self.kD )




	def set_drive_state( self, state ):
		"""
		Start of change state of drivetrain code. Changes the state by activating
		The solenoids which should push out/in the pistons.
		"""
		self.drive_state = state

		if state == const.ID_H_DRIVE:
			# Switch to H-DRIVE/OMNI
			# might be messed up
			self.actuate_solenoid_1.set( True )
			self.actuate_solenoid_2.set( False )
			
			if const.STRAFE_WHEELS_DISABLED:
				# Keep strafe wheels raised
				self.strafe_wheel_solenoid_1.set( True )
				self.strafe_wheel_solenoid_2.set( False )
			else:
				self.strafe_wheel_solenoid_1.set( False )
				self.strafe_wheel_solenoid_2.set( True )
				
			self.robot.drive_encoder_left.setDistancePerPulse( const.DRIVE_DISTANCE_PER_ENCODER_TICK_OMNI )
			self.robot.drive_encoder_right.setDistancePerPulse( const.DRIVE_DISTANCE_PER_ENCODER_TICK_OMNI )
			self.robot.drive_encoder_left.reset( )
			self.robot.drive_encoder_right.reset( )
						
		else:
			# Switch to tank
			self.actuate_solenoid_1.set( False )
			self.actuate_solenoid_2.set( True )
			self.strafe_wheel_solenoid_1.set( True )
			self.strafe_wheel_solenoid_2.set( False )
			self.robot.drive_encoder_left.setDistancePerPulse( const.DRIVE_DISTANCE_PER_ENCODER_TICK_TANK )
			self.robot.drive_encoder_right.setDistancePerPulse( const.DRIVE_DISTANCE_PER_ENCODER_TICK_TANK )			
			self.robot.drive_encoder_left.reset( )
			self.robot.drive_encoder_right.reset( )			


	def get_drive_state( self ):
		return self.drive_state


	def toggle_drive_state( self ):
		if self.drive_state == const.ID_H_DRIVE:
			self.set_drive_state( const.ID_TANK )
			return const.ID_TANK
		else:
			self.set_drive_state( const.ID_H_DRIVE )
			return const.ID_H_DRIVE

	def toggle_gear_state( self ):
		if self.gear_state == const.ID_LOW_GEAR:
			self.set_gear_state( const.ID_HIGH_GEAR )
			return const.ID_HIGH_GEAR
		else:
			self.set_gear_state( const.ID_LOW_GEAR )
			return const.ID_LOW_GEAR

	def set_gear_state( self, state ):
			"""
			Start of change state of drivetrain code. Changes the state by activating
			The solenoids which should push out/in the pistons.
			"""
			self.gear_state = state

			if state == const.ID_LOW_GEAR:
				self.shift_solenoid_1.set( True )
				self.shift_solenoid_2.set( False )
			else:
				self.shift_solenoid_1.set( False )
				self.shift_solenoid_2.set( True )


	def get_gear_state( self ):
		return self.gear_state

	def drive_with_tank_joysticks( self, left_axis, right_axis ):
		"""
		needs work, and support for correction
		"""
		self.drive.arcadeDrive( leftValue = left_axis( ), rightValue = right_axis( ) )


	def set_sensitivity ( self, sensitivity ):
		self.sensitivity = sensitivity

	def _get_corrected_rotation_gyro( self, rotation_value, y_value, strafe_value ):
		"""
		If gyro drive correction is enabled, and the user isn't manually rotating the
		robot, let the gyro angle correct the rotation.
		"""
		if not const.DRIVE_CORRECTION_ENABLED:
			wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'DISABLED' )
			self._correction_start_angle = None
			return rotation_value

		if ( abs( strafe_value ) > 0.1 or abs( y_value ) > 0.025 ) and abs(rotation_value) < const.DRIVE_CORRECTION_ROTATION_THRESHOLD:
			# This means driver is moving forward/back or strafing, but NOT rotating
			if self._correction_start_angle is None:
				# We were not correcting last time, so save gyro angle and start correcting to that
				self.robot.gyro.reset( )
				self._correction_start_angle = self.robot.gyro.getAngle( )
				return rotation_value

			else:
				# We're correcting so adjust rotation
				if y_value > 0 :
					tmp_correction_proportion = const.DRIVE_CORRECTION_PROPORTION_FORWARD
				else:
					tmp_correction_proportion = const.DRIVE_CORRECTION_PROPORTION_REVERSE

				correction_amt = ( self._correction_start_angle - self.robot.gyro.getAngle( ) ) * tmp_correction_proportion * -1
				rotation_value += correction_amt
				wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'ACTIVE - {0:.4f}'.format( correction_amt ) )
				wpilib.SmartDashboard.putNumber( 'Drive Correction Int: ', 1.0)
		else:
			wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'INACTIVE' )
			wpilib.SmartDashboard.putNumber( 'Drive Correction Int: ', 0.0)
			self._correction_start_angle = None

		return rotation_value
	
	def _get_corrected_rotation_enc( self, rotation_value, y_value, strafe_value ):
		
		if not const.DRIVE_CORRECTION_ENABLED:
			wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'DISABLED' )
			self._was_correcting = False
			return rotation_value

		if ( abs( y_value ) > 0.025 ) and abs(rotation_value) < const.DRIVE_CORRECTION_ROTATION_THRESHOLD:
			# This means driver is moving forward/back, but NOT rotating
			if self._was_correcting == False:
				# We were not correcting last time, so save gyro angle and start correcting to that
				self.robot.drive_encoder_right.reset( )
				self.robot.drive_encoder_left.reset( )
				self._was_correcting = True
				return rotation_value

			else:
				# We're correcting so adjust rotation
				if y_value > 0 :
					tmp_correction_proportion = const.DRIVE_CORRECTION_PROPORTION_FORWARD_ENC
				else:
					tmp_correction_proportion = const.DRIVE_CORRECTION_PROPORTION_REVERSE_ENC

				correction_amt = ( self.robot.drive_encoder_right.get( ) - self.robot.drive_encoder_left.get( ) ) * -tmp_correction_proportion
				rotation_value += correction_amt
				wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'ACTIVE - {0:.4f}'.format( correction_amt ) )
				wpilib.SmartDashboard.putNumber( 'Drive Correction Int: ', 1.0)
		else:
			wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'INACTIVE' )
			wpilib.SmartDashboard.putNumber( 'Drive Correction Int: ', 0.0)
			self._was_correcting = False

		return rotation_value	

	def run_full_forward( self, speed ):
		self.frontLeftMotor.set( speed )
		self.frontRightMotor.set( speed )
		self.rearLeftMotor.set( speed )
		self.rearRightMotor.set( speed )
		
	def drive_with_tank_values( self, rotation_value, y_value, strafe_value ):
		"""
		needs work, and support for correction
		"""
		
		self.r = rotation_value
		self.y = y_value * self.sensitivity
		if self.get_drive_state() != const.ID_H_DRIVE:
			self.x = 0
		else:
			self.x = strafe_value

		corrected_rotation_value = self._get_corrected_rotation_enc( rotation_value, y_value, strafe_value )
		self.corrected_rotation = corrected_rotation_value

		#if self.robot.gear_switch.get( ) and self.sensitivity != 1.0:
			#if self.y > 0:
				#self.y = 0

		#print(rotation_value)
		#print( 'rotation = {0:.2f}'.format( corrected_rotation_value ) )
		
		y_value = self.y
		rot_value = corrected_rotation_value

		if const.DEMO_MODE:
			# When doing demos, limit speed by some amount
			y_value = y_value * const.DEMO_TOP_SPEED_MULTIPLIER
			rot_value = rot_value * const.DEMO_TOP_SPEED_MULTIPLIER
			
		self.drive.arcadeDrive( y_value, rot_value )
		self.strafe_wheel_1.set( -self.x )
		self.strafe_wheel_2.set( -self.x )	
	
	def drive_with_tank_and_gear_camera( self, rotation_value, y_value, strafe_value ):
		"""
		needs work, and support for correction
		"""
		
		self.r = rotation_value
		self.y = y_value
		if self.get_drive_state() != const.ID_H_DRIVE:
			self.x = 0
		else:
			self.x = strafe_value

		#corrected_rotation_value = self._get_corrected_rotation_enc( rotation_value, y_value, strafe_value )
		#self.corrected_rotation = corrected_rotation_value
		angle_to_target = self.robot.gear_camera.calculate_angle( )
		rotation = angle_to_target / -6.0
		
		if rotation < -0.5:
			rotation = -0.5
		elif rotation > 0.5:
			rotation = 0.5
			
		#rotation = max( rotation, 0.8 )
		
		if self.robot.gear_switch.get( ):
			if y_value > 0:
				y_value = 0
				
		distance = self.calculate_distance( )
		speed = (0.5 + (0.05 * distance) )

		#print(rotation_value)
		#self.drive.arcadeDrive( y_value, rotation )
		self.drive.arcadeDrive( speed, rotation )
		self.strafe_wheel_1.set( -self.x * self.sensitivity )
		self.strafe_wheel_2.set( -self.x * self.sensitivity )
		
		wpilib.Timer.delay(2)

	def calculate_distance( self ):
		#creates a dictionary "target_values" that contains the grip values for the objects detected
		#the array is made up of 5 arrays which are accessed by name "x","y","width","height","area"
		target_values = self.robot.gear_camera.get_target_values( )

		#print( target_values )
	
		#check the number of "height" values we have which is equivalent to the number of targets
		if len( target_values[ 'height' ] ) == 0:
			# No vision targets found
			#print( 'No vision targets found' )
			return 0

		elif len( target_values[ 'height' ] ) == 1:
			#print( 'Only one of two targets found' )
			height = target_values[ 'height' ][ 0 ]
		else:
			#print( 'Two or more targets were found' )
			height = (target_values[ 'height' ][ 0 ] + target_values[ 'height' ][ 1 ]) / 2

		#print("  height: ", height)

		#equation for distance
		distance = const.TARGET_FEET_HEIGHT * const.CAMERA_RES_Y / ( 2 * height * 0.37 )
		#print( " height: ", height)
		#print (" distance: ", distance)

		return distance

	def stop( self ):
		self.drive_with_tank_values(0, 0, 0)
		self.drive.stopMotor( )


	def log( self ):
		'''
		logs various things about the robot
		'''
		drive_values = '{0:.2f}, {1:.2f}, {2:.2f}'.format( self.y, self.x, self.r )
		wpilib.SmartDashboard.putString( 'Drive Values (y,x,r): ', drive_values )
		drive_values = '{0:.2f}, {1:.2f}, {2:2f}'.format( self.y, self.x, self.corrected_rotation )
		wpilib.SmartDashboard.putString( 'Drive Values Corrected (y,x,r): ', drive_values )
		
		wpilib.SmartDashboard.putString( 'Gyro: ', '{0:.02f}'.format( self.robot.gyro.getAngle( ) ) )
		if( self.drive_state == const.ID_H_DRIVE ):
			wpilib.SmartDashboard.putString( 'Drive State: ', ' OMNI ' )
		else:
			wpilib.SmartDashboard.putString( 'Drive State: ', ' TANKS ' )
			
		if( self.gear_state == const.ID_LOW_GEAR ):
			wpilib.SmartDashboard.putString( 'Drivetrain Gear:', ' LOW ' )
		else:
			wpilib.SmartDashboard.putString( 'Drivetrain Gear:', ' HIGH ' )		
			
		if hasattr( self.robot, 'drive_encoder_left' ):
			rate_left = self.robot.drive_encoder_left.getDistance( )
			raw_left = self.robot.drive_encoder_left.get( )	
			distance_left = self.robot.drive_encoder_left.getDistance( )
			rate_left = self.robot.drive_encoder_left.getRate( )
			wpilib.SmartDashboard.putString( 'drive encoder left:', '{0:.4f}'.format( raw_left ) )
			wpilib.SmartDashboard.putString( 'drive encoder left distance:', distance_left )
			wpilib.SmartDashboard.putString( 'drive encoder left rate:',  rate_left  )

			rate_right = self.robot.drive_encoder_right.getDistance( )
			raw_right = self.robot.drive_encoder_right.get( )
			distance_right = self.robot.drive_encoder_right.getDistance( )
			rate_right = self.robot.drive_encoder_right.getRate( )
			wpilib.SmartDashboard.putString( 'drive encoder right:', '{0:.4f}'.format( raw_right ) )	
			wpilib.SmartDashboard.putString( 'drive encoder right distance:', distance_right  )
			wpilib.SmartDashboard.putString( 'drive encoder right rate:', rate_right )
			
			#wpilib.SmartDashboard.putNumber( 'Calculated Distance', self.calculate_distance( ) )