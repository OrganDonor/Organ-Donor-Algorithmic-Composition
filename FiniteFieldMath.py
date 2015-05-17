#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# make GF_2_12 for Organ Donor
# becomes FiniteFieldMath.py for github
# by Abraxas3d (Michelle Thompson)
# abraxas@sand.net
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#   Imports
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

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# setup rtmidi as our backend
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#select rtmidi as our backend
mido.set_backend('mido.backends.rtmidi')
print "Backend selected is %s " % mido.backend

#open up a rtmidi output port for playing midi files

try:
	out = mido.open_output()
except:
	pass
	print "Failed to open a MIDO output port, but going on with the rest of the show."

##test port by generating some tones
##turn this off when you don't have anything hooked up
#print "Test tones!"
#for i in range(36,45):
#	my_on_message = mido.Message('note_on', note=i, velocity=100)
#	print my_on_message
#	out.send(my_on_message)
#	time.sleep(0.2)
#	my_off_message = mido.Message('note_off', note=i, velocity=100)
#	print my_off_message
#	out.send(my_off_message)
#	time.sleep(0.05)








#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Play a midi file in MIDO
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


#print "The current mido object is %s " % mid

##You can get the total playback time in seconds by accessing the length property:
#print "Total playback time of %s is %f." % (mysong, mid.length)

##turn this off when nothing is hooked up
#for message in mid.play():
#	out.send(message)
#	print message




#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Custom functions
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#To answer the question first: you need to know the cardinality of the chord. That is, how many notes.
#Given that, you can determine which rotation of the chord (1) has the smallest interval between the 
#first and last elements, and (2) when the first criterion is met by more than one rotation, then which 
#rotation has the smallest interval at the bottom.

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
# Left justify the chord
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def left_justify_chord(element):
	for index, number in enumerate(F.ShowCoefficients(element)):
		if number != 0: # or 'if number:'
			#print "inside left_justify_chord(element): F.ShowCoefficients(",element,") is", F.ShowCoefficients(element)
			#print "after slicing out the first",index,"elements, which are zeros, we get:", F.ShowCoefficients(element)[index:12]
			#print "then we need to pad the end so that it is 12 zeros long. 
			#list(pad(F.ShowCoefficients(element)[index::], 13, '0'))
			# it was: return list(pad(F.ShowCoefficients(element)[index::], 13, 0))
			return list(pad(F.ShowCoefficients(element)[index::], 12, 0))

			
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# determine weight of chord
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def weigh(chord):
	w = 0
	for index, number in enumerate(chord): #index is the index, number is the value 0 or 1 at each index
		#print "the place in the chord is note#", index + 1,"and the value at that index is",number, "for weight of", number * (index + 1)
		if number == 1:
			w = w + (index + 1)*(index + 1) #index starts at zero, so put in an offset so that index 0 has a weight
	#print "weight is", w
	return w
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Rotate chord until minimum weight found, return chord
# So the proposition is something like, ""Among all density-K bit vectors, 
# that rotation with the highest density in # the low-order positions also 
# has the following properties:..." and proceed to enumerate the normal-form 
# properties.
#
#	import collections
#
#	d = collections.deque([1,2,3,4,5])
#	d.rotate(3)
#
#	print d
#	>>> deque([3, 4, 5, 1, 2])
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def minweight(chord):
	l = len(chord) #length of the chord
	our_index = 0 #if nothing needs to be done, the transposition level is 0
	startweight = math.factorial(l) #initial weight of the vector is measured. 
	#a large index is a larger weight, becuase we want left-packing.
	#print "startweight = ", startweight
	#print "the length of the chord is", l, "so we'll do", l,"rotations to find lowest weight"
	d = collections.deque(chord) #the rotated chord. Rotate once each time and test.
	e = collections.deque(chord) #the chord we modify to return as lowest weight rotation.
	for i in range(0, l):
		#print "round #", i
		#print "the rotated chord is ", d
		#print "and its weight is", weigh(d)
		if weigh(d) <= startweight:
			our_index = i
			#print "update our_index to",i
			startweight = weigh(d)
			#print "update our minimum weight so far to", startweight
		d.rotate(1)
	e.rotate(our_index)
	#print "e.rotate(",our_index,") is", e
	#the transposition level is "our_index". This is also important.
	return e #return the rotation that results in the lowest weight
	
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Rotate chord until minimum weight found, return transposition level.
# Same level of operation as minweight(chord)
# So the proposition is something like, "Among all density-K bit vectors, 
# that rotation with the highest density in # the low-order positions also 
# has the following properties:..." and proceed to enumerate the normal-form 
# properties.
#
#	import collections
#
#	d = collections.deque([1,2,3,4,5])
#	d.rotate(3)
#
#	print d
#	>>> deque([3, 4, 5, 1, 2])
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def transposition_level(chord):
	l = len(chord) #length of the chord
	#print "length of the chord is", l
	our_index = 0 #if nothing needs to be done, the transposition level is 0
	startweight = math.factorial(l) #initial weight of the vector is measured. 
	#a large index is a larger weight, becuase we want left-packing.
	#print "startweight = ", startweight
	#print "the length of the chord is", l, "so we'll do", l,"rotations to find lowest weight"
	d = collections.deque(chord) #the rotated chord. Rotate once each time and test.
	e = collections.deque(chord) #the chord we modify to return as lowest weight rotation.
	for i in range(0, l):
		#print "round #", i
		#print "the rotated chord is ", d
		#print "and its weight is", weigh(d)
		if weigh(d) < startweight:
			our_index = i
			#print "update our_index to",i
			startweight = weigh(d)
			#print "update our minimum weight so far to", startweight
		d.rotate(1)
	e.rotate(our_index)
	#print "e.rotate(",our_index,") is", e
	#the transposition level is "our_index". This is also important.
	#print "our_index before modification is", our_index
	our_index = (12 - our_index) % 12
	#print "our_index after modification is", our_index

	return our_index #return the transposition level

	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Express a Chord in Prime Form
