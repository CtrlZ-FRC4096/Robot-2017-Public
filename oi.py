"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import wpilib
from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.sendablechooser import SendableChooser
from wpilib.smartdashboard import SmartDashboard

# Subsystems
import subsystems.agitator
import subsystems.climber
import subsystems.drivetrain
import subsystems.gear_claw
import subsystems.gear_funnel
import subsystems.gear_lexan
import subsystems.feeder
import subsystems.shooter_camera
import subsystems.shooter

# Subsystems commands
import commands.agitator
import commands.climber
import commands.drivetrain
import commands.feeder
import commands.gear_claw
import commands.gear_funnel
import commands.gear_lexan
import commands.shooter
import commands.gear_camera
import commands.shooter_camera

# Autonomous commands
import commands.autonomous

from controls.joystick_pov import Joystick_POV
from controls.xbox_button import Xbox_Button
from controls.xbox_trigger import Xbox_Trigger
from commands.command_call import Command_Call

from common.smartdashboard_update_trigger import SmartDashboard_Update_Trigger

import const
import controls.xbox_controller

from controls.joystick_pov import Joystick_POV


## CONSTANTS ##

# Joystick axes
JOY_AXIS_LEFT_X			= 0
JOY_AXIS_LEFT_Y			= 1
JOY_AXIS_LEFT_SLIDER	= 3
JOY_AXIS_RIGHT_X		= 0
JOY_AXIS_RIGHT_Y		= 1
JOY_AXIS_RIGHT_SLIDER	= 3

# Invert any axes?
INVERT_JOY_LEFT_X		= True
INVERT_JOY_LEFT_Y		= True
INVERT_JOY_RIGHT_X		= True
INVERT_JOY_RIGHT_Y		= True

# Dead band
JOY_DEAD_BAND = 0.1

# Joystick Buttons
JOY_BTN_1				= 1
JOY_BTN_2				= 2
JOY_BTN_3				= 3
JOY_BTN_4				= 4
JOY_BTN_5				= 5
JOY_BTN_6				= 6
JOY_BTN_7				= 7
JOY_BTN_8				= 8
JOY_BTN_9				= 9
JOY_BTN_10				= 10
JOY_BTN_11				= 11
JOY_BTN_12				= 12
JOY_BTN_13				= 13
JOY_BTN_14				= 14

# Gamepad axes
GP_AXIS_LEFT_X			= 0
GP_AXIS_LEFT_Y			= 1
GP_AXIS_RIGHT_X			= 2
GP_AXIS_RIGHT_Y			= 3

# Gamepad Buttons
GP_BTN_X				= 1
GP_BTN_A				= 2
GP_BTN_B				= 3
GP_BTN_Y				= 4
GP_BTN_BUMPER_L			= 5
GP_BTN_BUMPER_R			= 6
GP_BTN_TRIGGER_L		= 7
GP_BTN_TRIGGER_R		= 8
GP_BTN_BACK				= 9
GP_BTN_START			= 10
GP_BTN_STICK_L			= 11
GP_BTN_STICK_R			= 12

# Xbox Controller
# buttons
XBOX_BTN_A				= 1
XBOX_BTN_B				= 2
XBOX_BTN_X				= 3
XBOX_BTN_Y				= 4
XBOX_BTN_LEFT_BUMPER	= 5
XBOX_BTN_RIGHT_BUMPER	= 6
XBOX_BTN_BACK 			= 7
XBOX_BTN_START 			= 8

# axes
XBOX_AXIS_LEFT_X        = 0
XBOX_AXIS_LEFT_Y		= 1
XBOX_AXIS_RIGHT_X		= 4
XBOX_AXIS_RIGHT_Y		= 5
XBOX_BTN_LEFT_TRIGGER	= 2
XBOX_BTN_RIGHT_TRIGGER	= 3


#DPAD
JOY_POV_NONE        	= -1
JOY_POV_UP				= 0
JOY_POV_RIGHT			= 90
JOY_POV_DOWN			= 180

INVERT_XBOX_LEFT_X		= True
INVERT_XBOX_LEFT_Y		= True
INVERT_XBOX_RIGHT_X		= True
INVERT_XBOX_RIGHT_Y		= True


