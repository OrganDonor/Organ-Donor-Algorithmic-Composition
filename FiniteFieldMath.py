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
# Left justify the signature
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def left_justify_signature(element):
	for index, number in enumerate(F.ShowCoefficients(element)):
		if number != 0: # or 'if number:'
			#print "inside left_justify_signature(element): F.ShowCoefficients(",element,") is", F.ShowCoefficients(element)
			#print "after slicing out the first",index,"elements, which are zeros, we get:", F.ShowCoefficients(element)[index:12]
			#print "then we need to pad the end so that it is 12 zeros long. 
			#list(pad(F.ShowCoefficients(element)[index::], 13, '0'))
			# it was: return list(pad(F.ShowCoefficients(element)[index::], 13, 0))
			return list(pad(F.ShowCoefficients(element)[index::], 12, 0))

			
			
			
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# determine weight of signature
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def weigh(signature):
	w = 0
	for index, number in enumerate(signature): #index is the index, number is the value 0 or 1 at each index
		#print "the place in the chord is note#", index + 1,"and the value at that index is",number, "for weight of", number * (index + 1)
		if number == 1:
			w = w + (index + 1)*(index + 1) #index starts at zero, so put in an offset so that index 0 has a weight
	#print "weight is", w
	return w
	
	
	
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# minweight(signature)
# Rotate signature until minimum weight found, 
# then return that signature.
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
def minweight(signature):
	l = len(signature) #length of the chord
	our_index = 0 #if nothing needs to be done, the transposition level is 0
	startweight = math.factorial(l) #initial weight of the vector is measured. 
	#a large index is a larger weight, becuase we want left-packing.
	#print "startweight = ", startweight
	#print "the length of the chord is", l, "so we'll do", l,"rotations to find lowest weight"
	d = collections.deque(signature) #the rotated chord. Rotate once each time and test.
	e = collections.deque(signature) #the chord we modify to return as lowest weight rotation.
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
# transposition_level(signature)
# Rotate chord until minimum weight found, 
# then return transposition level.
# Same level of operation as minweight(chord)
#
#	import collections
#
#	d = collections.deque([1,2,3,4,5])
#	d.rotate(3)
#
#	print d
#	>>> deque([3, 4, 5, 1, 2])
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def transposition_level(signature):
	l = len(signature) #length of the chord
	#print "length of the chord is", l
	our_index = 0 #if nothing needs to be done, the transposition level is 0
	startweight = math.factorial(l) #initial weight of the vector is measured. 
	#a large index is a larger weight, becuase we want left-packing.
	#print "startweight = ", startweight
	#print "the length of the chord is", l, "so we'll do", l,"rotations to find lowest weight"
	d = collections.deque(signature) #the rotated chord. Rotate once each time and test.
	e = collections.deque(signature) #the chord we modify to return as lowest weight rotation.
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
# primeform(signature)
# Express a signature in Prime Form
# prime form is a vector that contains the
# intervals in the chord. 
# Here is an example signature with prime form.
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
def primeform(signature):
	pf = []
	for index, number in enumerate(signature): 
		#index is the index, number is the value 0 or 1 at each index
		if number == 1:
			#print "there is a note at index", index 
			pf.append(index)
	return pf




#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# complement(pitch)
# find complement of a pitch
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def complement(pitch):
	if pitch == 11:
		return 1
	if pitch == 10:
		return 2
	if pitch == 9:
		return 3
	if pitch == 8:
		return 4
	if pitch == 7:
		return 5
	else:
		return pitch
	
	
	
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# intvect(primeform)
# express a primeform as an interval vector
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	
#It's a 6-long vector that gives the cardinality of each interval in the signature. An interval is the difference between two pitch-classes, mod 12. For reasons which I won't spell out now (but are pretty obvious), an interval larger than 6 is counted as its inversion -- that is, its complement, mod 12. (For example, 7, a perfect fifth, is counted as 5, a perfect fourth.)

