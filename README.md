# particledist

This is a package that uses deep learning to analyze event mass distributions and find new particles. Once you follow the installation instructions below, you can use the boilerplate code provided to replicate our analysis. You can also change some of the hyperparameters to investigate how the model optimizes.

**Installation Instructions**

Even if you have the normal canon of data analysis and machine learning tools installed (`numpy`, `scipy`, `tensorflow 1`, etc.), there are still a few packages that `particledist` requires: you should check to make sure you have them before attempting installation:

`matplotlib` - for making plots <br/>
`scikit-learn` - for calculating AUC scores <br/>
`energyflow` - contains the Particle Flow Network architecture used in our model <br/>
`h5py` - used to open MOD H5 files, which is how our data is stored <br/>
`POT` - a High Energy Physics package that contains some important functions <br/>

If all of these requirements are satisfied, try installation with `pip install --user particledist`. If there are missing packages, the error returned should tell you which package and what version you need to install. I have run into issues with `cython` and `tensorflow 1` in the past

. This will install the package and its dependencies without any issues.

If you don't have the canon of tools installed, you may have to install some of them yourself. Namely, you will get errors 'numpy',
        'matplotlib',
        'scikit-learn',
        'energyflow',
        'h5py',
        'POT'


More details on the exact technique used can be found in our NeurIPS submission paper, but below is a quick summary:

A specified number of CMS Open Data simulation jets are loaded (in the boilerplate 
