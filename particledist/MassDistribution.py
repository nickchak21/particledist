#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from time import process_time
import energyflow as ef
import numpy as np
import matplotlib.pyplot as plt


class MassDistribution:
    def __init__(self, mass_list, event_list):
        self.event_list = event_list
        self.mass_list = mass_list

    def divide_mass_bins(self, mass_bin_size, cutoff_jets):
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
        return self.mass_ranges

    def extract_jets_into_mass_bins(self):
        self.jet_mass_bins = []

        i = 0
        for mass_bin in self.event_mass_bins:
            self.jet_mass_bins.append([])
            for event in mass_bin:
                for jet in event:
                    self.jet_mass_bins[i].append(jet)
            i += 1

    def max_particles_per_jet(self):
        max_particles_per_jet = []
        for jet_mass_bin in self.jet_mass_bins:
            array_lengths = []
            for i in range(len(jet_mass_bin1)):
                array_lengths.append(len(jet_mass_bin1[i]))
            max_particles_per_jet.append(max(array_lengths))

        return max_particles_per_jet

    def pad_jet_arrays(self, num_particles):
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
            
