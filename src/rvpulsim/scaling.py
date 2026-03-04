import numpy as np

def asteroseismic_scaling(Teff: float, L: float, M: float, R: float):
    # calculate asteroseism parameters as a function of stellar params
    # Reference values for scaling taken from average of two known cases; see Figueira et al (2025)

    # amplitude of the mode [m/s] from Samadi (2007)
    p_mode_env = 0.3 * (L / 1.71) ** 0.7 * (M / 1.10) ** (-0.7)

    # frequency of the maximum amplitude and large separation frequency [Hz]; Eqs 43 and 44 from Garcia & Ballot (2019)
    nu_max = 2.1e-3 * (M / 1.10) * (R / 1.29) ** (-2) * (Teff / 5808.0) ** (-0.5)
    delta_nu = 1.0e-4 * (M / 1.10) ** 0.5 * (R / 1.29) ** (-1.5)

    return {
        "A_env": p_mode_env,
        "nu_max": nu_max,
        "delta_nu": delta_nu,
    }
