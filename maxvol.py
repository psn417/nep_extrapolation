import numpy as np


# avoid large value since GPUMD use float
def find_inverse(m):
    return np.linalg.pinv(m, rcond=1e-8)


def calculate_maxvol(
    A,
    struct_index,
    gamma_tol=1.001,
    maxvol_iter=1000,
    mode="GPU",
    batch_size=None,
    n_refinement=10,
):
    if mode == "GPU":
        from maxvol_gpu import maxvol
    elif mode == "CPU":
        from maxvol_cpu import maxvol
    else:
        raise Exception("mode should be CPU or GPU.")

    # one batch
    if batch_size is None:
        selected = maxvol(A, gamma_tol, maxvol_iter)
        return A[selected], struct_index[selected]

    # multiple batches
    batch_num = np.ceil(len(A) / batch_size)
    batch_splits_indices = np.array_split(
        np.arange(len(A)),
        batch_num,
    )

    # stage 1 - cumulative maxvol
    A_selected = None
    struct_index_selected = None
    for i, ind in enumerate(batch_splits_indices):
        # first batch
        if A_selected is None:
            A_joint = A[ind]
            struct_index_joint = struct_index[ind]
        # other batches
        else:
            A_joint = np.vstack([A_selected, A[ind]])
            struct_index_joint = np.hstack([struct_index_selected, struct_index[ind]])

        selected = maxvol(A_joint, gamma_tol, maxvol_iter)
        if A_selected is None:
            l = 0
        else:
            l = len(A_selected)
        A_selected = A_joint[selected]
        struct_index_selected = struct_index_joint[selected]
        n_add = (selected >= l).sum()
        print(f"Batch {i}: adding {n_add} envs. ")

    # stage 2 - refinement
    for ii in range(n_refinement):
        # check max gamma, if small enough, no need to refine
        inv = find_inverse(A_selected)
        gamma = np.abs(A_selected @ inv)
        large_gamma = gamma > gamma_tol
        print(
            f"Refinement round {ii}: {large_gamma.sum()} envs out of active set. Max gamma = {np.max(gamma)}"
        )
        if np.max(gamma) < gamma_tol:
            print("Refinement done.")
            return A_selected, struct_index_selected

        A_joint = np.vstack([A_selected, A[large_gamma]])
        struct_index_joint = np.hstack(
            [struct_index_selected, struct_index[large_gamma]]
        )
        selected = maxvol(A_joint, gamma_tol, maxvol_iter)
        A_selected = A_joint[selected]
        struct_index_selected = struct_index_joint[selected]
