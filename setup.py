import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='particledist',
    version='1.0.9',
    author='Nick Chakraborty',
    author_email='nc165@duke.edu',
    description='Automate the search for new particles in event mass distributions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nickchak21/particledist',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'scikit-learn',
        'energyflow',
        'h5py',
        'POT'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
