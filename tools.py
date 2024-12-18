import numpy as np
from tqdm import tqdm
from pynep.calculate import NEP
from asi_io import save_asi, load_asi
from maxvol import calculate_maxvol, find_inverse


def get_gamma(traj, nep_file, asi_file):
    calc = NEP(nep_file)
    active_set_inverse = load_asi(asi_file)
    for atoms in tqdm(traj):
        atoms.arrays["gamma"] = np.zeros(len(atoms))
        calc.calculate(atoms, ["B_projection"])
        B_projection = calc.results["B_projection"]
        for e in active_set_inverse.keys():
            index = [
                ii for ii in range(len(atoms)) if atoms.get_chemical_symbols()[ii] == e
            ]
            g = B_projection[index] @ active_set_inverse[e]
            g = np.max(np.abs(g), axis=1)
            atoms.arrays["gamma"][index] = g
    return traj


def get_B_projections(traj, nep_file):
    calc = NEP(nep_file)
    with open(nep_file) as f:
        first_line = f.readline()
        elements = first_line.split(" ")[2:-1]
        print(f"Elements in the NEP potential: {elements}")

    B_projections = {e: [] for e in elements}
    B_projections_struct_index = {e: [] for e in elements}
    print("Calculating B projections...")
    for index, atoms in enumerate(tqdm(traj)):
        calc.calculate(atoms, ["B_projection"])
        B_projection = calc.results["B_projection"]
        for b, e in zip(B_projection, atoms.get_chemical_symbols()):
            B_projections[e].append(b)
            B_projections_struct_index[e].append(index)

    B_projections_struct_index = {
        e: np.array(i) for e, i in B_projections_struct_index.items()
    }

    print("Shape of the B matrix:")
    for e, b in B_projections.items():
        B_projections[e] = np.vstack(b)
        print(f"{e}: {B_projections[e].shape}")
        assert (
            B_projections[e].shape[0] >= B_projections[e].shape[1]
        ), f"Not enough environments for {e}."

    return B_projections, B_projections_struct_index


def get_active_set(
    B_projections,
    B_projections_struct_index,
    write_asi=True,
    batch_size=10000,
    mode="GPU",
):
    print("Performing MaxVol...")
    active_set = {}
    active_set_struct = []  # the index of structure
    for e, b in B_projections.items():
        A, selected_index = calculate_maxvol(
            b, B_projections_struct_index[e], batch_size=batch_size, mode=mode
        )
        active_set[e] = A
        active_set_struct.extend(selected_index)
        print("Shape of the active set:")
        print(f"{e}: {active_set[e].shape}")

    active_set_struct = list(set(active_set_struct))
    active_set_struct.sort()

    print("Finding inverse...")
    active_set_inv = {e: find_inverse(b) for e, b in active_set.items()}

    if write_asi:
        print("Saving active set inverse...")
        save_asi(active_set_inv)

    return active_set_inv, active_set_struct
