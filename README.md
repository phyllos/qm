# PHYS 531

Coursework and numerical exercises for PHYS 531.

## Homework 1

### Problem 3 — Blackbody Radiation

`blackbody.py` numerically evaluates the Planck blackbody spectrum for
2300 K and 5000 K.

The script:

- integrates the visible portion of the spectrum,
- compares the numerical full-spectrum integral with \(u=aT^4\),
- verifies Wien's displacement law,
- generates individual and comparison plots.

Run with:

```bash
uv run python blackbody.py
```

This is a script-only project. `uv run` installs its dependencies without
building or installing a `qm` package.
