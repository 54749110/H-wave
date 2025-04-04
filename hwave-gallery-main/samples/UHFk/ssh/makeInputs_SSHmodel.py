import numpy as np
import hwave.qlms
import argparse
import subprocess
import os

def check_file_exists(file):
  if os.path.exists(file):
    print("Warning: {} exists! mv {} to {}.bak\n".format(file, file, file)) 
    subprocess.run(["mv", file, file+".bak"])

def makeInputs_SSH(v,w):

  Norb = 2
  Npts = 3

  ofile_trans = "transfer.dat"
  check_file_exists(ofile_trans)

  header_ = "Transfer in wannier90-like format for uhfk\n"
  with open(ofile_trans, "w") as fp:
    fp.write(header_) 
    fp.write("{}\n".format(Norb))
    fp.write("{}\n".format(Npts))
    [ fp.write("{}\t".format(1)) for i in range(Npts)]
    fp.write("\n")
    fp.write(" 0\t0\t0\t1\t2\t\t{}\t{}\n".format(v,0.0))
    fp.write(" 0\t0\t0\t2\t1\t\t{}\t{}\n".format(v,0.0))
    fp.write("-1\t0\t0\t1\t2\t\t{}\t{}\n".format(w,0.0))
    fp.write(" 1\t0\t0\t2\t1\t\t{}\t{}\n".format(w,0.0))

  ofile_geom = "geometry.dat"
  check_file_exists(ofile_geom)
  with open(ofile_geom, "w") as fp:
    fp.write("{}\t{}\t{}\n".format(1.0, 0.0, 0.0))
    fp.write("{}\t{}\t{}\n".format(0.0, 1.0, 0.0))
    fp.write("{}\t{}\t{}\n".format(0.0, 0.0, 1.0))
    fp.write("{}\n".format(Norb))
    fp.write("{}\t{}\t{}\n".format(0.0, 0.0, 0.0))
    fp.write("{}\t{}\t{}\n".format(0.5, 0.0, 0.0))
