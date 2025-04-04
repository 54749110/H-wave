import os
import os.path
import shutil
import sys
import subprocess
import itertools

import tomli, tomli_w
import numpy as np
import scipy.optimize as opt

import hwave.qlms

if len(sys.argv) == 1:
    print(f"Usage: python3 {sys.argv[0]} [path_to_hwave_dry]")
    sys.exit(1)
hwave_dry_path = os.path.abspath(sys.argv[1])

t = 1.0
U = 4.0
Vs = np.linspace(0.0, 2.0, num=20)

# parameters for finding phase boundary

Vmin_b = 0.8
Vmax_b = 1.2

baseinput = "input.toml"
with open(baseinput, "rb") as f:
    param_dict = tomli.load(f)
param_dict["file"] = {"input": {}, "output": {}}


def write_initial(filename, phase="cdw"):
    G = np.zeros((64, 2, 4, 2, 4), dtype=np.complex128)
    if phase == "cdw":
        G[0, 0, 0, 0, 0] = 1.0
        G[0, 0, 3, 0, 3] = 1.0
        G[0, 1, 0, 1, 0] = 1.0
        G[0, 1, 3, 1, 3] = 1.0
    elif phase == "sdw":
        G[0, 0, 0, 0, 0] = 1.0
        G[0, 1, 1, 1, 1] = 1.0
        G[0, 1, 2, 1, 2] = 1.0
        G[0, 0, 3, 0, 3] = 1.0
    np.savez(filename, green_sublattice=G)


def write_stanin(filepath: str, *, t: float = 1.0, U: float = 0.0, V: float = 0.0):
    std_template = """\
model = "Hubbard"
lattice = "square"
W = 4
L = 4
t = {t}
U = {U}
V = {V}
Ncond = 16
eps = 8
calcmode = "uhfk"
exportall = 0
"""
    stanin = std_template.format(t=t, U=U, V=V)
    with open(filepath, "w") as f:
        f.write(stanin)


def run_hwave(input_dir: str, output_dir: str, U: float, V: float, initial: str = ""):
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir)
    os.makedirs(input_dir)
    stan_in = os.path.abspath(os.path.join(input_dir, "stan.in"))
    write_stanin(stan_in, t=t, U=U, V=V)
    cwd = os.getcwd()
    os.chdir(input_dir)
    cmd = [hwave_dry_path, stan_in]
    subprocess.run(cmd)
    os.chdir(cwd)

    file_input = param_dict["file"]["input"]
    file_input["path_to_input"] = input_dir
    file_input_interaction = {
        "path_to_input": input_dir,
        "Geometry": "geom.dat",
        "Transfer": "transfer.dat",
    }
    file_output = {
        "path_to_output": output_dir,
        "energy": "energy.dat",
        "eigen": "eigen.dat",
        "green": "green.dat",
    }
    if U != 0.0:
        file_input_interaction["CoulombIntra"] = "coulombintra.dat"
    if V != 0.0:
        file_input_interaction["CoulombInter"] = "coulombinter.dat"
    file_input["interaction"] = file_input_interaction
    if initial != "":
        write_initial(os.path.join(input_dir, "initial.npz"), phase=initial)
        file_input["initial"] = "initial.npz"
    param_dict["file"]["input"] = file_input
    param_dict["file"]["output"] = file_output
    with open(os.path.join(input_dir, "input.toml"), "wb") as f:
        tomli_w.dump(param_dict, f)
    hwave.qlms.run(input_dict=param_dict)


def energy_diff(V: float) -> float:
    input_dir = "input_find_energy"
    output_dir = "output_find_energy"
    energy = {}
    for initial in ("cdw", "sdw"):
        run_hwave(input_dir, output_dir, U=U, V=V, initial=initial)
        with open(os.path.join(output_dir, "energy.dat")) as fe:
            for line in fe:
                words = line.strip().split("=")
                if words[0].strip() == "Energy_Total":
                    energy[initial] = float(words[1].strip())
                    break
    diff = energy["cdw"] - energy["sdw"]
    with open("find_crossing.log", "a") as f:
        f.write(f"{V} {diff} {energy['cdw']} {energy['sdw']}\n")
    return diff


