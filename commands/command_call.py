"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2017, "Steamworks"
Code for robot "Polyphemus"
contact@team4096.org
"""

import wpilib
from wpilib.command import Command


class Command_Call( Command ):
	'''
	This class allows us to create simple commands just by supplying a
	callable object (function). The function is called when the command is
	run, then the command immediately finishes.
	Adapted from code by FRC Team 2423
	'''
	def __init__( self, call ):
		'''
		Creates a new Command_Call
		'''
		super( ).__init__( )

		self.call = call


	def isFinished( self ):
		'''Command goes right to end'''

		return True


	def end( self ):
		'''The function is immediately executed'''

		if callable( self.call ):    
			self.call( )

