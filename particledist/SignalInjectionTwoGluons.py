#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from time import process_time
import energyflow as ef
import numpy as np
import matplotlib.pyplot as plt
import MassDistribution

class SignalInjectionTwoGluons:
    def __init__(self, mass_list, event_jet_labels, event_list, mass_bin_size):
        self.mass_list = mass_list
        self.event_jet_labels = event_jet_labels
        self.event_list = event_list
        self.mass_bin_size = mass_bin_size

    def filter_gluon_events(self):
        indexes_gluon_events = []

        index = 0
        for event in self.event_jet_labels:
            if event[0] == 21 and event[1] == 21:
                indexes_gluon_events.append(index)
            index += 1

        self.mass_list_2_gluons = [self.mass_list[j] for j in indexes_gluon_events]
        self.event_list_2_gluons = [self.event_list[j] for j in indexes_gluon_events]
        

    def sort_gluon_events(self):
        gluon_events = new MassDistribution(self.mass_list_2_gluons, self.event_list_2_gluons)
        gluon_events.divide_mass_bins(self.mass_bin_size, 0)
        self.event_mass_2_gluons_bins = gluon_events.event_mass_bins

    def get_gluon_events_in_bin(self, index):
        return self.event_mass_2_gluons_bins[index]

    

        
        
                
