from ase.io import write
from pynep.io import load_nep, dump_nep
from tools import get_gamma

nep_file = "nep.txt"
traj = load_nep("to_select.xyz")

get_gamma(traj, nep_file, "active_set.asi")

out_traj = [atoms for atoms in traj if atoms.arrays["gamma"].max() > 1]
try:
    dump_nep("large_gamma.xyz", out_traj)
except:
    write("large_gamma.xyz", out_traj)
