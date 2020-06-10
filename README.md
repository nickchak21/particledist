# particledist

`particledist` is the analysis package we built. It uses deep learning to analyze event mass distributions and find new signals/physics. Once you follow the installation instructions below, you can use the starter code provided to replicate our analysis. You can also change some of the hyperparameters to investigate how the model optimizes.

This package is mainly built on top of the EnergyFlow package (arXiv:1810.05165v2). EnergyFlow contains the base deep learning architecture we are using (the Particle Flow Network), as well as tools to load jet/event data and calculate invariant event masses. Our method makes use of these tools, but applies them in different ways than originally intended to find new physics.

<br/>

**What's Inside this Repository**

This repository includes the particledist package code, for any people that are curious as to how our analysis package functions. The code is inside the `particledist` folder. All the working methods and classes are fully commented, so you can get an idea of what's going on behind the scenes.

This repo also has some starter code for using our package and replicating our analysis (`starter_code.ipynb`). Instructions are below, after the installation instructions.

<br/>

**Installation Instructions**

Even if you have the normal canon of data analysis and machine learning tools installed (`numpy`, `scipy`, `tensorflow1`, etc.), there are still a few packages that `particledist` requires. You should check to make sure you have the following before attempting installation:

`energyflow` - contains the Particle Flow Network architecture used in our model, as well as tools to load data and calculate invariant event masses <br/>
`matplotlib` - for making plots <br/>
`scikit-learn` - for calculating AUC scores <br/>
`h5py` - used to open MOD H5 files, which is how our data is stored <br/>
`POT` - a High Energy Physics package that contains some important functions <br/>

If all of these requirements are satisfied, try installation with `pip install --user particledist`. If you are missing packages, the error message should tell you which package and what version you need to install. We have run into issues with `cython` and `tensorflow1` in the past -- just for reference. Once the package finishes installing, check that the version is `1.1.2` -- this is the latest version.

If you don't have the canon of tools installed, you will have to install the 5 required packages first before running `pip install --user particledist`. Although the pip installer will likely fill the rest of the dependencies by itself, sometimes it fails. Again, look at the error message to see which package and what version you need to install.

<br/>

**How the Analysis Works**

More details on the exact technique used can be found in our NeurIPS submission paper, but below is a quick summary.

A specified number of CMS Open Data simulation jets are loaded (in the starter code, this amounts to about `3,000,000` jets). These jets are sorted by event, and only 2-jet events are retained (this leaves us with about `500,000` events). Then, a specified number of events (`50,000`, `70,000`, and `100,000` for our analysis) are selected at random and graphed on a histogram with bins `660 - 760`, `760 - 860`, `860 - 960`, `960 - 1060`, `1060 - 1160 GeV`. The Particle Flow Network (PFN) is applied on consecutive bins, with the goal of classifying jets as part of one bin or another.

Ordinarily, the PFN classifies between event mass bins with an mean AUC of `0.5` (no better than chance). However, if the AUC ever fluctuates from `0.5`, we know that there is some form of new or unexpected physics.

<br/>

**What the Starter Code Does**

The starter code is a Jupyter Notebook (`starter_code.ipynb`) file. Ignore the output in the Jupyter Notebook -- yours will look different. We updated the library since we last ran the full analysis code.

The notebook will take `50` samples of `50,000`, `70,000`, and `100,000` events and try and classify them with the above method. Since there is just normal physics present, the code will output an AUC mean of about `0.5` for bins `1-2`, `2-3`, `3-4`, and `4-5`. 

The code will also output another number for each pair of bins -- this is the uncertainty in AUC. This is so that when we perform signal injection (we injected 2-gluon events), we know how many events it will take before our method has 3-sigma and 5-sigma confidence that there is new physics.

You will be able to change the number of samples taken and the number of events per sample if you want to try and optimize our model. Keep in mind that to run the starter code, it takes about 2-3 hours on 4 NVIDIA GPUs (it's not the model that is hard to train; rather, it's the fact that we have to train the Particle Flow Network 200 times).

We did not include our signal injection code with the starter code because it's a bit more messy (our analysis package doesn't support signal injection yet, so we had to do it manually). If you would like to replicate our analysis in that area, send us a query to us over Microsoft CMT (to maintain anonymity).