#	So, for the signature (in normal form) [0, 1, 3], we have
#	0 - 1 mod 12 = 11 -> 1.
#	0 - 3 mod 12 = 9 -> 3.
#	1 - 3 mod 12 = 10 -> 2.
#	The interval vector would be
#	[1, 1, 1, 0, 0, 0]

#	For the signature (in normal form) [0, 2, 4]:
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
# invindvect(primeform)
# express a primeform as an inversional index vector
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
# find_signatures(primeform)
# Find signature Instances from Prime Form
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# An inverted lookup, whereby any prime form 
# to look up all the instances of that signature 
# in the original list -- in other words, giving 
# a prime form gives you all the pc vectors with that form.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def find_signatures(primeform):
	signature = [0,0,0,0,0,0,0,0,0,0,0,0]
	instances = []
	for index, number in enumerate(primeform): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		signature[number] = 1;
	#print "chord we end up with is", chord
	r = collections.deque(signature)
	#print "possible combinations that corresponds to this prime form would be:"
	#print r #the initial one
	for i in range (0,11): #tried very hard to come up with a clever way to limit the number correctly
		r.rotate(1)
		instances.append(list(r)) #take the rotated signature, turn into a list (from deque), append to instances.
		#print "\n", instances
	# at this point we have a list of chords. 
	# We need to eliminate duplicates.
	# both deques and lists are unhashable, so set() didn't work
	# However, make_unique from Stack Overflow discussion worked. 
	
	return make_unique(instances)







#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# augury(primeform, signature)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# A search function whereby you can match or 
# partially-match any of the vectors we have 
# generated in this code.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def augury(primeform, pitch_class_collection):
	pitch_class = []
	result = []
	#print "primeform is", primeform
	#print "pitch_class_collection is", pitch_class_collection
	
	primeform_list = pitches_to_signature(primeform)
	#print "primeform list is", primeform_list
	
	primeform_inversion_list = first_inversion(primeform_list)
	#print "primeform inversion list is", primeform_inversion_list
	
	primeform_inversion = signature_to_pitches(primeform_inversion_list)
	#print "primeform inversion is", primeform_inversion
	
	#print "chord test"
	#search our pitch_class_collection for presence of primeform
	for index, number in enumerate(pitch_class_collection): 
		#index is the index, number is the value 0 or 1 at each index
		if number == 1:
			pitch_class.append(index)
	#print "pitch class collection we're searching is", pitch_class
	#we need to compare pitch_class and primeform
	for x in range(0, 11):
		#print "Round x =", x
		if set(primeform).issubset(pitch_class):
			#print "found a match at transposition", x
			#print "the signature that we need to return is", transpose(primeform_list, x)
			result.append(transpose(primeform_list, x))
		primeform = [(y+1)%12 for y in primeform]
		#print "for index", x,"primeform is", primeform, "and pitch class collection is", pitch_class
		
	#print "inversion test"
	#print "pitch class collection we're searching is", pitch_class
	#we need to compare pitch_class and primeform
	for x in range(0, 11):
		#print "Round x =", x
		if set(primeform_inversion).issubset(pitch_class):
			#print "found a match at transposition", x
			#print "the signature that we need to return is", transpose(primeform_inversion_list, x)
			result.append(transpose(primeform_inversion_list, x))
		primeform_inversion = [(y+1)%12 for y in primeform_inversion]
		#print "for index", x,"primeform is", primeform, "and pitch class collection is", pitch_class
	return result
	




