# File: ./examples2D/Collapse_2D.py
# Run as    python3 bpm.py Collapse_2D 2D
# Self-similar collapse of the Townes' profile

import numpy as np

Nx = 500						# Grid points
Ny = 500
dt = 0.005					# Evolution step
tmax = 7		            # End of propagation
xmax = 20					# x-window size
ymax = xmax					# y-window size
images = 70				# number of .png images
absorb_coeff = 0		# 0 = periodic boundary
output_choice = 3      # If 1, it plots on the screen but does not save the images
							# If 2, it saves the images but does not plot on the screen
							# If 3, it saves the images and plots on the screen
fixmaximum= 2           # Fixes a maximum scale of |psi|**2 for the plots. If 0, it does not fix it.

def psi_0(x,y):				

# Initial wavefunction: the Townes' profile (computed elsewhere) is loaded
# as initial data. With it, we build the initial condition for self-similar 
# collapse. The singularity should form at t=ts

	my_data = np.genfromtxt('./examples2D/townes_profile.csv', delimiter=',')
	r=my_data[0,:]
	f=my_data[1,:]
	dr=r[1]-r[0]


	ts=8
	Nx=len(x[:,1])
	Ny=len(y[1,:])
	psi0=np.zeros((Nx,Ny))+0.j
	maxr=r[len(r)-1]

	for ix in range(Nx):
		for iy in range(Ny):
			rhere=np.sqrt(x[ix,1]**2+y[1,iy]**2)/ts
			if rhere<maxr:
				ii=int(rhere/dr);
				psi0[ix,iy]=f[ii]+(f[ii+1]-f[ii])/dr*(rhere-r[ii])
				psi0[ix,iy]=1/ts*np.exp(1.j/ts)*psi0[ix,iy]*np.exp(-1.j*(x[ix,1]**2+y[1,iy]**2)/(2*ts))
       

	return psi0;

def V(x,y,t,psi):		# Kerr (cubic) focusing nonlinearity

	V = - abs(psi)**2
	return V;