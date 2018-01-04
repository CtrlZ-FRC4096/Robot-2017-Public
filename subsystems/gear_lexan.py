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

class Gear_Lexan( wpilib.command.Subsystem ):
	def __init__( self, robot ):
		super( ).__init__( 'gear lexan' )
		self.robot = robot

		self.gear_lexan_solenoid_1 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_LEXAN_SOLENOID_1 )
		self.gear_lexan_solenoid_2 = wpilib.Solenoid( const.ID_PCM_2, const.ID_GEAR_LEXAN_SOLENOID_2 )

		# Lexan Open means the slider is extended, ready to direct fuel into hopper
		self.gear_lexan_state = const.ID_GEAR_LEXAN_CLOSED


	def set_gear_lexan_state( self, state ):
		if( self.robot.gear_funnel.get_gear_funnel_state() == const.ID_GEAR_FUNNEL_OPEN and state == const.ID_GEAR_LEXAN_OPEN ):
			return
		self.gear_lexan_state = state

		if state == const.ID_GEAR_LEXAN_OPEN:
			print( 'Lexan OPEN' )
		else:
			print( 'Lexan CLOSED' )
			
		if state == const.ID_GEAR_FUNNEL_OPEN:
			self.gear_lexan_solenoid_1.set( False )
			self.gear_lexan_solenoid_2.set( True )
		else:
			self.gear_lexan_solenoid_1.set( True )
			self.gear_lexan_solenoid_2.set( False )		


	def toggle_gear_lexan_state( self ):
		if self.gear_lexan_state == const.ID_GEAR_FUNNEL_OPEN:
			self.set_gear_lexan_state( const.ID_GEAR_FUNNEL_CLOSED )
		else:
			self.set_gear_lexan_state( const.ID_GEAR_FUNNEL_OPEN )
		
	
	def log( self ):
		wpilib.SmartDashboard.putBoolean( 'Guilotine', self.gear_lexan_state == const.ID_GEAR_FUNNEL_OPEN )

