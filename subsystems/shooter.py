#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import math
import os
import sys

import wpilib
import ctre
import wpilib.command
from wpilib.interfaces import PIDSource
from ctre._impl.constants import TalonSRXConst
import networktables


import const
import time

class Shooter( wpilib.command.Subsystem ):
	def __init__( self, robot ):
		super( ).__init__( 'shooter' )
		self.robot = robot

		# PIDF values for shooter
		# Can be changed on-the-fly via the smartdashboard triggers
		self.default_kP = 0.034
		self.default_kI = 0
		self.default_kD = 0.130
		self.default_kF = 0.245
		self.shooter_talon = ctre.CANTalon( 1 )

		self.shooter_talon.setFeedbackDevice( TalonSRXConst.kFeedbackDev_CtreMagEncoder_Relative )
		self.shooter_talon.setPIDSourceType( PIDSource.PIDSourceType.kRate )
		self.shooter_talon.setInverted( True )

		self.shooter_talon.changeControlMode( ctre.CANTalon.ControlMode.Speed )
		#self.shooter_talon.changeControlMode( ctre.CANTalon.ControlMode.Voltage )

		self.shooter_talon.configNominalOutputVoltage( 0.0, -0.0 )
		self.shooter_talon.configPeakOutputVoltage( 12.0, -12.0 )

		self.shooter_talon.setProfile( 0 )

		self.shooter_talon.setP( self.default_kP )
		self.shooter_talon.setI( self.default_kI )
		self.shooter_talon.setD( self.default_kD )
		self.shooter_talon.setF( self.default_kF )


	def run_shooter( self, value ):
		
		# Use this for Speed mode
		value = value / 2400.0
		#print( 'run_shooter {0}'.format( value ) )
		self.shooter_talon.set( value )
		
		#Use this for Voltage mode, or direct
		#print( 'run_shooter {0}'.format( value ) )
		#self.shooter_talon.set( value )


	def stop_shooter(self):
		#print( 'stop shooter' )
		self.shooter_talon.set( 0 )


	def update_pid( self, p = None, i = None, d = None, f = None ):
		'''
		Updates the PID coefficients
		'''
		print( 'updating! {0}, {1}, {2}, {3}'.format( p, i, d, f ) )
		if p:
			self.shooter_talon.setP( p )
		if i:
			self.shooter_talon.setI( i )
		if d:
			self.shooter_talon.setD( d )
		if f:
			self.shooter_talon.setF( f )


	def log( self ):
		# 896, 611
		bus_voltage = self.shooter_talon.getBusVoltage( )

		if bus_voltage:
			motor_output = self.shooter_talon.getOutputVoltage( ) / bus_voltage
		else:
			motor_output = 0

		wheel_speed = self.shooter_talon.getSpeed( )
		
		wpilib.SmartDashboard.putNumber( 'Talon Motor Output:', motor_output )
		wpilib.SmartDashboard.putNumber( 'Talon Speed:', wheel_speed )
		#wpilib.SmartDashboard.putNumber( 'Talon Get:', self.shooter_talon.get( ) )

		#wpilib.SmartDashboard.putNumber( 'Talon Error:', self.shooter_talon.getClosedLoopError( ) )
		#wpilib.SmartDashboard.putNumber( 'Target Speed:', self.target_speed )
		
		#self.robot.log_file.write( '{0:.04},{1:.04}\n'.format( time.time( ) - self.robot.start_time, -wheel_speed ) )
		#self.robot.log_file.flush( )

