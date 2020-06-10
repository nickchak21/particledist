#!/usr/bin/env python3

# standard library imports
from __future__ import absolute_import, division, print_function

# standard numerical library imports
import numpy as np

# energyflow imports
import energyflow as ef
from energyflow.archs import PFN
from energyflow.datasets import qg_jets
from energyflow.utils import data_split, remap_pids, to_categorical

# import libraries to supress output
from contextlib import contextmanager
import sys, os

# attempt to import sklearn
try:
    from sklearn.metrics import roc_auc_score, roc_curve
except:
    print('please install scikit-learn in order to make ROC curves')
    roc_curve = False

# attempt to import matplotlib
try:
    import matplotlib.pyplot as plt
except:
    print('please install matplotlib in order to make plots')
    plt = False

    
'''Suppress output by EnergyFlow package during the Particle Flow Network (PFN) creation and training''' 
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def PFN_AUC_calculation(jet_array_1, jet_array_2, train_size, test_size):
    '''Trains a PFN on two jet-particle data arrays coming from two consecutive bins. The PFN will then attempt to
    classify testing jets as part of one bin or another.
    @param: size of training set (train_size), size of testing set (test_size) -- these values must be standardized
    to have a meaningful analysis
    @return: AUC score obtained from trying trained model on test set (auc)'''            

    X = np.concatenate([jet_array_1, jet_array_2])[:,:,:4]
    y = np.concatenate([np.ones(len(jet_array_1)), np.zeros(len(jet_array_2))])

    ################################### SETTINGS ###################################

    # data controls
    train, val, test = train_size, X.shape[0]-train_size-test_size, test_size
    use_pids = True

    # network architecture parameters
    Phi_sizes, F_sizes = (100, 100, 128), (100, 100, 100)

    # network training parameters
    num_epoch = 10
    batch_size = 500

    ################################################################################

    # convert labels to categorical
    Y = to_categorical(y, num_classes=2)

    # preprocess by centering jets and normalizing pts
    for x in X:
        mask = x[:,0] > 0
        yphi_avg = np.average(x[mask,1:3], weights=x[mask,0], axis=0)
        x[mask,1:3] -= yphi_avg
        x[mask,0] /= x[:,0].sum()

    # handle particle id channel
    if use_pids:
        remap_pids(X, pid_i=3)
    else:
        X = X[:,:,:3]

    # do train/val/test split 
    (X_train, X_val, X_test,
     Y_train, Y_val, Y_test) = data_split(X, Y, val=val, test=test)

    # build architecture
    pfn = 0
    with suppress_stdout(): #suppress output of creating model
        pfn = PFN(input_dim=X.shape[-1], Phi_sizes=Phi_sizes, F_sizes=F_sizes)

    # train model
    pfn.fit(X_train, Y_train,
              epochs=num_epoch,
              batch_size=batch_size,
              validation_data=(X_val, Y_val),
              verbose=0)

    # get predictions on test data
    preds = pfn.predict(X_test, batch_size=1000)

    # get area under the ROC curve
    auc = roc_auc_score(Y_test[:,1], preds[:,1])
    
    return auc

'''Parameters: the padded jet arrays from the sample event mass distribution

This class applies the PFN across consecutive bins in a mass distribution, generating an AUC score for each pair
of bins.

@param = parameters
@instance = new instance variables created
@return = values returned'''

class PFNDist:
    def __init__(self, padded_jet_arrays):
    '''Initializes the PFNDist object
    @param: list of padded jet arrays from event mass distribution (padded_jet_arrays)
    @instance: list of padded jet arrays (self.padded_jet_arrays)'''
    
        self.padded_jet_arrays = padded_jet_arrays

    def generate_AUCs(self, train_size, test_size):
    '''Generate list of AUCs by running PFN on consecutive mass bins in event mass distribution
    @param: amount of jets to train on (train_size), amount of jets to test on (test_size) -- these values must
    be standardized to have a meaningful analysis
    @instance: none
    @return: list of AUC scores generated across each onsecutive pair of bins (AUC_scores)'''
    
        AUC_scores = []
        for i in range(len(self.padded_jet_arrays) - 1):
            auc = PFN_AUC_calculation(self.padded_jet_arrays[i], self.padded_jet_arrays[i+1],
                                      train_size, test_size)
            AUC_scores.append(auc)

        print(AUC_scores)
        
        return AUC_scores
