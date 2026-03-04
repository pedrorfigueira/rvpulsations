import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm


def plot_distributions(
    rv_mean,
    rv_scatter,
    target_name,
    det_config,
    save_path: str | None = None,
):
    """
    Plot nightly RV mean and scatter distributions.

    If save_path is provided, the figure is saved there.
    Otherwise it is shown interactively.
    """

    rv_mean_cm = rv_mean * 100.0
    rv_scatter_cm = rv_scatter * 100.0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 10))
    fig.subplots_adjust(hspace=0.35)

    # ---- Nightly mean RV
    mu, sigma = norm.fit(rv_mean_cm)

    ax1.hist(rv_mean_cm, bins=30, density=True, alpha=0.5)

    x = np.linspace(rv_mean_cm.min(), rv_mean_cm.max(), 500)
    ax1.plot(
        x,
        norm.pdf(x, mu, sigma),
        linestyle="--",
        linewidth=2,
        label=f"Gaussian σ={sigma/100:.3f} m/s"
    )

    ax1.set_xlabel("Nightly average RV [cm/s]")
    ax1.set_ylabel("Density")
    ax1.legend()

    # ---- Nightly scatter
    shape, loc, scale = lognorm.fit(rv_scatter_cm)

    ax2.hist(rv_scatter_cm, bins=30, density=True, alpha=0.5)

    x = np.linspace(rv_scatter_cm.min(), rv_scatter_cm.max(), 500)
    ax2.plot(
        x,
        lognorm.pdf(x, shape, loc, scale),
        linestyle="--",
        linewidth=2,
        label=f"Lognormal median={lognorm.median(shape, loc, scale)/100:.3f} m/s"
    )

    ax2.set_xlabel("Nightly RV scatter [cm/s]")
    ax2.set_ylabel("Density")
    ax2.legend()

    fig.suptitle(
        f"{target_name} — "
        f"Nexp={det_config[0]}, "
        f"texp={det_config[1]} s, "
        f"readout={det_config[2]} s"
    )

    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()