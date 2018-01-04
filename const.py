"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import wpilib

### CONSTANTS ###

DEMO_MODE 							= True
DEMO_TOP_SPEED_MULTIPLIER 			= 0.8
STRAFE_WHEELS_DISABLED				= True

# PCM's
# PCM 1 controls the drivetrain and the ground feeder
ID_PCM_1							= 0
ID_PCM_2							= 2

# PWM port IDs

#Roborio Accelerometer
NEGATIVE_ACCEL_VALUE = 0

# Drivetrain
ID_DRIVE_MOTOR_FRONT_LEFT			= 2
ID_DRIVE_MOTOR_REAR_LEFT			= 3

ID_DRIVE_MOTOR_FRONT_RIGHT			= 0
ID_DRIVE_MOTOR_REAR_RIGHT			= 1

ID_STRAFE_WHEEL_1					= 4
ID_STRAFE_WHEEL_2					= 5

ID_DRIVE_SOLENOID_SHIFTER_1			= 4
ID_DRIVE_SOLENOID_SHIFTER_2			= 5

ID_DRIVE_SOLENOID_ACTUATOR_1        = 2
ID_DRIVE_SOLENOID_ACTUATOR_2		= 3
ID_STRAFE_WHEEL_SOLENOID_1			= 0
ID_STRAFE_WHEEL_SOLENOID_2			= 1

DRIVE_MIN_ROTATION_OUTPUT_OMNI		= 0.55   # 0.55 Min power output required to rotate robot at all
DRIVE_MIN_ROTATION_OUTPUT_TANK 	    = 0.60   # 0.60 Min power output required to rotate robot at all

DRIVE_CORRECTION_ENABLED			= True

DRIVE_CORRECTION_ROTATION_THRESHOLD	= 0.05
DRIVE_CORRECTION_PROPORTION_FORWARD = 0.15
DRIVE_CORRECTION_PROPORTION_REVERSE = 0.15
DRIVE_CORRECTION_PROPORTION_FORWARD_ENC = 0.01 #was .01
DRIVE_CORRECTION_PROPORTION_REVERSE_ENC = 0.01 #was .01

DRIVE_ENCODER_TICKS_PER_ROTATION	= 1144
DRIVE_DISTANCE_PER_ROTATION_TANK	= 1.112647398 #feet (13.35178 inches)
DRIVE_DISTANCE_PER_ROTATION_OMNI	= 1.047197551 #feet
DRIVE_DISTANCE_PER_ENCODER_TICK_TANK= DRIVE_DISTANCE_PER_ROTATION_TANK /  DRIVE_ENCODER_TICKS_PER_ROTATION
DRIVE_DISTANCE_PER_ENCODER_TICK_OMNI= DRIVE_DISTANCE_PER_ROTATION_OMNI /  DRIVE_ENCODER_TICKS_PER_ROTATION

# IDs for state of drive shifter
ID_H_DRIVE							= 0
ID_TANK								= 1
# IDs for gears
ID_LOW_GEAR							= 0
ID_HIGH_GEAR						= 1
# ID for strafe wheel sensitivity
ID_LOW_SENSITIVITY					= 0.60	

# Ground Feeder
ID_FEEDER_MOTOR_1					= 7 #NONE OF THESE VALUES ARE ACURATE
ID_FEEDER_MOTOR_2					= 8
ID_FEEDER_SOLENOID_1				= 6
ID_FEEDER_SOLENOID_2				= 7
ID_FEEDER_ENGAGED					= 1
ID_FEEDER_DISENGAGED				= 0
ID_FEEDER_RUNNING                   = 1
ID_FEEDER_STOPPED                   = 0

# Gear Feeding and Releasing
ID_GEAR_FUNNEL_SOLENOID_1			= 4
ID_GEAR_FUNNEL_SOLENOID_2			= 5

ID_GEAR_LEXAN_SOLENOID_1			= 0
ID_GEAR_LEXAN_SOLENOID_2			= 1

ID_GEAR_RELEASE_CLAWS_SOLENOID_1	= 6
ID_GEAR_RELEASE_CLAWS_SOLENOID_2	= 7

ID_GEAR_PUNCH_SOLENOID_1			= 2
ID_GEAR_PUNCH_SOLENOID_2			= 3

ID_GEAR_SWITCH 						= 4

ID_PRESSURE_SENSOR 					= 0

# STATES
ID_GEAR_FUNNEL_CLOSED				= 0
ID_GEAR_FUNNEL_OPEN					= 1
ID_GEAR_LEXAN_CLOSED				= 0
ID_GEAR_LEXAN_OPEN					= 1
ID_GEAR_CONTAINER_CLOSED			= 0
ID_GEAR_CONTAINER_OPEN				= 1

# Autonomous
ID_AUTO_CENTER_GEAR					= 0
ID_AUTO_RIGHT_GEAR					= 1
ID_AUTO_LEFT_GEAR					= 2
ID_AUTO_RED_SIDE					= 1
ID_AUTO_BLUE_SIDE					= 0

# Climber Constants
ID_CLIMBER_MOTOR_1					= 6

# Agitator Constants				
ID_AGITATOR_MOTOR_1					= 9

# Camera constants
CAMERA_RES_X						= 320      #320
CAMERA_RES_Y						= 240	   #240

DEFAULT_CAMERA_EXPOSURE				= 10

GEAR_CAMERA_GRIP					= 0
GEAR_CAMERA_STREAM					= 1

SHOOTER_CAMERA_GRIP					= 0
SHOOTER_CAMERA_STREAM				= 1

#to get the values for FOV_X and FOV_Y, we put a 2 foot piece of tape on the wall, 
#we moved the camera forward/backward until the tape took up the entire x or y axis. 
#Next, we measured the distance from the wall to the camera
#The FOV in degrees is equal to arctan(distance_to_camera / (length_of tape / 2))
CAMERA_FOV_X						= 68      #106.26  #degrees
CAMERA_FOV_Y						= 43.6028 #degrees
CAMERA_ALIGN_THRESHOLD				= 1		# degrees

TARGET_FEET_WIDTH					= .166666    #2 inches width of the retroreflective tape
TARGET_FEET_HEIGHT					= 0.41666666 #5 inches height of the retroreflective tape

MIN_DISTANCE_FROM_PEG				= 1.0
## FOV Degrees for Height
## height in inches 24, distance from wall 30 inches FOV =  2 * arctan(12/30)

##arctan16/12

# This was measured by observing 289 pulses per full wheel revolution, 1.0 / 289 = 0.00346
SHOOTER_ENCODER_DISTANCE_PER_PULSE	= 0.00346

GEAR_FEEDER_REVERSE_DISTANCE = -0.5				# in feet

SHOOTER_SPEED = 3800 #3200 against the plate

def update_gyro_const( new_value ):
	global DRIVE_CORRECTION_PROPORTION_FORWARD
	DRIVE_CORRECTION_PROPORTION_FORWARD = new_value
	
def update_enc_const( new_value ):
	global DRIVE_CORRECTION_PROPORTION_FORWARD_ENC
	global DRIVE_CORRECTION_PROPORTION_REVERSE_ENC
	DRIVE_CORRECTION_PROPORTION_FORWARD_ENC = new_value
	DRIVE_CORRECTION_PROPORTION_REVERSE_ENC = new_value
	
def update_auto_correct( new_value ):
	global DRIVE_CORRECTION_ENABLED
	DRIVE_CORRECTION_ENABLED = new_value
	
def update_shooter_speed( new_value ):
	global SHOOTER_SPEED
	SHOOTER_SPEED = new_value
	