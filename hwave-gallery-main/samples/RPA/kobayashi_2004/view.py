import os, sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

nx,ny = 128,128
nmat = 4096
T = 0.01
norb = 1
ns = 2
nd = ns * norb

kx = np.arange(nx) * np.pi * 2 / nx
ky = np.arange(ny) * np.pi * 2 / ny


X = [i for i in range(int(nx/2)*3)]
fig = plt.figure(figsize = (5, 5))
ax = fig.add_subplot(111)
ax.set_box_aspect(1)
ax.set_ylim(0, 1.75)
ax.set_xlim(0, int(nx/2)*3)
ax.set_xlabel("q")
ax.set_yticks(np.linspace(0, 2, 5))
ax.set_xticks([0, int(nx/2), int(nx/2)*2, int(nx/2)*3],["(0,0)", "($\pi$, 0)", "($\pi$,$\pi$)", "(0, 0)"])
ax.grid()


file_base_chiq  = os.path.join("output", "chiq.npz")
dir_interact = {"onsite":[3.7, 0], "coulomb":[0, 0.8]}


for dir_name in ["onsite", "coulomb"]:

    file_chiq = os.path.join(dir_name, file_base_chiq)
    chiq  = np.load(file_chiq)['chiq']

    # chiq[l][k][a,ap,b,bp]
    chi00 = (chiq[0, :, 0, 0]).reshape(nx,ny)
    chi01 = (chiq[0, :, 0, 1]).reshape(nx,ny)

    chis = chi00 - chi01
    chic = chi00 + chi01

    chic_plot = []
    chis_plot = []

    #(0, 0) to (pi, 0)
    for i in range(int(nx/2)):
        chic_plot.append(chic[i][0].real)
        chis_plot.append(chis[i][0].real)

    #(pi, 0) to (pi, pi)
    for j in range(int(ny/2)):
        i0 = int(nx/2)
        chic_plot.append(chic[i0][j].real)
        chis_plot.append(chis[i0][j].real)

    #(pi, pi) to (0, 0)
    for j in range(int(ny/2)):
        i0 = int(nx/2)
        j0 = int(ny/2)
        chic_plot.append(chic[i0-j][j0-j].real)
        chis_plot.append(chis[i0-j][j0-j].real)

    ax.plot(X, chis_plot, label="$\chi_s$(q, 0) ({}, {})".format(dir_interact[dir_name][0], dir_interact[dir_name][1]))
    ax.plot(X, chic_plot, label="$\chi_c$(q, 0) ({}, {})".format(dir_interact[dir_name][0], dir_interact[dir_name][1]),linestyle="dashed")
    
ax.legend()
plt.savefig("chi.png")
plt.show()
plt.close()
    
