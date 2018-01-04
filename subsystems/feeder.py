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

class Feeder( wpilib.command.Subsystem ):
	def __init__( self, robot ):
		super( ).__init__( 'ground feeder' )
		self.robot = robot
			
		#if you feel that this should be 0 and 1, because programmers count from 0 then too bad.
		self.feeder_motor_1 = wpilib.VictorSP( const.ID_FEEDER_MOTOR_1 )
		self.feeder_motor_2 = wpilib.VictorSP( const.ID_FEEDER_MOTOR_2 )
		self.feeder_motor_2.setInverted( True )
		
		self.feeder_solenoid_1 = wpilib.Solenoid( const.ID_PCM_1, const.ID_FEEDER_SOLENOID_1 )
		self.feeder_solenoid_2 = wpilib.Solenoid( const.ID_PCM_1, const.ID_FEEDER_SOLENOID_2 )
		
		self.feeder_running = const.ID_FEEDER_STOPPED		
		self.feeder_solenoid_state = const.ID_FEEDER_ENGAGED

	def set_feeder_solenoid( self, state ):
		self.feeder_solenoid_state = state

		if state == const.ID_FEEDER_DISENGAGED:
			self.feeder_solenoid_1.set( False )
			self.feeder_solenoid_2.set( True )
		else:
			self.feeder_solenoid_1.set( True )
			self.feeder_solenoid_2.set( False )
		return
	
	def toggle_feeder_state( self ):
		if self.feeder_solenoid_state == const.ID_FEEDER_DISENGAGED:
			self.set_feeder_solenoid( const.ID_FEEDER_ENGAGED )
			return const.ID_FEEDER_ENGAGED
		else:
			self.set_feeder_solenoid( const.ID_FEEDER_DISENGAGED )
			return const.ID_FEEDER_DISENGAGED
	
	def get_feeder_state( self ):
		return self.feeder_solenoid_state

	def toggle_feeder_running( self, value ):
		if self.feeder_running == const.ID_FEEDER_RUNNING:
			self.stop_feeder( )
			self.feeder_running = const.ID_FEEDER_STOPPED
			return const.ID_FEEDER_STOPPED
		else:
			self.run_feeder( value )
			self.feeder_running = const.ID_FEEDER_RUNNING
			return const.ID_FEEDER_RUNNING

	def run_feeder( self, value ):
		self.feeder_motor_1.set( value )
		self.feeder_motor_2.set( value )

	def stop_feeder(self):
		self.run_feeder(0.0)

	def log( self ):
		pass

