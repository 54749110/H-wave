# Sample for Su–Schrieffer–Heeger model

## What's this sample?

The Su–Schrieffer–Heeger model is one of the famous platforms where a topological insulator emerges, which was originally introduced as
 a toy model for the polyacetylene chain.
The Su–Schrieffer–Heeger model is defined as

```math
\mathcal{H}_\textrm{SSH} = v\sum_{i}^{N_\textrm{cell}} c^\dagger_{iA} c_{iB} + w \sum_{i}^{N_\textrm{cell}} c^\dagger_{iA} c_{i+1,B} + \text{h.c.},
```
where $`v`$ and $`w`$ are the intra and inter hopping integrals, respectively. $`c^\dagger_{i\alpha}`$/$`c_{i\alpha}`$ denotes the creation/annihilation operator at the $`i`$-th unitcell with the sublattice index $`\alpha`$.

In this tutorial, we solve the spinful Su–Schrieffer–Heeger (sSSH) model without interactions:
```math
\mathcal{H}_\textrm{sSSH} = v\sum_{i,\sigma} c^\dagger_{iA\sigma} c_{iB\sigma} + w \sum_{i,\sigma} c^\dagger_{iA\sigma} c_{i+1,B\sigma} + \text{h.c.}  
```

## Preparation

Make sure that both `hwave` package (this project).
We use the following python libraries:
- numpy
- tomli
- tomli_w
- matplotlib
- argparse


## How to run

By using `calc_ssh.py`, you can obtain the band dispersion and the topological number of the lowest band.
The following command is an example, where we solve the sSSH model for $`v=0.5`$, $`w=1.0`$, and $`N_\textrm{cell}=50`$.
```bash
python3 calc_ssh.py  -v 0.5 -w 1.0 -n 50
```

If you want to show the help message for `calc_ssh.py`, run the following command. 
```bash
$python3 calc_ssh.py -h
usage: makeinputs_SSHmodel.py [-h] -v V -w W -n NCELL

generate inputs of UHFk for the Su-Shuriffer-Heeger chain

optional arguments:
  -h, --help            show this help message and exit
  -v V                  Intra-hopping v
  -w W                  Inter-hopping w
  -n NCELL, --ncell NCELL
                        # of cell

end
```

Note that you do not need to run `makeinputs_SSHmodel.py` in this directory because this is a generator of the inputs for the Su–Schrieffer–Heeger model, which is called by `calc_ssh.py`.



After executing the command above, inputs for `H-wave` (`geometry.dat`, `transfer.dat` and `input.toml`), `band.png`, `band.dat` and `zakphase.dat` is outputted.
`band.dat` includes the band dispersion obtained as the `H-wave` results and `band.png` is the figure plotted by `matplotlib`.

![band dispersion for the sSSH model with $`v=0.5`$, $`w=1.0`$, and $`N_\textrm{cell}=50`$](./reference/band.png)

`zakphase.dat` includes the numerical results for the Zak phase of the lowest band, which corresponds to the topological number.
In this script, the Zak phase is calculated in two ways: one is the use of the Berry connection and the other is the King-Smith-Vanderbilt formula. Both results are consistent with each other in the thermodynamic limit.


## References
- W. P. Su, J. R. Schrieffer, and A. J. Heeger, Phys. Rev. Lett. **42**, 1698 (1979).
- W. P. Su, J. R. Schrieffer, and A. J. Heeger, Phys. Rev. B **22**, 2099 (1980).
- J. Zak, Phys. Rev. Lett. **62**, 2747 (1989).
- R. D. King-Smith and D. Vanderbilt, Phys. Rev. B **47**, 1651(R) (1993).
- D. Vanderbilt, "Berry Phases in Electronic Structure Theory: Electric Polarization, Orbital Magnetization and Topological Insulators", Cambridge University Press, 2018.
- https://en.wikipedia.org/wiki/Su–Schrieffer–Heeger_model
- http://www.physics.rutgers.edu/pythtb/formalism.html
