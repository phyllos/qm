---
name: physics-workflow
description: Solve and explain physics problems in the qm project through clear models, maintainable calculation scripts, meaningful checks, and helpful visualizations. Use when implementing a physical model, exploring parameters, interpreting numerical results, or choosing how to visualize a physics question.
---

# Physics Workflow

Project guidance for solving and visualizing physics problems in qm. Aim for understandable physics, results that can be checked, and code that is easy to modify. Adapt these principles to the problem and the user's goal.

## Start with the physics

Identify the requested quantities, model assumptions, variables, units, and domain of validity. Explain conventions that affect the result, such as coordinate directions, initial states, boundary conditions, and normalization. Keep the derivation, computation, and figures consistent.

## Organize code around the calculation

- Prefer calculation functions with clear inputs and outputs. Keep plotting and file output separate so parameters, methods, and presentations can change independently.
- Make important parameters, constants, and units easy to find. Comments should explain physical meaning, approximations, and numerical choices.
- A small problem can remain a single script. Extract shared functions or modules when actual repetition or maintenance difficulties justify them; let structure grow with the problem.
- Follow the project's existing execution and dependency conventions. Saved code should reproduce the results.

## Check results using physics and numerics

Choose useful checks for the problem: dimensions, limiting cases, symmetry, conservation or normalization, analytical results, convergence, or an independent method. Focus on checks that can reveal real errors. Match computational effort and precision to the question, and explain how approximations or numerical errors affect the conclusions.

## Make visualization answer a question

Decide what the figure should clarify: trends, magnitudes, directions, processes, parameter dependence, or differences between models. Choose curves, diagrams, panels, animation, or interaction to suit that purpose.

Keep units, states, probabilities, and intensities unambiguous. Explain coordinates and normalization when comparing results. Use the project's clean, readable scientific figures as a starting point; colors, shading, and annotations should support the explanation. Adjust layouts, limits, and annotations to the data.

Generate and inspect the output. Check readability, clipping, and agreement between the visual presentation and the calculation. Deliver the requested figures or numbers, explain the main physical conclusion, and provide the execution command when relevant.

## Maintain the guidance as the project evolves

Incorporate clearly reusable lessons concisely into this skill. Keep problem-specific parameters, axis limits, and local layout adjustments in that problem's code. Read [references/examples.md](references/examples.md) when concrete examples would help; they illustrate choices rather than prescribe a template.
