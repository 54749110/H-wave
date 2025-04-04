import numpy as np
import tomli, tomli_w
import hwave.qlms
import matplotlib.pyplot as plt
from makeInputs_SSHmodel import makeInputs_SSH
import argparse


parser = argparse.ArgumentParser(
        prog='calc_ssh.py',
        description='calculate the ground states for the Su-Shuriffer-Heeger model',
        epilog='end',
        add_help=True,
)

parser.add_argument('-v', action='store', dest='v',
                        type=float, choices=None,
                        required=True,
                        help=('Intra-hopping v'),
                        metavar=None)

parser.add_argument('-w', action='store', dest='w',
                        type=float, choices=None,
                        required=True,
                        help=('Inter-hopping w'),
                        metavar=None)

parser.add_argument('-n', '--ncell', action='store', dest='ncell',
                        default=0.0, 
                        type=int, choices=None,
                        required=True,
                        help=('# of cell'),
                        metavar=None)

args = parser.parse_args()
v = args.v
w = args.w
Ncell= args.ncell

makeInputs_SSH(v,w)


#make toml dict/ output input.toml
with open("input.toml.org", "rb") as fp:
  toml_dict = tomli.load(fp)
info_mode = toml_dict.get("mode", {})
info_mode["param"]["CellShape"][0] = Ncell
info_mode["param"]["Ncond"] = Ncell*2
with open("input.toml", "wb") as fp:
  tomli_w.dump(toml_dict, fp)



#UHFk runs 
hwave.qlms.run(input_dict=toml_dict)

#get eigenvalues
data = np.load("output/eigen.dat.npz") 
eigenvalue = data["eigenvalue"]
eigenvec = data["eigenvector"]
wavevec_index   = data["wavevector_index"]
wavevec_unit    = data["wavevector_unit"]

#the total number of the eigen states
neigen = int(eigenvalue.shape[1]) 

#calc wavevectors from index & reciprocal lattice vectors
wavevec = np.dot(wavevec_index, wavevec_unit.T)/np.pi

#concatenate wavevector & eigenvalue
Ene_k = np.concatenate([wavevec, eigenvalue], axis=1)

#####
#Zak phase: Berry connection
#####
# nabla_k |phi_k> of eigenstate 0
#Note: gradients at boundaries are calculated by using forward or backward approximation 
#      https://numpy.org/doc/stable/reference/generated/numpy.gradient.html
idx_eigenstate = 0
diff_eigenvec = np.gradient(eigenvec[:,:,idx_eigenstate], axis=0)

#calc Berry_connection: A_k = i<phi_k| nabla_k |phi_k>
Ak_list = []
[ Ak_list.append(1J*np.vdot(np.array(eigenvec[k,:,idx_eigenstate]), np.array(diff_eigenvec)[k,:])) for k in range(len(wavevec_index)) ]

#Zak phase: -\int dk Ak/pi
zak_phase = -np.sum(Ak_list)/np.pi
print("Zak phase from Berry connection: ", zak_phase)


#####
#Zak phase: KSV formula
#####
#calc |phi_k+1>
eigenvec4KSV = eigenvec[:,:,idx_eigenstate]
eigenvec4KSV = np.roll(eigenvec4KSV, -1, axis=0)
#calc Mk = <phi_k| phi_k+1>
Mmn_list = []
[ Mmn_list.append(np.vdot(eigenvec[k,:,idx_eigenstate], eigenvec4KSV[k,:])) for k in range(len(wavevec_index)) ]

#calc Zak phase: -\sum_k Im ln Mk/pi
zak_phase_KSV = -np.sum(np.log(np.array(Mmn_list)).imag/np.pi)
print("Zak phase from KSV formula: ", zak_phase_KSV)
with open("zak_phase.dat", "w") as fp:
  fp.write("Zak phase from Berry connection: {}\n".format(zak_phase))
  fp.write("Zak phase from KSV formula: {}".format(zak_phase_KSV))



#output wavenumber & eigenvalues to dat file
header_ = "# kx/pi  ky/pi  kz/pi  ene_eigen0 ene..."
np.savetxt("band.dat", Ene_k, header = header_)


# plot dispersion by matplotlib
size_list = np.linspace(50*neigen,10,neigen)
kmin = -1
kmax =  1
krange = np.linspace(kmin,kmax,100)
ene_exact = np.sqrt(v*v + w*w + 2.0*v*w*np.cos(np.pi*krange))
plt.plot(krange,  ene_exact, color="black", zorder=6, label="exact")
plt.plot(krange, -ene_exact, color="black", zorder=6)

plt.xlim(kmin, kmax)
[plt.scatter(wavevec[:, idx_eigenstate], eigenvalue[:,i], marker="o", s=size_list[i], label="H-wave: state{}".format(i)) for i in range(neigen) ]

plt.legend()
plt.xlabel("k/pi")
plt.ylabel("E(k)")
plt.savefig("band.png")
#plt.show()
