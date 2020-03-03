#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from time import process_time
import energyflow as ef
import numpy as np
import matplotlib.pyplot as plt

def PFN_AUC_calculation(jet_array_1, jet_array_2, train_size, test_size):
    X = np.concatenate([jet_array_1, jet_array_2])[:,:,:4]
    y = np.concatenate([np.ones(len(jet_array_1)), np.zeros(len(jet_array_2))])

    ################################### SETTINGS ###################################
    # the commented values correspond to those in 1810.05165
    ###############################################################################

    # data controls, can go up to 2000000 for full dataset
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

    print('Loaded quark and gluon jets')

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

    print('Finished preprocessing')

    # do train/val/test split 
    (X_train, X_val, X_test,
     Y_train, Y_val, Y_test) = data_split(X, Y, val=val, test=test)

    print('Done train/val/test split')
    print('Model summary:')

    # build architecture
    pfn = PFN(input_dim=X.shape[-1], Phi_sizes=Phi_sizes, F_sizes=F_sizes)

    # train model
    pfn.fit(X_train, Y_train,
              epochs=num_epoch,
              batch_size=batch_size,
              validation_data=(X_val, Y_val),
              verbose=1)

    # get predictions on test data
    preds = pfn.predict(X_test, batch_size=1000)

    # get area under the ROC curve
    auc = roc_auc_score(Y_test[:,1], preds[:,1])

    return auc


class PFNDist:
    def __init__(self, padded_jet_arrays):
        self.padded_jet_arrays = padded_jet_arrays

    def generate_AUCs(self, train_size, test_size):
        AUC_scores = []
        for i in range(len(self.padded_jet_arrays) - 1):
            auc = PFN_AUC_calculation(self.padded_jet_arrays[i], self.padded_jet_arrays[i+1],
                                      train_size, test_size)
            AUC_scores.append(auc)

        return AUC_scores
