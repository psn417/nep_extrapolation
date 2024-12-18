from tools import get_gamma
from pynep.io import load_nep, dump_nep

nep_file = "nep.txt"
traj = load_nep("to_select.xyz", ftype="exyz")

get_gamma(traj, nep_file, "active_set.asi")

out_traj = [atoms for atoms in traj if atoms.arrays["gamma"].max() > 1]
dump_nep("large_gamma.xyz", out_traj, ftype="exyz")
