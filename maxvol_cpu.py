import numpy as np
from scipy.linalg import lu, solve_triangular
from time import time

"""
The following code comes from https://github.com/AndreiChertkov/teneva
"""


def maxvol(A, e, k):
    """Compute the maximal-volume submatrix for given tall matrix.

    Args:
        A (np.ndarray): tall matrix of the shape [n, r] (n > r).
        e (float): accuracy parameter (should be >= 1). If the parameter is
            equal to 1, then the maximum number of iterations will be performed
            until true convergence is achieved. If the value is greater than
            one, the algorithm will complete its work faster, but the accuracy
            will be slightly lower (in most cases, the optimal value is within
            the range of 1.01 - 1.1).
        k (int): maximum number of iterations (should be >= 1).

    Returns:
        (np.ndarray, np.ndarray): the row numbers I containing the maximal
        volume submatrix in the form of 1D array of length r and coefficient
        matrix B in the form of 2D array of shape [n, r], such that
        A = B A[I, :] and A (A[I, :])^{-1} = B.

    Note:
        The description of the basic implementation of this algorithm is
        presented in the work: Goreinov S., Oseledets, I., Savostyanov, D.,
        Tyrtyshnikov, E., Zamarashkin, N. "How to find a good submatrix".
        Matrix Methods: Theory, Algorithms And Applications: Dedicated to the Memory of Gene Golub (2010): 247-256.

    """
    n, r = A.shape

    if n <= r:
        raise ValueError('Input matrix should be "tall"')

    P, L, U = lu(A, check_finite=False)
    I = P[:, :r].argmax(axis=0)
    Q = solve_triangular(U, A.T, trans=1, check_finite=False)
    B = solve_triangular(
        L[:r, :], Q, trans=1, check_finite=False, unit_diagonal=True, lower=True
    ).T

    t0 = time()
    for iter in range(k):
        i, j = np.divmod(np.abs(B).argmax(), r)
        E = np.abs(B[i, j])
        if E <= e:
            v = iter / (time() - t0)
            print(f"Maxvol Speed: {int(v)} iters/s")
            break

        I[j] = i

        bj = B[:, j]
        bi = B[i, :].copy()
        bi[j] -= 1.0

        B -= np.outer(bj, bi / B[i, j])

    return I
