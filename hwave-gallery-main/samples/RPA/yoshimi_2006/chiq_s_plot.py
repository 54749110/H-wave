import numpy as np
import matplotlib.pyplot as plt

Nx,Ny = 64,64
fig, ax = plt.subplots()
ax.set_ylabel("$X_+^S (q)$")
ax.set_ylim(0, 25)
for U in [0.4, 0.5]:
    #get eigenvalues
    file_chiq = "onsite/output/chiq_U{}.npz".format(U)
    data = np.load(file_chiq)
    chiq = data["chiq"]

    norb = int(chiq.shape[2]/2)
    chic_mat = np.zeros((chiq.shape[1], norb, norb), dtype = np.complex64)
    chis_mat = np.zeros((chiq.shape[1], norb, norb), dtype = np.complex64)
    for i in range(norb):
        for j in range(norb):
            chic_mat[:, i, j] = chiq[0,:,i, j] + chiq[0,:,i+2, j+2] ## (up, up) + (up, down)
            chis_mat[:, i, j] = chiq[0,:,i, j] - chiq[0,:,i+2, j+2] ## (up, up) - (up, down)

    chic = np.zeros((chiq.shape[1], 2), dtype = np.complex64)
    chis = np.zeros((chiq.shape[1], 2), dtype = np.complex64)
    for iorb in range(norb):
        for jorb in range(norb):
            if iorb == jorb:
                sign = 1
            else:
                sign = -1
            chic[:, 0] += chic_mat[:, iorb, jorb]
            chic[:, 1] += sign*chic_mat[:, iorb, jorb]
            chis[:, 0] += chis_mat[:, iorb, jorb]
            chis[:, 1] += sign*chis_mat[:, iorb, jorb]

    chic /= 2.0
    chis /= 2.0

    chi_plot = np.zeros((int(Nx/2)*6, 4))

    def _add_to_chi_plot(kidx, chi_plot, plot_idx):
        chi_plot[plot_idx] = (chic[kidx][0].real, chic[kidx][1].real, chis[kidx][0].real, chis[kidx][1].real)
        return plot_idx + 1
    
    plot_idx = 0
    # (0, 0) to (pi, 0)
    for idx in range(int(Nx/2)):
        kidx = idx*Ny
        plot_idx = _add_to_chi_plot(kidx, chi_plot, plot_idx)

    # (pi, 0) to (pi, pi)
    for idx in range(int(Ny/2)):
        kidx = int(Nx*Ny/2) + idx
        plot_idx = _add_to_chi_plot(kidx, chi_plot, plot_idx)

    # (pi, pi) to (0, 0)
    for idx in range(int(Ny/2)):
        kidx = Nx*int(Ny/2-idx) + int(Ny/2)-idx
        plot_idx = _add_to_chi_plot(kidx, chi_plot, plot_idx)

    #(0, 0) to (-pi, pi)
    for idx in range(int(Ny/2)):
        kidx = (Nx*(Ny-idx) + idx)%(Nx*Ny)
        plot_idx = _add_to_chi_plot(kidx, chi_plot, plot_idx)

    #(-pi, pi) to (0, pi)
    for idx in range(int(Nx/2)):
        kidx = Nx*int(Ny/2+idx) + int(Ny/2)
        plot_idx = _add_to_chi_plot(kidx, chi_plot, plot_idx)

    #(0, pi) to (0, 0)
    for idx in range(int(Nx/2)):
        kidx = int(Ny/2)-idx
        plot_idx = _add_to_chi_plot(kidx, chi_plot, plot_idx)

    plt.plot(chi_plot[:,0], label="U={}".format(U))
    plt.xticks([int(Nx/2)*i for i in range(7)], ["(0, 0)", "($\pi$, 0)", "($\pi$, $\pi$)", "(0, 0)", "(-$\pi$, $\pi$)", "(0, $\pi$)", "(0, 0)"])
ax.legend(loc=0)
plt.savefig("chis_plot.png")
