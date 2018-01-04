"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "SteamWorks"
Code for robot "Name TBD"
contact@team4096.org
"""

import math
import sys
import time

import wpilib
import wpilib.command

import const

import networktables


### CONSTANTS ###

### CLASSES ###

class Gear_Camera( wpilib.command.Subsystem ):

	def __init__( self, robot ):

		super( ).__init__( 'gear camera' )

		self.robot = robot
		
		self.camera_mode = const.GEAR_CAMERA_GRIP


	def set_camera_mode( self, mode ):
		self.camera_mode = mode		
		
		if self.camera_mode == const.GEAR_CAMERA_STREAM:
			self.robot.nt_vision.putBoolean( "Gear Camera Stream", True ) 
		else:
			self.robot.nt_vision.putBoolean( "Gear Camera Stream", False ) 
			
	
	def toggle_camera_mode( self ):
		if self.camera_mode == const.GEAR_CAMERA_GRIP:
			self.set_camera_mode( const.GEAR_CAMERA_STREAM )
		else:
			self.set_camera_mode( const.GEAR_CAMERA_GRIP )


	def get_target_values( self ):
		values = { }

		keys = [
		    'x',
		    'y',
		    'width',
		    'height',
		    'area',
		]

		for key in keys:
			try:
				values[ key ] = self.robot.nt_grip_peg.getNumberArray( key )
			except:
				# No values found in NT for GRIP
				values[ key ] = [ ]

		return values


	def calculate_angle( self ):
		target_values = self.robot.gear_camera.get_target_values( )
		print( target_values )
		if len( target_values[ 'x' ] ) == 0:
			# No vision targets found
			print( 'No vision targets found' )
			return 0

		elif len( target_values[ 'x' ] ) == 1:
			print( 'Only one of two targets found' )
			center_x = target_values[ 'x' ][ 0 ]
		else:
			x1 = target_values[ 'x' ][ 0 ]
			x2 = target_values[ 'x' ][ 1 ]
			center_x = (x1+x2)/2
			"""
		else:
			# Multiple targets found, so choose the best one

			if len( target_values[ 'area' ] ) != len( target_values[ 'x' ] ):
				# These two arrays must be same length for us to pick right one.
				# Sometimes GRIP finds 3 areas, but only 2 centerX values, for instance
				return 0

			# Find index of target with largest area
			largest_area_idx = 0

			for i in range( len( target_values[ 'area' ] ) ):
				if target_values[ 'area' ][ i ] > largest_area_idx:
					largest_area_idx = i

			center_x = target_values[ 'x' ][ largest_area_idx ]
			"""

		print("  center_x: ", center_x)

		#target_x = const.CAMERA_RES_X / 2.0 + const.CAMERA_SHOOTER_PIXEL_OFFSET
		#cam_fudge_value = wpilib.SmartDashboard.getNumber( 'Cam Fudge: ' )
		cam_fudge_value = 0
		target_x = const.CAMERA_RES_X / 2.0 + cam_fudge_value

		pixel_offset = target_x - center_x
		print("  pixel_offset", pixel_offset)

		degrees_per_pixel = const.CAMERA_FOV_X / const.CAMERA_RES_X
		print( '  degrees_per_pixel', degrees_per_pixel )

		degrees_offset = pixel_offset * degrees_per_pixel * -1.0
		print( '  degrees_offset', degrees_offset )

		return degrees_offset		



	def log( self ):
		'''
		logs info about various things
		'''
		targets_visible = len( self.get_target_values( )[ 'area' ] ) > 0

		wpilib.SmartDashboard.putBoolean( 'Gear Targets Visible', targets_visible )
		#wpilib.SmartDashboard.put( 'center_x', targets_visible )

		#wpilib.SmartDashboard.putString('Shooter Angle', '{0}'.format(self.current_shooter_angle))