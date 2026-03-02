# rvpulsim

## Overview

This package simulates the impact of stellar p-mode pulsations on
radial-velocity observations. Described in [Figueira et al. (2025)](https://ui.adsabs.harvard.edu/abs/2025A%26A...700A.174F/abstract), 
used also in Figueira et al. (2026, *in press*).

We consider a sequence of `N` consecutive observations, each defined by:

- an exposure time `T` [s],
- a photon-noise uncertainty `Pn` [m/s],
- and a readout / interval `I` [s] between exposures.

For a star characterized by the fundamental parameters
`Teff`, `L`, `M`, and `R`, asteroseismic scaling relations are used to
estimate the oscillation properties (`nu_max`, `Delta_nu`, envelope amplitude).

A multi-mode sinusoidal pulsation spectrum is constructed and
analytically integrated over each exposure duration, allowing the
exact computation of exposure-averaged radial velocities without
time-domain sampling.

Monte Carlo simulations are then used to estimate:

- the dispersion of nightly mean radial velocities, and
- the intra-night radial-velocity scatter,

enabling direct comparison with observed RV measurement statistics.

### Exposure Averaging

Earlier versions of the code computed exposure-averaged radial velocities by numerically sampling the pulsation signal in time and averaging the sampled values.
The current versions use an **analytic exposure integration**. For a sinusoidal mode

    v(t) = A * sin(omega * t - phi)

the exposure-averaged velocity over duration T can be computed exactly as:

    <v> = A * sinc(omega * T / 2) * sin(omega * t_mid - phi)

where:

- `omega = 2 * pi / P`
- `T` is the exposure duration
- `t_mid` is the exposure midpoint
- `sinc(x) = sin(x) / x`

This formula is mathematically exact for a linear sinusoidal signal.
For multiple p-modes, the exposure-averaged velocity is simply the sum
over all modes using the same expression.

---

### Performance Improvement

The previous numerical approach scaled as:

    O(n_iter × N_exp × N_time × N_modes)

because the signal was sampled in time. The analytic approach removes the time-sampling dimension and scales as:

    O(n_iter × N_exp × N_modes)

This typically results in a **15–100× speed improvement**, depending on
the number of time samples previously used.

---


## 📦 Installation

### 1. Install Python ≥ 3.10

### 2. Create and activate a virtual environment (recommended)

For instance, using `conda`
```
conda create -n RVenv python=3.10
conda activate RVend
```
### 3. Download and install package locally

Clone the repository and move to its local folder

```
git clone https://github.com/pedrorfigueira/RVpulsations.git
cd RVpulsations
```

and run

```
pip install .
```
To install in editable / developer mode use the flag `-e`; this enables live code editing without having to reinstall.


## 🖥️ Command Line Usage

Basic run:

```bash
rvpulsim --target HD127195
```

to load the target observation setup defined in `targets.py`

### Options

| Option                  | Description                                       |
| ----------------------- | ------------------------------------------------- |
| `--target NAME`         | Target star name (required)                       |
| `--model {sin,p_modes}` | Signal model (default: p_modes)                   |
| `--n-iter N`            | Number of Monte Carlo iterations (default: 10000) |
| `--plot`                | Display distribution plots                        |
| `--save-fig path.pdf`   | Save figure to file                               |
| `--seed INT`            | Set random seed for reproducibility               |

---

## Examples

Run 20k simulations:

```bash
rvpulsim --target HD127195 --n-iter 20000
```

Reproducible run:

```bash
rvpulsim --target HD127195 --n-iter 20000 --seed 42
```

Show plots:

```bash
rvpulsim --target HD127195 --plot
```

Save figure without displaying:

```bash
rvpulsim --target HD127195 --n-iter 20000 --save-fig results.pdf
```

Plot and save:

```bash
rvpulsim --target HD127195 --plot --save-fig results.pdf
```

---

## Reproducibility

The `--seed` option ensures deterministic Monte Carlo output using NumPy's `default_rng`.

---


## 📚 Program Structure

```
rvpulsations/
├─ pyproject.toml
├─ README.md
├─ .gitignore
└─ src/
   └─ rvpulsations/
      ├─ __init__.py
      ├─ targets.py          # targets & observational setup
      ├─ scaling.py          # asteroseismic scaling relations
      ├─ models.py           # sinusoid + p-modes models
      ├─ simulation.py       # Monte Carlo engine
      ├─ plotting.py         # visualization
      └─ cli.py              # command-line interface
```


## 🙌 Acknowledgements

Pedro Figueira acknowledges financial support from the Severo Ochoa grant CEX2021-001131-S funded by MCIN/AEI/10.13039/501100011033. Pedro Figueira is also funded by the European Union (ERC, THIRSTEE, 101164189). Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.

This project depends on several open-source scientific and visualization packages: NumPy, SciPy and Matplotlib.
We extend sincere thanks to all of these communities for developing and maintaining the scientific Python ecosystem.
