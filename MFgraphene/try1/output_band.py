import numpy as np
import tomli
import hwave.qlms
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

#read toml file
with open("input.toml", "rb") as fp:
  toml_dict = tomli.load(fp)

#UHFk runs 
hwave.qlms.run(input_dict=toml_dict)

#get eigenvalues
data = np.load("output/eigen.npz") 
eigenvalue = data["eigenvalue"]
wavevec_index   = data["wavevector_index"]
wavevec_unit    = data["wavevector_unit"]


#the total number of the eigen states
neigen = int(eigenvalue.shape[1]) 

#calc wavevectors from index & reciprocal lattice vectors
wavevec = np.dot(wavevec_index, wavevec_unit.T)/np.pi

#concatenate wavevector & eigenvalue
Ene_k = np.concatenate([wavevec, eigenvalue], axis=1)

#output wavenumber & eigenvalues to dat file
header_ = "# kx/pi  ky/pi  kz/pi  ene_spin0  ene_spin1"
np.savetxt("band.dat", Ene_k, header = header_)

# plot dispersion by matplotlib


kmin = -1.3
kmax = 1.3
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(wavevec[:, 0], wavevec[:, 1], eigenvalue[:, 0], c='r',marker='*')
ax.scatter(wavevec[:, 0], wavevec[:, 1], eigenvalue[:, 1], c='b',marker='^')
# print(wavevec[:, 1])
# print(wavevec[:, 1])
# print(wavevec[:, 1])
# print(wavevec[:, 2])
# print(eigenvalue[:, 1])

ax.set_xlabel('kx/pi')
ax.set_ylabel('ky/pi')
ax.set_zlabel('E(k)')

plt.savefig("band.png")
plt.show()




# size_list = np.linspace(100,10,neigen)
# kmin = -1.3
# kmax =  1.3

# plt.xlim(kmin, kmax)
# plt.ylim(kmin, kmax)
# [ax.scatter(wavevec[:, 1], wavevec[:, 2], eigenvalue[:,i], marker="o", s=size_list[i], label="H-wave: spin{}".format(i)) for i in range(neigen) ]

# plt.legend()
# plt.xlabel("kx/pi")
# plt.ylabel("ky/pi")
# plt.zlabel("E(k)")
# plt.savefig("band.png")
# #plt.show()
