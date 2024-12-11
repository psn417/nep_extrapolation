from tools import get_B_projections, get_active_set
from pynep.io import load_nep, dump_nep

nep_file = "nep.txt"
traj = load_nep("train.xyz", ftype="exyz")

B_projections, B_projections_struct_index = get_B_projections(traj, nep_file)
active_set_inv, active_set_struct = get_active_set(
    B_projections, B_projections_struct_index
)

out_traj = [traj[i] for i in active_set_struct]
dump_nep("active_set.xyz", out_traj, ftype="exyz")
