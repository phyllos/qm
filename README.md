# PHYS 531

Coursework and numerical exercises for PHYS 531.

This is a script-only project. `uv run` installs the dependencies without
building or installing a `qm` package. Generated figures are saved to `figs/`.

## Homework 1

### Problem 3 — Blackbody Radiation

`blackbody.py` numerically evaluates the Planck blackbody spectrum for
2300 K and 5000 K.

The script:

- integrates the visible portion of the spectrum,
- compares the numerical full-spectrum integral with $u=aT^4$,
- verifies Wien's displacement law,
- generates individual and comparison plots.

Run:

```bash
uv run python blackbody.py
```

Output: four PNG figures with individual spectra and normalized and absolute
comparisons.

## Homework 3

### Polarization and Spin Measurement

`spin_measurement.py` compares transmission through three linear polarizers
and three spin-1/2 Stern-Gerlach filters.

The script:

- calculates transmission as a function of the middle apparatus angle,
- marks the optimal angles of $45^\circ$ for light and $90^\circ$ for spin 1/2,
- shows the shared maximum transmission of $1/4$ relative to the beam after
  the first filter, with each SG keeping only its positive output,
- generates separate transmission curves and apparatus diagrams.

Run:

```bash
uv run python spin_measurement.py
```

Output: two figures, each in PNG and SVG format. Add `--show` to open the
plot windows.

See [the derivation and physical interpretation](docs/spin_measurement.md).

### Problem 5(a) — Dirac Delta Sequence

`delta_sequence.py` plots $\sin(gx)/(\pi x)$ for positive cutoffs $g=1,4,12,30$.

The script:

- evaluates the continuous value $g/\pi$ at $x=0$,
- compares the full profile and central zoom on the same vertical scale,
- shows the taller, narrower central peak and increasingly rapid oscillations,
- reports the peak height and the width between the first zeros.

Run:

```bash
uv run python delta_sequence.py
```

Output: one two-panel figure in PNG and SVG format. Use `--g 1 4 12 30`
to select cutoffs, and add `--show` to open the plot window.

See [the interpretation and limiting behavior](docs/delta_sequence.md).

## Homework 4

### Problem 1(d,e) — Sudden Expansion of an Infinite Well

`sudden_well_expansion.py` plots the relative error of the series with its
$N^{-3}$ asymptote and marks where the partial sum first reaches 90% and 99%.
It also plots the dimensionless probability density $L\lvert\psi(3L/2,t)\rvert^2$
over one revival period, $T_{\mathrm{rev}}=16mL^2/(\pi\hbar)$, and checks
the exact densities at eighths of the period.

Run the script from the project root.

```bash
uv run python sudden_well_expansion.py
```

The two-panel figure is saved as `figs/sudden_well_expansion.png` and
`figs/sudden_well_expansion.svg`. Add `--show` to open the plot window.

See [the derivation and numerical checks](docs/sudden_well_expansion.md).

## Project Skill

Use [`$scientific-workflow`](.agents/skills/scientific-workflow/SKILL.md)
to model, solve, check, or visualize scientific and engineering problems.

