# ALFOSC-quickred
Quick data reduction code for ALFOSC spectra 

version 0.1 - This is a very short description of the code. a better version will be provided after the "official release" (YEAH!)

This code reduces ALFOSC@NOT spectra, obtained with the grism #4 (ver 0.1) and provides a flux-calibrated spectrum using old calibration files. You need to download the entire set of files and directories somewhere into your computer.

This script requires pyraf given that it is based on IRAF scripts.
Then, the main pre-requisite consists in a working version of pyraf, which works better with python 2.7.
My suggestion consists in creating a new conda environment, in this case named "iraf27" (of course, you need first conda) using the following command

> conda create -n iraf27 python=2.7 iraf-all pyraf-all stsci

and then activate the environment with

> source activate iraf27

You should need to install astropy inside this environment, and other classical libraries like matplotlib (but it is not necessary) numpy and shutil, unless these are already available within your environment.

The code is still in a very preliminary version, but it works (at least on my mac).
The main core is the 'quick_code_test.py' script and can be easily launched from the shell once you move into the downloaded folder containing the script and the calibration files. At the moment you only need to launch 

> python quick_code_test.py

Of course, before launching, you MUST copy your science raw files (e.g. the 2D slit images named 'ALxxxxxfits') into the main root folder (what is named "folderroot" in the main script itself). The code starts reading these raw science files, correct for bias and flat field (illumination and response) and use iraf.apall to identify the trace of your target in the 2D fits. 

It then opens an interactive (classical) window where you can select the trace and the background. Instruction about the interactive use of apall can be found in the internet (e.g. http://joshwalawender.github.io/IRAFtutorial/IRAFintro_06.html)

Note that the ALFOSC images generally do not have a signal from the trace in the first ~400-500 pixels toward the blue part of the spectrum (upper part of ALFOSC 2D images)

The spectrum is then calibrated in wavelength and flux using old calibration files (obtained on December 2019) and finally cutted in the observed wavelength range (4000-9000 \AA) and moved into the output folder. The raw science files are then deleted.

Future improvements will concern detailed parameters of apall, and likely improve the structure of the code (maybe writing it in a "pythonic way")

I acknowledge the support and discussions with Charlotte Angus, Christa Gall and Daniele B. Malesani.