#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# dark_augury(primeform, signature)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# A search function whereby you can match or 
# partially-match any of the vectors we have 
# generated in this code, using Galois field math.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def dark_augury(primeform, pitch_class_collection):
	#we have a list of pitches in normal form
	#convert it to a list so we can get the
	#finite field element. 
	print "primeform is", primeform
	print "pitch_class_collection is", pitch_class_collection
	primeform_list = pitches_to_signature(primeform)
	print "primeform list is", primeform_list
	d = F.ConvertListToElement(primeform_list)
	print "the finite field element for primeform list is", d
	#pitch_class_collection is already a list.
	#just convert it to a finite field element.
	e = F.ConvertListToElement(pitch_class_collection)
	print "the finite field element for pitch_class_collection is", e
	f = F.Divide(e,d)
	print "pitch class collection divided by primeform list is", f
	g = F.ShowCoefficients(f)
	print "this result's coefficients are", g
	primeform_inversion_list = first_inversion(primeform_list)
	print "primeform inversion list is", primeform_inversion_list
	h = F.ConvertListToElement(primeform_inversion_list)
	print "the finite field element for primeform inversion list is", h
	i = F.Divide(e,h)
	print "pitch class collection divided by primeform inversion list is", i
	j = F.ShowCoefficients(i)
	print "this result's coeffcients are", j


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# You can find the duplicates analytically, too. 
# Since we also have (trivially, now) the 
# transposition level of each pc vector along 
# with its normal form, and the interval vector 
# for each, you can inspect the interval vector 
# for the number of duplications between any two transpositions.
#
# Remember that the value in the interval vector 
# is the number of occurrences of that interval 
# in the normal form.
# That value also tells you how many elements 
# will be in common between two instances of 
# the chord at those transpositions.
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
	signatureu = []
	signaturev = []
	common_notes = []
	result = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u): 
		# index is the index of (u), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			signatureu.append(index)
	for index, number in enumerate(v): 
		# index is the index of (v), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			signaturev.append(index)
	print "comparing", signatureu, "with", signaturev

	common_notes = list(set(signatureu).intersection(signaturev))
	print common_notes

	for index, number in enumerate(common_notes): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		result[number] = 1;
	
	return result




#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# transpose(u, t)
# take a signature and music-transposes 
# it by t, mod 12.
# transpose(u, t) sends each u_i -> u_{(i+t)%12}
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def transpose(u, t):
	signature_u = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			signature_u[(index + t)%12] = 1;
	return signature_u



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
	signature_v = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(v): 
		# index is the index of (primeform), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		signature_v[number] = 1;
	return signature_v




	

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# signature_complement(u)
# complement of a signature
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def signature_complement(u):
	signature_u = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u): 
		# index is the index of (u), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number == 1:
			signature_u[index] = 0
		if number == 0:
			signature_u[index] = 1
	return signature_u






#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# first_inversion(u)
# first inversion of a signature
# takes a signature, returns the inversion
# of that signature, left justified.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def first_inversion(u):
	#print "attempting to invert the signature", u
	inversion = [0,0,0,0,0,0,0,0,0,0,0,0]
	for index, number in enumerate(u):
		# index is the index of (u), number is the existence of
		# value 0 or 1 at each index
		#print "at index",index,"there is value",number
		if number != 0:
			inversion[11 - index] = 1
	#print inversion
	#print "and now I left justify this entire thing"
	for index, number in enumerate(inversion):
		if number != 0:
			return list(pad(inversion[index::], 12, 0))
		
		
		




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
#print "F.ShowCoefficients(2222)", F.ShowCoefficients(2222)

