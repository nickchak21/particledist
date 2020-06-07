# particledist

This is a package that uses deep learning to analyze event mass distributions and find new particles. Once you follow the installation instructions below, you can use the starter code provided to replicate our analysis. You can also change some of the hyperparameters to investigate how the model optimizes.

**Installation Instructions**

Even if you have the normal canon of data analysis and machine learning tools installed (`numpy`, `scipy`, `tensorflow1`, etc.), there are still a few packages that `particledist` requires. You should check to make sure you have the following before attempting installation:

`matplotlib` - for making plots <br/>
`scikit-learn` - for calculating AUC scores <br/>
`energyflow` - contains the Particle Flow Network architecture used in our model <br/>
`h5py` - used to open MOD H5 files, which is how our data is stored <br/>
`POT` - a High Energy Physics package that contains some important functions <br/>

If all of these requirements are satisfied, try installation with `pip install --user particledist`. If you are missing packages, the error message should tell you which package and what version you need to install. I have run into issues with `cython` and `tensorflow1` in the past -- just for reference. Once the package finishes installing, check that the version is 1.1.2 -- this is the latest version.

If you don't have the canon of tools installed, you will have to install the 5 required packages first before running `pip install --user particledist`. Although the pip installer will likely fill the rest of the dependencies by itself, sometimes it fails. Again, look at the error message to see which package and what version you need to install.

**How the Analysis Works**

More details on the exact technique used can be found in our NeurIPS submission paper, but below is a quick summary.

A specified number of CMS Open Data simulation jets are loaded (in the starter code, this amounts to about 3,000,000 jets). These jets are sorted by event. Then, 50,000 events are selected at random and graphed on a histogram with bins 660 - 760, 760 - 860, 860 - 960, 960 - 1060, 1060 - 1160.


