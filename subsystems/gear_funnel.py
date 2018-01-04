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

class Gear_Funnel( wpilib.command.Subsystem ):
	def __init__( self, robot ):
		super( ).__init__( 'gear funnel' )
		self.robot = robot

		self.gear_funnel_solenoid_1 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_FUNNEL_SOLENOID_1 )
		self.gear_funnel_solenoid_2 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_FUNNEL_SOLENOID_2 )

		# Funnel Open means the Funnel to collect the gear is pushed out and the lexan is not in the way
		self.gear_funnel_state = const.ID_GEAR_FUNNEL_CLOSED

	def get_gear_funnel_state( self ):
		return self.gear_funnel_state
	
	def set_gear_funnel_state( self, state ):
		self.gear_funnel_state = state
		
		if state == const.ID_GEAR_FUNNEL_OPEN:
			print( 'Funnel OPEN' )
		else:
			print( 'Funnel CLOSED' )
	
		if state == const.ID_GEAR_FUNNEL_OPEN:
			self.gear_funnel_solenoid_1.set( False )
			self.gear_funnel_solenoid_2.set( True )			
		else:
			self.gear_funnel_solenoid_1.set( True )
			self.gear_funnel_solenoid_2.set( False )			

	
	def toggle_gear_funnel_state( self ):
		if self.gear_funnel_state == const.ID_GEAR_FUNNEL_OPEN:
			self.set_gear_funnel_state( const.ID_GEAR_FUNNEL_CLOSED )
		else:
			self.set_gear_funnel_state( const.ID_GEAR_FUNNEL_OPEN )


	def log( self ):
		pass

