"""PHYS 531 HW3: three polarizers versus three spin-1/2 SG filters.

I0 is measured AFTER the first polarizer/filter. Every SG device keeps
only its positive output; the negative output is blocked, not recombined.
Run `uv run python spin_measurement.py` to save the comparison figure.
"""

import argparse
from pathlib import Path

import matplotlib
import numpy as np


def light_transmission(angle_deg):
    """Transmission through the middle and final (90 degree) polarizers."""
    phi = np.deg2rad(angle_deg)
    return np.cos(phi) ** 2 * np.sin(phi) ** 2


def spin_transmission(angle_deg):
    """Transmission through SG_n(+) followed by SG_-x(+)."""
    gamma = np.deg2rad(angle_deg)
    return np.cos(gamma / 2) ** 2 * np.sin(gamma / 2) ** 2


def make_figure():
    """Plot the transmission curves using the blackbody figures' style."""
    import matplotlib.pyplot as plt

    angles = np.linspace(0, 180, 721)
    light_color, spin_color = "#C47116", "#2864C5"
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.plot(angles, light_transmission(angles), linewidth=2, color=light_color,
            label=r"Light: $\frac{1}{4}\sin^2(2\phi)$")
    ax.plot(angles, spin_transmission(angles), linewidth=2, color=spin_color,
            label=r"Spin 1/2: $\frac{1}{4}\sin^2\gamma$")

    for angle, color, label, offset in (
        (45, light_color, r"$\phi=45^\circ$", (22, 30)),
        (90, spin_color, r"$\gamma=90^\circ$", (22, 30)),
    ):
        ax.vlines(angle, 0, 0.25, color="#B8A99A",
                  linestyle="--", linewidth=1.5)
        ax.scatter(angle, 0.25, color=color, zorder=4)
        ax.annotate(label, xy=(angle, 0.25), xytext=offset,
                    textcoords="offset points", ha="center", va="bottom",
                    arrowprops={"arrowstyle": "->"})

    ax.set(xlim=(0, 180), ylim=(0, 0.30),
           xlabel=r"Middle apparatus angle ($\phi$ or $\gamma$)",
           ylabel=r"Transmitted intensity $I/I_0$",
           title="Transmission: Linear Polarizers and Spin-1/2 Filters")
    ticks = [0, 45, 90, 135, 180]
    ax.set_xticks(ticks, [f"{x}\N{DEGREE SIGN}" for x in ticks])
    ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25])
    ax.legend()
    fig.tight_layout()
    return fig


def make_apparatus_figure():
    """Save the apparatus explanation separately from the curve plot."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, axes = plt.subplots(2, 1, figsize=(8.5, 4.3))
    rows = (
        ("(b) Three linear polarizers",
         (r"$0^\circ$", r"$\phi$", r"$90^\circ$"),
         (r"$\cos^2\phi$", r"$\sin^2\phi$")),
        ("(c) Three SG filters (positive outputs selected)",
         (r"$SG_x$", r"$SG_{\mathbf{n}}$", r"$SG_{-x}$"),
         (r"$\cos^2(\gamma/2)$", r"$\sin^2(\gamma/2)$")),
    )
    for ax, (title, labels, factors) in zip(axes, rows):
        ax.set(xlim=(-0.8, 6), ylim=(-0.6, 1.3))
        ax.axis("off")
        ax.set_title(title, fontsize=11)
        for x, label in zip((0, 2.5, 5), labels):
            ax.add_patch(Rectangle((x - 0.5, 0), 1, 0.75,
                                   facecolor="white", edgecolor="black"))
            ax.text(x, 0.375, label, ha="center", va="center", fontsize=12)
        for start, end, factor in ((0.5, 2, factors[0]), (3, 4.5, factors[1])):
            ax.annotate("", xy=(end, 0.375), xytext=(start, 0.375),
                        arrowprops={"arrowstyle": "->"})
            ax.text((start + end) / 2, 0.8, factor, ha="center")
        ax.text(1.25, -0.25, r"$I_0$", ha="center")
        ax.annotate("", xy=(5.95, 0.375), xytext=(5.5, 0.375),
                    arrowprops={"arrowstyle": "->"})
        ax.text(5.75, -0.25, r"$I$", ha="center")
    fig.text(0.5, 0.04,
             r"$I_0$: intensity after the first filter. "
             "Each SG negative output is blocked.", ha="center", fontsize=10)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true", help="Also open the figure window")
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir = Path(__file__).resolve().parent / "figs"
    out_dir.mkdir(exist_ok=True)
    figures = {
        "spin_measurement_comparison": make_figure(),
        "spin_measurement_apparatus": make_apparatus_figure(),
    }
    for name, fig in figures.items():
        for suffix in ("png", "svg"):
            path = out_dir / f"{name}.{suffix}"
            fig.savefig(path, dpi=300, bbox_inches="tight")
            print(f"Saved {path}")
    if args.show:
        plt.show()
    for fig in figures.values():
        plt.close(fig)


if __name__ == "__main__":
    main()
