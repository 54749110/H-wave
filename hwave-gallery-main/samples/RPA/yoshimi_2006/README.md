# Sample for the extended Hubbard model with 2 orbitals (h-wave ver.1.0)

## What's this sample?

The Hamiltonian for the extended Hubbard model with orbitals on a two-dimensional square lattice is given by
```math
\mathcal{H} = -t\sum_{ \langle ij \rangle, \sigma}\sum_{\alpha\beta}(c^\dagger_{i\alpha\sigma} c_{j\beta\sigma} + \text{h.c.}) + \sum_{i}\sum_{\alpha} U_{\alpha} n_{i\alpha\uparrow} n_{i\alpha\downarrow} + \sum_{\langle ij \rangle}\sum_{\alpha\beta} V_{i\alpha j\beta}n_{i\alpha} n_{j\beta},
```
where $\alpha$ and $\beta$ are indices of orbitals, $t$, $U$ and $V$ are transfer integrals, onsite and nearest-neighbor Coulomb interactions, respectively. 

In the following, we repoduce spin and charge suceptibilities (Fig. 3 (b) and Fig. 5 (b) in the following reference):

- K. Yoshimi, M. Nakamura, and H. Mori, "Superconductivity in the Vicinity of Charge Ordered State in Organic Conductor \beta-(meso-DMBEDT-TTF)_2 PF_6"
  - [J.Phys.Soc.Jpn. 76, 024706 (2007)](https://journals.jps.jp/doi/10.1143/JPSJ.76.024706).
  - [arXiv:cond-mat/0608466](https://arxiv.org/abs/cond-mat/0608466).

In this sample, the electron filling is set as 3/4.
We set Nx=Ny=64 and Nmat=1024, respectively.

## Preparation

In this sample, we use the following python library in ``chiq_s_plot.py`` and ``chiq_c_plot.py`` :
- matplotlib

## How to run


1. Create input files for H-wave.
In this sample, the input files ``input.toml`` ,  ``geom.dat`` , ``transfer.dat`` , ``coulombintra.dat`` , and ``coulombinter.dat`` are already prepared in the ``onsite`` and ``coulomb`` directory.


2. Execute H-wave by typing the following commands:

```
$ cd onsite
$ hwave input_U0.4.toml
$ hwave input_U0.5.toml
$ cd ../coulomb
$ hwave input_A.toml
$ hwave input_B.toml
$ hwave input_C.toml
$ hwave input_D.toml
$ hwave input_E.toml
$ cd ..
```

It takes about a minute for all calculations to be completed.
After finishing the calculations, ``chiq_xx.npz`` (xx is the same as the index in input_xx.toml) is outputted to the ``output`` directory.

4. See the calculation results.

To check the calculation results, ``chiq_s_plot.py`` and ``chiq_c_plot.py`` are prepared. ``chiq_s_plot.py`` and ``chiq_c_plot.py`` can be run with the following command:

```
$ python3 chiq_s_plot.py
$ python3 chiq_c_plot.py
```

Then, you can see the following image.

![Spin suceptibilities corresponidng to Fig. 3(b)](chis_plot.png)
![Charge susceptibilities corresponding to Fig. 5(b)]

For details of the parameters, see the reference.

Author: Kazuyoshi Yoshimi (2023/04/08)