#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from time import process_time
import energyflow as ef
import numpy as np
import matplotlib.pyplot as plt

'''Parameters: list of event masses, and a list of the corresponding event data

This class creates mass distributions with a constant bin size, eliminating any bins
with less than the cutoff number of jets. It also pads the jet information arrays to
prepare them for input into the Particle Flow Network.

@param = parameters
@instance = new instance variables created
@return = values returned'''

class MassDistribution:

    def __init__(self, mass_list, event_list):
    '''Initializes the MassDistribution object
    @param: list of event masses (mass_list), list of corresponding event data (event_list)
    @instance: list of event masses (self.mass_list), list of corresponding event data (self.event_list)'''
    
        self.event_list = event_list
        self.mass_list = mass_list

    def divide_mass_bins(self, mass_bin_size, cutoff_jets):
    '''Divides the event data into mass bins
    @param: size of each mass bin (mass_bin_size), minimum number of jets in each bin (cutoff_jets) -- these
    values must be standardized to have a meaningful analysis
    @instance: list of mass ranges that have more events than cutoff_jets (self.mass_ranges),
    list of events divided by eligible mass ranges (self.event_mass_bins)'''    
        
        mass_ranges = []
        max_mass = max(self.mass_list)
        min_mass = min(self.mass_list)
        previous_mass = min_mass
        for current_mass in np.arange(min_mass + mass_bin_size, max_mass, mass_bin_size):
            mass_ranges.append([previous_mass, current_mass])
            previous_mass = current_mass

        self.mass_ranges = mass_ranges

        #Sort indices into different mass ranges
        
        index_bins = []
        for mass_range in mass_ranges:
            index_bins.append([])

        index = 0
        for event_mass in self.mass_list:
            mass_bin = 0
            for mass_range in mass_ranges:
                if event_mass > mass_range[0] and event_mass <= mass_range[1]:
                    index_bins[mass_bin].append(index)
                    break
                mass_bin += 1
            index += 1

        #Remove bins that don't have enough jets   
        remove_indices = []
        i = 0
        for mass_bin in index_bins:
            if len(mass_bin) < cutoff_jets:
                remove_indices.append(i)
            i += 1
        
        for index in sorted(remove_indices, reverse=True):
            del index_bins[index]
            
        for index in sorted(remove_indices, reverse=True):
            del self.mass_ranges[index]

            
        #Create bins with event mass and particles
            
        self.event_mass_bins = []
        i = 0
        for mass_bin in index_bins:
            self.event_mass_bins.append([])
            for index in mass_bin:
                self.event_mass_bins[i].append(self.event_list[index])
            i += 1


    def get_mass_ranges(self):
    '''Retrieval method so we can see the mass bin boundaries that made the cut.
    @param: none
    @instance: none
    @return: eligible mass bin boundaries (self.mass_ranges)'''
    
        return self.mass_ranges

    def extract_jets_into_mass_bins(self):
    '''Extracts the jet data out of the events within each bin.
    @param: none
    @instance: list of jet data divided by event mass bins (self.jet_mass_bins)'''
        
        self.jet_mass_bins = []

        i = 0
        for mass_bin in self.event_mass_bins:
            self.jet_mass_bins.append([])
            for event in mass_bin:
                for jet in event:
                    self.jet_mass_bins[i].append(jet)
            i += 1

    def max_particles_per_jet(self)
    '''Returns the max number of particles contained within a jet (this is useful when we pad the jet arrays).
    @param: none
    @instance: none
    @return: maximum number of particles in a jet (max_particles_per_jet)'''
    
        max_particles_per_jet = []
        for jet_mass_bin in self.jet_mass_bins:
            array_lengths = []
            for i in range(len(jet_mass_bin1)):
                array_lengths.append(len(jet_mass_bin1[i]))
            max_particles_per_jet.append(max(array_lengths))

        return max_particles_per_jet

    def pad_jet_arrays(self, num_particles):
    '''Pad the jet data arrays so they are not jagged (jagged means have different numbers of data points per row)
    @param: amount of particles to pad to -- will become 2nd component of array shape (num_particles)
    @instance: padded jet data sorted by event mass bins (self.padded_jet_arrays)'''
        
        self.padded_jet_arrays = []
        
        for mass_bin in self.jet_mass_bins:
            jet_array = np.zeros((len(mass_bin),num_particles,6))
            for i in range(len(mass_bin)):
                for j in range(num_particles):
                    for k in range(6):
                        try:
                            jet_array[i,j,k] = mass_bin[i][j][k]
                        except IndexError:
                            jet_array[i,j,k] = 0
            self.padded_jet_arrays.append(jet_array)
            
