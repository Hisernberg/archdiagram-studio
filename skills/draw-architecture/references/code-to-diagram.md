# From code to architecture

1. Read the entry point, module definitions, model configuration, and runtime wiring. Cite file paths and symbols in `evidence` strings. Inspect data types, shapes, calls, return values, conditionals, loops, and shared objects.
2. Build a component/edge inventory before assigning coordinates. Separate logical modules from deployed services, and training from inference. Collapse implementation detail into a module only when the audience benefits.
3. Trace tensor shapes with a representative input only if execution is appropriate. Run in evaluation mode with gradients disabled, document the example shape, and avoid modifying parameters. Static inspection remains the default when execution is unnecessary.
4. Mark dynamic paths that a trace does not cover. A forward hook inventory is not a complete graph: functional operations, residual additions, reused modules, branches, and data-dependent loops can be missed. `torch.fx` symbolic tracing also has limits around data-dependent control flow. Never present either as a proof of the full architecture.
5. Build the JSON source or native TikZ. Map every visible component to code evidence. Keep uncertain shapes symbolic (`B x T x D`) and explain unknown values in `assumptions`.
6. Compare the final figure back to the implementation. Count branches and merges; check that an edge means the same thing in the source and in the figure.

For a PyTorch-first 3D rendering workflow, the requested `pytorch2tikz` project exposes an `Architecture(model)` interface and captures a forward pass. Its repository license restricts use to specified internal non-commercial evaluation, testing, and academic research. Read the current license before choosing it; use the original bundled renderer when those restrictions do not fit. This skill does not vendor, install, or execute it automatically.