# prime form is a vector that contains the
# intervals in the chord. 
# Here is an example chord with prime form.
# chord: [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1]
# prime form: [0, 2, 7]
# there is always a 0 if there is a note.
# a note has 0 interval with itself.
# the 2 means an interval of 2 half steps 
# exists in the chord. The 7 means an 
# interval with 7 half steps exists in the
# chord. The prime form is found after 
# minimum weight is determined. 
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def primeform(chord):
	pf = []
	for index, number in enumerate(chord): 
		#index is the index, number is the value 0 or 1 at each index
		if number == 1:
			#print "there is a note at index", index 
			pf.append(index)
	return pf
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# find complement of a note
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def complement(note):
	if note == 11:
		return 1
	if note == 10:
		return 2
	if note == 9:
		return 3
	if note == 8:
		return 4
	if note == 7:
		return 5
	else:
		return note
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# express a chord as an interval vector
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	
#It's a 6-long vector that gives the cardinality of each interval in the chord. An interval is the difference between two pitch-classes, mod 12. For reasons which I won't spell out now (but are pretty obvious), an interval larger than 6 is counted as its inversion -- that is, its complement, mod 12. (For example, 7, a perfect fifth, is counted as 5, a perfect fourth.)

#	So, for the chord (in normal form) [0, 1, 3], we have
#	0 - 1 mod 12 = 11 -> 1.
#	0 - 3 mod 12 = 9 -> 3.
#	1 - 3 mod 12 = 10 -> 2.
#	The interval vector would be
#	[1, 1, 1, 0, 0, 0]

#	For the chord [0, 2, 4]:
#	0 - 2 mod 12 = 10 -> 2.
#	0 - 4 mod 12 = 8 -> 4.
#	2 - 4 mod 12 = 10 -> 2.
#	The interval vector would be
#	[0, 2, 0, 1, 0, 0]

#Find C(n,r) where:
#C(n,r) = n! / ( r! (n - r)! )

