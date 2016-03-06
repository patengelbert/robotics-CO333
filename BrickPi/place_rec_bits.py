
#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os
import math
from robot import Robot

# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 180):
        self.sig = [0] * no_bins
        
    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self, size = 5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
		
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number. 
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;
 
    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)
            
        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = None
        filename = self.filenames[index]
        if os.path.isfile(filename):
            ls = LocationSignature()
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline().rstrip()
                if (s != ''):
                    ls.sig[i] = float(s)
            f.close();
        else:
            print "WARNING: Signature does not exist."
        
        return ls
    
class PlaceRecognition():    

	def __init__(self, robot):
		self.depth = 0;
		self.robot = robot
		
		self.signatures = SignatureContainer(5);
		
		self.rotateStep = 2; # Degrees between each reading
	
	def run(self, option):
		# Prior to starting learning the locations, it should delete files from previous
		# learning either manually or by calling signatures.delete_loc_files(). 
		# Then, either learn a location, until all the locations are learned, or try to
		# recognize one of them, if locations have already been learned.
		
		if option== 2:
			self.signatures.delete_loc_files()
		elif option == 1:
			self.learn_location();
		elif option == 0:
			self.recognize_location();
		else:
			print "Error: Unknown command"	
			return True
		return False

	# runs ultraSonic scan and puts values into signature
	def characterize_location(self):
		ls = LocationSignature()
		robot.ultraSonic.ultrasonicScans = len(ls.sig)
		robot.ultraSonic.scan()
		for i in range(len(ls.sig)):
			if math.isinf(robot.ultraSonic.scanData[i]):
				ls.sig[i] = 255
			else:
				ls.sig[i] = robot.ultraSonic.scanData[i]
		return ls

	# converts signatures to angle invariant arrays and computes a difference between them
	def compare_signatures_invariant(self, ls1, ls2):
		if len(ls1.sig) != len(ls2.sig):
			return -1
		dist = 0
		rangeSize = 10.0
		rangeLen = int(math.ceil(256/rangeSize))
		rangeA = [0]*rangeLen
		rangeB = [0]*rangeLen
		for i in range(len(ls1.sig)):
			a = int(ls1.sig[i]/rangeSize)
			b = int(ls2.sig[i]/rangeSize)
			rangeA[a]+= 1
			rangeB[b]+= 1
		
		#print "Range A:\n"
		#for n in rangeA:
		#	print( (u'\u2588' * (n)) + "\n")

		#print "Range B:\n"
		#for n in rangeB:
		#	print( (u'\u2588' * (n)) + "\n")

		for i in range(len(rangeA)):
			dist += (rangeA[i] - rangeB[i]) ** 2
		return dist

	# This function characterizes the current location, and stores the obtained 
	# signature into the next available file.
	def learn_location(self):
		ls = LocationSignature()
		ls = self.characterize_location()
		idx = self.signatures.get_free_index();
		if (idx == -1): # run out of signature files
			print "\nWARNING:"
			print "No signature file is available. NOTHING NEW will be learned and stored."
			print "Please remove some loc_%%.dat files.\n"
			return
		
		self.signatures.save(ls,idx)
		print "STATUS:  Location " + str(idx) + " learned and saved."

	# This function tries to recognize the current location.
	# 1.   Characterize current location
	# 2.   For every learned locations
	# 2.1. Read signature of learned location from file
	# 2.2. Compare signature to signature coming from actual characterization
	# 3.   Retain the learned location whose minimum distance with
	#      actual characterization is the smallest.
	# 4.   Display the index of the recognized location on the screen
	def recognize_location(self):
		ls_obs = self.characterize_location();
		closest = (0, float('inf'))
		angle = (0, float('inf'))
		# FILL IN: COMPARE ls_read with ls_obs and find the best match
		for idx in range(self.signatures.size):
			print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
			ls_read = self.signatures.read(idx);
			if(ls_read is None):
				continue
			dist    = self.compare_signatures_invariant(ls_obs, ls_read)
			if dist < closest[1]:
				closest = (idx, dist)
		print "STATUS:	Found current waypoint at " + str(closest[0])
		curr_loc = self.signatures.read(closest[0])
		for i in range(0, len(ls_obs.sig)):
			dist = self.compare_signatures_variant(curr_loc, ls_obs, i)
			if dist < angle[1]:
				angle = (i, dist)
		print "STATUS:	Found current angle at " + str(angle[0]*360/len(ls_obs.sig))
		return {'location': closest[0], 'angle': angle[0]*360/len(ls_obs.sig)}

	def compare_signatures_variant(self, ls1, ls2, offset):
		dist = 0
		if len(ls1.sig) != len(ls2.sig):
			return -1
		for i in range(0, len(ls1.sig)):
			dist += (ls1.sig[(i+offset)%len(ls1.sig)]-ls2.sig[i])**2
		return dist

if __name__ == '__main__':
	robot = Robot()
	p = PlaceRecognition(robot)
	error = False
	while not error:
		option = input("Option: Scan=0, Learn=1, Clear=2\n")
		error = p.run(option)

