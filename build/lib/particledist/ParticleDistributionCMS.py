#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from time import process_time
import energyflow as ef
import numpy as np
import matplotlib.pyplot as plt


class ParticleDistributionCMS:
    def __init__(self, sim):
        sim_numbers = set(sim.evns)
        t1_start = process_time() 

        self.event_list = []
        self.event_jet_labels = []
        
        self.event_pts = []
        self.event_etas = []
        self.event_phis = []
        self.event_ms = []

        for evn_num in sim_numbers:
            self.event_list.append(np.asarray(sim.particles[sim.jets_i[:,sim.evn]==evn_num]))
            self.event_jet_labels.append(np.asarray(sim.hard_pids[sim.jets_i[:,sim.evn]==evn_num]))
            
            self.event_pts.append(np.asarray(sim.jet_pts[sim.jets_i[:,sim.evn]==evn_num]))
            self.event_etas.append(np.asarray(sim.jet_etas[sim.jets_i[:,sim.evn]==evn_num]))
            self.event_phis.append(np.asarray(sim.jet_phis[sim.jets_i[:,sim.evn]==evn_num]))
            self.event_ms.append(np.asarray(sim.jet_ms[sim.jets_i[:,sim.evn]==evn_num]))

        self.event_stats = []

        for i in range(len(self.event_pts)):
            self.event_stats.append([])
    
            for j in range(len(self.event_pts[i])):
                ptyphims = []
                ptyphims.append(self.event_pts[i][j])
                ptyphims.append(self.event_etas[i][j])
                ptyphims.append(self.event_phis[i][j])
                ptyphims.append(self.event_ms[i][j])
                p4s = ef.p4s_from_ptyphims(np.array(ptyphims))
        
                self.event_stats[i].append(p4s.tolist())
        
        t1_stop = process_time()

        print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)


    def max_jets_in_event(self):
        max_jets_in_event = max([len(self.event_pts[i]) for i in range(len(self.event_pts))])
        return max_jets_in_event
        
    def num_events(self):
        return len(self.event_pts)

    def choose_1jet_events(self):
        self.event_list_1 = []
        indexes = []
        i = 0
        for evn in self.event_list:
            if len(evn) == 1:
              self.event_list_1.append(evn)
              indexes.append(i)
            i += 1
        self.event_stats_1 = [self.event_stats[j] for j in indexes]
        self.event_jet_labels_1 = [self.event_jet_labels[j] for j in indexes]

    def choose_2jet_events(self):
        self.event_list_2 = []
        indexes = []
        i = 0
        for evn in self.event_list:
            if len(evn) == 2:
              self.event_list_2.append(evn)
              indexes.append(i)
            i += 1
        self.event_stats_2 = [self.event_stats[j] for j in indexes]
        self.event_jet_labels_2 = [self.event_jet_labels[j] for j in indexes]

    def choose_3jet_events(self):
        self.event_list_3 = []
        indexes = []
        i = 0
        for evn in self.event_list:
            if len(evn) == 3:
              self.event_list_3.append(evn)
              indexes.append(i)
            i += 1
        self.event_stats_3 = [self.event_stats[j] for j in indexes]
        self.event_jet_labels_3 = [self.event_jet_labels[j] for j in indexes]

    def choose_4jet_events(self):
        self.event_list_4 = []
        indexes = []
        i = 0
        for evn in self.event_list:
            if len(evn) == 4:
              self.event_list_4.append(evn)
              indexes.append(i)
            i += 1
        self.event_stats_4 = [self.event_stats[j] for j in indexes]
        self.event_jet_labels_4 = [self.event_jet_labels[j] for j in indexes]

    def length_1jet_events(self):
        return len(self.event_list_1)

    def length_2jet_events(self):
        return len(self.event_list_2)

    def length_3jet_events(self):
        return len(self.event_list_3)

    def length_4jet_events(self):
        return len(self.event_list_4)


    def add_event4vectors_1jet(self):
        self.event_stats_added_1 = []
        for i in range(len(self.event_stats_1)):
            event_1 = self.event_stats_1[i][0][0]
            event_2 = self.event_stats_1[i][0][1]
            event_3 = self.event_stats_1[i][0][2]
            event_4 = self.event_stats_1[i][0][3]
            event = [event_1, event_2, event_3, event_4]
            self.event_stats_added_1.append(event)

    def add_event4vectors_2jet(self):
        self.event_stats_added_2 = []
        for i in range(len(self.event_stats_2)):
            event_1 = self.event_stats_2[i][0][0] + self.event_stats_2[i][1][0]
            event_2 = self.event_stats_2[i][0][1] + self.event_stats_2[i][1][1]
            event_3 = self.event_stats_2[i][0][2] + self.event_stats_2[i][1][2]
            event_4 = self.event_stats_2[i][0][3] + self.event_stats_2[i][1][3]
            event = [event_1, event_2, event_3, event_4]
            self.event_stats_added_2.append(event)

    def add_event4vectors_3jet(self):
        self.event_stats_added_3 = []
        for i in range(len(self.event_stats_3)):
            event_1 = self.event_stats_3[i][0][0] + self.event_stats_3[i][1][0] + self.event_stats_3[i][2][0]
            event_2 = self.event_stats_3[i][0][1] + self.event_stats_3[i][1][1] + self.event_stats_3[i][2][1]
            event_3 = self.event_stats_3[i][0][2] + self.event_stats_3[i][1][2] + self.event_stats_3[i][2][2]
            event_4 = self.event_stats_3[i][0][3] + self.event_stats_3[i][1][3] + self.event_stats_3[i][2][3]
            event = [event_1, event_2, event_3, event_4]
            self.event_stats_added_3.append(event)

    def add_event4vectors_4jet(self):
        self.event_stats_added_4 = []
        for i in range(len(self.event_stats_4)):
            event_1 = self.event_stats_4[i][0][0] + self.event_stats_4[i][1][0] + self.event_stats_4[i][2][0] + self.event_stats_4[i][3][0]
            event_2 = self.event_stats_4[i][0][1] + self.event_stats_4[i][1][1] + self.event_stats_4[i][2][1] + self.event_stats_4[i][3][1]
            event_3 = self.event_stats_4[i][0][2] + self.event_stats_4[i][1][2] + self.event_stats_4[i][2][2] + self.event_stats_4[i][3][2]
            event_4 = self.event_stats_4[i][0][3] + self.event_stats_4[i][1][3] + self.event_stats_4[i][2][3] + self.event_stats_4[i][3][3]
            event = [event_1, event_2, event_3, event_4]
            self.event_stats_added_3.append(event)

    def event_mass_1jet(self):
        self.event_mass_1jet = []
        for event_4_vector in self.event_stats_added_1:
            event_4_list = list(event_4_vector)
            event_4_array = np.array(event_4_list)
            event_mass = ef.ms_from_p4s(event_4_array)
            self.event_mass_1jet.append(event_mass)

    def event_mass_2jet(self):
        self.event_mass_2jet = []
        for event_4_vector in self.event_stats_added_2:
            event_4_list = list(event_4_vector)
            event_4_array = np.array(event_4_list)
            event_mass = ef.ms_from_p4s(event_4_array)
            self.event_mass_2jet.append(event_mass)

    def event_mass_3jet(self):
        self.event_mass_3jet = []
        for event_4_vector in self.event_stats_added_3:
            event_4_list = list(event_4_vector)
            event_4_array = np.array(event_4_list)
            event_mass = ef.ms_from_p4s(event_4_array)
            self.event_mass_3jet.append(event_mass)

    def event_mass_4jet(self):
        self.event_mass_4jet = []
        for event_4_vector in event_stats_added_4:
            event_4_list = list(event_4_vector)
            event_4_array = np.array(event_4_list)
            event_mass = ef.ms_from_p4s(event_4_array)
            self.event_mass_4jet.append(event_mass)

    def max_event_njet(self, n):
        if n == 1:
            return max(self.event_mass_1jet)
        elif n == 2:
            return max(self.event_mass_2jet)
        elif n == 3:
            return max(self.event_mass_3jet)
        elif n == 4:
            return max(self.event_mass_4jet)
        else:
            print("No masses calculated for events of this size")
            
