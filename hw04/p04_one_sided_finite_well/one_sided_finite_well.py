"""PHYS 531 HW4, Problem 4: bound states in a one-sided finite well."""

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import ArrayLike, NDArray
from scipy.constants import electron_mass, electron_volt, hbar, nano
from scipy.integrate import quad
from scipy.optimize import brentq


WIDTH_NM = 1.0
ENERGY_SCALE_EV = hbar**2 / (2 * electron_mass * (WIDTH_NM * nano)**2) / electron_volt
STATE_COLORS = ("#176B88", "#B6502C", "#587D69")


@dataclass(frozen=True)
class BoundState:
    """The dimensionless matching root for one normalizable state."""

    level: int
    z: float  # kL inside the well
    w: float  # kappa L in the exterior

    @property
    def energy_ev(self) -> float:
        return -ENERGY_SCALE_EV * self.w**2

    @property
    def outside_probability(self) -> float:
        return np.sin(self.z)**2 / (1 + self.w)

    def scaled_density(self, position: ArrayLike) -> np.float64 | NDArray[np.float64]:
        """Evaluate L |psi|^2 at dimensionless position x/L."""
        y = np.asarray(position, dtype=float)
        # Clamp the sine at the well edges, then apply the exponential for y > 1.
        sine_squared = np.sin(self.z * np.clip(y, 0, 1))**2
        tail = np.exp(-2 * self.w * np.maximum(y - 1, 0))
        # Normalizing the interior and tail gives L A² = 2w / (1 + w).
        scaled_amplitude_squared = 2 * self.w / (1 + self.w)
        return scaled_amplitude_squared * sine_squared * tail


def threshold_depth_ev(level: int) -> float:
    """Depth where the specified mode reaches E=0."""
    return ENERGY_SCALE_EV * ((level - 0.5) * np.pi)**2


def solve_bound_state(level: int, depth_ev: float) -> BoundState | None:
    """Find the root on one branch when its energy is strictly below zero."""
    excess_depth_ev = depth_ev - threshold_depth_ev(level)
    if excess_depth_ev <= 0:
        return None

    rho = np.sqrt(depth_ev / ENERGY_SCALE_EV)
    z_threshold = (level - 0.5) * np.pi
    # Rationalize rho - z_threshold to retain precision near the threshold.
    radius_excess = excess_depth_ev / (ENERGY_SCALE_EV * (rho + z_threshold))

    def phase_residual(theta: float) -> float:
        # z = z_threshold + theta = rho cos(theta), using 1 - cos(theta) = 2 sin²(theta/2).
        return theta + 2 * rho * np.sin(theta / 2)**2 - radius_excess

    theta = brentq(
        phase_residual, 0, min(radius_excess, np.pi / 2), xtol=np.finfo(float).tiny,
    )
    return BoundState(level, z_threshold + theta, rho * np.sin(theta))


def verify_bound_state(state: BoundState) -> float:
    """Check slope matching and normalization, and return the integrated tail probability."""
    slope_residual = state.z * np.cos(state.z) + state.w * np.sin(state.z)
    inside, _ = quad(state.scaled_density, 0, 1)
    outside, _ = quad(state.scaled_density, 1, np.inf)
    np.testing.assert_allclose(slope_residual, 0, atol=1e-11, rtol=0)
    np.testing.assert_allclose(inside + outside, 1, atol=1e-10, rtol=0)
    np.testing.assert_allclose(outside, state.outside_probability, atol=1e-10, rtol=0)
    return outside


def style_axes(*axes: Axes) -> None:
    for ax in axes:
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#DCE3E7", lw=0.7)
        ax.spines[["top", "right"]].set_visible(False)


