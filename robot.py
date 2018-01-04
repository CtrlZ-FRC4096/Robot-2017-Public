#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import logging
import os
import time

import wpilib
import wpilib.sendablechooser
import wpilib.smartdashboard
import wpilib.command

import networktables

import robotpy_ext.autonomous
import robotpy_ext.control.xbox_controller

import subsystems.agitator
import subsystems.drivetrain
import subsystems.shooter
import subsystems.shooter_camera
import subsystems.climber
import subsystems.gear_funnel
import subsystems.gear_lexan
import subsystems.gear_claw
import subsystems.feeder
import subsystems.gear_camera

import controls.xbox_controller
import oi
import const

import commands.drivetrain
import commands.gear_funnel
import commands.gear_lexan

log = logging.getLogger( 'robot' )

# Uncomment following line to deploy files in this folder to the
# Raspberry Pi
#RPI_VISION_DIR = "vision"


class Robot( wpilib.IterativeRobot ):
	"""
	Main robot class.

	This is the central object, holding instances of all the robot subsystem
	and sensor classes.

	It also contains the init & periodic methods for autonomous and
	teloperated modes, called during mode changes and repeatedly when those
	modes are active.

	The one instance of this class is also passed as an argument to the
	various other classes, so they have full access to all its properties.
	"""
	def robotInit( self ):

		# Gear plate limit switch
		self.gear_switch = wpilib.DigitalInput( const.ID_GEAR_SWITCH )

		### Subsystems ###

		# Agitator
		self.agitator = subsystems.agitator.Agitator( self )

		# Climber
		self.climber = subsystems.climber.Climber( self )

		# Drive for Xbox Controller
		self.drive = subsystems.drivetrain.Drivetrain( self )

		# Gear
		self.gear_funnel = subsystems.gear_funnel.Gear_Funnel( self )
		self.gear_lexan = subsystems.gear_lexan.Gear_Lexan( self )
		self.gear_claw = subsystems.gear_claw.Gear_Claw( self )

		# Ground Feeder
		self.feeder = subsystems.feeder.Feeder( self )

		# Shooter
		self.shooter = subsystems.shooter.Shooter( self )

		# Shooter Camera
		self.shooter_camera = subsystems.shooter_camera.Shooter_Camera( self )

		# Gear Camera
		self.gear_camera = subsystems.gear_camera.Gear_Camera( self )


		# Encoders
		self.drive_encoder_left = wpilib.Encoder( 2, 3, reverseDirection = True )
		self.drive_encoder_left.setDistancePerPulse( const.DRIVE_DISTANCE_PER_ENCODER_TICK_OMNI )
		self.drive_encoder_left.reset( )

		self.drive_encoder_right = wpilib.Encoder( 0, 1, reverseDirection = False )
		self.drive_encoder_right.setDistancePerPulse( const.DRIVE_DISTANCE_PER_ENCODER_TICK_OMNI )
		self.drive_encoder_right.reset( )

		# Pressure sensor (200 psi)
		self.pressure_sensor = wpilib.AnalogInput( const.ID_PRESSURE_SENSOR )
		self._pressure_samples = [ ]
		self._last_pressure_value = 0.0

		# Gyro
		self.gyro = wpilib.ADXRS450_Gyro( )
		#self.gyro = wpilib.AnalogGyro( 0 )
		#self.gyro.setSensitivity( 0.08 )

		### Misc ###

		# Operator Input
		self.oi = oi.OI( self )

		# Log to file
		self.log_file = open( os.path.join( os.path.dirname( __file__ ), 'log.csv' ), 'w' )

		# Time robot object was created
		self.start_time = time.time( )

		## Autonomous ##

		self.subsystems = {
		    'agitator' : self.agitator,
		    'climber' : self.climber,
			'drive':	self.drive,
		    'gear_funnel' : self.gear_funnel,
		    'gear_lexan' : self.gear_lexan,
		    'gear_claw' : self.gear_claw,
		    'feeder' : self.feeder,
		    'shooter_camera': self.shooter_camera,
		    'gear_camera' : self.gear_camera,
		    'shooter' : self.shooter,
		}

		## Scheduler ##

		self.scheduler = wpilib.command.Scheduler.getInstance( )

		## MISC ##

		self.gear_is_ejecting = False
		self.gear_ejecting_start_time = 0

		### Logging ###

		# NetworkTables
		self.nt_smartdash = networktables.NetworkTable.getTable( 'SmartDashboard' )
		self.nt_grip_peg = networktables.NetworkTable.getTable( 'vision/peg_targets' )
		self.nt_grip_boiler = networktables.NetworkTable.getTable( 'vision/boiler_targets' )
		self.nt_vision = networktables.NetworkTable.getTable( 'vision' )


		# Timers for NetworkTables update so we don't use too much bandwidth
		self.log_timer = wpilib.Timer( )
		self.log_timer.start( )
		self.log_timer_delay = 0.1		# 10 times/second

		# Timer for pressure sensor's running average
		self.pressure_timer = wpilib.Timer( )
		self.pressure_timer.start( )
		self.pressure_timer_delay = 1.0		# once per second

		self.log( )


	### Disabled ###

	def disabledInit( self ):
		"""
		Runs once when disabled
		"""
		self.nt_vision.putBoolean('isTeleop', False)


	def disabledPeriodic( self ):
		"""
		Runs perodically when disabled
		"""
		pass


	### Autonomous ###

	def autonomousInit( self ):
		'''
		Initializes our autonomous mode
		'''
		self.nt_vision.putBoolean('isTeleop', False)

		self.gyro.reset( )
		
		self.scheduler.add( commands.drivetrain.Set_Gear_State_Low( self ) )

		# Get the driver-selected auto mode from SmartDashboard and start it
		print( 'Running Auto mode: {0}'.format( self.oi.auto_choose.getSelected( ) ) )
		#commands.autonomous.Shoot_From_Hopper( self.robot, const.ID_AUTO_RED_SIDE ) 
		self.oi.auto_choose.getSelected( ).start( )


	def autonomousPeriodic( self ):
		'''
		Periodically calls all autonomous based commands
		'''
		wpilib.command.Scheduler.getInstance( ).run( )
		self.log( )


	### Teleoperated ###

	def teleopInit( self ):
		'''
		Initializes our teleop mode
		'''
		self.nt_vision.putBoolean('isTeleop', True)

		# Stop auto mode commands
		#self.oi.auto_choose.getSelected( ).cancel( )

		self.gyro.reset( )
		self.drive_encoder_right.reset( )
		self.drive_encoder_left.reset( )

		# Set initial state on a couple things
		if const.DEMO_MODE:
			self.scheduler.add( commands.drivetrain.Set_State_H_Drive( self ) )
		else:
			self.scheduler.add( commands.drivetrain.Set_State_Tank( self ) )
		
		self.scheduler.add( commands.drivetrain.Set_Gear_State_Low( self ) )
		self.scheduler.add( commands.gear_funnel.Set_Gear_Funnel_State( self, const.ID_GEAR_FUNNEL_CLOSED ) )
		self.scheduler.add( commands.gear_lexan.Set_Gear_Lexan_State( self, const.ID_GEAR_LEXAN_CLOSED ) )
		self.scheduler.add( commands.gear_claw.Close_Container( self ) )
		self.scheduler.add( commands.shooter.Stop_Shooter_Wheel( self ) )
		self.scheduler.add( commands.agitator.Stop_Agitator( self ) )


	def teleopPeriodic( self ):
		'''
		Periodically calls all teleop code
		'''
		wpilib.command.Scheduler.getInstance( ).run( )

		self.gear_claw.check_for_gear_release( )

		self.log( )


	### Misc ###

	def get_pressure( self ):
		"""
		Calculate a running average of pressure values.  The sensor seems to jitter its values
		a lot, so this should smooth it out and make the SD display more readable.
		"""
		voltage_pressure = self.pressure_sensor.getVoltage( )
		new_value = ( 250 * voltage_pressure / 5 ) - 25

		self._pressure_samples.append( new_value )

		if not self.pressure_timer.hasPeriodPassed( self.pressure_timer_delay ):
			return self._last_pressure_value

		# Calculate new running average
		new_avg = sum( self._pressure_samples ) / len( self._pressure_samples )

		self._pressure_samples = [ ]
		self._last_pressure_value = new_avg

		return new_avg



	def log( self ):
		'''
		Logs some info to the SmartDashboard, and standard output
		'''
		# Only every 1/10 second (or so) to avoid flooding networktables
		if not self.log_timer.running or not self.log_timer.hasPeriodPassed( self.log_timer_delay ):
			return

		wpilib.SmartDashboard.putNumber( 'Gyro Angle: ', self.gyro.getAngle( ) )
		#wpilib.SmartDashboard.putBoolean( 'Gear Switch: ', self.gear_switch.get( ) )

		wpilib.SmartDashboard.putString( 'pressure: ', '{0:.2f}'.format( self.get_pressure( ) ) )

		self.drive.log( )
		self.shooter_camera.log( )
		self.gear_camera.log( )
		self.shooter.log( )
		self.agitator.log( )
		self.climber.log( )
		self.gear_funnel.log( )
		self.gear_claw.log( )
		self.feeder.log( )


### MAIN ###

if __name__ == "__main__":
	wpilib.run( Robot )