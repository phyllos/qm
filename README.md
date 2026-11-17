# PHYS 531

Coursework and numerical exercises for PHYS 531, from blackbody radiation
and spin measurements to quantum wells. Each problem folder has a Python
script, notes on the calculation, and the generated figures.

## Coursework

| Homework | Problem | Topic | Calculation and figures |
| --- | --- | --- | --- |
| 1 | 3 | [Blackbody radiation](hw01/p03_blackbody/README.md) | Compares the Planck spectra at 2300 K and 5000 K, integrates the visible band, and checks the Stefan–Boltzmann and Wien laws. |
| 3 | — | [Polarization and spin measurement](hw03/spin_measurement/README.md) | Uses transmission curves and apparatus diagrams to explain why the middle filter reaches peak transmission at different angles for light and spin 1/2. |
| 3 | 5(a) | [Dirac delta sequence](hw03/p05_delta_sequence/README.md) | Shows how the central peak and side lobes of the sinc sequence change with the cutoff. |
| 4 | 1(d,e) | [Sudden expansion of an infinite well](hw04/p01_sudden_well_expansion/README.md) | Checks the $N^{-3}$ decay of the series remainder and plots the probability density at $x=3L/2$ over one revival period. |
| 4 | 4(a–c,f) | [One-sided finite well](hw04/p04_one_sided_finite_well/README.md) | Finds bound states graphically, follows their energies as the well deepens, and compares their probabilities outside the well. |

## Run a script

Run the commands in each problem's README from the repository root. The
project uses `uv run` to install dependencies and run scripts.

```bash
uv run python hw04/p04_one_sided_finite_well/one_sided_finite_well.py
```

Each script writes its plots to the `figs/` directory next to the script.
When a problem has multiple figures, the two-digit prefix gives their reading
order. PNG and SVG exports of the same figure share a filename stem.

## Project Skill

Use [`$scientific-workflow`](.agents/skills/scientific-workflow/SKILL.md)
to model, solve, check, or visualize scientific and engineering problems.
