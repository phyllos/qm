---
name: scientific-workflow
description: Solve and explain scientific and engineering problems through conceptual reasoning, analytical derivations, numerical calculations, and explanatory figures. Use when choosing how to model, solve, check, or visualize a scientific question.
---

# Scientific Workflow

## Frame the question and choose a method

Identify what the user wants to understand, compare, or compute. State assumptions and conventions where they affect the answer, including the range in which the model applies. Start from a relation, diagram, or limiting case that helps explain the behavior. Choose a conceptual argument, derivation, or calculation that answers the question.

## Keep code proportional to the problem

One readable script can handle a small problem. Separate calculation, plotting, and file output when they need to be checked or changed independently. Extract shared code when repetition makes changes harder. Keep units, model parameters, and numerical settings easy to find. Follow the project's existing commands and dependencies.

## Choose checks that can detect plausible errors

Consider a plausible error and ask whether the check would detect it. If two plausible implementations agree at the endpoints or share a symmetry, test a point where their predictions differ against an analytic value or an independent calculation. Use dimensions, limiting behavior, conservation, and normalization when they test a relevant part of the model.

When several approximations contribute to the result, change one setting at a time and hold the others fixed. Compare the observable the user cares about. For example, refine a basis cutoff at fixed sample points, then refine the grid at a fixed cutoff. Explain what each comparison measures and whether it is an observed discrepancy or a justified error bound.

## Make the reasoning and figures easy to follow

Explain how the key steps connect the model to the result. Choose a diagram when the geometry or mechanism matters, a curve when the dependence on a variable matters, or comparable views when the differences between cases matter. Label variables, units, and normalizations, and match the sampling and axis scales to the features being interpreted. Inspect generated output for readability and agreement with the reasoning.

State the main conclusion and how any approximation affects it. Include the command or inputs needed to reproduce computed results when relevant. Match math markup to the delivery renderer and check the rendered output when available.