def make_matching_figure(states: tuple[BoundState, BoundState], critical_depth: float) -> Figure:
    """Show the well and the graphical solution at the chosen depth."""
    import matplotlib.pyplot as plt

    fig, (potential, matching) = plt.subplots(1, 2, figsize=(12, 4.6), layout="constrained")
    wall_color, arc_color = "#25394A", "#9A541E"

    x_left, x_right = -0.24 * WIDTH_NM, 1.42 * WIDTH_NM
    potential.plot([x_left, 0], [0, 0], color="#58646A", lw=2)
    potential.plot([0, WIDTH_NM, WIDTH_NM, x_right],
                   [-critical_depth, -critical_depth, 0, 0], color=wall_color, lw=2.3)
    potential.annotate("", (0, 0.23 * critical_depth), (0, -critical_depth),
                       arrowprops={"arrowstyle": "-|>", "color": wall_color, "lw": 2.3,
                                   "shrinkA": 0, "shrinkB": 0})
    potential.text(0.055 * WIDTH_NM, 0.18 * critical_depth, "Hard wall", color=wall_color)
    potential.text(0.09 * WIDTH_NM, -1.08 * critical_depth,
                   rf"$-V_0={-critical_depth:.3f}$ eV", color=wall_color, va="center")

    for state, color in zip(states, STATE_COLORS):
        potential.hlines(state.energy_ev, 0.04 * WIDTH_NM, 0.97 * WIDTH_NM,
                         colors=color, linestyles="--", linewidth=1.7)
        potential.annotate(rf"$E_{state.level}={state.energy_ev:.3f}$ eV",
                           (0.08 * WIDTH_NM, state.energy_ev), xytext=(0, 5),
                           textcoords="offset points", color=color)

    potential.set(xlim=(x_left, x_right), ylim=(-1.17 * critical_depth, 0.27 * critical_depth),
                  xticks=[0, 0.5 * WIDTH_NM, WIDTH_NM], xlabel=r"Position $x$ (nm)",
                  ylabel=r"Energy (eV)", title="Potential and bound-state energies")

    rho = np.sqrt(critical_depth / ENERGY_SCALE_EV)
    z_limit = rho + 0.8
    for level in (1, 2, 3):
        z_threshold = (level - 0.5) * np.pi
        z = np.linspace(z_threshold, min(z_limit, level * np.pi), 600, endpoint=False)
        # Evaluate -z cot(z) on a single branch with an exact zero at its start.
        matching.plot(z, z * np.tan(z - z_threshold), color=STATE_COLORS[0], lw=2.1)

    angle = np.linspace(0, np.pi / 2, 400)
    matching.plot(rho * np.sin(angle), rho * np.cos(angle), color=arc_color, ls="--", lw=2.1)
    matching.text(0.45, 0.90 * rho, r"$w=\sqrt{\rho^2-z^2}$", color=arc_color)
    matching.text(3.0, 0.38 * rho, r"$w=-z\cot z$", color=STATE_COLORS[0])
    for state in states:
        point = (state.z, state.w)
        matching.scatter(*point, s=42, color=wall_color, edgecolor="white", zorder=4)
        matching.annotate(rf"$n={state.level}$", point, xytext=(8, 7),
                          textcoords="offset points", color=wall_color)

    matching.scatter(rho, 0, s=61, facecolor="white", edgecolor=wall_color,
                     linewidth=1.7, zorder=4)
    matching.annotate("Threshold\n" + r"$n=3,\ E=0$", (rho, 0), xytext=(-28, 32),
                      textcoords="offset points", ha="right", color=wall_color,
                      arrowprops={"arrowstyle": "-", "color": wall_color})
    matching.set(xlim=(0, z_limit), ylim=(-0.18, 1.11 * rho),
                 xlabel=r"$z=kL$", ylabel=r"$w=\kappa L$",
                 title="Graphical solution at the third-state threshold")
    matching.set_xticks(np.arange(6) * np.pi / 2,
                        ["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$", r"$5\pi/2$"])

    style_axes(potential, matching)
    return fig


