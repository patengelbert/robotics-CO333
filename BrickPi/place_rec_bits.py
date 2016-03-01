#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os

# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 360):
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
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
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
	
	def run(self):
		# Prior to starting learning the locations, it should delete files from previous
		# learning either manually or by calling signatures.delete_loc_files(). 
		# Then, either learn a location, until all the locations are learned, or try to
		# recognize one of them, if locations have already been learned.
		
		#signatures.delete_loc_files()
		learn_location();
		recognize_location();

	def characterize_location(self):
		# TODO make the signature angle invariant
		ls = LocationSignature()
		for i in range(len(ls.sig)):
			robot.rotateSonar()
			self.depth = self.robot.ultraSonic.getValue()
			ls.sig[i] = self.depth
		return ls

	# FILL IN: compare two signatures
	def compare_signatures(self, ls1, ls2):
		dist = 0
		print "TODO:    You should implement the function that compares two signatures."
		return dist

	# This function characterizes the current location, and stores the obtained 
	# signature into the next available file.
	def learn_location(self):
		ls = LocationSignature()
		ls = characterize_location()
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
		ls_obs = LocationSignature();
		characterize_location(ls_obs);

		# FILL IN: COMPARE ls_read with ls_obs and find the best match
		for idx in range(self.signatures.size):
			print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
			ls_read = self.signatures.read(idx);
			dist    = compare_signatures(ls_obs, ls_read)