def calc_nsi_ntj(g: np.ndarray):
    # g[s,i,t,j] = <c_{i,s}^\dagger c_{j,t}>
    # i, j: site index
    # s, t: spin index
    assert g.ndim == 4
    nsites = g.shape[1]
    assert g.shape == (2, nsites, 2, nsites)
    res = np.zeros((2, nsites, 2, nsites), dtype=np.complex128)
    for s in range(2):
        for i in range(nsites):
            for t in range(2):
                for j in range(nsites):
                    res[s, i, t, j] = g[s, i, s, i] * g[t, j, t, j]
                    res[s, i, t, j] -= g[s, i, t, j] * g[t, j, s, i]
            res[s, i, s, i] += g[s, i, s, i]
    return res


# search for transition point
if os.path.exists("find_crossing.log"):
    os.remove("find_crossing.log")
sol = opt.root_scalar(energy_diff, bracket=[Vmin_b, Vmax_b])
phase_boundary = sol.root

# V sweep
f = open("res.dat", "w")
f.write(f"# Vc = {phase_boundary}\n")
f.write("# $1:  V\n")
index = 2
for name in ("GS", "from CDW", "from SDW"):
    f.write(f"# ${index}:  E         [{name}]\n")
    index += 1
    f.write(f"# ${index}:  n(pi,pi)  [{name}]\n")
    index += 1
    f.write(f"# ${index}:  s(pi,pi)  [{name}]\n")
    index += 1
    f.write(f"# ${index}:  Sn(pi,pi) [{name}]\n")
    index += 1
    f.write(f"# ${index}:  Ss(pi,pi) [{name}]\n")
    index += 1
f.write(f"# ${index}: name of the phase\n")

for i, V in enumerate(Vs):
    res = {"cdw": {}, "sdw": {}}
    for initial in ("cdw", "sdw"):
        input_dir = f"input_{i}_{initial}"
        output_dir = f"output_{i}_{initial}"
        run_hwave(input_dir, output_dir, U=U, V=V, initial=initial)

        with open(os.path.join(output_dir, "energy.dat")) as fe:
            for line in fe:
                words = line.strip().split("=")
                if words[0].strip() == "Energy_Total":
                    res[initial]["ene"] = float(words[1].strip())
                    break

        green_file = os.path.join(output_dir, "green.dat.npz")
        g = np.load(green_file)["green_sublattice"]
        nsites = g.shape[2]
        density = np.zeros(nsites, dtype=np.float64)
        spin = np.zeros(nsites, dtype=np.float64)
        for i in range(nsites):
            density[i] = np.real(g[0, 0, i, 0, i]) + np.real(g[0, 1, i, 1, i])
            spin[i] = 0.5 * (np.real(g[0, 0, i, 0, i]) - np.real(g[0, 1, i, 1, i]))

        nsi_ntj = calc_nsi_ntj(g[0, :, :, :, :])
        ninj = np.zeros((nsites, nsites), dtype=np.float64)
        sisj = np.zeros((nsites, nsites), dtype=np.float64)
        sz = [0.5, -0.5]
        for s, t in itertools.product(range(2), repeat=2):
            ninj += np.real(nsi_ntj[s, :, t, :])
            sisj += np.real(nsi_ntj[s, :, t, :]) * sz[s] * sz[t]

        sublattice = [1, -1, -1, 1]
        res[initial]["cdw"] = 0.0
        res[initial]["sdw"] = 0.0
        res[initial]["charge structure factor"] = 0.0
        res[initial]["spin structure factor"] = 0.0
        for i in range(4):
            res[initial]["cdw"] += sublattice[i] * density[i]
            res[initial]["sdw"] += sublattice[i] * spin[i]
        res[initial]["cdw"] /= 4.0
        res[initial]["sdw"] /= 4.0
        for i, j in itertools.product(range(4), repeat=2):
            res[initial]["charge structure factor"] += (
                sublattice[i] * sublattice[j] * ninj[i, j]
            )
            res[initial]["spin structure factor"] += (
                sublattice[i] * sublattice[j] * sisj[i, j]
            )
        res[initial]["charge structure factor"] /= 4.0
        res[initial]["spin structure factor"] /= 4.0
    f.write(f"{V}")
    if V < phase_boundary:
        stable_phase = "sdw"
    else:
        stable_phase = "cdw"
    for initial in (stable_phase, "cdw", "sdw"):
        r = res[initial]
        f.write(f" {r['ene']}")
        f.write(f" {r['cdw']}")
        f.write(f" {np.abs(r['sdw'])}")
        f.write(f" {r['charge structure factor']}")
        f.write(f" {r['spin structure factor']}")
    f.write(f" {stable_phase}")
    f.write(f"\n")
f.close()
print(f"Vc = {phase_boundary}")
