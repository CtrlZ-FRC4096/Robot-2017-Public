#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import math
import sys

import wpilib
import ctre
import wpilib.command
import networktables

import const
import time

import commands.gear_claw

class Gear_Claw( wpilib.command.Subsystem ):
	def __init__( self, robot ):
		super( ).__init__( 'gear claw' )
		self.robot = robot
		
		self.gear_release_claws_solenoid_1 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_RELEASE_CLAWS_SOLENOID_1 )
		self.gear_release_claws_solenoid_2 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_RELEASE_CLAWS_SOLENOID_2 )
		
		self.gear_punch_solenoid_1 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_PUNCH_SOLENOID_1 )
		self.gear_punch_solenoid_2 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_PUNCH_SOLENOID_2 )
		
		# Container Open means that the doors are opent and the piston is actuated (no gear in compartment)
		self.gear_container_solenoid_state = const.ID_GEAR_CONTAINER_CLOSED

		self.last_gear_switch_state = self.robot.gear_switch.get( )
	

	def set_gear_container_state( self, state ):
		self.gear_container_solenoid_state = state

		if state == const.ID_GEAR_CONTAINER_OPEN:
			self.gear_release_claws_solenoid_1.set( True )
			self.gear_release_claws_solenoid_2.set( False )
			self.gear_punch_solenoid_1.set( True )
			self.gear_punch_solenoid_2.set( False )			
		else:
			self.gear_release_claws_solenoid_1.set( False )
			self.gear_release_claws_solenoid_2.set( True )
			self.gear_punch_solenoid_1.set( False )
			self.gear_punch_solenoid_2.set( True )				


	def toggle_gear_container_state( self ):
		if self.gear_container_solenoid_state == const.ID_GEAR_CONTAINER_OPEN:
			self.set_gear_container_state( const.ID_GEAR_CONTAINER_CLOSED )
		else:
			self.set_gear_container_state( const.ID_GEAR_CONTAINER_OPEN )
	
	def open_gear_claws( self ):
		self.gear_release_claws_solenoid_1.set( True )
		self.gear_release_claws_solenoid_2.set( False )
		
	def close_gear_claws( self ):
		self.gear_release_claws_solenoid_1.set( False )
		self.gear_release_claws_solenoid_2.set( True )
		
	def open_gear_punch( self ):
		self.gear_punch_solenoid_1.set( True )
		self.gear_punch_solenoid_2.set( False )
		
	def close_gear_punch( self ):
		self.gear_punch_solenoid_1.set( False )
		self.gear_punch_solenoid_2.set( True )	
	
	def check_for_gear_release( self ):
		#if(  self.robot.gear_switch.get( ) ):
		#	print("triggered")
		if self.robot.gear_switch.get( ) and not self.last_gear_switch_state:
			# Switch just turned on, so release gear
			self.robot.scheduler.add( commands.gear_claw.Open_Container( self.robot ) )
			self.last_gear_switch_state = True
		elif self.last_gear_switch_state and not self.robot.gear_switch.get( ):
			# Switch just turned off so stop releasing
			self.last_gear_switch_state = False	
		#	print("switch untripped")
			self.robot.scheduler.add( commands.gear_claw.Close_Container( self.robot ) )


	def log( self ):
		wpilib.SmartDashboard.putBoolean( 'Gear Switch', self.robot.gear_switch.get( ) )

