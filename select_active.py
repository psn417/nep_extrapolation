from ase.io import write
from pynep.io import load_nep, dump_nep
from tools import get_B_projections, get_active_set

nep_file = "nep.txt"
traj = load_nep("train.xyz")

B_projections, B_projections_struct_index = get_B_projections(traj, nep_file)
active_set_inv, active_set_struct = get_active_set(
    B_projections, B_projections_struct_index
)

out_traj = [traj[i] for i in active_set_struct]
try:
    dump_nep("active_set.xyz", out_traj)
except:
    write("active_set.xyz", out_traj)
