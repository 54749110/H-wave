import numpy as np
import os
import tomli
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, default="input.toml", help="input file of hwave")
parser.add_argument('--ene_window', default=None, type=float,
                    help='energy window; [ene_low, ene_high]. If None, ene_low = ene_min - 0.2, ene_high = ene_max + 0.2')
parser.add_argument('--ene_num', default=100, type=int, help='energy step')
parser.add_argument("--plot", action="store_true", help="plot DOS")

args = parser.parse_args()

file_toml = args.input
if os.path.exists(file_toml):
    print("Reading input file: ", file_toml)
    with open(file_toml, "rb") as f:
        input_dict = tomli.load(f)
else:
    raise ValueError("Input file does not exist")

print("Reading eigenvalues")
output_info_dict = input_dict["file"]["output"]
data = np.load(os.path.join(output_info_dict["path_to_output"], output_info_dict["eigen"] + ".npz"))
eigenvalues = data["eigenvalue"]
Lx, Ly, Lz = input_dict["mode"]["param"]["CellShape"]
norb = eigenvalues.shape[1]
print("Lx, Ly, Lz, norb: ", Lx, Ly, Lz, norb)
eigenvalues.reshape(Lx, Ly, Lz, norb)

def read_geom(file_name="./dir-model/zvo_geom.dat"):
    with open(file_name, "r") as fr:
        lines = fr.readlines()
        # unit vector
        uvec = np.zeros((3, 3))
        for i in range(3):
            uvec[i] = np.array(lines[i].split())
    return uvec

print("Reading geometry")
input_info_dict = input_dict["file"]["input"]["interaction"]
file_name = os.path.join(input_info_dict["path_to_input"], input_info_dict["Geometry"])
uvec = read_geom(file_name)
bvec = 2.0 * np.pi * np.linalg.inv(uvec).T

if args.ene_window is None:
    ene_min = np.min(eigenvalues) - 0.2
    ene_max = np.max(eigenvalues) + 0.2
else:
    ene_min = args.ene_window[0]
    ene_max = args.ene_window[1]

ene = np.linspace(ene_min, ene_max, args.ene_num)
print("ene_min, ene_max, ene_num: ", ene_min, ene_max, args.ene_num)

import libtetrabz

eig = eigenvalues.reshape(Lx, Ly, Lz, norb)
print("Calculating DOS")
wght = libtetrabz.dos(bvec, eig, ene)
dos = wght.sum(2).sum(1).sum(0)
total_dos = np.sum(dos, axis=0)

print("Writing DOS to dos.dat")
with open("dos.dat", "w") as fw:
    for i in range(args.ene_num):
        fw.write("{:15.8f} ".format(ene[i]))
        fw.write("{:15.8f} ".format(total_dos[i]))
        for j in range(norb):
            fw.write("{:15.8f} ".format(dos[j, i]))
        fw.write("\n")

if not args.plot:
    exit()

import matplotlib.pyplot as plt
print("Plotting DOS to dos.png")
plt.plot(ene, total_dos, label="Total")
for i in range(norb):
    plt.plot(ene, dos[i], label=str(i))
plt.xlabel("Energy")
plt.ylabel("DOS")
plt.ylim(0)
plt.legend()
plt.savefig("dos.png")
plt.close()
