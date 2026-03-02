from dataclasses import dataclass

@dataclass(frozen=True)
class Target:
    name: str
    Teff: float
    L: float
    M: float
    R: float
    det_config: tuple[int, float, float]  # Nexp, exptime[s], interval[s]
    photon_noise: float  # m/s


TARGETS = {
    "HD125136": Target(
        name="HD125136",
        Teff=4960.0, L=16.0, M=1.5, R=5.5,
        det_config=(3, 600.0, 3000.0),
        photon_noise=4.3,
    ),
    "HD127195": Target(
        name="HD127195",
        Teff=5000.0, L=10.0, M=1.40, R=4.20,
        det_config=(3, 300.0, 1200.0),
        photon_noise=3.6,
    ),
}


def get_target(name: str) -> Target:
    try:
        return TARGETS[name]
    except KeyError:
        raise ValueError(f"Unknown target '{name}'. Available: {list(TARGETS)}")