def make_spectrum_figure(states: tuple[BoundState, BoundState], critical_depth: float) -> Figure:
    """Show the three branches that reach threshold over the plotted depth range."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8.4, 5.2), layout="constrained")
    depth_limit = 1.28 * critical_depth
    second_threshold = threshold_depth_ev(2)
    ax.axvspan(second_threshold, critical_depth, color="#E1EEE8", zorder=0)
    ax.axhline(0, color="#58646A", lw=1)
    ax.axvline(critical_depth, color="#58646A", lw=1, ls="--")

    for level, color in enumerate(STATE_COLORS, start=1):
        threshold = threshold_depth_ev(level)
        depths = np.linspace(threshold, depth_limit, 320)
        # Draw the E=0 threshold separately from the normalizable states.
        energies = [0.0]
        for depth in depths[1:]:
            state = solve_bound_state(level, depth)
            if state is None:
                raise RuntimeError(f"Missing bound state n={level} at V0={depth:g} eV")
            energies.append(state.energy_ev)
        ax.plot(depths, energies, color=color, lw=2.1, label=rf"$n={level}$")
        ax.scatter(threshold, 0, s=44, facecolor="white", edgecolor=color,
                   linewidth=1.6, zorder=4)

    for state, color in zip(states, STATE_COLORS):
        point = (critical_depth, state.energy_ev)
        ax.scatter(*point, s=39, color=color, zorder=4)
        ax.annotate(rf"$E_{state.level}={state.energy_ev:.4f}$ eV", point,
                    xytext=(8, 8), textcoords="offset points", color=color)

    ax.text((second_threshold + critical_depth) / 2, 0.13, "Two bound states",
            color="#37594B", ha="center", va="bottom")
    ax.annotate(f"{second_threshold:.4f} eV", (second_threshold, 0),
                xytext=(-7, 12), textcoords="offset points", ha="right",
                color=STATE_COLORS[1])
    ax.annotate(f"Third-state threshold\n{critical_depth:.4f} eV",
                (critical_depth, 0), xytext=(13, 25), textcoords="offset points",
                color=STATE_COLORS[2], va="center",
                arrowprops={"arrowstyle": "-", "color": STATE_COLORS[2]})
    ax.set(xlim=(0, depth_limit), ylim=(-depth_limit, 0.44),
           xlabel=r"Well depth $V_0$ (eV)", ylabel=r"Energy $E$ (eV)",
           title=rf"Bound-state spectrum for an electron in a ${WIDTH_NM:g}$ nm well")
    style_axes(ax)
    ax.legend(loc="lower left", frameon=False)
    return fig


def make_density_figure(states: tuple[BoundState, BoundState], critical_depth: float) -> Figure:
    """Compare normalized densities and shade their probability beyond x=L."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8.4, 5.2), layout="constrained")
    # Three amplitude decay lengths show the tail of the least bound state.
    position_limit = 1 + 3 / min(state.w for state in states)
    inside = np.linspace(0, 1, 401)
    outside = np.linspace(1, position_limit, 241)
    position = np.concatenate((inside, outside[1:]))

    for state, color, label in zip(states, STATE_COLORS, ("Ground state", "First excited state")):
        density = state.scaled_density(position)
        ax.plot(position, density, lw=2.1, color=color,
                label=f"{label} ({state.outside_probability:.2%} outside)")
        ax.fill_between(outside, state.scaled_density(outside), color=color, alpha=0.25)

    ax.axvline(1, color="#58646A", lw=1, ls="--")
    ax.text(1.02, 1.46, r"Well edge $x=L$", color="#58646A", va="center")
    ax.set(xlim=(0, position_limit), ylim=(0, 2.24), xlabel=r"Position $x/L$",
           ylabel=r"Scaled probability density $L|\psi(x)|^2$",
           title=rf"Probability densities at $V_0={critical_depth:.4f}$ eV")
    style_axes(ax)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="none")
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true", help="Also open the plot windows")
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    critical_depth = threshold_depth_ev(3)
    ground = solve_bound_state(1, critical_depth)
    excited = solve_bound_state(2, critical_depth)
    if ground is None or excited is None or solve_bound_state(3, critical_depth) is not None:
        raise RuntimeError("Expected exactly two bound states at the third-state threshold")
    states = (ground, excited)
    print(f"Exactly two bound states for {threshold_depth_ev(2):.6f} < V0 <= {critical_depth:.6f} eV")
    print(f"At third-state threshold V0 = {critical_depth:.6f} eV")
    for state in states:
        outside = verify_bound_state(state)
        print(f"  n={state.level}: E = {state.energy_ev:.6f} eV, P(outside) = {outside:.4%}")

    figures = {
        "01_matching": make_matching_figure(states, critical_depth),
        "02_spectrum": make_spectrum_figure(states, critical_depth),
        "03_density": make_density_figure(states, critical_depth),
    }
    out_dir = Path(__file__).resolve().parent / "figs"
    out_dir.mkdir(exist_ok=True)
    for name, fig in figures.items():
        for suffix in ("png", "svg"):
            path = out_dir / f"{name}.{suffix}"
            fig.savefig(path, dpi=300)
            print(f"Saved {path}")
    if args.show:
        plt.show()
    for fig in figures.values():
        plt.close(fig)


if __name__ == "__main__":
    main()