def intvect(primeform):
	#print "primeform received is", primeform
	length = len(primeform)
	iv = [0,0,0,0,0,0]
	if length == 1:
		return iv
	if length == 2:
		iv[complement(((primeform[0] - primeform[1])%12))-1] = iv[complement(((primeform[0] - primeform[1])%12))-1] + 1
	else:	
		for x in range(0, length - 1): #was - 2
			for y in range(x+1, length): #was - 1
				iv[complement(((primeform[x] - primeform[y])%12))-1] = iv[complement(((primeform[x] - primeform[y])%12))-1] + 1
				#print "complement(((primeform[",x,"] - primeform[",y,"])%12)) is ", complement(((primeform[x] - primeform[y])%12))
	return iv
	
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# express a chord as an inversional index vector
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def invindvect(primeform):
	#print "primeform received by inverse interval vector function is", primeform
	length = len(primeform)
	iv = [0,0,0,0,0,0,0,0,0,0,0,0]
	if length == 1:
		return iv
	if length == 2:
		iv[((primeform[0] + primeform[1])%12)-1] = iv[((primeform[0] + primeform[1])%12)-1] + 1
	else:	
		for x in range(0, length - 1): #was - 2
			for y in range(x+1, length): #was - 1
				iv[((primeform[x] + primeform[y])%12)-1] = iv[((primeform[x] + primeform[y])%12)-1] + 1
				#print "((primeform[",x,"] - primeform[",y,"])%12) is ", ((primeform[x] - primeform[y])%12)
	return iv






#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#  Find Chord Instances from Prime Form
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# An inverted lookup, whereby any prime form 
# (can we call it a signature?) can be used 
# to look up all the instances of that signature 
# in the original list -- in other words, giving 
# a prime form gives you all the pc vectors with that form.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def findchords(primeform):
	chord = [0,0,0,0,0,0,0,0,0,0,0,0]
	instances = []
	for index, number in enumerate(primeform): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		chord[number] = 1;
	#print "chord we end up with is", chord
	r = collections.deque(chord)
	#print "possible combinations that corresponds to this prime form would be:"
	#print r #the initial one
	for i in range (0,11): #tried very hard to come up with a clever way to limit the number correctly
		r.rotate(1)
		instances.append(list(r)) #take the rotated chord, turn into a list (from deque), append to instances.
		#print "\n", instances
	# at this point we have a list of chords. 
	# We need to eliminate duplicates.
	# both deques and lists are unhashable, so set() didn't work
	# However, make_unique from Stack Overflow discussion worked. 
	
	return make_unique(instances)



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Augury
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# A search function whereby you can match or 
# partially-match any of the vectors we have 
# generated in this code
# You can find the duplicates analytically, too. 
# Since we also have (trivially, now) the 
# transposition level of each pc vector along 
# with its normal form, and the interval vector 
# for each, you can inspect the interval vector 
# for the number of duplications between any two transpositions.
# Pitch-classes in common between any two pc vectors.
# Remember that the value in the interval vector is the number of occurrences of that interval in the normal form.
# That value also tells you how many elements will be in common between two instances of the chord at those transpositions.
# And in the case of generative algorithms 
# (that is, compositional ones), then many 
# of these give the branches out from the 
# current node of the tree.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=










#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# common_tone(u, v)
# we need a function common_tone(u, v) 
# where u and v are signatures, telling which 
# pitch classes they have in common.
# It returns a vector with 1's where they 
# have common pitches.
# this is the same as a union of signatures.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def common_tone(u, v):
	chordu = []
	chordv = []
	common_notes = []
	result = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u): 
		# index is the index of (u), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			chordu.append(index)
	for index, number in enumerate(v): 
		# index is the index of (v), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			chordv.append(index)
	print "comparing", chordu, "with", chordv

	common_notes = list(set(chordu).intersection(chordv))
	print common_notes

	for index, number in enumerate(common_notes): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		result[number] = 1;
	
	return result











# pc inversion of a vector
# Oh, and transposition, where transpose(x, t) takes vector x and music-transposes it by t, mod 12.
# function invert(x) takes each x_i and sends it to x_{12-i%12}.

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# transpose(u, t)
# take a signature and music-transposes 
# it by t, mod 12.
# transpose(u, t) sends each u_i -> u_{(i+t)%12}
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def transpose(u, t):
	chord_u = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			chord_u[(index + t)%12] = 1;
	return chord_u
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# invert(u)
# takes each x_i and sends it to x_{12-i%12}.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def invert(u):
	chord_u = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u): 
		# index is the index of (u), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			chord_u[(12 - (index))%12] = 1;
	return chord_u




