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

from Signature import *



#<#Custom Functions#>
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Custom functions
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





print "Test creating default signature"
a = Signature()
print "a is ", a.data

print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

print "Test setting default signatures with new data."
x = Signature()
print "x is ", x.data
x.data = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
print "now, x is ", x.data
y = Signature()
print "y is ", y.data
y.data = [0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0]
print "now, y is ", y.data

print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

print "Testing signature.weigh()"
print "x is", x.data,"and x.weigh() is", x.weigh()
print "y is", y.data,"and y.weigh() is", y.weigh()

print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

print "Testing signature.left_justify()"
print "x.left_justify()"
print x.left_justify()
print "x is", x.data,"and x.weigh() is", x.weigh()
print "y is", y.data,"and y.weigh() is", y.weigh()

print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

print "Test weighing and left justifying all zeros case (rest)"
z = Signature()
print "z is ", z.data, "and z.weigh() is", z.weigh()
print "z.left_justify() results in", z.left_justify()

print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
print "Test minweight"
b = Signature()
print "we have a signature b equal to ", b.data
b.data = [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1]
print "we modified b with pitches ", b.data
b.minweight()
print "running minimum weight on it gives", b.data
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="


print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
print "test rotate"
c = Signature()
print "c is ", c.data
c.rotate(3)
print "c.rotate(3) is", c.data 

c.data = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
print "c is ", c.data
c.rotate(3)
print "c.rotate(3) is", c.data

c.data = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
print "c is ", c.data
c.rotate(-3)
print "c.rotate(-3) is", c.data

c.data = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
print "c is ", c.data
c.rotate(48)
print "c.rotate(48) is", c.data
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

print "test arpeggiate"
c = Signature()
print "c is ", c.data
c.arpeggiate()

c.data = [1,0,1,0,1,0,1,0,1,0,1,0]
print "c is ", c.data
c.arpeggiate()

c.data = [0,0,0,0,0,0,0,0,0,0,0,1]
print "c is ", c.data
c.arpeggiate()

print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="




print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# setup rtmidi as our backend
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#select rtmidi as our backend
mido.set_backend('mido.backends.rtmidi')
print "Backend selected is %s " % mido.backend
out = None

#open up a rtmidi output port for playing midi files

try:
	out = mido.open_output()
except:
	pass
	print "Failed to open a MIDO output port, but going on with the rest of the show."

if out != None:
	print "Test tones!"
	for i in range(36,45):
		my_on_message = mido.Message('note_on', note=i, velocity=100)
		print my_on_message
		out.send(my_on_message)
		time.sleep(0.2)
		my_off_message = mido.Message('note_off', note=i, velocity=100)
		print my_off_message
		out.send(my_off_message)
		time.sleep(0.05)