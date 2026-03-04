import numpy as np

def sinusoid(t_min, A, P_min, phase):
    return A * np.sin(2 * np.pi * t_min / P_min - phase)


def gaussian_envelope(x, A, sigma):
    return A * np.exp(-(x**2) / (2 * sigma**2))

# not used, old version
def p_modes_signal(t_min, phases, A_env, nu_max, delta_nu, fwhm_factor=10.0):
    sigma = (fwhm_factor * delta_nu) / (2 * np.sqrt(2 * np.log(2)))
    P0 = 1.0 / (nu_max * 60.0)

    signal = sinusoid(t_min, A_env, P0, phases[0])
    k = 1
    mode_delta = delta_nu

    while gaussian_envelope(mode_delta, A_env, sigma) >= 0.01:
        amp = gaussian_envelope(mode_delta, A_env, sigma)
        P_minus = 1.0 / ((nu_max - mode_delta) * 60.0)
        P_plus  = 1.0 / ((nu_max + mode_delta) * 60.0)

        signal += sinusoid(t_min, amp, P_minus, phases[k])
        signal += sinusoid(t_min, amp, P_plus, phases[k + 1])

        k += 2
        mode_delta += delta_nu / 2.0

    return signal
