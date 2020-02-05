import os
folderroot = '/Users/lucaizzo/Documents/NOT/test/'
os.chdir(folderroot)
import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
import shutil

import sys
from pyraf import iraf
iraf.noao(_doprint=0)
iraf.imred(_doprint=0)
iraf.ccdred(_doprint=0)
iraf.twodspec(_doprint=0)
iraf.longslit(_doprint=0)
iraf.kpnoslit(_doprint=0)
iraf.astutil(_doprint=0)
iraf.onedspec(_doprint=0)
iraf.twodspec.longslit.dispaxis = 2

#read object keywords
for file in os.listdir(os.getcwd()):
    if file.endswith('.fits'):
        testfile = file


hduo = fits.open(testfile)

#name targets (science & standard)
target = hduo[0].header['OBJECT']
#target2 = 'SP0644p375'
#std = 'SP0305+261'

#create list of science files
sci = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.fits'):
        sci.append(file+'[1]')


file1 = open('listasci', 'w')
file1.writelines(["%s\n" % item  for item in sci])
file1.close()

#copy calib files in the current dir
shutil.copy(folderroot+'bias/bias.fits', folderroot)
shutil.copy(folderroot+'flat/response.fits', folderroot)

#Subtract bias
iraf.imarith('@listasci', '-', 'bias.fits', '@listasci//_2b')

#flat subtraction
iraf.imarith('*_2b.fits', '/', 'response.fits', '@listasci//_2bf')

#SCIENCE
#APALL
iraf.imred.kpnoslit
final = []
for file in os.listdir(os.getcwd()):
    if file.endswith('2bf.fits'):
        final.append(file)


file1 = open('listafinal', 'w')
file1.writelines(["%s\n" % item  for item in final])
file1.close()

f = open('listafinal')
i = 1
for item in f:
    file = item.split('\n')[0]
    shutil.copy(file, 'spec'+str(i)+'.fits')
    i += 1


#FROM NOW -> iraf
iraf.noao.twodspec.apextract
iraf.apall('spec*.fits')

#assign dispersion solution - from now IRAF

shutil.copy('./arc/database/idarc1.ms','./database/.')
for file in os.listdir(os.getcwd()):
    if file.endswith('ms.fits'):
        iraf.hedit(file,fields="REFSPEC1",value="arc1.ms",add='yes',ver='no',show='yes')

#wavelength calinration
for file in os.listdir(os.getcwd()):
    if file.endswith('ms.fits'):
        iraf.dispcor(file, 'd'+file)


#flux calibration
shutil.copy('./stds/sens.0001.fits','.')
shutil.copy('./stds/lapalmaextinct.dat','.')


for file in os.listdir(os.getcwd()):
    if file.startswith('dspec'):
        iraf.calibrate(file, 'f'+file)

#combine spectra
finalcomb = []
for file in os.listdir(os.getcwd()):
    if file.startswith('fds'):
        finalcomb.append(file)


file1 = open('listascombine', 'w')
file1.writelines(["%s\n" % item  for item in finalcomb])
file1.close()

iraf.scombine('@listascombine', 'temp_quick.fits')

iraf.scopy('temp_quick.fits',target+'_quick.fits',w1='4000',w2='9000')

#mv final file in a dedicated folder
shutil.copy(target+'_quick.fits','./output/.')

#remove temp FILES
os.remove('lapalmaextinct.dat')
for file in os.listdir(os.getcwd()):
    if file.endswith('fits'):
        os.remove(file)
    elif file.startswith('lista'):
        os.remove(file)
    elif file.startswith('log'):
        os.remove(file)


shutil.rmtree('database')
