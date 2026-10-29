"""PHYS 531 HW3, Problem 5(a): the sinc delta sequence for positive g.

Plot sin(g*x)/(pi*x), with the continuous value g/pi at x = 0.
The limit is distributional: values at fixed nonzero x keep oscillating.
"""

import argparse
from pathlib import Path

import matplotlib
import numpy as np


G_VALUES = (1.0, 4.0, 12.0, 30.0)
FULL_HALF_WIDTH = 5.0
ZOOM_HALF_WIDTH = 0.8
COLORS = ("#4A4A4A", "#527EA5", "#629187", "#B76455")


def delta_sequence(x, g):
    """Evaluate delta_g(x), including its removable singularity at zero.

    NumPy defines sinc(z) = sin(pi*z)/(pi*z). The product g*x is
    dimensionless; if x has length units, g has inverse-length units.
    """
    if not np.isfinite(g) or g <= 0:
        raise ValueError("g must be finite and positive")
    x = np.asarray(x, dtype=float)
    return (g / np.pi) * np.sinc(g * x / np.pi)


def make_figure(g_values=G_VALUES):
    """Compare the full oscillatory profile and its central peak."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for ax, half_width, title in zip(
        axes,
        (FULL_HALF_WIDTH, ZOOM_HALF_WIDTH),
        (r"$\delta_g(x)=\sin(gx)/(\pi x)$", "Central zoom"),
    ):
        # Resolve the fastest oscillation with at least 60 points per period.
        # An odd grid includes x = 0, preserving the exact peak height.
        half_samples = max(1000, int(np.ceil(half_width * max(g_values) * 30 / np.pi)))
        x = np.linspace(-half_width, half_width, 2 * half_samples + 1)
        for i, g in enumerate(g_values):
            ax.plot(x, delta_sequence(x, g), linewidth=2,
                    color=COLORS[i % len(COLORS)], label=rf"$g={g:g}$")
        ax.axhline(0, color="0.45", linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.grid(True, linestyle="--", linewidth=0.7, color="#D5DADD", alpha=0.7)
        ax.set(xlim=(-half_width, half_width), xlabel=r"$x$", title=title)
        ax.margins(y=0.06)
        ax.legend()
    axes[0].set_ylabel(r"$\delta_g(x)$")
    fig.tight_layout()
    return fig


def positive_g(value):
    """Parse the positive cutoff parameter used in this problem."""
    try:
        g = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("g must be a number") from exc
    if not np.isfinite(g) or g <= 0:
        raise argparse.ArgumentTypeError("g must be finite and positive")
    return g


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--g", nargs="+", type=positive_g, default=G_VALUES,
                        help="Positive cutoff values (default: 1 4 12 30)")
    parser.add_argument("--show", action="store_true", help="Also open the plot window")
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    print("g        peak g/pi       central width 2*pi/g")
    for g in args.g:
        print(f"{g:<8g} {g / np.pi:<15.6g} {2 * np.pi / g:.6g}")
    print("Width is measured between the first zeros; the signed integral over the real line is 1.")
    out_dir = Path(__file__).resolve().parent / "figs"
    out_dir.mkdir(exist_ok=True)
    fig = make_figure(args.g)
    for suffix in ("png", "svg"):
        path = out_dir / f"delta_sequence.{suffix}"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"Saved {path}")
    if args.show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
