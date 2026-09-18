"""
PHYS 531 - Homework 1, Problem 3
Blackbody Radiation

This script:

1. Defines the Planck spectral energy density rho_lambda(lambda, T).
2. Numerically integrates the visible portion of the spectrum.
3. Numerically integrates the full spectrum.
4. Compares the numerical full-spectrum integral with u = a T^4.
5. Finds the spectral peak.
6. Tests Wien's displacement law.
7. Generates spectra for 2300 K and 5000 K.
8. Generates normalized and absolute comparison plots.
9. Gives a semi-quantitative comparison between a
   60 W incandescent bulb and a 6 W LED bulb.

All figures are saved automatically to:

    figs/
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar


# ============================================================
# Paths
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
FIG_DIR = SCRIPT_DIR / "figs"

FIG_DIR.mkdir(exist_ok=True)


# ============================================================
# Settings
# ============================================================

TEMPERATURES = (2300.0, 5000.0)

# Visible wavelength range
LAMBDA_VIS_MIN = 380e-9     # [m]
LAMBDA_VIS_MAX = 750e-9     # [m]

# Approximate full-spectrum integration range
LAMBDA_FULL_MIN = 1e-9      # 1 nm
LAMBDA_FULL_MAX = 1e-2      # 1 cm

# Whether figures should also appear on screen
SHOW_PLOTS = True

# Peak-line color
PEAK_COLOR = "#B8A99A"      # warm taupe


# ============================================================
# Physical constants
# ============================================================

h = 6.62607015e-34          # Planck constant [J s]
c = 2.99792458e8            # speed of light [m/s]
k_B = 1.380649e-23          # Boltzmann constant [J/K]

sigma = 5.670374419e-8      # Stefan-Boltzmann constant
                            # [W m^-2 K^-4]

# Radiation constant:
#
#     u = a T^4
#
# where
#
#     a = 4 sigma / c

a_rad = 4.0 * sigma / c     # [J m^-3 K^-4]

# Wien displacement constant:
#
#     lambda_max T = b

b_wien = 2.897771955e-3     # [m K]


# ============================================================
# Planck spectral energy density
# ============================================================

def rho_lambda(lam, T):
    """
    Planck spectral energy density per unit wavelength.

        rho_lambda(lambda, T)
            = (8 pi h c / lambda^5)
              / [exp(hc / (lambda k_B T)) - 1]

    Parameters
    ----------
    lam : float or ndarray
        Wavelength [m].

    T : float
        Temperature [K].

    Returns
    -------
    float or ndarray
        Spectral energy density [J m^-4].
    """

    x = h * c / (lam * k_B * T)

    with np.errstate(
        over="ignore",
        divide="ignore",
        invalid="ignore",
    ):
        return (
            8.0 * np.pi * h * c
            / lam**5
            / np.expm1(x)
        )


# ============================================================
# Spectral exitance
# ============================================================

def M_lambda(lam, T):
    """
    Spectral radiant exitance.

    For isotropic blackbody radiation:

        M_lambda = (c / 4) rho_lambda

    Units:
        W m^-3
    """

    return (c / 4.0) * rho_lambda(lam, T)


# ============================================================
# Numerical integration
# ============================================================

def integrate_band(T, lam_min, lam_max):
    """
    Integrate rho_lambda over a finite wavelength interval.
    """

    result, estimated_error = quad(
        lambda lam: rho_lambda(lam, T),
        lam_min,
        lam_max,
        epsabs=0.0,
        epsrel=1e-10,
        limit=300,
    )

    return result, estimated_error


def integrate_total(T):
    """
    Numerically approximate the full blackbody spectrum.

    Use the transformation

        lambda = exp(y),

    so that

        d lambda = exp(y) dy.

    This is more stable over many orders of magnitude
    in wavelength.
    """

    y_min = np.log(LAMBDA_FULL_MIN)
    y_max = np.log(LAMBDA_FULL_MAX)

    def integrand(y):
        lam = np.exp(y)
        return rho_lambda(lam, T) * lam

    result, estimated_error = quad(
        integrand,
        y_min,
        y_max,
        epsabs=0.0,
        epsrel=1e-10,
        limit=300,
    )

    return result, estimated_error


# ============================================================
# Exact full-spectrum result
# ============================================================

def total_energy_density_exact(T):
    """
    Exact total blackbody energy density:

        u = a T^4
    """

    return a_rad * T**4


# ============================================================
# Spectral peak
# ============================================================

def find_peak(T):
    """
    Numerically locate the maximum of rho_lambda.

    Optimization is performed in log(lambda).
    """

    def objective(log_lam):
        lam = np.exp(log_lam)
        return -rho_lambda(lam, T)

    result = minimize_scalar(
        objective,
        bounds=(
            np.log(100e-9),
            np.log(5000e-9),
        ),
        method="bounded",
    )

    lam_peak = np.exp(result.x)
    rho_peak = rho_lambda(lam_peak, T)

    return lam_peak, rho_peak


# ============================================================
# Analysis for one temperature
# ============================================================

def analyze_temperature(T):
    """
    Perform all numerical calculations for one temperature.
    """

    # Visible-spectrum integral
    u_visible, visible_quad_error = integrate_band(
        T,
        LAMBDA_VIS_MIN,
        LAMBDA_VIS_MAX,
    )

    # Full-spectrum numerical integral
    u_numeric, total_quad_error = integrate_total(T)

    # Exact result
    u_exact = total_energy_density_exact(T)

    # Visible fraction
    visible_fraction = u_visible / u_exact

    # Numerical integration accuracy
    integration_relative_error = abs(
        u_numeric - u_exact
    ) / u_exact

    # Spectral peak
    lam_peak, rho_peak = find_peak(T)

    # Wien displacement law
    wien_product = lam_peak * T

    wien_relative_error = abs(
        wien_product - b_wien
    ) / b_wien

    # Convert energy density into outward flux
    M_visible = (c / 4.0) * u_visible
    M_total = (c / 4.0) * u_exact

    return {
        "T": T,
        "u_visible": u_visible,
        "u_numeric": u_numeric,
        "u_exact": u_exact,
        "visible_fraction": visible_fraction,
        "visible_quad_error": visible_quad_error,
        "total_quad_error": total_quad_error,
        "integration_relative_error": integration_relative_error,
        "lam_peak": lam_peak,
        "rho_peak": rho_peak,
        "wien_product": wien_product,
        "wien_relative_error": wien_relative_error,
        "M_visible": M_visible,
        "M_total": M_total,
    }


# ============================================================
# Print results
# ============================================================

def print_results(result):
    """
    Print the important numerical results.
    """

    T = result["T"]

    print()
    print("=" * 68)
    print(f"Blackbody Radiation: T = {T:.0f} K")
    print("=" * 68)

    print("\nVisible wavelength interval")

    print(
        f"  {LAMBDA_VIS_MIN * 1e9:.0f}"
        f" - "
        f"{LAMBDA_VIS_MAX * 1e9:.0f} nm"
    )

    print("\nEnergy-density integrals")

    print(
        f"  Visible integral    : "
        f"{result['u_visible']:.8e} J/m^3"
    )

    print(
        f"  Full numerical      : "
        f"{result['u_numeric']:.8e} J/m^3"
    )

    print(
        f"  Exact a T^4         : "
        f"{result['u_exact']:.8e} J/m^3"
    )

    print("\nNumerical accuracy")

    print(
        f"  Relative error      : "
        f"{result['integration_relative_error']:.3e}"
    )

    print("\nVisible fraction")

    print(
        f"  f_visible           : "
        f"{result['visible_fraction']:.8f}"
    )

    print(
        f"  Visible percentage  : "
        f"{100 * result['visible_fraction']:.4f} %"
    )

    print("\nEquivalent emitted flux")

    print(
        f"  Visible M           : "
        f"{result['M_visible']:.8e} W/m^2"
    )

    print(
        f"  Total M             : "
        f"{result['M_total']:.8e} W/m^2"
    )

    print("\nSpectral peak")

    print(
        f"  lambda_max          : "
        f"{result['lam_peak'] * 1e9:.3f} nm"
    )

    print(
        f"  rho_lambda,max      : "
        f"{result['rho_peak'] * 1e-9:.8e} "
        f"J m^-3 nm^-1"
    )

    print("\nWien displacement law")

    print(
        f"  lambda_max T        : "
        f"{result['wien_product']:.8e} m K"
    )

    print(
        f"  Wien constant b     : "
        f"{b_wien:.8e} m K"
    )

    print(
        f"  Relative error      : "
        f"{result['wien_relative_error']:.3e}"
    )


# ============================================================
# Save / show helper
# ============================================================

def finish_figure(filename):
    """
    Save the current figure into figs/.
    """

    output_path = FIG_DIR / filename

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    print(f"Saved figure: {output_path}")

    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()


# ============================================================
# Individual spectrum plot
# ============================================================

def plot_spectrum(result):
    """
    Plot one blackbody spectrum.

    Shows:
        - blackbody spectrum,
        - visible region,
        - visible-region boundaries,
        - lambda_max dashed line,
        - peak marker.
    """

    T = result["T"]

    if T <= 3000:
        lam_nm = np.linspace(
            100,
            5000,
            6000,
        )
    else:
        lam_nm = np.linspace(
            100,
            2500,
            6000,
        )

    lam = lam_nm * 1e-9

    # Convert from per meter to per nanometer
    rho_nm = rho_lambda(lam, T) * 1e-9

    visible_mask = (
        (lam_nm >= LAMBDA_VIS_MIN * 1e9)
        & (lam_nm <= LAMBDA_VIS_MAX * 1e9)
    )

    lam_peak_nm = result["lam_peak"] * 1e9
    rho_peak_nm = result["rho_peak"] * 1e-9

    plt.figure(
        figsize=(8.5, 5.5)
    )

    # Spectrum
    plt.plot(
        lam_nm,
        rho_nm,
        linewidth=2,
        label=f"{T:.0f} K blackbody",
    )

    # Visible-region shaded area
    plt.fill_between(
        lam_nm[visible_mask],
        rho_nm[visible_mask],
        alpha=0.30,
        label="Visible range (380-750 nm)",
    )

    # Visible-region boundaries
    plt.axvline(
        LAMBDA_VIS_MIN * 1e9,
        linestyle="--",
        linewidth=1.0,
    )

    plt.axvline(
        LAMBDA_VIS_MAX * 1e9,
        linestyle="--",
        linewidth=1.0,
    )

    # Peak position
    plt.axvline(
        lam_peak_nm,
        color=PEAK_COLOR,
        linestyle="--",
        linewidth=1.5,
    )

    # Peak marker
    plt.scatter(
        lam_peak_nm,
        rho_peak_nm,
        zorder=4,
    )

    # Peak annotation
    plt.annotate(
        rf"$\lambda_{{\max}} = "
        rf"{lam_peak_nm:.0f}$ nm",
        xy=(
            lam_peak_nm,
            rho_peak_nm,
        ),
        xytext=(30, -40),
        textcoords="offset points",
        arrowprops={
            "arrowstyle": "->",
        },
    )

    plt.xlabel(
        "Wavelength (nm)"
    )

    plt.ylabel(
        r"Spectral energy density "
        r"$\rho_\lambda$ "
        r"(J m$^{-3}$ nm$^{-1}$)"
    )

    plt.title(
        f"Blackbody Spectrum at {T:.0f} K"
    )

    plt.xlim(
        lam_nm[0],
        lam_nm[-1],
    )

    plt.ylim(bottom=0)

    plt.legend()

    finish_figure(
        f"blackbody_{int(T)}K.png"
    )


# ============================================================
# Normalized comparison
# ============================================================

def plot_comparison_normalized():
    """
    Compare the shapes of the 2300 K and 5000 K spectra.

    Each spectrum is normalized by its own maximum.
    """

    lam_nm = np.linspace(
        100,
        3000,
        6000,
    )

    lam = lam_nm * 1e-9

    rho_2300 = (
        rho_lambda(
            lam,
            2300.0,
        )
        * 1e-9
    )

    rho_5000 = (
        rho_lambda(
            lam,
            5000.0,
        )
        * 1e-9
    )

    rho_2300_norm = (
        rho_2300
        / np.max(rho_2300)
    )

    rho_5000_norm = (
        rho_5000
        / np.max(rho_5000)
    )

    lam_peak_2300, _ = find_peak(
        2300.0
    )

    lam_peak_5000, _ = find_peak(
        5000.0
    )

    lam_peak_2300_nm = (
        lam_peak_2300 * 1e9
    )

    lam_peak_5000_nm = (
        lam_peak_5000 * 1e9
    )

    plt.figure(
        figsize=(8.5, 5.5)
    )

    # Spectra
    plt.plot(
        lam_nm,
        rho_2300_norm,
        linewidth=2,
        label="2300 K",
    )

    plt.plot(
        lam_nm,
        rho_5000_norm,
        linewidth=2,
        label="5000 K",
    )

    # Visible region
    plt.axvspan(
        380,
        750,
        alpha=0.20,
        label="Visible range",
    )

    # Visible boundaries
    plt.axvline(
        380,
        linestyle="--",
        linewidth=1.0,
    )

    plt.axvline(
        750,
        linestyle="--",
        linewidth=1.0,
    )

    # Peak lines
    plt.axvline(
        lam_peak_2300_nm,
        color=PEAK_COLOR,
        linestyle="--",
        linewidth=1.5,
    )

    plt.axvline(
        lam_peak_5000_nm,
        color=PEAK_COLOR,
        linestyle="--",
        linewidth=1.5,
    )

    # Peak markers
    plt.scatter(
        lam_peak_2300_nm,
        1.0,
        zorder=4,
    )

    plt.scatter(
        lam_peak_5000_nm,
        1.0,
        zorder=4,
    )

    # Peak labels
    plt.annotate(
        rf"$\lambda_{{\max}} "
        rf"\approx {lam_peak_2300_nm:.0f}$ nm",
        xy=(
            lam_peak_2300_nm,
            1.0,
        ),
        xytext=(25, -35),
        textcoords="offset points",
        arrowprops={
            "arrowstyle": "->",
        },
    )

    plt.annotate(
        rf"$\lambda_{{\max}} "
        rf"\approx {lam_peak_5000_nm:.0f}$ nm",
        xy=(
            lam_peak_5000_nm,
            1.0,
        ),
        xytext=(25, -70),
        textcoords="offset points",
        arrowprops={
            "arrowstyle": "->",
        },
    )

    plt.xlabel(
        "Wavelength (nm)"
    )

    plt.ylabel(
        "Normalized spectral energy density"
    )

    plt.title(
        "Normalized Comparison of Blackbody Spectra"
    )

    plt.xlim(
        100,
        3000,
    )

    plt.ylim(
        0,
        1.08,
    )

    plt.legend()

    finish_figure(
        "blackbody_comparison_normalized.png"
    )


# ============================================================
# Absolute comparison
# ============================================================

def plot_comparison_absolute():
    """
    Compare the actual spectral energy densities
    for 2300 K and 5000 K.
    """

    lam_nm = np.linspace(
        100,
        3000,
        6000,
    )

    lam = lam_nm * 1e-9

    rho_2300 = (
        rho_lambda(
            lam,
            2300.0,
        )
        * 1e-9
    )

    rho_5000 = (
        rho_lambda(
            lam,
            5000.0,
        )
        * 1e-9
    )

    lam_peak_2300, rho_peak_2300 = (
        find_peak(2300.0)
    )

    lam_peak_5000, rho_peak_5000 = (
        find_peak(5000.0)
    )

    lam_peak_2300_nm = (
        lam_peak_2300 * 1e9
    )

    lam_peak_5000_nm = (
        lam_peak_5000 * 1e9
    )

    rho_peak_2300_nm = (
        rho_peak_2300 * 1e-9
    )

    rho_peak_5000_nm = (
        rho_peak_5000 * 1e-9
    )

    plt.figure(
        figsize=(8.5, 5.5)
    )

    # Spectra
    plt.plot(
        lam_nm,
        rho_2300,
        linewidth=2,
        label="2300 K",
    )

    plt.plot(
        lam_nm,
        rho_5000,
        linewidth=2,
        label="5000 K",
    )

    # Visible region
    plt.axvspan(
        380,
        750,
        alpha=0.20,
        label="Visible range",
    )

    # Visible boundaries
    plt.axvline(
        380,
        linestyle="--",
        linewidth=1.0,
    )

    plt.axvline(
        750,
        linestyle="--",
        linewidth=1.0,
    )

    # Peak lines
    plt.axvline(
        lam_peak_2300_nm,
        color=PEAK_COLOR,
        linestyle="--",
        linewidth=1.5,
    )

    plt.axvline(
        lam_peak_5000_nm,
        color=PEAK_COLOR,
        linestyle="--",
        linewidth=1.5,
    )

    # Peak markers
    plt.scatter(
        lam_peak_2300_nm,
        rho_peak_2300_nm,
        zorder=4,
    )

    plt.scatter(
        lam_peak_5000_nm,
        rho_peak_5000_nm,
        zorder=4,
    )

    # Peak labels
    plt.annotate(
        rf"$\lambda_{{\max}} "
        rf"\approx {lam_peak_2300_nm:.0f}$ nm",
        xy=(
            lam_peak_2300_nm,
            rho_peak_2300_nm,
        ),
        xytext=(35, 30),
        textcoords="offset points",
        arrowprops={
            "arrowstyle": "->",
        },
    )

    plt.annotate(
        rf"$\lambda_{{\max}} "
        rf"\approx {lam_peak_5000_nm:.0f}$ nm",
        xy=(
            lam_peak_5000_nm,
            rho_peak_5000_nm,
        ),
        xytext=(35, -45),
        textcoords="offset points",
        arrowprops={
            "arrowstyle": "->",
        },
    )

    plt.xlabel(
        "Wavelength (nm)"
    )

    plt.ylabel(
        r"Spectral energy density "
        r"$\rho_\lambda$ "
        r"(J m$^{-3}$ nm$^{-1}$)"
    )

    plt.title(
        "Absolute Comparison of Blackbody Spectra"
    )

    plt.xlim(
        100,
        3000,
    )

    plt.ylim(bottom=0)

    plt.legend()

    finish_figure(
        "blackbody_comparison_absolute.png"
    )


# ============================================================
# Incandescent / LED comparison
# ============================================================

def incandescent_led_comparison(result_2300):
    """
    Semi-quantitative comparison between:

        60 W incandescent bulb
        6 W LED bulb
    """

    P_incandescent = 60.0    # [W]
    P_LED = 6.0              # [W]

    f_visible = (
        result_2300["visible_fraction"]
    )

    P_visible_incandescent = (
        P_incandescent
        * f_visible
    )

    required_LED_fraction = (
        P_visible_incandescent
        / P_LED
    )

    print()
    print("=" * 68)
    print(
        "Semi-quantitative Incandescent / LED Comparison"
    )
    print("=" * 68)

    print(
        "\nVisible fraction of a "
        "2300 K blackbody:"
    )

    print(
        f"  {100 * f_visible:.3f} %"
    )

    print(
        "\nIf a 60 W incandescent bulb behaved "
        "as an ideal 2300 K blackbody:"
    )

    print(
        f"  visible radiant power "
        f"~ {P_visible_incandescent:.3f} W"
    )

    print(
        "\nFor a 6 W LED to produce the same "
        "visible radiant power:"
    )

    print(
        f"  required visible fraction "
        f"~ {100 * required_LED_fraction:.1f} %"
    )

    print(
        "\nThus the blackbody calculation "
        "semi-quantitatively explains the "
        "order-of-magnitude difference "
        "in electrical power."
    )


# ============================================================
# Main
# ============================================================

def main():

    print(
        f"Figure directory: {FIG_DIR}"
    )

    # --------------------------------------------------------
    # Numerical analysis
    # --------------------------------------------------------

    results = {
        T: analyze_temperature(T)
        for T in TEMPERATURES
    }

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    for T in TEMPERATURES:
        print_results(
            results[T]
        )

    # --------------------------------------------------------
    # Individual spectra
    # --------------------------------------------------------

    for T in TEMPERATURES:
        plot_spectrum(
            results[T]
        )

    # --------------------------------------------------------
    # Comparison plots
    # --------------------------------------------------------

    plot_comparison_normalized()

    plot_comparison_absolute()

    # --------------------------------------------------------
    # Incandescent / LED estimate
    # --------------------------------------------------------

    incandescent_led_comparison(
        results[2300.0]
    )


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    main()


