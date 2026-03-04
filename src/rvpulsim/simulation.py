import numpy as np


def _precompute_exposure_geometry(det_config):
    """
    Precompute exposure midpoints and duration (minutes).
    """
    Nexp, exp_s, readout_s = det_config
    exp_min = exp_s / 60.0
    readout_min = readout_s / 60.0

    t_mid = []
    Texp = exp_min

    for i in range(Nexp):
        t0 = i * (exp_min + readout_min)
        t_mid.append(t0 + exp_min / 2.0)

    return np.array(t_mid), Texp


def _precompute_pmode_structure(A_env, nu_max, delta_nu, fwhm_factor=10.0):
    """
    Precompute all mode frequencies and amplitudes.
    """

    sigma = (fwhm_factor * delta_nu) / (2 * np.sqrt(2 * np.log(2)))

    if A_env <= 0.01:
        return np.array([nu_max]), np.array([A_env])

    x_max = np.sqrt(-2.0 * sigma**2 * np.log(0.01 / A_env))
    mode_deltas = np.arange(delta_nu, x_max, delta_nu / 2.0)

    freqs = [nu_max]
    amps = [A_env]

    for d in mode_deltas:
        amp = A_env * np.exp(-(d**2) / (2 * sigma**2))
        freqs.append(nu_max - d)
        freqs.append(nu_max + d)
        amps.append(amp)
        amps.append(amp)

    return np.array(freqs), np.array(amps)


def simulate_nightly_rv(
    model: str,
    det_config,
    photon_noise: float,
    p_mode_params: dict,
    n_iter: int = 10000,
    rng: np.random.Generator | None = None,
):
    """
    Analytic Monte Carlo simulation using exact exposure integration.
    """

    if rng is None:
        rng = np.random.default_rng()

    # ---- Exposure geometry
    t_mid, Texp = _precompute_exposure_geometry(det_config)
    Nexp = len(t_mid)

    # ---- Mode structure
    if model == "p_modes":
        freqs, amps = _precompute_pmode_structure(
            p_mode_params["A_env"],
            p_mode_params["nu_max"],
            p_mode_params["delta_nu"],
        )
    elif model == "sin":
        freqs = np.array([1.0 / (5.5 * 60.0)])  # Hz
        amps = np.array([0.6])
    else:
        raise ValueError(f"Unknown model '{model}'")

    n_modes = len(freqs)

    # Convert to angular frequency (rad/min)
    periods_min = 1.0 / (freqs * 60.0)
    omega = 2.0 * np.pi / periods_min

    # Finite exposure attenuation factor
    x = omega * Texp / 2.0
    sinc = np.ones_like(x)
    mask = np.abs(x) > 1e-12
    sinc[mask] = np.sin(x[mask]) / x[mask]

    # Photon noise
    photon_noise_matrix = rng.normal(
        0.0,
        photon_noise,
        size=(n_iter, Nexp),
    )

    nightly_matrix = np.zeros((n_iter, Nexp))

    # ---- Monte Carlo loop
    for it in range(n_iter):

        phases = rng.uniform(0, 2 * np.pi, size=n_modes)

        for j in range(Nexp):
            signal = np.sum(
                amps * sinc * np.sin(omega * t_mid[j] - phases)
            )
            nightly_matrix[it, j] = signal + photon_noise_matrix[it, j]

    RV_mean = nightly_matrix.mean(axis=1)
    RV_scatter = nightly_matrix.std(axis=1)

    return RV_mean, RV_scatter