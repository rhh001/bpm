#Integrating a 1+1D or 1+2D NLSE with different initial conditions and for different potentials. 
#To run this code type the command: 
#python3 bpm.py example 1D    for a 1D example   (1D.py file needed)
#python3 bpm.py example 2D    for a 2D example   (2D.py file needed)
#You can find predefined examples inside of the example folders

import numpy as np
import sys
import os
import importlib
import shutil
from shutil import copyfile
from math import floor
from tkinter import *

import_dimension = input("Select between 1D or 2D: ")           # Selects between 1D or 2D dimensions

if import_dimension == '1D':
	src=input("Select the file you want to use (full path): ")
	import_example=input("Write the name of the file (without extension): ")
	dst='./examples1D'
if import_dimension == '2D':
	src=input("Select the file you want to use (full path): ")
	import_example=input("Write the name of the file (without extension): ")
	dst='./examples2D'

shutil.copy2(src, dst) #Copy the file with the data of the example in the local directory

sys.path.insert(0, './examples'+import_dimension)		     	# adds to path the directory with examples
output_folder = './examples'+import_dimension+'/'+import_example	# directory for images and video output


if not os.path.exists(output_folder):                       # creates folder if it does not exist
    os.makedirs(output_folder)
os.system('rm '+output_folder+'/*.png')          # Erase all image files before starting computation and generating new output

my = importlib.__import__(import_example)		     # imports the file with the details for the computation
build = importlib.__import__(import_dimension)	     # selects 1D or 2D


x, y = build.grid(my.Nx,my.Ny,my.xmax,my.ymax)		# builds spatial grid
psi = my.psi_0(x,y) 					         	# loads initial condition

fft = build.fft(my.Nx,my.Ny)						# function for fast Fourier transform
ifft = build.ifft(my.Nx,my.Ny)						# function for inverse fast Fourier transform
L = build.L(my.Nx,my.Ny,my.xmax,my.ymax)			# Laplacian in Fourier space
linear_phase = np.fft.fftshift(np.exp(1.j*L*my.dt/2))            	# linear phase in Fourier space (including point swap)
border = build.absorb(x,y,my.xmax,my.ymax,my.dt,my.absorb_coeff)    # Absorbing shell at the border of the computational window

savepsi=np.zeros((my.Nx,my.images+1))     # Creates a vector to save the data of |psi|^2 for the final plot
steps_image=int(my.tmax/my.dt/my.images)  # Number of computational steps between consecutive graphic outputs


for j in range(steps_image*my.images+1):					# propagation loop

	if j%steps_image == 0:			       # Generates image output 
		build.output(x,y,psi,j/steps_image,j*my.dt,output_folder,my.output_choice,my.fixmaximum)
		savepsi[:,floor(j/steps_image)]=build.savepsi(my.Ny,psi)
		#savepsi[:,j/steps_image]=build.savepsi(my.Ny,psi)

	V = my.V(x,y,j*my.dt,psi)				# potential operator
	psi *= np.exp(-1.j*my.dt*V)				# potential phase
	psi = fft(psi)							# Fourier transform
	psi *=linear_phase		                # linear phase from the Laplacian term
	psi = border*ifft(psi)					# inverse Fourier transform and damping by the absorbing shell
	
print("output_folder: ", output_folder)
#print("x: ", x)
#print("steps_image*my: ", steps_image*my)
#print("psi:", psi)
#print("savepsi", savepsi)
print("my.output_choice", my.output_choice)
print("my.images", my.images)
print("my.fixmaximum", my.fixmaximum)
dir_path = os.path.dirname(os.path.realpath(__file__))
print("dir_path: ", dir_path)
cwd = os.getcwd()
print("cwd: ", cwd)

# Generates some extra output after the computation is finished and save the final value of psi:
build.final_output(output_folder,x,steps_image*my.dt,psi,savepsi,my.output_choice,my.images,my.fixmaximum)

