import argparse
import numpy as np
import warnings 

from scipy.stats import norm, lognorm

from .targets import get_target
from .scaling import asteroseismic_scaling
from .simulation import simulate_nightly_rv
from .plotting import plot_distributions


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--target", required=True)

    parser.add_argument(
        "--model",
        default="p_modes",
        choices=["sin", "p_modes"]
    )
    parser.add_argument("--n-iter", type=int, default=50000)

    parser.add_argument(
        "--plot",
        action="store_true",
        help="Show distribution plots (default: False)"
    )

    parser.add_argument(
        "--save-fig",
        type=str,
        default=None,
        help="Save figure to given path (e.g. results.pdf)"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    # ---- RNG handling
    rng = np.random.default_rng(args.seed)

    target = get_target(args.target)

    # ============================================================
    # 1) INPUT PARAMETERS
    # ============================================================

    print("\n================= Simulation Configuration =================")
    print(f"Target              : {args.target}")
    print(f"Model               : {args.model}")
    print(f"Monte Carlo iters   : {args.n_iter}")
    print(f"Random seed         : {args.seed}")
    print("============================================================\n")

    # ============================================================
    # 2) STELLAR & DETECTOR PARAMETERS
    # ============================================================

    Nexp, exp_s, readout_s = target.det_config

    print("---------------- Stellar Parameters ----------------")
    print(f"Teff        : {target.Teff:.0f} K")
    print(f"L           : {target.L:.3f} L_sun")
    print(f"M           : {target.M:.3f} M_sun")
    print(f"R           : {target.R:.3f} R_sun")
    print("----------------------------------------------------\n")

    print("---------------- Detector Configuration ------------")
    print(f"Number of consecutive exposures      : {Nexp}")
    print(f"Exposure time (per exposure)         : {exp_s:.1f} s")
    print(f"Gap between exposures                : {readout_s:.1f} s")
    print(f"Photon noise (per exposure)          : {target.photon_noise:.2f} m/s")
    print("----------------------------------------------------\n")

    # ============================================================
    # 3) ASTEROSEISMIC SCALED PARAMETERS
    # ============================================================

    ppars = asteroseismic_scaling(
        target.Teff,
        target.L,
        target.M,
        target.R
    )

    A_env = ppars["A_env"]
    nu_max = ppars["nu_max"]
    delta_nu = ppars["delta_nu"]

    P_max_min = 1.0 / (nu_max * 60.0)
    inv_delta_nu_hours = 1.0 / (delta_nu * 3600.0)
    ratio = nu_max / delta_nu

    print("---------------- Asteroseismic Parameters -----------")
    print(f"A_env          : {A_env:.3f} m/s")
    print(f"nu_max         : {nu_max:.3e} Hz   (P_max = {P_max_min:.2f} min)")
    print(f"Delta_nu       : {delta_nu:.3e} Hz   (1/Δnu = {inv_delta_nu_hours:.2f} h)")
    print(f"nu_max/Δnu     : {ratio:.2f}")
    print("----------------------------------------------------\n")

    # ============================================================
    # 4) RUN SIMULATION
    # ============================================================

    rv_mean, rv_scat = simulate_nightly_rv(
        model=args.model,
        det_config=target.det_config,
        photon_noise=target.photon_noise,
        p_mode_params=ppars,
        n_iter=args.n_iter,
        rng=rng,
    )

    print("==================== Results ========================")
    
    mu, sigma = norm.fit(rv_mean * 100.0)
    sigma_val = sigma / 100.0
    
    print(f"Nightly mean RV σ (Gaussian fit)     : {sigma_val:.2f} m/s")
    
    if Nexp > 1:
        shape, loc, scale = lognorm.fit(rv_scat * 100.0)
        scatter_median = lognorm.median(shape, loc, scale) / 100.0
        print(f"Nightly scatter median (Lognormal fit): {scatter_median:.2f} m/s")
    else:
        print("Nightly scatter median (Lognormal fit): --")

    print("=====================================================\n")

    # Plot or save if requested
    if args.plot or args.save_fig:
        plot_distributions(
            rv_mean,
            rv_scat,
            target.name,
            target.det_config,
            save_path=args.save_fig,
        )