#print "F.ConvertListToElement([1,0,0,1,0,0,0,1,0,0,0,0])", F.ConvertListToElement([1,0,0,1,0,0,0,1,0,0,0,0])
#print "testing augury(primeform, pitch_class_collection)", augury(primeform([1,0,0,1,0,0,0,1,0,0,0,0]), [1,0,1,0,1,1,0,1,0,1,0,1])



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# mess around zone 
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#number_of_notes = 0
#j = 0
#number_of_chords = 0
#
#for i in range(0, (2**12)):
#	#print "F.ShowPolynomial(",i,")", F.ShowPolynomial(i)
#	#print "F.ShowCoefficients(",i,")", F.ShowCoefficients(i)
#	if F.ShowCoefficients(i).count(1) == 12:
#		print "F.ShowCoefficients(",i,")", F.ShowCoefficients(i)
#		print "number of notes in this signature is", F.ShowCoefficients(i).count(1)
#		number_of_chords = number_of_chords + 1
#	number_of_notes = 0
#	j = 0
#print "number of signature in this run is", number_of_chords
#print "all done."
#
#print "Just printing F.ShowCoefficients(2222) is", F.ShowCoefficients(2222)[1:13]
#
#print "left_justify_signature(2222) is", left_justify_signature(2222)
#print "weigh this signature 2222:\n", weigh(left_justify_signature(2222))
#print "rotate this signature and find minimum weight 2222:\n", minweight(left_justify_signature(2222))
#print "2222:", F.ShowCoefficients(2222)
#print "attempt to find prime form for 2222:\n", primeform(minweight(left_justify_signature(2222)))
#print "attempt to find interval vector for 2222\n", intvect(primeform(minweight(left_justify_signature(2222))))
#print "attempt to find inversional index vector for 2222\n", invindvect(primeform(minweight(left_justify_signature(2222))))
#print "attempt to find all signature that make the prime form for 2222\n",find_signatures(primeform(minweight(left_justify_signature(2222))))
#
#print "attempt to find all signature that make the prime form for 1\n",find_signatures(primeform(minweight(left_justify_signature(1))))
#
#print "attempt to find all signature that make the prime form for 4095\n",find_signatures(primeform(minweight(left_justify_signature(4095))))
#
#print "attempt to find all signature that make the prime form for off-on\n",find_signatures(primeform(minweight([0,1,0,1,0,1,0,1,0,1,0,1])))
#
#print "attempt to find transposition level for [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]:", transposition_level([0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0])
#
#
#print "testing common_tone (number of pitch classes in common between two signatures)", common_tone(F.ShowCoefficients(1074)[1:13], F.ShowCoefficients(3333)[1:13])
#
#print "testing signature_to_pitches(3333). Signature for (3333) is", F.ShowCoefficients(3333)[1:13], "and the list of pitches for that is ", signature_to_pitches(F.ShowCoefficients(3333)[1:13])
#
#print "testing pitches_to_signature(3333). Pitches for (3333) is", signature_to_pitches(F.ShowCoefficients(3333)[1:13]), "and the list of pitches for that is ", pitches_to_signature(signature_to_pitches(F.ShowCoefficients(3333)[1:13]))
#
#
#print "testing def signature_complement([0,0,0,0,0,0,1,1,1,1,1,1])", signature_complement([0,0,0,0,0,0,1,1,1,1,1,1])
#
#print "testing transpose([0,0,0,0,0,0,1,1,1,1,1,1], 2)", transpose([0,0,0,0,0,0,1,1,1,1,1,1], 2)
#print "testing invert([0,0,0,0,0,0,1,1,1,1,1,1])", invert([0,0,0,0,0,0,1,1,1,1,1,1])
#
#print "testing first_inversion([1,0,0,0,1,0,0,1,0,0,0,0])", first_inversion([1,0,0,0,1,0,0,1,0,0,0,0])






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
	#lut_dict[F.ShowCoefficients(i)] = primeform(minweight(left_justify_signature(i)))
	print >>normal_form_lut_fp, F.ShowCoefficients(i)[1:13]
	print >>interval_vector_lut_fp, "prime form is", primeform(minweight(left_justify_signature(i)))
	print >>inversional_index_vector_lut_fp, "prime form is", primeform(minweight(left_justify_signature(i)))
	#print the normal form for this vector right after
	#print the interval vector for this result right after
	#print the inversional index vector right after
	print >>normal_form_lut_fp, primeform(minweight(left_justify_signature(i)))
	print >>interval_vector_lut_fp, "interval vector is",intvect(primeform(minweight(left_justify_signature(i)))),"\n"
	print >>inversional_index_vector_lut_fp, "inversional index vector is", invindvect(primeform(minweight(left_justify_signature(i)))),"\n"
	print >>transposition_level_lut_fp, F.ShowCoefficients(i)[1:13], transposition_level(F.ShowCoefficients(i)[1:13])