class OI:
	"""
	Operator Input - This class ties together controls and commands
	"""
	def __init__( self, robot ):

		self.robot = robot

		# Controllers
		# Xbox
		self.xbox_controller_1 = controls.xbox_controller.Xbox_Controller( 0 )
		self.xbox_controller_2 = controls.xbox_controller.Xbox_Controller( 1 )

		## COMMANDS ##
		##Controller 1 Commands
		# DRIVE COMMANDS
		self.drive_command = commands.drivetrain.Drive_With_Tank_Values(
		                            	self.robot,
		                            	self._get_axis(self.xbox_controller_1, controls.xbox_controller.XBOX_AXIS_RIGHT_X, inverted = INVERT_XBOX_RIGHT_X ),
		                               	self._get_axis(self.xbox_controller_1, controls.xbox_controller.XBOX_AXIS_LEFT_Y, inverted = INVERT_XBOX_LEFT_Y ),
		                               	self._get_axis(self.xbox_controller_1, controls.xbox_controller.XBOX_AXIS_LEFT_X, inverted = INVERT_XBOX_LEFT_X ),
		                    )
		
		self.robot.drive.setDefaultCommand( self.drive_command )

		self.auto_choose = SendableChooser( )
	
		self.auto_choose.addObject( 'Do Nothing', commands.autonomous.Do_Nothing( self.robot ) )
		self.auto_choose.addDefault( 'Cross Baseline', commands.autonomous.Cross_Baseline( self.robot ) )
		self.auto_choose.addObject( 'Center Gear', commands.autonomous.Move_To_Gear( self.robot, const.ID_AUTO_CENTER_GEAR ) )
		self.auto_choose.addDefault( 'Center Gear No Camera', commands.autonomous.Center_Gear_Without_Camera( self.robot ) )
		self.auto_choose.addObject( 'Right Gear', commands.autonomous.Move_To_Gear( self.robot, const.ID_AUTO_RIGHT_GEAR ) )
		self.auto_choose.addObject( 'Right Gear And Shoot Red', commands.autonomous.Move_To_Gear_And_Shoot( self.robot, const.ID_AUTO_RED_SIDE ) )
		self.auto_choose.addObject( 'Left Gear', commands.autonomous.Move_To_Gear( self.robot, const.ID_AUTO_LEFT_GEAR ) )
		self.auto_choose.addObject( 'Left Gear And Shoot Blue', commands.autonomous.Move_To_Gear_And_Shoot( self.robot, const.ID_AUTO_BLUE_SIDE ) )
		self.auto_choose.addObject( 'Shoot From Hopper Red', commands.autonomous.Shoot_From_Hopper( self.robot, const.ID_AUTO_RED_SIDE ) )	
		self.auto_choose.addObject( 'Shoot From Hopper Blue', commands.autonomous.Shoot_From_Hopper( self.robot, const.ID_AUTO_BLUE_SIDE ) )
		self.auto_choose.addObject( 'Shoot From Start', commands.autonomous.Shoot_From_Start( self.robot ) )
		
		SmartDashboard.putData( 'Autonomous Mode', self.auto_choose )

		# Toggle Drive State
		self.button_drive_shift = Xbox_Trigger( self.xbox_controller_1, XBOX_BTN_LEFT_TRIGGER )
		self.button_drive_shift.whenPressed( commands.drivetrain.Toggle_Drive_State( self.robot ) )
		
		# Toggle drivetrain gear
		if not const.DEMO_MODE:
			self.button_gear_shift = Xbox_Button( self.xbox_controller_1, XBOX_BTN_LEFT_BUMPER )
			self.button_gear_shift.whenPressed( commands.drivetrain.Toggle_Gear_State( self.robot ) )		
		
		# Slow speed for driving in Y direction so that we slow down before the gear peg
		self.button_slow_driving = Xbox_Trigger( self.xbox_controller_1, XBOX_BTN_RIGHT_TRIGGER )
		self.button_slow_driving.whenPressed( commands.drivetrain.Set_Sensitivity_Low( self.robot ) )
		self.button_slow_driving.whenReleased( commands.drivetrain.Set_Sensitivity_High( self.robot ) )		
		
		# Drives backwards small distance, to align better for gear feeding
		self.button_drive_gear_feeder_reverse = Xbox_Button( self.xbox_controller_1, XBOX_BTN_X )
		self.button_drive_gear_feeder_reverse.whenPressed( commands.drivetrain.Back_Up( self.robot ) )
		
		if not const.DEMO_MODE:
			# For testing
			self.button_rotate_to_boiler = Xbox_Button( self.xbox_controller_1, XBOX_BTN_Y )
			self.button_rotate_to_boiler.whenPressed( commands.drivetrain.Rotate_To_Boiler( self.robot ) )
			
			# For testing
			self.rotate = Xbox_Button( self.xbox_controller_1, XBOX_BTN_RIGHT_BUMPER )
			self.rotate.whenPressed( commands.drivetrain.Rotate_To_Angle( self.robot, -52 ) )
			
			self.rotate_to_gear = Xbox_Button( self.xbox_controller_1, XBOX_BTN_A )
			self.rotate_to_gear.whenPressed( commands.drivetrain.Rotate_To_Gear( self.robot ) )
			
		
		
		## Controller 2 Commands		
		
		# Run Shooter
		if const.DEMO_MODE:
			# Lower top speed on shooter when in demo mode
			self.button_run_shooter = Xbox_Trigger( self.xbox_controller_2, XBOX_BTN_RIGHT_TRIGGER )
			self.button_run_shooter.whenPressed( commands.shooter.Run_Shooter_Wheel( self.robot ) )
			self.button_run_shooter.whenReleased( commands.shooter.Stop_Shooter_Wheel( self.robot ) )
		else:		
			self.button_run_shooter = Xbox_Trigger( self.xbox_controller_2, XBOX_BTN_RIGHT_TRIGGER )
			self.button_run_shooter.whenPressed( commands.shooter.Run_Shooter_Wheel_Full_Speed( self.robot ) )
			self.button_run_shooter.whenReleased( commands.shooter.Stop_Shooter_Wheel( self.robot ) )
		
		# Run Agitator
		self.button_run_agitator = Xbox_Trigger( self.xbox_controller_2, XBOX_BTN_LEFT_TRIGGER )
		self.button_run_agitator.whenPressed( commands.agitator.Run_Agitator( self.robot, 0.8 ) )
		self.button_run_agitator.whenReleased( commands.agitator.Stop_Agitator( self.robot ) )	

		# FEEDER COMMANDS

		# Toggles feeder on/off when pressed
		self.button_run_feeder_forward = Xbox_Button( self.xbox_controller_2, XBOX_BTN_RIGHT_BUMPER )
		self.button_run_feeder_forward.whenPressed( commands.feeder.Run_Feeder( self.robot, 1.0 ) )
		self.button_run_feeder_forward.whenReleased( commands.feeder.Stop_Feeder( self.robot ) )
		
		self.button_run_feeder_backward = Xbox_Button( self.xbox_controller_2, XBOX_BTN_LEFT_BUMPER )
		self.button_run_feeder_backward.whenPressed( commands.feeder.Run_Feeder( self.robot, -1.0 ) )
		self.button_run_feeder_backward.whenReleased( commands.feeder.Stop_Feeder( self.robot ) )	
		
		if not const.DEMO_MODE:
			# GILLOTUINNEE
			self.button_toggle_gear_lexan = Xbox_Button( self.xbox_controller_2, XBOX_BTN_Y )
			self.button_toggle_gear_lexan.whenPressed( commands.gear_lexan.Toggle_Gear_Lexan_State( self.robot ) )
			#self.button_toggle_gear_lexan.whenPressed( commands.gear_lexan.Set_Gear_Lexan_State( self.robot, const.ID_GEAR_LEXAN_OPEN ) )
			#self.button_toggle_gear_lexan.whenReleased( commands.gear_lexan.Set_Gear_Lexan_State( self.robot, const.ID_GEAR_LEXAN_CLOSED) )
		
		# Release gear
		self.button_toggle_gear_release = Xbox_Button( self.xbox_controller_2, XBOX_BTN_A )
		self.button_toggle_gear_release.whenPressed( commands.gear_claw.Open_Container( self.robot ) )
		self.button_toggle_gear_release.whenReleased( commands.gear_claw.Close_Container( self.robot ) )
		
		# Toggle funnel
		self.button_toggle_gear_funnel = Xbox_Button( self.xbox_controller_2, XBOX_BTN_B )
		self.button_toggle_gear_funnel.whenPressed( commands.gear_funnel.Toggle_Gear_Funnel_State( self.robot ) )
		self.button_toggle_gear_funnel.whenPressed( commands.gear_lexan.Set_Gear_Lexan_State( self.robot, const.ID_GEAR_LEXAN_CLOSED) )
		self.button_toggle_gear_funnel.whenReleased( commands.gear_funnel.Toggle_Gear_Funnel_State( self.robot ) )

		# CLIMBER COMMANDS
		self.button_run_climber_up = Joystick_POV( self.xbox_controller_2, controls.joystick_pov.JOY_POV_UP )
		self.button_run_climber_up.whenPressed( commands.climber.Run_Climber( self.robot, 1.0 ) )
		self.button_run_climber_up.whenReleased( commands.climber.Stop_Climber( self.robot ) )

		#self.button_run_climber_down = Joystick_POV( self.xbox_controller_1, controls.joystick_pov.JOY_POV_DOWN )
		#self.button_run_climber_down.whenPressed( commands.climber.Run_Climber( self.robot, -0.2 ) )
		#self.button_run_climber_down.whenReleased( commands.climber.Stop_Climber( self.robot ) )

		#self.button_change_gear_camera_type = Xbox_Button( self.xbox_controller_2, XBOX_BTN_BACK )
		#self.button_change_gear_camera_type.whenPressed( commands.gear_camera.Toggle_Gear_Camera_Mode( self.robot ) )
		
		#self.button_change_shooter_camera_type = Xbox_Button( self.xbox_controller_2, XBOX_BTN_START )
		#self.button_change_shooter_camera_type.whenPressed( commands.shooter_camera.Toggle_Shooter_Camera_Mode( self.robot ) )		

		#smart dashboard changing PID values
		dp_trigger = SmartDashboard_Update_Trigger( 'Drive P: ', self.robot.drive.default_kP )
		dp_trigger.whenActive(
		    Command_Call( lambda : self.robot.drive.update_pid( p = dp_trigger.get_key_value( ) ) )
		)

		di_trigger = SmartDashboard_Update_Trigger( 'Drive I: ', self.robot.drive.default_kI )
		di_trigger.whenActive(
		    Command_Call( lambda : self.robot.drive.update_pid( i = di_trigger.get_key_value( ) ) )
		)

		dd_trigger = SmartDashboard_Update_Trigger( 'Drive D: ', self.robot.drive.default_kD )
		dd_trigger.whenActive(
		    Command_Call( lambda : self.robot.drive.update_pid( d = dd_trigger.get_key_value( ) ) )
		)

		#smart dashboard changing Shooter PID values
		sp_trigger = SmartDashboard_Update_Trigger( 'Shooter P: ', self.robot.shooter.default_kP )
		sp_trigger.whenActive(
			Command_Call( lambda : self.robot.shooter.update_pid( p = sp_trigger.get_key_value( ) ) )
		)
	
		si_trigger = SmartDashboard_Update_Trigger( 'Shooter I: ', self.robot.shooter.default_kI )
		si_trigger.whenActive(
			Command_Call( lambda : self.robot.shooter.update_pid( i = si_trigger.get_key_value( ) ) )
		)
	
		sd_trigger = SmartDashboard_Update_Trigger( 'Shooter D: ', self.robot.shooter.default_kD )
		sd_trigger.whenActive(
			Command_Call( lambda : self.robot.shooter.update_pid( d = sd_trigger.get_key_value( ) ) )
		)		
	
		sf_trigger = SmartDashboard_Update_Trigger( 'Shooter F: ', self.robot.shooter.default_kF )
		sf_trigger.whenActive(
			Command_Call( lambda : self.robot.shooter.update_pid( f = sf_trigger.get_key_value( ) ) )
		)
		
		enc_trigger = SmartDashboard_Update_Trigger( 'ENC Autocorrect constant ', const.DRIVE_CORRECTION_PROPORTION_FORWARD_ENC )
		enc_trigger.whenActive(
		    Command_Call( lambda : const.update_enc_const( enc_trigger.get_key_value( ) ) )
		)		
		
		drive_corr_trigger = SmartDashboard_Update_Trigger( 'Drive Correction Enbaled ', const.DRIVE_CORRECTION_ENABLED )
		drive_corr_trigger.whenActive(
			Command_Call( lambda : const.update_auto_correct( drive_corr_trigger.get_key_value( ) ) )
		)
		
		shooter_trigger = SmartDashboard_Update_Trigger( 'Shooter Speed ', const.SHOOTER_SPEED )
		shooter_trigger.whenActive(
			Command_Call( lambda : const.update_shooter_speed( shooter_trigger.get_key_value( ) ) )
		)		
		
		# Trigger for changing cameras exposure
		cam_exp_trigger = SmartDashboard_Update_Trigger( 'Cam Exposure ', const.DEFAULT_CAMERA_EXPOSURE )
		cam_exp_trigger.whenActive(
		    Command_Call( lambda : self._update_cameras_exposure( cam_exp_trigger.get_key_value( ) ) )
		)		


	def _update_cameras_exposure( self, exposure ):
		# Do nothing, because RPi reads the value right from the SD trigger
		pass
		#self.robot.gear_camera.update_exposure( exposure )
		#self.robot.shooter_camera.update_exposure( exposure )


	def _get_axis( self, joystick, axis, inverted = False ):
		"""
		Handles inverted joy axes and dead band
		"""
		def axis_func():
			val = joystick.getAxis(axis)

			if abs(val) < JOY_DEAD_BAND:
				val = 0

			if inverted:
				val *= -1

			return val

		return axis_func

