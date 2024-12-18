# Active Learning of NEP

## Features

- Selecting active set with `MaxVol` algorithem by CPU or GPU.
- Calcualting extrapolation grade with `PyNEP`.
- Calcualting extrapolation grade during MD simulations with `GPUMD`.


## Installation

### 1. (Optional) Create a conda environment
```shell
conda install -n nep_active python=3.10
conda activate nep_active
```
If you choose to install it in your current env, jump to the next step.


### 2. Install PyNEP
Install the **latest** `PyNEP`. You can check its own [repository](https://github.com/bigd4/PyNEP) for details. 

```shell
pip install git+https://github.com/bigd4/PyNEP.git
```

### 3. (Optional) Install CuPy
When selecting the active set, you may use `cupy` or `numpy`. `cupy` uses your GPU and is much faster when performing `MaxVol`. Since you are using `GPUMD`, I assume you have a GPU. You can check its [website](https://cupy.dev/) for installation details.

```shell
pip install cupy-cuda12x
```

## Usage
### 1. Training an NEP potential
You need to have a NEP.

### 2. Selecting an *Active Set*
An active set invsersion (`.asi` file) is needed when calculating the extrapolation grade. The active set can also be considered as the environments with the maximum diversity. You can use `select_active.py` to get an active set inversion (`.asi` file) by `MaxVol` and corresponding structures (`.xyz` file).

### 3. Selecting structures with large gamma
If you want to select some structures to add to the training set, you can calculate their extrapolation grade (`gamma`) and judge if their are outside the training set.
This can be performed by the `compute_extrapolatione` command in `GPUMD` or by `select_gamma.py`. You may modify the gamma cutoff to control how far they are from the training set. The default value in `select_gamma.py` is `1`.

However, the selected structures can be dupelicated, so you need to perform the next step.

### 4. Extending your training set
If you want to select some structures to add to the training set, your can put them together and perform a `MaxVol` selection. This is in `select_extend.py`.