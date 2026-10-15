# Backend selection

The bundled JSON renderer and native TikZ templates are original implementations. The following projects are external references, not bundled dependencies or automatically tested adapters. See `sources.md` for pinned commits and license observations.

| Reference | Useful for | Practical consideration |
|---|---|---|
| fraserlove/nntikz | Consistent academic transformer, attention, recurrent, and neural figures | TikZ source; MIT observed |
| HarisIqbal88/PlotNeuralNet | Perspective CNN feature blocks and skip connections | Python-generated TikZ; requires TeX; MIT observed |
| xinychen/awesome-latex-drawing | Tensors, Bayesian networks, matrices, framework illustrations | Match notation to the actual model; MIT observed |
| xiaohanyu/awesome-tikz | Discovering TikZ libraries and tutorials | Curated links; no clear repository license found |
| PetarV-/TikZ | Graph attention, recurrent models, graph and neural figures | Broad reference gallery; MIT observed |
| ccfang2/nndiagram | Neuron-level diagrams and selective dense connectivity | R package; MIT text in `LICENSE.md` |
| FraunhoferHHI/pytorch2tikz | PyTorch forward-pass-driven CNN diagrams | Academic/non-commercial restrictions; traces are partial evidence |
| pzeina/transformer-verif | Attention masks and concrete coordinate-level computation | Specialized hard-attention example; no clear license found |
| shrenikvz/tikz-codes | Standalone neural and recurrent paper figures | Apache-2.0 observed; preserve obligations if reusing |
| LIVazquezS/Tikz_graphs | Educational CNN, GNN, and transformer examples | No clear license found; references other original sources |
| mvoelk/nn_graphics | Activation/pooling graphics and explanatory neural details | Interpreted as the user's `nn_graphics`; MIT observed |

For external use, inspect the pinned source first and then verify the current API/license if installing a newer revision. Preserve required notices for copied or adapted material. Do not label the entire ecosystem as MIT. Avoid importing an entire repository just to get one shape. Prefer the bundled renderer for portable agentic/system figures; prefer native TikZ when equations or paper typography matter.
