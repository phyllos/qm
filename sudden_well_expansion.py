"""PHYS 531 HW4, Problem 1(d,e): an infinite well expands from L to 2L."""

import argparse
from pathlib import Path

import matplotlib
import numpy as np


EXACT_SUM = np.pi**2 / 64
MAX_SERIES_INDEX = 100
TARGET_FRACTIONS = (0.90, 0.99)
MAX_ODD_MODE = 1023
CHECK_ODD_MODE = 2047
TIME_INTERVALS = 32_768
REVIVAL_TIMES = (0, 0.5, 1)
REVIVAL_DENSITIES = (0, 2, 0)


def relative_series_error(max_index):
    """Return the indices N and the relative remainder after terms 0 through N."""
    n = np.arange(max_index + 1)
    partial_sums = np.cumsum(1 / (4.0 * n**2 + 4 * n - 3)**2)
    return n, 1 - partial_sums / EXACT_SUM


def density_at_right_center(tau, max_odd_mode):
    """Evaluate L |psi(3L/2, t)|^2 at tau = t / T_rev."""
    tau = np.asarray(tau, dtype=float)
    odd_modes = np.arange(1, max_odd_mode + 1, 2)
    coefficients = (4 * np.sqrt(2) / np.pi) * (
        np.sin(np.pi * odd_modes / 2) / (4 - odd_modes**2)
    )
    weights = coefficients * np.sin(3 * np.pi * odd_modes / 4)

    # Only j=2 has nonzero overlap among the even modes. Its spatial sine is -1.
    phase = -2j * np.pi * tau
    amplitude = -np.exp(4 * phase) / np.sqrt(2)
    for mode, weight in zip(odd_modes, weights):
        amplitude += weight * np.exp(mode**2 * phase)
    return np.abs(amplitude)**2


def make_figure(n, error, threshold_indices, tau, density):
    """Show the series remainder and one full period of the point density."""
    import matplotlib.pyplot as plt

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.2), layout="constrained")
    blue, orange = "#176B88", "#B6502C"

    left.plot(n, error, color=blue, lw=2, label=r"$1 - S_N/Q$")
    large_n = n[n >= 4]
    left.plot(large_n, 4 / (3 * np.pi**2 * large_n**3), color=orange,
              lw=1.5, ls="--", label=r"$4/(3\pi^2N^3)$")
    # Use linear spacing between 0 and 1 so N=0 appears on the same axis.
    left.set_xscale("symlog", linthresh=1, linscale=0.45)
    left.set_yscale("log")
    left.set_xticks([0, 1, 2, 5, 10, 30, 100], labels=["0", "1", "2", "5", "10", "30", "100"])
    left.set(xlim=(0, 110), ylim=(6e-8, 0.65), xlabel=r"Last index $N$",
             ylabel=r"Relative error $\Delta(N)$", title="(d) Convergence of the series")
    for fraction, index in zip(TARGET_FRACTIONS, threshold_indices):
        remainder = 1 - fraction
        left.axhline(remainder, color="#87959E", lw=0.9, ls=":")
        left.text(85, 1.16 * remainder, f"{fraction:.0%} of $Q$",
                  color="#52626B", va="bottom", ha="right", fontsize=9)
        point = (n[index], error[index])
        left.scatter(*point, color=blue, s=22, zorder=3)
        left.annotate(rf"$N={n[index]}$", xy=point, xytext=(8, 13),
                      textcoords="offset points", color=blue, fontsize=9, va="bottom")
    left.legend(loc="lower left", frameon=False)

    right.plot(tau, density, color=blue, lw=1.35)
    right.scatter(REVIVAL_TIMES, REVIVAL_DENSITIES, s=24, color=orange,
                  zorder=3, clip_on=False)
    right.annotate("Mirror revival", xy=(0.5, 2), xytext=(0.57, 2.19),
                   color=orange, fontsize=9,
                   arrowprops={"arrowstyle": "-", "color": orange, "lw": 0.8})
    right.set(xlim=(0, 1), ylim=(0, 2.35), xlabel=r"Time $t/T_{\mathrm{rev}}$",
              ylabel=r"$L\,|\psi(3L/2,t)|^2$", title=r"(e) Density at $x=3L/2$")
    right.set_xticks([0, 0.25, 0.5, 0.75, 1])

    for ax in (left, right):
        ax.set_axisbelow(True)
        ax.grid(color="#DCE3E7", lw=0.7)
        ax.spines[["top", "right"]].set_visible(False)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true", help="Also open the plot window")
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n, error = relative_series_error(MAX_SERIES_INDEX)
    fractions = 1 - error
    threshold_indices = np.searchsorted(fractions, TARGET_FRACTIONS)
    for target, index in zip(TARGET_FRACTIONS, threshold_indices):
        print(f"{target:.0%} reached at N={n[index]} ({fractions[index]:.4%} of Q)")

    tau = np.linspace(0, 1, TIME_INTERVALS + 1)
    density = density_at_right_center(tau, MAX_ODD_MODE)

    # At k/8 of a period all odd j have j**2 = 1 mod 8, so they share one
    # phase. Their amplitude cancels the j=2 term at t=0 in the new half.
    eighths = np.arange(9) / 8
    exact_eighths = 1 - np.cos(6 * np.pi * eighths)
    np.testing.assert_allclose(
        density_at_right_center(eighths, MAX_ODD_MODE), exact_eighths,
        atol=0.002, rtol=0, err_msg="Density at eighths of the revival period",
    )
    np.testing.assert_allclose(density, density[::-1], atol=1e-9, rtol=0)

    refined_density = density_at_right_center(tau, CHECK_ODD_MODE)
    mode_change = np.max(np.abs(density - refined_density))

    # Doubling the number of time intervals adds one midpoint between each
    # pair of plotted samples. Compare it with the plotted linear segment.
    midpoint_times = (tau[:-1] + tau[1:]) / 2
    midpoint_density = density_at_right_center(midpoint_times, MAX_ODD_MODE)
    interpolated_density = (density[:-1] + density[1:]) / 2
    grid_change = np.max(np.abs(midpoint_density - interpolated_density))
    print(f"Max change in L*rho on the plot grid (odd j cutoff {MAX_ODD_MODE} to "
          f"{CHECK_ODD_MODE}): {mode_change:.3g}")
    print(f"Max midpoint error in L*rho from plot interpolation "
          f"({TIME_INTERVALS:,} to {2 * TIME_INTERVALS:,} time intervals): {grid_change:.3g}")

    fig = make_figure(n, error, threshold_indices, tau, density)
    out_dir = Path(__file__).resolve().parent / "figs"
    out_dir.mkdir(exist_ok=True)
    for suffix in ("png", "svg"):
        path = out_dir / f"sudden_well_expansion.{suffix}"
        fig.savefig(path, dpi=300)
        print(f"Saved {path}")
    if args.show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
