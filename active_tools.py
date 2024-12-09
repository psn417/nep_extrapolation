import numpy as np


def find_inverse(m):
    return np.linalg.pinv(m, rcond=1e-10)


def save_asi(asi, filename="active_set.asi"):
    with open(filename, "w") as f:
        for k, v in asi.items():
            f.write(f"{k} {v.shape[0]} {v.shape[1]}\n")
            for i in v.T.flatten():
                f.write(str(i) + "\n")


def load_asi(asi):
    ret = {}
    with open(asi, "r") as f:
        while True:
            B = []
            line1 = f.readline()
            if len(line1) == 0:
                break
            line1 = line1.split(" ")
            element, shape1, shape2 = line1[0], int(line1[1]), int(line1[2])
            for _ in range(shape1 * shape2):
                B.append(float(f.readline()))
            ret[element] = np.array(B).reshape((shape1, shape2)).T
    return ret
