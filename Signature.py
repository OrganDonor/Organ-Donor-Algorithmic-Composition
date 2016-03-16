#Becomes Signature in organ donor github documents folder

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#MAKE:   Imports
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#import ffield.py
import ffield

#import mido library
import mido

#import markov chain library
import pykov

#import pysparse
import pysparse

#import random
import random

#import os
import os
from os import listdir
from os.path import isfile, join

#get the MidiFile, MidiTrack, and Message commands working
from mido import MidiFile
from mido.midifiles import MidiTrack
from mido import Message


#get the ports setup stuff working
from mido.ports import MultiPort

#so it knows what a MetaMessage is?
from mido import MetaMessage

#for using the rtmidi port manager
import time
import rtmidi
from rtmidi.midiutil import open_midiport
from rtmidi.midiconstants import *

#for using sliding window in entropy_toy()
from itertools import chain, repeat, islice

import collections
import math





#<#Custom Functions#>
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Custom functions
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# pad out a chord vector to necessary places
# Usage:
#
# >>> list(pad([1,2,3], 7, ''))
# [1, 2, 3, '', '', '', '']
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


def pad_infinite(iterable, padding=None):
   return chain(iterable, repeat(padding))

def pad(iterable, size, padding=None):
   return islice(pad_infinite(iterable, padding), size)



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Get rid of duplicates in a list of lists
# From Stack Overflow 
# http://stackoverflow.com/questions/7961363/python-removing-duplicates-in-lists
#
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# left_justify_signature(signature)
# Left justify the signature
# and return a signature.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def left_justify_signature(signature):
	for index, number in enumerate(signature):
		if number != 0: # or 'if number:' 
			#print "inside left_justify_signature(element): F.ShowCoefficients(",element,") is", F.ShowCoefficients(element)
			#print "after slicing out the first",index,"elements, which are zeros, we get:", F.ShowCoefficients(element)[index:12]
			#print "then we need to pad the end so that it is 12 zeros long. 
			#list(pad(F.ShowCoefficients(element)[index::], 13, '0'))
			# it was: return list(pad(F.ShowCoefficients(element)[index::], 13, 0))
			return list(pad(signature[index::], 12, 0))

























#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#MAKE:   Class definitions
# Signature is created with default 
# values of all zeros, from the init. 
# This makes it a rest until modified.
# 
# The attributes are:
# self.data = [0,0,0,0,1,1,1,0,0,1,0,0] 


# The methods are:
# self.addtrick(trick) appends value "trick" to end of data
# self.left_justify() left justifies the signature. Gets rid of leading zeros.
# self.weigh() returns the weight of current self.data

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Signature:
	def __init__(self):
		self.data = [0,0,0,0,0,0,0,0,0,0,0,0]
		#demo data [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
	
	def addtrick(self, trick):
		self.data.append(trick)
				
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	# left_justify_signature(signature)
	# Left justify the signature by modifying self.data
	# and return that signature.
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	def left_justify(self):
		if self.data.count(1) == 0:
			return self.data
		newdata = [0,0,0,0,0,0,0,0,0,0,0,0]
		#print "newdata is", newdata
		for index, number in enumerate(self.data):
			#print "index is", index, "and number is", number
			if number != 0:
				newdata = list(pad(self.data[index::], 12, 0))
				#print "new self.data is", newdata
				self.data = newdata
				return self.data
				
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	# determine weight of signature
	# the weight is the index of a nonzero value squared
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	def weigh(self):
		w = 0
		for index, number in enumerate(self.data): #index is the index, number is the nonzero value at each index
			#print "the place in the chord is note#", index + 1,"and the value at that index is",number, "for weight of", number * (index + 1)
			if number != 0:
				w = w + (index + 1)*(index + 1) #index starts at zero, so put in an offset so that index 0 has a weight
		#print "weight is", w
		return w	
		
		
		
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	# rotate a signature by a some number.
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	def rotate(self, shifts):
		if self.data.count(1) == 0:
			return self.data #all zeroes don't need rotating
		newdata = [0,0,0,0,0,0,0,0,0,0,0,0]
		#print "length of self is ", len(self.data)
		for index, number in enumerate(self.data):
			#print "index is", index, "and number is", number
			newindex = (index + shifts)%len(self.data)
			#print "new index is", newindex, "for number", number
			newdata[newindex] = number
		#print "old signature data was", self.data
		#print "newdata is", newdata
		self.data = newdata
		return self.data
		
		

		
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	# minweight(signature)
	# Rotate signature until minimum weight found, 
	# then return that signature. This modifies self.data
	# So the proposition is something like, "Among all density-K bit vectors, 
	# that rotation with the highest density in # the low-order positions also 
	# has the following properties:..." and proceed to enumerate the normal-form 
	# properties.
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	def minweight(self):
		l = len(self.data) #length of the chord
		print "length of the chord is", l
		our_index = 0 #if nothing needs to be done, the transposition level is 0
		startweight = math.factorial(l) #initial weight of the vector is measured. 
		#a large index is a larger weight, becuase we want left-packing.
		print "startweight = ", startweight
		print "the length of the chord is", l, "so we'll do", l,"rotations to find lowest weight"
		d = self #a copy of the rotated chord. Rotate once each time and test.
		e = self #the chord we modify to return as lowest weight rotation.
		for i in range(0, l):
			print "round #", i
			print "the rotated chord is ", d.data
			print "and its weight is", Signature.weigh(d)
			if Signature.weigh(d) <= startweight:
				our_index = i
				print "update our_index to",i
				startweight = Signature.weigh(d)
				print "update our minimum weight so far to", startweight
			d.rotate(1)
		e.rotate(our_index)
		print "e.rotate(",our_index,") is", e.data
		#the transposition level is "our_index". This is also important.
		self.data = e.data
		#return e #return the rotation that results in the lowest weight
		
		
		
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	# arpeggiate a signature.
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	def arpeggiate(self):
		if self.data.count(1) == 0:
			print "rest"
			
		#print "length of self is ", len(self.data)
		for index, number in enumerate(self.data):
			if number != 0:
				print "going up, index is", index, "and number is", number
				my_on_message = mido.Message('note_on', note=i, velocity=100)
				print my_on_message
				out.send(my_on_message)
				time.sleep(0.2)
				my_off_message = mido.Message('note_off', note=i, velocity=100)
				print my_off_message
				out.send(my_off_message)
				time.sleep(0.05)
		for index, number in reversed(list(enumerate(self.data))):
			if number != 0:
				print "going down, index is", index, "and number is", number
				my_on_message = mido.Message('note_on', note=i, velocity=100)
				print my_on_message
				out.send(my_on_message)
				time.sleep(0.2)
				my_off_message = mido.Message('note_off', note=i, velocity=100)
				print my_off_message
				out.send(my_off_message)
				time.sleep(0.05)
				
#middle c in MIDI is note 60.
#we need to decide what means what in the signature.
#in other words, calculate the MIDI note from the number and index in a signature


#AI what is the best possible way to arpeggiate? set a time signature? Use a time signature? 
#write a new method that plays one particular note out of a signature and call that instead of test tone code.
  
		
		
		
		