import numpy as np
data = np.load("eigen.npz")
eigenvalue = data["eigenvalue"]
eigenvector = data["eigenvector"]
wavevector_unit = data["wavevector_unit"]
wavevector_index = data["wavevector_index"]


#k_vec = np.dot(wavevector_index[2], wavevector_unit)
print(eigenvalue)
#print(eigenvector)
print(wavevector_unit)
print(wavevector_index)
#print(k_vec)