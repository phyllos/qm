# HW1 Problem 3 — Blackbody radiation

`blackbody.py` numerically evaluates the Planck blackbody spectrum for
2300 K and 5000 K. It integrates the visible portion of each spectrum,
compares the full-spectrum integral with $u=aT^4$, and verifies Wien's
displacement law.

## Figures

1. [Spectrum at 2300 K](figs/01_spectrum_2300K.png)
2. [Spectrum at 5000 K](figs/02_spectrum_5000K.png)
3. [Normalized comparison](figs/03_comparison_normalized.png)
4. [Absolute comparison](figs/04_comparison_absolute.png)

## Run

Run from the repository root.

```bash
uv run python hw01/p03_blackbody/blackbody.py
```

The script saves the four PNG files in the problem's `figs/` directory.
