# Two examples from this project

File paths below are relative to the repository root.

## Blackbody radiation

`blackbody.py` computes integrals and peaks from the Planck spectrum, checks total energy density and the Stefan-Boltzmann / Wien relations, and produces individual and comparison plots.

Transferable lessons: connect formulas, numerical methods, and physical checks; distinguish curve shape from absolute magnitude when normalizing; keep plotted units consistent with changes of variables in the calculation.

## Polarization and spin measurement

`spin_measurement.py` separates transmission calculations from plotting. Its probability formulas were independently checked with state projections during implementation. Curves and apparatus diagrams explain the different optimal angles.

Transferable lessons: identify the initial state and conditional probabilities, state where I0 is defined, and use figures to explain differences between formulas. Apparatus diagrams and numerical curves can be separate outputs; choose the layout to suit the content.

## Visual references

See the existing `figs/blackbody_comparison_normalized.png` and `figs/spin_measurement_comparison.png`.

The accepted deep orange `#C47116`, blue `#2864C5`, and angled annotations above peaks are useful starting points for later curve plots. Adapt line styles, colors, frames, grids, and annotation placement to each figure. The SG plot's 0.3 upper limit and hidden top tick apply only to that plot.
