# Active Learning of NEP

## Features

- Selecting active set with `MaxVol` algorithem by CPU or GPU.
- Calcualting extrapolation grade with `PyNEP`.
- Calcualting extrapolation grade during MD simulations with `GPUMD`.


## Installation

### (Optional) Create a conda environment
```shell
conda install -n nep_active python=3.10
conda activate nep_active
```
If you choose to install it in your current env, jump to the next step.


### Install PyNEP
Install the **latest** `PyNEP`. You can check its own [repository](https://github.com/bigd4/PyNEP) for details. 

```shell
pip install git+https://github.com/bigd4/PyNEP.git
```

### (Optional) Install CuPy
When selecting the active set, you may use `cupy` or `numpy`. `cupy` uses your GPU and is much faster when performing `MaxVol`. Since you are using `GPUMD`, I assume you have a GPU. You can check its [website](https://cupy.dev/) for installation details.

```shell
pip install cupy-cuda12x
```

## Usage
I provide an `example.ipynb`. I'm writing more detail.