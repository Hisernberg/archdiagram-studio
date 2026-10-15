# Sources and attribution

Reviewed on 2026-10-15. Pin each reference to a concrete revision when revisiting it. The renderer, templates, examples, and prose in this repository are original. The sources below inform the reference catalog; they are not bundled dependencies or a claim of affiliation.

Repository-level license observations are not legal advice and do not establish rights to every third-party artifact mentioned by that repository. Review exact files and current terms before copying. In particular, do not describe pytorch2tikz as MIT: its license limits specified uses to internal non-commercial evaluation, testing, and academic research. No restricted or unclearly licensed source has been copied into this skill.

| Repository | Pinned revision | Observed license | Role in the catalog |
|---|---|---|---|
| [fraserlove/nntikz](https://github.com/fraserlove/nntikz) | [3dc29cfda3bd](https://github.com/fraserlove/nntikz/tree/3dc29cfda3bd18db2d1e73830f95b4d0985e050f) | MIT | Academic neural and attention figure consistency. |
| [harisiqbal88/PlotNeuralNet](https://github.com/harisiqbal88/PlotNeuralNet) | [e96bc852189c](https://github.com/harisiqbal88/PlotNeuralNet/tree/e96bc852189c2089dd500527a0a01a5a36e8977e) | MIT | Perspective CNN blocks and named anchor routing. |
| [xinychen/awesome-latex-drawing](https://github.com/xinychen/awesome-latex-drawing) | [a11dbbb3796f](https://github.com/xinychen/awesome-latex-drawing/tree/a11dbbb3796fb279790509fb87e0083f8d11fc96) | MIT | Tensor, Bayesian, and mathematical framework examples. |
| [xiaohanyu/awesome-tikz](https://github.com/xiaohanyu/awesome-tikz) | [8539838ba12a](https://github.com/xiaohanyu/awesome-tikz/tree/8539838ba12a3291f76d84047e804c50134c8254) | No clear repository license found | Resource discovery; duplicated user link deduplicated. |
| [PetarV-/TikZ](https://github.com/PetarV-/TikZ) | [86aee049f535](https://github.com/PetarV-/TikZ/tree/86aee049f5355d77c598b936399e42caf8941e60) | MIT | Broad graph, attention, and neural figure vocabulary. |
| [ccfang2/nndiagram](https://github.com/ccfang2/nndiagram) | [37e13168c6cf](https://github.com/ccfang2/nndiagram/tree/37e13168c6cf2612fbe85c7b0b33afb720945082) | MIT in LICENSE.md; LICENSE is an R metadata stub | Neuron-level dense connectivity and selected connections. |
| [FraunhoferHHI/pytorch2tikz](https://github.com/FraunhoferHHI/pytorch2tikz) | [95d40aa98be9](https://github.com/FraunhoferHHI/pytorch2tikz/tree/95d40aa98be99b87c68efa6d6e8ddd531ca1a4f7) | Custom academic/non-commercial license | Forward-pass-driven architecture capture; do not assume permissive reuse. |
| [pzeina/transformer-verif](https://github.com/pzeina/transformer-verif) | [05f42826db8a](https://github.com/pzeina/transformer-verif/tree/05f42826db8ad10584cb127e2408c1b58022d441) | No clear repository license found | Specialized hard-attention/mask visualization, not a generic transformer specification. |
| [shrenikvz/tikz-codes](https://github.com/shrenikvz/tikz-codes) | [16ea51aff7b0](https://github.com/shrenikvz/tikz-codes/tree/16ea51aff7b0cdede563946f14eacbd79879389a) | Apache-2.0 | Standalone neural figure organization and editable customization. |
| [LIVazquezS/Tikz_graphs](https://github.com/LIVazquezS/Tikz_graphs) | [171070532505](https://github.com/LIVazquezS/Tikz_graphs/tree/171070532505203263c1e73f1a2ff649a39fb74b) | No clear repository license found | Educational neural figures; README credits other originating sources. |
| [mvoelk/nn_graphics](https://github.com/mvoelk/nn_graphics) | [22c8ad79645b](https://github.com/mvoelk/nn_graphics/tree/22c8ad79645b46f3b7b84d81bc421257cbcae8ae) | MIT | Interpreted from the unqualified nn_graphics name; activation/pooling explanation figures. |

The user supplied `xiaohanyu/awesome-tikz` twice; it appears once here. `nn_graphics` was resolved to `mvoelk/nn_graphics` from its name and subject; if another project was intended, replace this catalog entry rather than inventing provenance.

## Practical reuse policy

Prefer original implementation and links. If a future contribution copies/adapts an upstream file, record its origin, exact revision, license, and modifications; preserve required notices; and update the attribution inventory. A missing license is not permission to redistribute. Keep the custom Fraunhofer license separate from this repository's MIT license.

## Scope of validation

Local tests cover this repository's renderer, installer, and example builds. They do not validate the upstream libraries, their maintenance status, or compatibility with every future TeX/PyTorch version. The examples are illustrative rather than diagrams of an audited deployed system.

## Sebastian Raschka study

The [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) and its [workflow article](https://sebastianraschka.com/blog/2026/llm-architecture-gallery.html) were studied for main-stream hierarchy, residual lanes, repeated blocks, and detail callouts. Three representative architecture thumbnails and the public contact sheet were downloaded for private inspection. They are not part of this repository. The [LLMs-from-scratch license](https://github.com/rasbt/LLMs-from-scratch/blob/main/LICENSE.txt) explicitly excludes related books and images from its licensed software Source. Original diagrams in this atlas are not an official Raschka collection and do not use his seal, signature, or watermark. See raschka-study.json for the study manifest. Each atlas figure separately records primary technical sources in its family index.