#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# signature_to_pitches()
# take a signature and list the pitches
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def signature_to_pitches(u):
	pitches_u = []
	for index, number in enumerate(u): 
		# index is the index of (u), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			pitches_u.append(index)
	return pitches_u


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# pitches_to_signature()
# take a list of pitches and make a signature
# !!!currently doesn't do any error checking.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def pitches_to_signature(v):
	chord_v = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(v): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		chord_v[number] = 1;
	return chord_v




	

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# signature_complement(u)
# complement of a signature
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def signature_complement(u):
	chord_u = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u): 
		# index is the index of (u), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			chord_u[index] = 0
		if number == 0:
			chord_u[index] = 1
	return chord_u








#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Create and show GF(2^5)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#F = ffield.FField(5) # create the field GF(2^5) 
#a = 7 # field elements are denoted as integers from 0 to 2^5-1
#b = 15
#print "F.ShowPolynomial(a) is ", F.ShowPolynomial(a) # show the polynomial representation of a 'x^2 + x^1 + 1'
#print "F.ShowPolynomial(b) is ", F.ShowPolynomial(b) # 'x^3 + x^2 + x^1 + 1'
#c = F.Multiply(a,b) # multiply a and b modulo the field generator
#print "F.ShowPolynomial(c) is ", F.ShowPolynomial(c) # should be x^3
#print "c is ", c
#print "F.Multiply(c,F.Inverse(a)) == b", F.Multiply(c,F.Inverse(a)) == b # verify multiplication works, should be 1
#print "F.Multiply(c,F.Inverse(b)) == a", F.Multiply(c,F.Inverse(b)) == a # verify multiplication works, should be 1
#d = F.Divide(c,b)
#print "d = F.Divide(c,b)", d # since c = F.Multiply(a,b), d should give a, should be 7

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Create and do some math with GF(2^12)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
F = ffield.FField(12) # create the field GF(2^12) 
#for i in range(0, (2**12)-1):
#	print "F.ShowPolynomial(",i,")", F.ShowPolynomial(i)
#print "all done."
#print "(F.Inverse(32)) is", F.Inverse(32)
#print "F.ShowPolynomial(32) is", F.ShowPolynomial(32)
#print "F.ShowPolynomial(F.Inverse(32)) is", F.ShowPolynomial(F.Inverse(32))
#print "F.Multiply(32, 3041)", F.Multiply(32, 3041)
#print "F.ShowCoefficients(3041)", F.ShowCoefficients(3041)
print "F.ShowCoefficients(2222)", F.ShowCoefficients(2222)


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# mess around zone 
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

number_of_notes = 0
j = 0
number_of_chords = 0

for i in range(0, (2**12)):
	#print "F.ShowPolynomial(",i,")", F.ShowPolynomial(i)
	#print "F.ShowCoefficients(",i,")", F.ShowCoefficients(i)
	if F.ShowCoefficients(i).count(1) == 12:
		print "F.ShowCoefficients(",i,")", F.ShowCoefficients(i)
		print "number of notes in this chord is", F.ShowCoefficients(i).count(1)
		number_of_chords = number_of_chords + 1
	number_of_notes = 0
	j = 0
print "number of chords in this run is", number_of_chords
print "all done."

print "Just printing F.ShowCoefficients(2222) is", F.ShowCoefficients(2222)[1:13]

print "left_justify_chord(2222) is", left_justify_chord(2222)
print "weigh this chord 2222:\n", weigh(left_justify_chord(2222))
print "rotate this chord and find minimum weight 2222:\n", minweight(left_justify_chord(2222))
print "attempt to find transpositional level:\n", transposition_level(left_justify_chord(2222))
#print "2222:", F.ShowCoefficients(2222)
print "attempt to find prime form for 2222:\n", primeform(minweight(left_justify_chord(2222)))
print "attempt to find interval vector for 2222\n", intvect(primeform(minweight(left_justify_chord(2222))))
print "attempt to find inversional index vector for 2222\n", invindvect(primeform(minweight(left_justify_chord(2222))))
print "attempt to find all chords that make the prime form for 2222\n",findchords(primeform(minweight(left_justify_chord(2222))))

print "attempt to find all chords that make the prime form for 1\n",findchords(primeform(minweight(left_justify_chord(1))))

