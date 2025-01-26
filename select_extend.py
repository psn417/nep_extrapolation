from ase.io import write, read
from pynep.io import load_nep, dump_nep
from tools import get_B_projections, get_active_set

nep_file = "nep.txt"
data1 = load_nep("train.xyz")
try:
    data2 = load_nep("large_gamma.xyz")
except:
    data2 = read("large_gamma.xyz", index=":")

data = data1 + data2

B_projections, B_projections_struct_index = get_B_projections(data, nep_file)
active_set_inv, active_set_struct = get_active_set(
    B_projections, B_projections_struct_index, write_asi=False
)

out = [data[i] for i in active_set_struct if i >= len(data1)]

try:
    dump_nep("to_add.xyz", out)
except:
    write("to_add.xyz", out)