print "attempt to find all chords that make the prime form for 4095\n",findchords(primeform(minweight(left_justify_chord(4095))))

print "attempt to find all chords that make the prime form for off-on\n",findchords(primeform(minweight([0,1,0,1,0,1,0,1,0,1,0,1])))

print "attempt to find transposition level for [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]:", transposition_level([0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0])


print "testing common_tone (number of pitch classes in common between two chords)", common_tone(F.ShowCoefficients(1074)[1:13], F.ShowCoefficients(3333)[1:13])

print "testing signature_to_pitches(3333). Signature for (3333) is", F.ShowCoefficients(3333)[1:13], "and the list of pitches for that is ", signature_to_pitches(F.ShowCoefficients(3333)[1:13])

print "testing pitches_to_signature(3333). Pitches for (3333) is", signature_to_pitches(F.ShowCoefficients(3333)[1:13]), "and the list of pitches for that is ", pitches_to_signature(signature_to_pitches(F.ShowCoefficients(3333)[1:13]))


print "testing def signature_complement([0,0,0,0,0,0,1,1,1,1,1,1])", signature_complement([0,0,0,0,0,0,1,1,1,1,1,1])

print "testing transpose([0,0,0,0,0,0,1,1,1,1,1,1], 2)", transpose([0,0,0,0,0,0,1,1,1,1,1,1], 2)
print "testing invert([0,0,0,0,0,0,1,1,1,1,1,1])", invert([0,0,0,0,0,0,1,1,1,1,1,1])







#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Create a lookup table for normal form 
# of all the chords in GF 2^12
# Normal form classifies all the shapes
# of all the chords, regardless of the
# starting note. 
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Interval Vector: It's telling you the 
# multiplicity of each interval in the chord. 
# Main payoff: the multiplicity tells you how 
# many pitches will overlap if you transpose 
# by that interval.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# and inversional index vector
# The algorithm is the same as for the Interval Vector, 
# except you takes sums mod 12 rather than differences, 
# and you don't wrap around 6.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#>>> d = {'key':'value'}
#>>> print d
#{'key': 'value'}
#>>> d['mynewkey'] = 'mynewvalue'
#>>> print d
#{'mynewkey': 'mynewvalue', 'key': 'value'}
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

normal_form_lut = "/Users/w5nyv/Dropbox/Pipe_Organ/MIDI/normal_form_lut.txt"
normal_form_lut_fp = open(normal_form_lut, 'w+')
interval_vector_lut = "/Users/w5nyv/Dropbox/Pipe_Organ/MIDI/interval_vector_lut.txt"
interval_vector_lut_fp = open(interval_vector_lut, 'w+')
inversional_index_vector_lut = "/Users/w5nyv/Dropbox/Pipe_Organ/MIDI/inversional_index_vector_lut.txt"
inversional_index_vector_lut_fp = open(inversional_index_vector_lut, 'w+')
transposition_level_lut = "/Users/w5nyv/Dropbox/Pipe_Organ/MIDI/transposition_level_lut.txt"
transposition_level_lut_fp = open(transposition_level_lut, 'w+')

for i in range(1, (2**12)):
	#lut_dict[F.ShowCoefficients(i)] = primeform(minweight(left_justify_chord(i)))
	print >>normal_form_lut_fp, F.ShowCoefficients(i)[1:13]
	print >>interval_vector_lut_fp, "prime form is", primeform(minweight(left_justify_chord(i)))
	print >>inversional_index_vector_lut_fp, "prime form is", primeform(minweight(left_justify_chord(i)))
	#print the normal form for this vector right after
	#print the interval vector for this result right after
	#print the inversional index vector right after
	print >>normal_form_lut_fp, primeform(minweight(left_justify_chord(i)))
	print >>interval_vector_lut_fp, "interval vector is",intvect(primeform(minweight(left_justify_chord(i)))),"\n"
	print >>inversional_index_vector_lut_fp, "inversional index vector is", invindvect(primeform(minweight(left_justify_chord(i)))),"\n"
	print >>transposition_level_lut_fp, F.ShowCoefficients(i)[1:13], transposition_level(F.ShowCoefficients(i)[1:13])


#print lut_dict
#can't use a list as a hash - but convert it into a binary number and then use that?
	




