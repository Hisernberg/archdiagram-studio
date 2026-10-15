window.ARCHDIAGRAM_GALLERY = {
  "renderer_version": "2.0.0",
  "theme": "monochrome",
  "families": {
    "vision": 20,
    "text": 20,
    "audio": 20,
    "multimodal": 15,
    "agents": 15,
    "robotics-graphs": 10
  },
  "examples": [
    {
      "id": "vision-convolution",
      "title": "Spatial convolution: one local response",
      "family": "vision",
      "description": "A shared spatial kernel, its receptive field, and the multi-channel convolution equation.",
      "caption": "A kernel is reused at each spatial location; channel sums create each output channel.",
      "sources": [
        "https://docs.pytorch.org/docs/2.14/generated/torch.nn.Conv2d.html"
      ],
      "assumptions": [
        "The illustrated spatial sizes are pedagogical; no model checkpoint is specified.",
        "The equation follows the cross-correlation convention used by common deep-learning libraries."
      ],
      "tags": [
        "cnn",
        "convolution",
        "receptive-field"
      ],
      "nodes": 4,
      "edges": 0,
      "source_file": "vision-convolution.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-convolution.json",
      "svg": "gallery/atlas/vision-convolution.svg",
      "png": "gallery/atlas/vision-convolution.png",
      "pdf": "gallery/atlas/vision-convolution.pdf",
      "tex": "gallery/atlas/vision-convolution.tex"
    },
    {
      "id": "vision-residual-block",
      "title": "Residual block: preserve an identity route",
      "family": "vision",
      "description": "A post-activation two-convolution residual block with an explicit identity shortcut.",
      "caption": "The residual branch learns a correction; an identity shortcut reaches the same addition node.",
      "sources": [
        "https://arxiv.org/abs/1512.03385"
      ],
      "assumptions": [
        "An identity shortcut assumes matching tensor shapes; projection shortcuts are outside this concept view."
      ],
      "tags": [
        "cnn",
        "residual",
        "identity"
      ],
      "nodes": 6,
      "edges": 6,
      "source_file": "vision-residual-block.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-residual-block.json",
      "svg": "gallery/atlas/vision-residual-block.svg",
      "png": "gallery/atlas/vision-residual-block.png",
      "pdf": "gallery/atlas/vision-residual-block.pdf",
      "tex": "gallery/atlas/vision-residual-block.tex"
    },
    {
      "id": "vision-dense-block",
      "title": "Dense block: accumulate earlier feature maps",
      "family": "vision",
      "description": "A three-layer DenseNet concept with explicit growing feature banks and reuse routes.",
      "caption": "Each transform reads the complete feature bank; concatenation appends its new channels.",
      "sources": [
        "https://arxiv.org/abs/1608.06993"
      ],
      "assumptions": [
        "Conceptual schematic; dimensions and details vary by implementation."
      ],
      "tags": [
        "cnn",
        "densenet",
        "concatenation"
      ],
      "nodes": 7,
      "edges": 9,
      "source_file": "vision-dense-block.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-dense-block.json",
      "svg": "gallery/atlas/vision-dense-block.svg",
      "png": "gallery/atlas/vision-dense-block.png",
      "pdf": "gallery/atlas/vision-dense-block.pdf",
      "tex": "gallery/atlas/vision-dense-block.tex"
    },
    {
      "id": "vision-unet",
      "title": "U-Net: contract for context, expand for localization",
      "family": "vision",
      "description": "A reduced U-Net hierarchy with contracting and expanding paths and aligned skip concatenations.",
      "caption": "Skip features are aligned and concatenated with the upsampled decoder stream at matching scales.",
      "sources": [
        "https://arxiv.org/abs/1505.04597"
      ],
      "assumptions": [
        "Two resolution changes illustrate the topology rather than reproduce the depth of a published checkpoint.",
        "Alignment represents the cropping required by the original valid-convolution formulation."
      ],
      "tags": [
        "segmentation",
        "unet",
        "encoder-decoder"
      ],
      "nodes": 7,
      "edges": 8,
      "source_file": "vision-unet.tex",
      "width_cm": 18,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-unet.json",
      "svg": "gallery/atlas/vision-unet.svg",
      "png": "gallery/atlas/vision-unet.png",
      "pdf": "gallery/atlas/vision-unet.pdf",
      "tex": "gallery/atlas/vision-unet.tex"
    },
    {
      "id": "vision-feature-pyramid",
      "title": "Feature pyramid: bottom-up detail, top-down semantics",
      "family": "vision",
      "description": "A four-scale FPN with lateral 1x1 projections, top-down upsampling, addition, and 3x3 smoothing.",
      "caption": "Lateral projections combine backbone features with upsampled coarse features before spatial smoothing.",
      "sources": [
        "https://arxiv.org/abs/1612.03144"
      ],
      "assumptions": [
        "Conceptual schematic; dimensions and details vary by implementation."
      ],
      "tags": [
        "detection",
        "fpn",
        "multiscale"
      ],
      "nodes": 16,
      "edges": 18,
      "source_file": "vision-feature-pyramid.tex",
      "width_cm": 18,
      "height_cm": 10.5,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-feature-pyramid.json",
      "svg": "gallery/atlas/vision-feature-pyramid.svg",
      "png": "gallery/atlas/vision-feature-pyramid.png",
      "pdf": "gallery/atlas/vision-feature-pyramid.pdf",
      "tex": "gallery/atlas/vision-feature-pyramid.tex"
    },
    {
      "id": "vision-vision-transformer",
      "title": "Vision Transformer: an image becomes a token sequence",
      "family": "vision",
      "description": "A ViT concept showing a patch grid, embeddings, class and position tokens, repeated encoder, and class readout.",
      "caption": "Patch embeddings and a learned class token receive positions before repeated global attention blocks.",
      "sources": [
        "https://arxiv.org/abs/2010.11929"
      ],
      "assumptions": [
        "Conceptual schematic; dimensions and details vary by implementation."
      ],
      "tags": [
        "transformer",
        "vit",
        "patches"
      ],
      "nodes": 8,
      "edges": 7,
      "source_file": "vision-vision-transformer.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-vision-transformer.json",
      "svg": "gallery/atlas/vision-vision-transformer.svg",
      "png": "gallery/atlas/vision-vision-transformer.png",
      "pdf": "gallery/atlas/vision-vision-transformer.pdf",
      "tex": "gallery/atlas/vision-vision-transformer.tex"
    },
    {
      "id": "vision-shifted-windows",
      "title": "Shifted-window attention: connect neighboring windows",
      "family": "vision",
      "description": "Regular and shifted window grids linked to alternating Swin attention blocks and boundary masking.",
      "caption": "Alternating regular and shifted partitions creates cross-window communication without global attention.",
      "sources": [
        "https://arxiv.org/abs/2103.14030"
      ],
      "assumptions": [
        "An eight-by-eight token grid with four-token windows illustrates the two-token partition shift."
      ],
      "tags": [
        "transformer",
        "swin",
        "window-attention"
      ],
      "nodes": 4,
      "edges": 2,
      "source_file": "vision-shifted-windows.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-shifted-windows.json",
      "svg": "gallery/atlas/vision-shifted-windows.svg",
      "png": "gallery/atlas/vision-shifted-windows.png",
      "pdf": "gallery/atlas/vision-shifted-windows.pdf",
      "tex": "gallery/atlas/vision-shifted-windows.tex"
    },
    {
      "id": "vision-masked-autoencoder",
      "title": "Masked autoencoder: encode only visible image patches",
      "family": "vision",
      "description": "An asymmetric masked autoencoder with visible-token encoding, mask-token restoration, and masked-pixel objective.",
      "caption": "A lightweight decoder restores missing positions; reconstruction loss is evaluated on masked patches.",
      "sources": [
        "https://arxiv.org/abs/2111.06377"
      ],
      "assumptions": [
        "Conceptual schematic; dimensions and details vary by implementation."
      ],
      "tags": [
        "self-supervised",
        "mae",
        "masking"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "vision-masked-autoencoder.tex",
      "width_cm": 18,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-masked-autoencoder.json",
      "svg": "gallery/atlas/vision-masked-autoencoder.svg",
      "png": "gallery/atlas/vision-masked-autoencoder.png",
      "pdf": "gallery/atlas/vision-masked-autoencoder.pdf",
      "tex": "gallery/atlas/vision-masked-autoencoder.tex"
    },
    {
      "id": "vision-deterministic-autoencoder",
      "title": "Deterministic autoencoder: compress and reconstruct",
      "family": "vision",
      "description": "A deterministic encoder-decoder bottleneck with reconstruction paths from input and output into the objective.",
      "caption": "The compact code is a deterministic function of the input; reconstruction error trains both paths.",
      "sources": [
        "https://www.cs.toronto.edu/~hinton/absps/science.pdf"
      ],
      "assumptions": [
        "This general image autoencoder concept does not reproduce the layer widths or pretraining of the cited work."
      ],
      "tags": [
        "autoencoder",
        "representation",
        "reconstruction"
      ],
      "nodes": 6,
      "edges": 6,
      "source_file": "vision-deterministic-autoencoder.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-deterministic-autoencoder.json",
      "svg": "gallery/atlas/vision-deterministic-autoencoder.svg",
      "png": "gallery/atlas/vision-deterministic-autoencoder.png",
      "pdf": "gallery/atlas/vision-deterministic-autoencoder.pdf",
      "tex": "gallery/atlas/vision-deterministic-autoencoder.tex"
    },
    {
      "id": "vision-variational-autoencoder",
      "title": "Variational autoencoder: a distribution at the bottleneck",
      "family": "vision",
      "description": "A VAE with posterior parameters, noise reparameterization, reconstruction likelihood and KL objective paths.",
      "caption": "Reparameterized samples connect reconstruction learning to a posterior regularized toward the prior.",
      "sources": [
        "https://arxiv.org/abs/1312.6114"
      ],
      "assumptions": [
        "A diagonal Gaussian posterior and standard-normal prior are shown; decoder likelihood is abstract."
      ],
      "tags": [
        "vae",
        "generative",
        "latent-variable"
      ],
      "nodes": 11,
      "edges": 14,
      "source_file": "vision-variational-autoencoder.tex",
      "width_cm": 18,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-variational-autoencoder.json",
      "svg": "gallery/atlas/vision-variational-autoencoder.svg",
      "png": "gallery/atlas/vision-variational-autoencoder.png",
      "pdf": "gallery/atlas/vision-variational-autoencoder.pdf",
      "tex": "gallery/atlas/vision-variational-autoencoder.tex"
    },
    {
      "id": "vision-gan",
      "title": "Adversarial generation: two models, one learning game",
      "family": "vision",
      "description": "A two-player GAN with shared discriminator calls, real and generated data paths, and generator update feedback.",
      "caption": "The discriminator shares parameters across real and generated examples; gradient feedback updates both players.",
      "sources": [
        "https://arxiv.org/abs/1406.2661"
      ],
      "assumptions": [
        "The original minimax objective is shown; practical generator losses can differ."
      ],
      "tags": [
        "gan",
        "adversarial",
        "training"
      ],
      "nodes": 9,
      "edges": 11,
      "source_file": "vision-gan.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-gan.json",
      "svg": "gallery/atlas/vision-gan.svg",
      "png": "gallery/atlas/vision-gan.png",
      "pdf": "gallery/atlas/vision-gan.pdf",
      "tex": "gallery/atlas/vision-gan.tex"
    },
    {
      "id": "vision-ddpm",
      "title": "Denoising diffusion: corrupt forward, learn the reverse",
      "family": "vision",
      "description": "A DDPM forward/reverse timeline and noise-prediction training graph with sampled noise and time.",
      "caption": "Training predicts the sampled noise at a random time; generation repeatedly applies the learned reverse transition.",
      "sources": [
        "https://arxiv.org/abs/2006.11239"
      ],
      "assumptions": [
        "Conceptual schematic; dimensions and details vary by implementation."
      ],
      "tags": [
        "diffusion",
        "ddpm",
        "denoising"
      ],
      "nodes": 10,
      "edges": 12,
      "source_file": "vision-ddpm.tex",
      "width_cm": 18,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-ddpm.json",
      "svg": "gallery/atlas/vision-ddpm.svg",
      "png": "gallery/atlas/vision-ddpm.png",
      "pdf": "gallery/atlas/vision-ddpm.pdf",
      "tex": "gallery/atlas/vision-ddpm.tex"
    },
    {
      "id": "vision-latent-diffusion",
      "title": "Latent diffusion: denoise a compressed image representation",
      "family": "vision",
      "description": "Distinct latent-diffusion training and sampling panels with image compression, conditioning, reverse iteration and decoding.",
      "caption": "An autoencoder defines latent space; a conditioned denoiser learns there and its reverse process feeds the decoder.",
      "sources": [
        "https://arxiv.org/abs/2112.10752"
      ],
      "assumptions": [
        "This is a generic latent diffusion concept, not a particular Stable Diffusion checkpoint or conditioning encoder."
      ],
      "tags": [
        "diffusion",
        "latent-diffusion",
        "conditioning"
      ],
      "nodes": 13,
      "edges": 11,
      "source_file": "vision-latent-diffusion.tex",
      "width_cm": 18,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-latent-diffusion.json",
      "svg": "gallery/atlas/vision-latent-diffusion.svg",
      "png": "gallery/atlas/vision-latent-diffusion.png",
      "pdf": "gallery/atlas/vision-latent-diffusion.pdf",
      "tex": "gallery/atlas/vision-latent-diffusion.tex"
    },
    {
      "id": "vision-detr",
      "title": "DETR: object queries predict an unordered set",
      "family": "vision",
      "description": "A DETR concept with spatial encodings, learned object queries, class/box set prediction and bipartite matching supervision.",
      "caption": "Learned queries attend to encoded image features; bipartite matching assigns predictions to target objects.",
      "sources": [
        "https://arxiv.org/abs/2005.12872"
      ],
      "assumptions": [
        "Conceptual schematic; dimensions and details vary by implementation."
      ],
      "tags": [
        "detection",
        "detr",
        "set-prediction"
      ],
      "nodes": 11,
      "edges": 10,
      "source_file": "vision-detr.tex",
      "width_cm": 18,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-detr.json",
      "svg": "gallery/atlas/vision-detr.svg",
      "png": "gallery/atlas/vision-detr.png",
      "pdf": "gallery/atlas/vision-detr.pdf",
      "tex": "gallery/atlas/vision-detr.tex"
    },
    {
      "id": "vision-two-stage-detector",
      "title": "Two-stage detection: propose regions, then recognize them",
      "family": "vision",
      "description": "A Faster R-CNN concept with shared image features, proposal generation/selection, RoI pooling, and two prediction branches.",
      "caption": "The region proposal network and RoI feature extraction share a backbone feature map.",
      "sources": [
        "https://arxiv.org/abs/1506.01497"
      ],
      "assumptions": [
        "RoI pooling follows the original Faster R-CNN concept; implementation-specific backbone and anchor counts are omitted."
      ],
      "tags": [
        "detection",
        "faster-rcnn",
        "proposals"
      ],
      "nodes": 11,
      "edges": 11,
      "source_file": "vision-two-stage-detector.tex",
      "width_cm": 18,
      "height_cm": 9.5,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-two-stage-detector.json",
      "svg": "gallery/atlas/vision-two-stage-detector.svg",
      "png": "gallery/atlas/vision-two-stage-detector.png",
      "pdf": "gallery/atlas/vision-two-stage-detector.pdf",
      "tex": "gallery/atlas/vision-two-stage-detector.tex"
    },
    {
      "id": "vision-one-stage-detector",
      "title": "One-stage dense detection: predictions at every pyramid level",
      "family": "vision",
      "description": "A RetinaNet concept with per-level shared dense heads and separate classification/focal and box-regression objectives.",
      "caption": "Shared classification and box subnets are applied separately to each feature level; focal loss addresses class imbalance.",
      "sources": [
        "https://arxiv.org/abs/1708.02002"
      ],
      "assumptions": [
        "Three pyramid levels illustrate the repeated mapping; they are not the complete RetinaNet scale configuration."
      ],
      "tags": [
        "detection",
        "retinanet",
        "focal-loss"
      ],
      "nodes": 8,
      "edges": 11,
      "source_file": "vision-one-stage-detector.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-one-stage-detector.json",
      "svg": "gallery/atlas/vision-one-stage-detector.svg",
      "png": "gallery/atlas/vision-one-stage-detector.png",
      "pdf": "gallery/atlas/vision-one-stage-detector.pdf",
      "tex": "gallery/atlas/vision-one-stage-detector.tex"
    },
    {
      "id": "vision-siamese-similarity",
      "title": "Siamese image similarity: compare two shared representations",
      "family": "vision",
      "description": "A Siamese image pair architecture with tied CNN weights, absolute feature difference, learned similarity and pair supervision.",
      "caption": "Both images pass through the same encoder; a learned comparison maps their absolute feature difference to similarity.",
      "sources": [
        "https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf"
      ],
      "assumptions": [
        "Conceptual schematic; dimensions and details vary by implementation."
      ],
      "tags": [
        "siamese",
        "metric-learning",
        "similarity"
      ],
      "nodes": 11,
      "edges": 11,
      "source_file": "vision-siamese-similarity.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-siamese-similarity.json",
      "svg": "gallery/atlas/vision-siamese-similarity.svg",
      "png": "gallery/atlas/vision-siamese-similarity.png",
      "pdf": "gallery/atlas/vision-siamese-similarity.pdf",
      "tex": "gallery/atlas/vision-siamese-similarity.tex"
    },
    {
      "id": "vision-depthwise-separable",
      "title": "Depthwise separable convolution: split spatial and channel mixing",
      "family": "vision",
      "description": "A channel-explicit depthwise convolution followed by cross-channel pointwise mixing and its parameter expression.",
      "caption": "Depthwise filters act independently on input channels; pointwise filters combine the resulting channels.",
      "sources": [
        "https://arxiv.org/abs/1704.04861"
      ],
      "assumptions": [
        "Three input channels are drawn as an illustration; channel counts and spatial sizes are symbolic."
      ],
      "tags": [
        "cnn",
        "mobilenet",
        "depthwise"
      ],
      "nodes": 11,
      "edges": 10,
      "source_file": "vision-depthwise-separable.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-depthwise-separable.json",
      "svg": "gallery/atlas/vision-depthwise-separable.svg",
      "png": "gallery/atlas/vision-depthwise-separable.png",
      "pdf": "gallery/atlas/vision-depthwise-separable.pdf",
      "tex": "gallery/atlas/vision-depthwise-separable.tex"
    },
    {
      "id": "vision-atrous-segmentation",
      "title": "Atrous spatial pyramid pooling: parallel scales of context",
      "family": "vision",
      "description": "A DeepLabv3-style ASPP context module with three atrous branches, a 1x1 branch, image pooling, fusion and resizing.",
      "caption": "Dilated convolutions and image-level pooling gather complementary context before concatenation and dense prediction.",
      "sources": [
        "https://arxiv.org/abs/1706.05587"
      ],
      "assumptions": [
        "Dilation rates are symbolic and depend on output stride and implementation."
      ],
      "tags": [
        "segmentation",
        "deeplab",
        "aspp",
        "dilated-convolution"
      ],
      "nodes": 11,
      "edges": 14,
      "source_file": "vision-atrous-segmentation.tex",
      "width_cm": 18,
      "height_cm": 10.5,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-atrous-segmentation.json",
      "svg": "gallery/atlas/vision-atrous-segmentation.svg",
      "png": "gallery/atlas/vision-atrous-segmentation.png",
      "pdf": "gallery/atlas/vision-atrous-segmentation.pdf",
      "tex": "gallery/atlas/vision-atrous-segmentation.tex"
    },
    {
      "id": "vision-patch-merging",
      "title": "Hierarchical patch merging: trade resolution for channels",
      "family": "vision",
      "description": "A hierarchical patch merging operation with a 2x2 neighborhood grid, 4C concatenation, normalization and 2C projection.",
      "caption": "Four neighboring tokens are concatenated, normalized, and projected into one token at the next stage.",
      "sources": [
        "https://arxiv.org/abs/2103.14030"
      ],
      "assumptions": [
        "H and W are even. The 4C-to-2C projection follows the original Swin patch-merging formulation."
      ],
      "tags": [
        "transformer",
        "swin",
        "patch-merging",
        "hierarchy"
      ],
      "nodes": 9,
      "edges": 7,
      "source_file": "vision-patch-merging.tex",
      "width_cm": 18,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/vision-patch-merging.json",
      "svg": "gallery/atlas/vision-patch-merging.svg",
      "png": "gallery/atlas/vision-patch-merging.png",
      "pdf": "gallery/atlas/vision-patch-merging.pdf",
      "tex": "gallery/atlas/vision-patch-merging.tex"
    },
    {
      "id": "text_01_token_embedding",
      "title": "Subword tokenization and embedding lookup",
      "family": "text",
      "description": "Subword segmentation, vocabulary identifiers, learned embedding lookup, and additive position vectors.",
      "caption": "Token boundaries and identifiers are illustrative; a learned table maps each token to a model-width vector.",
      "sources": [
        "https://arxiv.org/abs/1508.07909",
        "https://arxiv.org/abs/1706.03762"
      ],
      "assumptions": [
        "Illustrative segmentation is not the output of a particular trained tokenizer.",
        "Additive position vectors are a chosen example; RoPE is a different mechanism."
      ],
      "tags": [
        "tokenization",
        "embedding",
        "subword"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "text_01_token_embedding.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_01_token_embedding.json",
      "svg": "gallery/atlas/text_01_token_embedding.svg",
      "png": "gallery/atlas/text_01_token_embedding.png",
      "pdf": "gallery/atlas/text_01_token_embedding.pdf",
      "tex": "gallery/atlas/text_01_token_embedding.tex"
    },
    {
      "id": "text_02_causal_decoder",
      "title": "Causal decoder with pre-normalized residual blocks",
      "family": "text",
      "description": "Pre-normalized causal decoder block with two correctly originated identity residuals and a language-model readout.",
      "caption": "Each residual starts before its normalization; the block repeats with distinct parameters across layers.",
      "sources": [
        "https://arxiv.org/abs/1706.03762",
        "https://arxiv.org/abs/2002.04745"
      ],
      "assumptions": [
        "Conceptual pre-normalized decoder; no particular model's layer count, norm type, or position method is implied."
      ],
      "tags": [
        "decoder",
        "causal",
        "residual",
        "pre-norm"
      ],
      "nodes": 11,
      "edges": 11,
      "source_file": "text_02_causal_decoder.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_02_causal_decoder.json",
      "svg": "gallery/atlas/text_02_causal_decoder.svg",
      "png": "gallery/atlas/text_02_causal_decoder.png",
      "pdf": "gallery/atlas/text_02_causal_decoder.pdf",
      "tex": "gallery/atlas/text_02_causal_decoder.tex"
    },
    {
      "id": "text_03_encoder_decoder",
      "title": "Encoder--decoder Transformer",
      "family": "text",
      "description": "Paired encoder and autoregressive decoder stacks with source memory connected only to decoder cross-attention keys and values.",
      "caption": "Encoder memory supplies keys and values to every decoder cross-attention layer.",
      "sources": [
        "https://arxiv.org/abs/1706.03762"
      ],
      "assumptions": [
        "Original post-norm ordering is summarized in labels; residual wires are not expanded.",
        "Layer repeat counts are symbolic."
      ],
      "tags": [
        "transformer",
        "encoder-decoder",
        "cross-attention"
      ],
      "nodes": 12,
      "edges": 10,
      "source_file": "text_03_encoder_decoder.tex",
      "width_cm": 16,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_03_encoder_decoder.json",
      "svg": "gallery/atlas/text_03_encoder_decoder.svg",
      "png": "gallery/atlas/text_03_encoder_decoder.png",
      "pdf": "gallery/atlas/text_03_encoder_decoder.pdf",
      "tex": "gallery/atlas/text_03_encoder_decoder.tex"
    },
    {
      "id": "text_04_scaled_self_attention",
      "title": "Scaled dot-product self-attention",
      "family": "text",
      "description": "Self-attention factorization with symbolic query/key/value shapes, correct attention axes, and an illustrative causal mask.",
      "caption": "Rows are queries, columns are keys; normalization runs over allowed key positions for each query.",
      "sources": [
        "https://arxiv.org/abs/1706.03762"
      ],
      "assumptions": [
        "Single attention head; the batch axis is omitted.",
        "Causal masking is the selected example; full self-attention omits that mask."
      ],
      "tags": [
        "attention",
        "mask",
        "tensor-shapes"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "text_04_scaled_self_attention.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_04_scaled_self_attention.json",
      "svg": "gallery/atlas/text_04_scaled_self_attention.svg",
      "png": "gallery/atlas/text_04_scaled_self_attention.png",
      "pdf": "gallery/atlas/text_04_scaled_self_attention.pdf",
      "tex": "gallery/atlas/text_04_scaled_self_attention.tex"
    },
    {
      "id": "text_05_cross_attention",
      "title": "Cross-attention with a query-stream residual",
      "family": "text",
      "description": "Cross-attention with rectangular T-by-S weights and a residual that originates from the decoder query stream.",
      "caption": "The output has the query length; the identity path starts at the decoder state, before query projection.",
      "sources": [
        "https://arxiv.org/abs/1706.03762"
      ],
      "assumptions": [
        "Single head shown; output projection restores the query stream width d.",
        "Normalization wrapper omitted to isolate attention and residual origin."
      ],
      "tags": [
        "cross-attention",
        "residual",
        "query-memory"
      ],
      "nodes": 8,
      "edges": 9,
      "source_file": "text_05_cross_attention.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_05_cross_attention.json",
      "svg": "gallery/atlas/text_05_cross_attention.svg",
      "png": "gallery/atlas/text_05_cross_attention.png",
      "pdf": "gallery/atlas/text_05_cross_attention.pdf",
      "tex": "gallery/atlas/text_05_cross_attention.tex"
    },
    {
      "id": "text_06_multi_head_attention",
      "title": "Multi-head attention: separate projections, joined outputs",
      "family": "text",
      "description": "Parallel head-specific query/key/value projections and attention maps followed by feature concatenation and output projection.",
      "caption": "Each head computes its own attention map; concatenation precedes the shared output projection.",
      "sources": [
        "https://arxiv.org/abs/1706.03762"
      ],
      "assumptions": [
        "Representative heads 1, i, and h stand for an arbitrary number of heads.",
        "Feature widths are symbolic and need not be assigned numeric values."
      ],
      "tags": [
        "multi-head",
        "attention",
        "parallel-branches"
      ],
      "nodes": 13,
      "edges": 13,
      "source_file": "text_06_multi_head_attention.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_06_multi_head_attention.json",
      "svg": "gallery/atlas/text_06_multi_head_attention.svg",
      "png": "gallery/atlas/text_06_multi_head_attention.png",
      "pdf": "gallery/atlas/text_06_multi_head_attention.pdf",
      "tex": "gallery/atlas/text_06_multi_head_attention.tex"
    },
    {
      "id": "text_07_grouped_query_attention",
      "title": "Grouped-query attention: several queries share keys and values",
      "family": "text",
      "description": "Grouped-query attention shows explicitly shared K/V tensors within groups and distinct query-head attention computations.",
      "caption": "A query head uses the key/value head of its assigned group; head outputs are then concatenated.",
      "sources": [
        "https://arxiv.org/abs/2305.13245"
      ],
      "assumptions": [
        "Two representative groups with two representative queries each are a schematic partition, not a fixed model configuration.",
        "All projections are from the same sequence X."
      ],
      "tags": [
        "GQA",
        "attention",
        "shared-KV"
      ],
      "nodes": 11,
      "edges": 8,
      "source_file": "text_07_grouped_query_attention.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_07_grouped_query_attention.json",
      "svg": "gallery/atlas/text_07_grouped_query_attention.svg",
      "png": "gallery/atlas/text_07_grouped_query_attention.png",
      "pdf": "gallery/atlas/text_07_grouped_query_attention.pdf",
      "tex": "gallery/atlas/text_07_grouped_query_attention.tex"
    },
    {
      "id": "text_08_kv_cache",
      "title": "Autoregressive decoding with a per-layer KV cache",
      "family": "text",
      "description": "Single-step autoregressive attention with separate current Q and new K/V, explicit cache append, and cache read.",
      "caption": "Only the current query is evaluated against the enlarged cache; past keys and values are reused.",
      "sources": [
        "https://arxiv.org/abs/1911.02150",
        "https://arxiv.org/abs/1706.03762"
      ],
      "assumptions": [
        "One layer and representative head shown; implementations may pack or page the cache differently.",
        "Projection and attention normalization wrappers omitted."
      ],
      "tags": [
        "KV-cache",
        "decoding",
        "storage"
      ],
      "nodes": 10,
      "edges": 9,
      "source_file": "text_08_kv_cache.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_08_kv_cache.json",
      "svg": "gallery/atlas/text_08_kv_cache.svg",
      "png": "gallery/atlas/text_08_kv_cache.png",
      "pdf": "gallery/atlas/text_08_kv_cache.pdf",
      "tex": "gallery/atlas/text_08_kv_cache.tex"
    },
    {
      "id": "text_09_rotary_positions",
      "title": "Rotary positions act on query and key feature pairs",
      "family": "text",
      "description": "Separate position-indexed rotations of query and key feature pairs and their relative-position dot-product identity.",
      "caption": "Position rotations change query--key dot products through relative position; values follow their ordinary projection path.",
      "sources": [
        "https://arxiv.org/abs/2104.09864"
      ],
      "assumptions": [
        "Column-vector convention is used in this figure; model-wide row-vector notation is equivalent after transposition.",
        "Pair-specific frequencies theta_a are symbolic; value rotation is not shown."
      ],
      "tags": [
        "RoPE",
        "position",
        "rotation"
      ],
      "nodes": 9,
      "edges": 6,
      "source_file": "text_09_rotary_positions.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_09_rotary_positions.json",
      "svg": "gallery/atlas/text_09_rotary_positions.svg",
      "png": "gallery/atlas/text_09_rotary_positions.png",
      "pdf": "gallery/atlas/text_09_rotary_positions.pdf",
      "tex": "gallery/atlas/text_09_rotary_positions.tex"
    },
    {
      "id": "text_10_swiglu_ffn",
      "title": "SwiGLU feed-forward network",
      "family": "text",
      "description": "Two-branch SwiGLU feed-forward network with SiLU gate, elementwise multiplication, and output projection.",
      "caption": "A SiLU-transformed gate modulates the parallel up-projection before the down-projection restores model width.",
      "sources": [
        "https://arxiv.org/abs/2002.05202"
      ],
      "assumptions": [
        "Biases and residual/norm wrappers are omitted to isolate the feed-forward transformation.",
        "The intermediate width d_f is symbolic."
      ],
      "tags": [
        "SwiGLU",
        "FFN",
        "gating"
      ],
      "nodes": 8,
      "edges": 7,
      "source_file": "text_10_swiglu_ffn.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_10_swiglu_ffn.json",
      "svg": "gallery/atlas/text_10_swiglu_ffn.svg",
      "png": "gallery/atlas/text_10_swiglu_ffn.png",
      "pdf": "gallery/atlas/text_10_swiglu_ffn.pdf",
      "tex": "gallery/atlas/text_10_swiglu_ffn.tex"
    },
    {
      "id": "text_11_sparse_moe",
      "title": "Sparse mixture-of-experts decoder and routing detail",
      "family": "text",
      "description": "Per-token sparse expert selection, dispatch to active experts, and gate-weighted aggregation, with an explicitly inactive expert.",
      "caption": "The router selects experts per token; only selected experts receive data and contribute weighted outputs.",
      "sources": [
        "https://arxiv.org/abs/1701.06538"
      ],
      "assumptions": [
        "The two selected experts are illustrative, not a universal routing configuration.",
        "Capacity limits, auxiliary losses, and distributed expert placement are outside this layer-level view."
      ],
      "tags": [
        "MoE",
        "routing",
        "sparse"
      ],
      "nodes": 12,
      "edges": 12,
      "source_file": "text_11_sparse_moe.tex",
      "width_cm": 16,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_11_sparse_moe.json",
      "svg": "gallery/atlas/text_11_sparse_moe.svg",
      "png": "gallery/atlas/text_11_sparse_moe.png",
      "pdf": "gallery/atlas/text_11_sparse_moe.pdf",
      "tex": "gallery/atlas/text_11_sparse_moe.tex"
    },
    {
      "id": "text_12_lora",
      "title": "LoRA: a frozen dense path plus a trainable low-rank update",
      "family": "text",
      "description": "Low-rank trainable matrices A and B operate in parallel with a frozen base layer, then add at the output.",
      "caption": "The adapter branch has a rank bottleneck; its scaled output adds to the frozen base-layer output.",
      "sources": [
        "https://arxiv.org/abs/2106.09685"
      ],
      "assumptions": [
        "Column-vector convention; A maps input width to rank r and B maps r to output width.",
        "The common alpha/r scaling convention is shown; bias and optimizer details are omitted."
      ],
      "tags": [
        "LoRA",
        "adapter",
        "low-rank"
      ],
      "nodes": 8,
      "edges": 7,
      "source_file": "text_12_lora.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_12_lora.json",
      "svg": "gallery/atlas/text_12_lora.svg",
      "png": "gallery/atlas/text_12_lora.png",
      "pdf": "gallery/atlas/text_12_lora.pdf",
      "tex": "gallery/atlas/text_12_lora.tex"
    },
    {
      "id": "text_13_qlora",
      "title": "QLoRA: quantized base storage, higher-precision computation",
      "family": "text",
      "description": "Conceptual QLoRA base-weight storage and dequantization path, alongside a trainable low-rank adapter branch.",
      "caption": "Quantized base parameters stay frozen; adapters receive parameter updates while gradients can pass through the computation.",
      "sources": [
        "https://arxiv.org/abs/2305.14314"
      ],
      "assumptions": [
        "Quantizer, storage bit width, compute dtype, and optimizer are unspecified in this conceptual view.",
        "Frozen parameters do not mean that the base matmul blocks gradients to its inputs."
      ],
      "tags": [
        "QLoRA",
        "quantization",
        "adapter"
      ],
      "nodes": 10,
      "edges": 9,
      "source_file": "text_13_qlora.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_13_qlora.json",
      "svg": "gallery/atlas/text_13_qlora.svg",
      "png": "gallery/atlas/text_13_qlora.png",
      "pdf": "gallery/atlas/text_13_qlora.pdf",
      "tex": "gallery/atlas/text_13_qlora.tex"
    },
    {
      "id": "text_14_beam_search",
      "title": "Beam search expands prefixes, then prunes globally",
      "family": "text",
      "description": "A prefix tree with local candidate expansion and global top-B pruning, including a visibly discarded branch.",
      "caption": "An illustrative beam of two prefixes survives each step; every expansion accumulates its parent prefix score.",
      "sources": [
        "https://arxiv.org/abs/1409.3215"
      ],
      "assumptions": [
        "B=2 is an illustrative search setting, not an architecture claim.",
        "The score is unnormalized cumulative log probability; length penalties and EOS bookkeeping are omitted."
      ],
      "tags": [
        "beam-search",
        "decoding",
        "tree"
      ],
      "nodes": 12,
      "edges": 13,
      "source_file": "text_14_beam_search.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_14_beam_search.json",
      "svg": "gallery/atlas/text_14_beam_search.svg",
      "png": "gallery/atlas/text_14_beam_search.png",
      "pdf": "gallery/atlas/text_14_beam_search.pdf",
      "tex": "gallery/atlas/text_14_beam_search.tex"
    },
    {
      "id": "text_15_speculative_decoding",
      "title": "Speculative decoding: propose, verify, accept a prefix",
      "family": "text",
      "description": "Speculative sampling separates draft proposal, target verification, prefix acceptance, corrected rejection sampling, and next-round feedback.",
      "caption": "Draft proposals are sequential; the target scores their conditional positions together, then corrected sampling preserves its distribution.",
      "sources": [
        "https://arxiv.org/abs/2211.17192"
      ],
      "assumptions": [
        "This is the exact sampling form with normalized positive-part correction, rather than a greedy matching variant.",
        "If all proposals are accepted, the extra token is sampled from p_(gamma+1)."
      ],
      "tags": [
        "speculative",
        "decoding",
        "verification"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "text_15_speculative_decoding.tex",
      "width_cm": 16,
      "height_cm": 9.5,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_15_speculative_decoding.json",
      "svg": "gallery/atlas/text_15_speculative_decoding.svg",
      "png": "gallery/atlas/text_15_speculative_decoding.png",
      "pdf": "gallery/atlas/text_15_speculative_decoding.pdf",
      "tex": "gallery/atlas/text_15_speculative_decoding.tex"
    },
    {
      "id": "text_16_selective_state_space",
      "title": "Selective state-space recurrence",
      "family": "text",
      "description": "An unrolled input-selective state-space core with input-dependent discretization and readout parameters, plus a state carried across time.",
      "caption": "Input-dependent selection changes the state transition across time; this view isolates the recurrence core.",
      "sources": [
        "https://arxiv.org/abs/2312.00752"
      ],
      "assumptions": [
        "Channel mixing, convolution, gating, and output skip terms are omitted to isolate the selective recurrence.",
        "Bars denote discretized transition/input parameters; the discretization scheme for B is not fixed in the drawing."
      ],
      "tags": [
        "SSM",
        "Mamba",
        "recurrence",
        "selectivity"
      ],
      "nodes": 13,
      "edges": 17,
      "source_file": "text_16_selective_state_space.tex",
      "width_cm": 16,
      "height_cm": 9.5,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_16_selective_state_space.json",
      "svg": "gallery/atlas/text_16_selective_state_space.svg",
      "png": "gallery/atlas/text_16_selective_state_space.png",
      "pdf": "gallery/atlas/text_16_selective_state_space.pdf",
      "tex": "gallery/atlas/text_16_selective_state_space.tex"
    },
    {
      "id": "text_17_hybrid_attention_ssm",
      "title": "Hybrid sequence layer: recurrence and local attention",
      "family": "text",
      "description": "Conceptual hybrid layer contrasts compressed recurrent state with a finite explicit KV attention window, with per-step updates of each memory.",
      "caption": "Recurrent state summarizes the past; the local attention cache retains explicit recent key/value positions.",
      "sources": [
        "https://arxiv.org/abs/2402.19427",
        "https://arxiv.org/abs/2312.00752"
      ],
      "assumptions": [
        "Conceptual hybrid; this is not an exact reproduction of Griffin or any specified layer schedule.",
        "The window width w is symbolic; residual/norm wrappers are omitted."
      ],
      "tags": [
        "hybrid",
        "SSM",
        "local-attention",
        "memory"
      ],
      "nodes": 10,
      "edges": 10,
      "source_file": "text_17_hybrid_attention_ssm.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_17_hybrid_attention_ssm.json",
      "svg": "gallery/atlas/text_17_hybrid_attention_ssm.svg",
      "png": "gallery/atlas/text_17_hybrid_attention_ssm.png",
      "pdf": "gallery/atlas/text_17_hybrid_attention_ssm.pdf",
      "tex": "gallery/atlas/text_17_hybrid_attention_ssm.tex"
    },
    {
      "id": "text_18_rnn_seq2seq",
      "title": "Recurrent sequence-to-sequence model",
      "family": "text",
      "description": "Unrolled LSTM encoder-decoder model with final-state initialization of the decoder and explicitly shifted target inputs.",
      "caption": "The encoder's final hidden and cell states initialize the decoder; target inputs are shifted by one position.",
      "sources": [
        "https://arxiv.org/abs/1409.3215"
      ],
      "assumptions": [
        "Representative source positions and three illustrative target steps are drawn.",
        "The source order is not prescribed; this schematic isolates the fixed-summary encoder-decoder topology."
      ],
      "tags": [
        "RNN",
        "LSTM",
        "seq2seq"
      ],
      "nodes": 18,
      "edges": 14,
      "source_file": "text_18_rnn_seq2seq.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_18_rnn_seq2seq.json",
      "svg": "gallery/atlas/text_18_rnn_seq2seq.svg",
      "png": "gallery/atlas/text_18_rnn_seq2seq.png",
      "pdf": "gallery/atlas/text_18_rnn_seq2seq.pdf",
      "tex": "gallery/atlas/text_18_rnn_seq2seq.tex"
    },
    {
      "id": "text_19_bidirectional_lstm",
      "title": "Bidirectional LSTM with aligned token readouts",
      "family": "text",
      "description": "Two oppositely directed LSTM state chains share aligned inputs and feed per-position concatenation/readout functions.",
      "caption": "Forward and backward recurrences run in opposite directions; each readout combines states aligned to the same input.",
      "sources": [
        "https://www.cs.toronto.edu/~graves/nn_2005.pdf"
      ],
      "assumptions": [
        "Representative positions are drawn; ellipsis edges summarize intermediate steps.",
        "Cell states and LSTM gates are contained inside the LSTM blocks; this is a noncausal sequence encoder."
      ],
      "tags": [
        "bidirectional",
        "LSTM",
        "sequence-labeling"
      ],
      "nodes": 16,
      "edges": 22,
      "source_file": "text_19_bidirectional_lstm.tex",
      "width_cm": 16,
      "height_cm": 10,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_19_bidirectional_lstm.json",
      "svg": "gallery/atlas/text_19_bidirectional_lstm.svg",
      "png": "gallery/atlas/text_19_bidirectional_lstm.png",
      "pdf": "gallery/atlas/text_19_bidirectional_lstm.pdf",
      "tex": "gallery/atlas/text_19_bidirectional_lstm.tex"
    },
    {
      "id": "text_20_cross_encoder_reranker",
      "title": "Cross-encoder reranker jointly encodes query and document",
      "family": "text",
      "description": "BERT-style pair packing, joint bidirectional encoding, classification-state extraction, and a document-query relevance head.",
      "caption": "A single encoder allows query--document token interactions; the classification position supplies a relevance score.",
      "sources": [
        "https://arxiv.org/abs/1901.04085",
        "https://arxiv.org/abs/1810.04805"
      ],
      "assumptions": [
        "Special-token count m+n+3 follows the explicitly shown two-segment BERT packing convention.",
        "The relevance-head activation and loss are task choices; the displayed score is a pre-activation scalar."
      ],
      "tags": [
        "reranking",
        "cross-encoder",
        "BERT"
      ],
      "nodes": 8,
      "edges": 7,
      "source_file": "text_20_cross_encoder_reranker.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/text_20_cross_encoder_reranker.json",
      "svg": "gallery/atlas/text_20_cross_encoder_reranker.svg",
      "png": "gallery/atlas/text_20_cross_encoder_reranker.png",
      "pdf": "gallery/atlas/text_20_cross_encoder_reranker.pdf",
      "tex": "gallery/atlas/text_20_cross_encoder_reranker.tex"
    },
    {
      "id": "audio-01-waveform-framing",
      "title": "Waveform framing and windowing",
      "family": "audio",
      "description": "Overlapping sampled frames and a shared window in local frame coordinates.",
      "caption": "Overlapping slices preserve local time structure before spectral analysis.",
      "sources": [
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Displayed waveforms and windows are illustrative; no sampling rate or frame length is asserted."
      ],
      "tags": [
        "waveform",
        "framing",
        "window"
      ],
      "nodes": 3,
      "edges": 0,
      "source_file": "audio-01-waveform-framing.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-01-waveform-framing.json",
      "svg": "gallery/atlas/audio-01-waveform-framing.svg",
      "png": "gallery/atlas/audio-01-waveform-framing.png",
      "pdf": "gallery/atlas/audio-01-waveform-framing.pdf",
      "tex": "gallery/atlas/audio-01-waveform-framing.tex"
    },
    {
      "id": "audio-02-stft-spectrogram",
      "title": "Short-time Fourier transform",
      "family": "audio",
      "description": "Windowed Fourier analysis maps time samples into a spectrogram grid.",
      "caption": "One DFT per windowed frame becomes one column in a time--frequency array.",
      "sources": [
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The energy grid is synthetic. The exponent p may be 1 (magnitude) or 2 (power)."
      ],
      "tags": [
        "STFT",
        "spectrogram",
        "Fourier"
      ],
      "nodes": 3,
      "edges": 2,
      "source_file": "audio-02-stft-spectrogram.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-02-stft-spectrogram.json",
      "svg": "gallery/atlas/audio-02-stft-spectrogram.svg",
      "png": "gallery/atlas/audio-02-stft-spectrogram.png",
      "pdf": "gallery/atlas/audio-02-stft-spectrogram.pdf",
      "tex": "gallery/atlas/audio-02-stft-spectrogram.tex"
    },
    {
      "id": "audio-03-spectrogram-cnn",
      "title": "Spectrogram convolutional classifier",
      "family": "audio",
      "description": "A conceptual PANNs-inspired spectrogram CNN for multilabel audio tagging.",
      "caption": "Local time--frequency filters feed progressively pooled features and clip-level tags.",
      "sources": [
        "https://arxiv.org/abs/1912.10211"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "This is a generic spectrogram CNN, not the exact CNN14 layer inventory. Tensor depths are illustrative."
      ],
      "tags": [
        "CNN",
        "audio tagging",
        "receptive field"
      ],
      "nodes": 6,
      "edges": 5,
      "source_file": "audio-03-spectrogram-cnn.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-03-spectrogram-cnn.json",
      "svg": "gallery/atlas/audio-03-spectrogram-cnn.svg",
      "png": "gallery/atlas/audio-03-spectrogram-cnn.png",
      "pdf": "gallery/atlas/audio-03-spectrogram-cnn.pdf",
      "tex": "gallery/atlas/audio-03-spectrogram-cnn.tex"
    },
    {
      "id": "audio-04-ctc-recognition",
      "title": "CTC speech recognition",
      "family": "audio",
      "description": "Framewise CTC probabilities, an explicit repeated-and-blank path, and the collapse map.",
      "caption": "CTC sums frame paths during training; a collapse map removes repeats and blank symbols.",
      "sources": [
        "https://www.cs.toronto.edu/~graves/icml_2006.pdf"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The displayed path is illustrative; recognition may use beam search rather than greedy decoding."
      ],
      "tags": [
        "ASR",
        "CTC",
        "alignment"
      ],
      "nodes": 6,
      "edges": 4,
      "source_file": "audio-04-ctc-recognition.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-04-ctc-recognition.json",
      "svg": "gallery/atlas/audio-04-ctc-recognition.svg",
      "png": "gallery/atlas/audio-04-ctc-recognition.png",
      "pdf": "gallery/atlas/audio-04-ctc-recognition.pdf",
      "tex": "gallery/atlas/audio-04-ctc-recognition.tex"
    },
    {
      "id": "audio-05-rnnt-transducer",
      "title": "RNN-T transducer",
      "family": "audio",
      "description": "Acoustic encoder and label-prefix predictor meet at a joint distribution over blank and labels.",
      "caption": "The joint distribution depends on both acoustic time and the emitted-label prefix.",
      "sources": [
        "https://arxiv.org/abs/1211.3711"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The small lattice is illustrative. Blank transitions move right and label transitions move upward."
      ],
      "tags": [
        "ASR",
        "RNN-T",
        "lattice"
      ],
      "nodes": 6,
      "edges": 5,
      "source_file": "audio-05-rnnt-transducer.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-05-rnnt-transducer.json",
      "svg": "gallery/atlas/audio-05-rnnt-transducer.svg",
      "png": "gallery/atlas/audio-05-rnnt-transducer.png",
      "pdf": "gallery/atlas/audio-05-rnnt-transducer.pdf",
      "tex": "gallery/atlas/audio-05-rnnt-transducer.tex"
    },
    {
      "id": "audio-06-attention-asr",
      "title": "Attention-based speech recognition",
      "family": "audio",
      "description": "A LAS-inspired listener, attention memory, and recurrent character speller.",
      "caption": "A listener encodes audio; the speller queries its memory for each output character.",
      "sources": [
        "https://arxiv.org/abs/1508.01211"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The listener is conceptual; its pyramid depth and temporal reduction factor are omitted."
      ],
      "tags": [
        "ASR",
        "attention",
        "LAS"
      ],
      "nodes": 8,
      "edges": 9,
      "source_file": "audio-06-attention-asr.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-06-attention-asr.json",
      "svg": "gallery/atlas/audio-06-attention-asr.svg",
      "png": "gallery/atlas/audio-06-attention-asr.png",
      "pdf": "gallery/atlas/audio-06-attention-asr.pdf",
      "tex": "gallery/atlas/audio-06-attention-asr.tex"
    },
    {
      "id": "audio-07-conformer-block",
      "title": "Conformer encoder block",
      "family": "audio",
      "description": "A Conformer block with explicit residual origins, half-step FFNs, and expanded convolution module.",
      "caption": "Macaron feed-forward halves surround global self-attention and a local convolution module.",
      "sources": [
        "https://arxiv.org/abs/2005.08100"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Pre-normalization is implicit in the attention and FFN boxes. The convolution callout omits dropout."
      ],
      "tags": [
        "Conformer",
        "residual",
        "convolution"
      ],
      "nodes": 16,
      "edges": 15,
      "source_file": "audio-07-conformer-block.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-07-conformer-block.json",
      "svg": "gallery/atlas/audio-07-conformer-block.svg",
      "png": "gallery/atlas/audio-07-conformer-block.png",
      "pdf": "gallery/atlas/audio-07-conformer-block.pdf",
      "tex": "gallery/atlas/audio-07-conformer-block.tex"
    },
    {
      "id": "audio-08-whisper-encoder-decoder",
      "title": "Whisper-style encoder--decoder",
      "family": "audio",
      "description": "A conceptual Whisper-style audio encoder and autoregressive task-conditioned text decoder.",
      "caption": "Audio memory conditions a causal text decoder; task tokens select the decoding objective.",
      "sources": [
        "https://cdn.openai.com/papers/whisper.pdf"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "This is an architecture overview. Exact model sizes and positional-embedding choices are omitted."
      ],
      "tags": [
        "Whisper",
        "ASR",
        "encoder-decoder"
      ],
      "nodes": 8,
      "edges": 8,
      "source_file": "audio-08-whisper-encoder-decoder.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-08-whisper-encoder-decoder.json",
      "svg": "gallery/atlas/audio-08-whisper-encoder-decoder.svg",
      "png": "gallery/atlas/audio-08-whisper-encoder-decoder.png",
      "pdf": "gallery/atlas/audio-08-whisper-encoder-decoder.pdf",
      "tex": "gallery/atlas/audio-08-whisper-encoder-decoder.tex"
    },
    {
      "id": "audio-09-wav2vec2-pretraining",
      "title": "wav2vec 2.0 pretraining",
      "family": "audio",
      "description": "Latent masking, contextual representations, product-quantized contrastive targets, and diversity regularization.",
      "caption": "Latent span masking feeds contextual prediction; an unmasked branch supplies learned quantized targets.",
      "sources": [
        "https://arxiv.org/abs/2006.11477"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Only the pretraining graph is shown. Codebook counts and distractor-sampling details are omitted."
      ],
      "tags": [
        "self-supervised",
        "wav2vec2",
        "contrastive"
      ],
      "nodes": 8,
      "edges": 8,
      "source_file": "audio-09-wav2vec2-pretraining.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-09-wav2vec2-pretraining.json",
      "svg": "gallery/atlas/audio-09-wav2vec2-pretraining.svg",
      "png": "gallery/atlas/audio-09-wav2vec2-pretraining.png",
      "pdf": "gallery/atlas/audio-09-wav2vec2-pretraining.pdf",
      "tex": "gallery/atlas/audio-09-wav2vec2-pretraining.tex"
    },
    {
      "id": "audio-10-hubert-pretraining",
      "title": "HuBERT masked-unit pretraining",
      "family": "audio",
      "description": "Offline discrete-unit clustering and masked student prediction with optional iterative reclustering.",
      "caption": "An offline clustering teacher supplies discrete units; the student predicts masked units from context.",
      "sources": [
        "https://arxiv.org/abs/2106.07447"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The teacher feature type changes across training iterations; one generic offline lane represents these choices."
      ],
      "tags": [
        "HuBERT",
        "self-supervised",
        "masked prediction"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "audio-10-hubert-pretraining.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-10-hubert-pretraining.json",
      "svg": "gallery/atlas/audio-10-hubert-pretraining.svg",
      "png": "gallery/atlas/audio-10-hubert-pretraining.png",
      "pdf": "gallery/atlas/audio-10-hubert-pretraining.pdf",
      "tex": "gallery/atlas/audio-10-hubert-pretraining.tex"
    },
    {
      "id": "audio-11-speaker-embedding",
      "title": "Speaker embedding with statistics pooling",
      "family": "audio",
      "description": "An x-vector-style TDNN, temporal statistics pooling, segment embedding, and scoring backend.",
      "caption": "Frame-level representations become a fixed-size segment embedding through mean and standard-deviation pooling.",
      "sources": [
        "https://www.danielpovey.com/files/2018_icassp_xvectors.pdf"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The diagram does not prescribe a particular scoring backend. The classifier is training-only."
      ],
      "tags": [
        "speaker recognition",
        "x-vector",
        "statistics pooling"
      ],
      "nodes": 10,
      "edges": 10,
      "source_file": "audio-11-speaker-embedding.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-11-speaker-embedding.json",
      "svg": "gallery/atlas/audio-11-speaker-embedding.svg",
      "png": "gallery/atlas/audio-11-speaker-embedding.png",
      "pdf": "gallery/atlas/audio-11-speaker-embedding.pdf",
      "tex": "gallery/atlas/audio-11-speaker-embedding.tex"
    },
    {
      "id": "audio-12-speaker-diarization",
      "title": "Speaker diarization by embedding clustering",
      "family": "audio",
      "description": "A conceptual embedding-clustering diarization pipeline and speaker activity timeline.",
      "caption": "Speech turns are segmented, embedded, clustered, and placed back on the recording timeline.",
      "sources": [
        "https://arxiv.org/abs/2012.14952"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The timeline is invented. Overlapping speech handling is outside this simplified clustering schematic."
      ],
      "tags": [
        "diarization",
        "timeline",
        "clustering"
      ],
      "nodes": 5,
      "edges": 5,
      "source_file": "audio-12-speaker-diarization.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-12-speaker-diarization.json",
      "svg": "gallery/atlas/audio-12-speaker-diarization.svg",
      "png": "gallery/atlas/audio-12-speaker-diarization.png",
      "pdf": "gallery/atlas/audio-12-speaker-diarization.pdf",
      "tex": "gallery/atlas/audio-12-speaker-diarization.tex"
    },
    {
      "id": "audio-13-tts-overview",
      "title": "Text-to-speech: two-stage synthesis",
      "family": "audio",
      "description": "A two-stage text-to-speech overview with linguistic, acoustic, and waveform-generation interfaces.",
      "caption": "A linguistic frontend and acoustic model predict an intermediate representation for a neural vocoder.",
      "sources": [
        "https://arxiv.org/abs/1712.05884",
        "https://arxiv.org/abs/2006.04558"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Phonemization and explicit prosody controls are common design choices, not claims about all TTS systems."
      ],
      "tags": [
        "TTS",
        "vocoder",
        "conditioning"
      ],
      "nodes": 7,
      "edges": 6,
      "source_file": "audio-13-tts-overview.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-13-tts-overview.json",
      "svg": "gallery/atlas/audio-13-tts-overview.svg",
      "png": "gallery/atlas/audio-13-tts-overview.png",
      "pdf": "gallery/atlas/audio-13-tts-overview.pdf",
      "tex": "gallery/atlas/audio-13-tts-overview.tex"
    },
    {
      "id": "audio-14-tacotron-attention-tts",
      "title": "Tacotron-style attention TTS",
      "family": "audio",
      "description": "Text-memory attention, recurrent mel decoding, pre-net feedback, and post-net refinement.",
      "caption": "An autoregressive acoustic decoder attends to text memory and feeds back the preceding mel frame.",
      "sources": [
        "https://arxiv.org/abs/1712.05884"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Stop-token prediction, decoder frame grouping, and the downstream vocoder are omitted."
      ],
      "tags": [
        "TTS",
        "Tacotron",
        "autoregressive"
      ],
      "nodes": 10,
      "edges": 11,
      "source_file": "audio-14-tacotron-attention-tts.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-14-tacotron-attention-tts.json",
      "svg": "gallery/atlas/audio-14-tacotron-attention-tts.svg",
      "png": "gallery/atlas/audio-14-tacotron-attention-tts.png",
      "pdf": "gallery/atlas/audio-14-tacotron-attention-tts.pdf",
      "tex": "gallery/atlas/audio-14-tacotron-attention-tts.tex"
    },
    {
      "id": "audio-15-fastspeech2-variance",
      "title": "FastSpeech 2-style variance adaptor",
      "family": "audio",
      "description": "Parallel duration, pitch, and energy prediction with explicit length expansion.",
      "caption": "Duration expands token states into frames; pitch and energy embeddings enrich the acoustic representation.",
      "sources": [
        "https://arxiv.org/abs/2006.04558"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "This phoneme-level variance-adaptor abstraction does not prescribe every pitch or energy granularity choice."
      ],
      "tags": [
        "TTS",
        "FastSpeech2",
        "duration"
      ],
      "nodes": 11,
      "edges": 13,
      "source_file": "audio-15-fastspeech2-variance.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-15-fastspeech2-variance.json",
      "svg": "gallery/atlas/audio-15-fastspeech2-variance.svg",
      "png": "gallery/atlas/audio-15-fastspeech2-variance.png",
      "pdf": "gallery/atlas/audio-15-fastspeech2-variance.pdf",
      "tex": "gallery/atlas/audio-15-fastspeech2-variance.tex"
    },
    {
      "id": "audio-16-vits-conceptual",
      "title": "VITS conceptual training and inference",
      "family": "audio",
      "description": "Separate training and inference graphs for a variational flow-based end-to-end TTS model.",
      "caption": "A text-conditioned prior is matched to a speech posterior; inference samples the prior and inverts the flow.",
      "sources": [
        "https://arxiv.org/abs/2106.06103"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Training losses and alignment dependencies are aggregated; no specific flow family or decoder depth is asserted."
      ],
      "tags": [
        "TTS",
        "VITS",
        "normalizing flow"
      ],
      "nodes": 15,
      "edges": 14,
      "source_file": "audio-16-vits-conceptual.tex",
      "width_cm": 16,
      "height_cm": 9.6,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-16-vits-conceptual.json",
      "svg": "gallery/atlas/audio-16-vits-conceptual.svg",
      "png": "gallery/atlas/audio-16-vits-conceptual.png",
      "pdf": "gallery/atlas/audio-16-vits-conceptual.pdf",
      "tex": "gallery/atlas/audio-16-vits-conceptual.tex"
    },
    {
      "id": "audio-17-hifigan-vocoder",
      "title": "HiFi-GAN neural vocoder",
      "family": "audio",
      "description": "Upsampling generator, parallel MRF receptive fields, and multi-period/multi-scale training discriminators.",
      "caption": "Upsampling and multi-receptive-field fusion generate audio; period and scale discriminator families supervise training.",
      "sources": [
        "https://arxiv.org/abs/2010.05646"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "The MRF branch widths and number of upsampling stages are schematic; discriminator internals are omitted."
      ],
      "tags": [
        "vocoder",
        "HiFi-GAN",
        "GAN"
      ],
      "nodes": 13,
      "edges": 15,
      "source_file": "audio-17-hifigan-vocoder.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-17-hifigan-vocoder.json",
      "svg": "gallery/atlas/audio-17-hifigan-vocoder.svg",
      "png": "gallery/atlas/audio-17-hifigan-vocoder.png",
      "pdf": "gallery/atlas/audio-17-hifigan-vocoder.pdf",
      "tex": "gallery/atlas/audio-17-hifigan-vocoder.tex"
    },
    {
      "id": "audio-18-diffusion-vocoder",
      "title": "Diffusion vocoder",
      "family": "audio",
      "description": "A DiffWave-inspired conditional waveform diffusion process with forward and reverse lanes.",
      "caption": "Forward training noise and reverse conditional denoising run in opposite directions.",
      "sources": [
        "https://arxiv.org/abs/2009.09761"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Only the high-level diffusion schedule is shown; step counts and numerical sampler coefficients are unspecified."
      ],
      "tags": [
        "vocoder",
        "diffusion",
        "DiffWave"
      ],
      "nodes": 10,
      "edges": 8,
      "source_file": "audio-18-diffusion-vocoder.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-18-diffusion-vocoder.json",
      "svg": "gallery/atlas/audio-18-diffusion-vocoder.svg",
      "png": "gallery/atlas/audio-18-diffusion-vocoder.png",
      "pdf": "gallery/atlas/audio-18-diffusion-vocoder.pdf",
      "tex": "gallery/atlas/audio-18-diffusion-vocoder.tex"
    },
    {
      "id": "audio-19-speech-enhancement",
      "title": "Complex-mask speech enhancement",
      "family": "audio",
      "description": "DCCRN-inspired complex spectral masking with encoder skips and a mixture-spectrum multiplication bypass.",
      "caption": "A complex convolution--recurrent network estimates a mask, then reconstructs the enhanced waveform.",
      "sources": [
        "https://arxiv.org/abs/2008.00264",
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "A single recurrent bottleneck and one skip path stand for repeated implementation-specific layers."
      ],
      "tags": [
        "enhancement",
        "complex mask",
        "DCCRN"
      ],
      "nodes": 8,
      "edges": 9,
      "source_file": "audio-19-speech-enhancement.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-19-speech-enhancement.json",
      "svg": "gallery/atlas/audio-19-speech-enhancement.svg",
      "png": "gallery/atlas/audio-19-speech-enhancement.png",
      "pdf": "gallery/atlas/audio-19-speech-enhancement.pdf",
      "tex": "gallery/atlas/audio-19-speech-enhancement.tex"
    },
    {
      "id": "audio-20-residual-vq-codec",
      "title": "Residual vector-quantized audio codec",
      "family": "audio",
      "description": "A SoundStream-inspired neural codec with expanded residual quantization, subtraction paths, and code-vector summation.",
      "caption": "Each codebook quantizes the previous residual; summed code vectors reconstruct the encoder latent.",
      "sources": [
        "https://arxiv.org/abs/2107.03312"
      ],
      "assumptions": [
        "Conceptual original schematic; layer counts, widths, and signal lengths are illustrative.",
        "Three codebooks illustrate the recurrence. Codec bandwidth, codebook size, and actual number of stages are unspecified."
      ],
      "tags": [
        "codec",
        "residual VQ",
        "SoundStream"
      ],
      "nodes": 13,
      "edges": 14,
      "source_file": "audio-20-residual-vq-codec.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/audio-20-residual-vq-codec.json",
      "svg": "gallery/atlas/audio-20-residual-vq-codec.svg",
      "png": "gallery/atlas/audio-20-residual-vq-codec.png",
      "pdf": "gallery/atlas/audio-20-residual-vq-codec.pdf",
      "tex": "gallery/atlas/audio-20-residual-vq-codec.tex"
    },
    {
      "id": "multimodal-01-clip-dual-encoder",
      "title": "CLIP contrastive dual encoder",
      "family": "multimodal",
      "description": "Dual encoder contrastive pretraining with normalized embeddings, a batch similarity matrix, and symmetric losses.",
      "caption": "The diagonal of the cross-modal similarity matrix supplies positives for two directional classification losses.",
      "sources": [
        "https://proceedings.mlr.press/v139/radford21a.html"
      ],
      "assumptions": [
        "Original conceptual schematic; all dimensions are symbolic and implementation dependent."
      ],
      "tags": [
        "contrastive",
        "dual-encoder",
        "CLIP",
        "training"
      ],
      "nodes": 10,
      "edges": 10,
      "source_file": "multimodal-01-clip-dual-encoder.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-01-clip-dual-encoder.json",
      "svg": "gallery/atlas/multimodal-01-clip-dual-encoder.svg",
      "png": "gallery/atlas/multimodal-01-clip-dual-encoder.png",
      "pdf": "gallery/atlas/multimodal-01-clip-dual-encoder.pdf",
      "tex": "gallery/atlas/multimodal-01-clip-dual-encoder.tex"
    },
    {
      "id": "multimodal-02-visual-question-answering",
      "title": "Visual question answering",
      "family": "multimodal",
      "description": "Region-based question answering with question-conditioned attention, weighted visual pooling, and answer supervision.",
      "caption": "Question-conditioned weights pool region values; a separate question path preserves linguistic context.",
      "sources": [
        "https://openaccess.thecvf.com/content_cvpr_2018/html/Anderson_Bottom-Up_and_Top-Down_CVPR_2018_paper.html"
      ],
      "assumptions": [
        "Original conceptual schematic; all dimensions are symbolic and implementation dependent."
      ],
      "tags": [
        "VQA",
        "attention",
        "fusion"
      ],
      "nodes": 10,
      "edges": 11,
      "source_file": "multimodal-02-visual-question-answering.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-02-visual-question-answering.json",
      "svg": "gallery/atlas/multimodal-02-visual-question-answering.svg",
      "png": "gallery/atlas/multimodal-02-visual-question-answering.png",
      "pdf": "gallery/atlas/multimodal-02-visual-question-answering.pdf",
      "tex": "gallery/atlas/multimodal-02-visual-question-answering.tex"
    },
    {
      "id": "multimodal-03-image-captioning",
      "title": "Attention-based image captioning",
      "family": "multimodal",
      "description": "Image captioning with recurrent visual attention, a token likelihood objective, and an autoregressive word feedback loop.",
      "caption": "Visual memory is reused at each token step; the hidden state controls attention and sampled words feed the decoder.",
      "sources": [
        "https://proceedings.mlr.press/v37/xuc15.html"
      ],
      "assumptions": [
        "Original conceptual schematic; all dimensions are symbolic and implementation dependent."
      ],
      "tags": [
        "captioning",
        "autoregressive",
        "visual-attention"
      ],
      "nodes": 9,
      "edges": 10,
      "source_file": "multimodal-03-image-captioning.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-03-image-captioning.json",
      "svg": "gallery/atlas/multimodal-03-image-captioning.svg",
      "png": "gallery/atlas/multimodal-03-image-captioning.png",
      "pdf": "gallery/atlas/multimodal-03-image-captioning.pdf",
      "tex": "gallery/atlas/multimodal-03-image-captioning.tex"
    },
    {
      "id": "multimodal-04-vision-language-projector",
      "title": "Vision-language projection bridge",
      "family": "multimodal",
      "description": "LLaVA-style alignment of image encoder patch features with a causal language model through a learned projection.",
      "caption": "Projected image tokens and text embeddings enter one causal sequence; response tokens carry the language objective.",
      "sources": [
        "https://arxiv.org/abs/2304.08485",
        "https://github.com/haotian-liu/LLaVA"
      ],
      "assumptions": [
        "Conceptual LLaVA-style bridge; the linear projector follows the initial formulation, while later versions may use an MLP.",
        "Visual token counts and embedding widths are symbolic; the diagram does not fix training-stage freeze policies."
      ],
      "tags": [
        "LLaVA",
        "projector",
        "vision-language",
        "causal-LM"
      ],
      "nodes": 9,
      "edges": 8,
      "source_file": "multimodal-04-vision-language-projector.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-04-vision-language-projector.json",
      "svg": "gallery/atlas/multimodal-04-vision-language-projector.svg",
      "png": "gallery/atlas/multimodal-04-vision-language-projector.png",
      "pdf": "gallery/atlas/multimodal-04-vision-language-projector.pdf",
      "tex": "gallery/atlas/multimodal-04-vision-language-projector.tex"
    },
    {
      "id": "multimodal-05-resampler-cross-attention",
      "title": "Resampling with gated visual cross-attention",
      "family": "multimodal",
      "description": "Flamingo-style learned visual resampling and gated cross-attention inserted between language model blocks.",
      "caption": "Learned latent queries resample vision features; text queries read those latents through a gated residual path.",
      "sources": [
        "https://arxiv.org/abs/2204.14198"
      ],
      "assumptions": [
        "Original conceptual schematic; all dimensions are symbolic and implementation dependent."
      ],
      "tags": [
        "Flamingo",
        "Perceiver",
        "cross-attention",
        "gated-residual"
      ],
      "nodes": 11,
      "edges": 11,
      "source_file": "multimodal-05-resampler-cross-attention.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-05-resampler-cross-attention.json",
      "svg": "gallery/atlas/multimodal-05-resampler-cross-attention.svg",
      "png": "gallery/atlas/multimodal-05-resampler-cross-attention.png",
      "pdf": "gallery/atlas/multimodal-05-resampler-cross-attention.pdf",
      "tex": "gallery/atlas/multimodal-05-resampler-cross-attention.tex"
    },
    {
      "id": "multimodal-06-clap-audio-text",
      "title": "Audio-text contrastive learning and zero-shot scoring",
      "family": "multimodal",
      "description": "Audio-text contrastive pretraining with duration pooling and a distinct zero-shot text-label retrieval panel.",
      "caption": "Training aligns paired audio and descriptions; zero-shot inference ranks candidate text embeddings by cosine similarity.",
      "sources": [
        "https://arxiv.org/abs/2206.04769",
        "https://www.microsoft.com/en-us/research/publication/clap-learning-audio-concepts-from-natural-language-supervision/"
      ],
      "assumptions": [
        "Original conceptual schematic; all dimensions are symbolic and implementation dependent."
      ],
      "tags": [
        "CLAP",
        "audio-text",
        "contrastive",
        "zero-shot"
      ],
      "nodes": 11,
      "edges": 9,
      "source_file": "multimodal-06-clap-audio-text.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-06-clap-audio-text.json",
      "svg": "gallery/atlas/multimodal-06-clap-audio-text.svg",
      "png": "gallery/atlas/multimodal-06-clap-audio-text.png",
      "pdf": "gallery/atlas/multimodal-06-clap-audio-text.pdf",
      "tex": "gallery/atlas/multimodal-06-clap-audio-text.tex"
    },
    {
      "id": "multimodal-07-speech-language-bridge",
      "title": "Speech-to-language-model bridge",
      "family": "multimodal",
      "description": "SALMONN-style speech and audio encoder fusion through a window-level query adapter into a language model.",
      "caption": "A windowed query adapter compresses aligned encoder features; prompt embeddings and audio tokens condition text generation.",
      "sources": [
        "https://arxiv.org/abs/2310.13289",
        "https://github.com/bytedance/SALMONN"
      ],
      "assumptions": [
        "Conceptual SALMONN-style bridge, shown for transcription; encoder alignment, query counts, and widths remain symbolic.",
        "The figure omits low-rank adaptation and detailed training stages."
      ],
      "tags": [
        "speech",
        "audio",
        "Q-Former",
        "language-model",
        "adapter"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "multimodal-07-speech-language-bridge.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-07-speech-language-bridge.json",
      "svg": "gallery/atlas/multimodal-07-speech-language-bridge.svg",
      "png": "gallery/atlas/multimodal-07-speech-language-bridge.png",
      "pdf": "gallery/atlas/multimodal-07-speech-language-bridge.pdf",
      "tex": "gallery/atlas/multimodal-07-speech-language-bridge.tex"
    },
    {
      "id": "multimodal-08-video-temporal-encoder",
      "title": "Video temporal encoder",
      "family": "multimodal",
      "description": "A factorized video encoder with shared spatial frame encoders, frame summaries, temporal positions, and temporal attention.",
      "caption": "Each frame contributes a spatial summary; temporal position codes preserve order before the video-level readout.",
      "sources": [
        "https://openaccess.thecvf.com/content/ICCV2021/html/Arnab_ViViT_A_Video_Vision_Transformer_ICCV_2021_paper.html"
      ],
      "assumptions": [
        "Conceptual frame-level factorized encoder inspired by ViViT; temporal tubelets and other ViViT variants are not shown.",
        "All frame counts, sequence lengths, and channel widths are symbolic."
      ],
      "tags": [
        "video",
        "temporal-attention",
        "factorized-encoder",
        "ViViT"
      ],
      "nodes": 11,
      "edges": 10,
      "source_file": "multimodal-08-video-temporal-encoder.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-08-video-temporal-encoder.json",
      "svg": "gallery/atlas/multimodal-08-video-temporal-encoder.svg",
      "png": "gallery/atlas/multimodal-08-video-temporal-encoder.png",
      "pdf": "gallery/atlas/multimodal-08-video-temporal-encoder.pdf",
      "tex": "gallery/atlas/multimodal-08-video-temporal-encoder.tex"
    },
    {
      "id": "multimodal-09-audiovisual-speech-fusion",
      "title": "Audio-visual speech fusion",
      "family": "multimodal",
      "description": "Synchronized audio-visual speech fusion with masked multimodal representations and discrete cluster prediction.",
      "caption": "Aligned audio and visual streams feed a masked joint encoder; discrete cluster targets supervise only selected positions.",
      "sources": [
        "https://arxiv.org/abs/2201.02184",
        "https://github.com/facebookresearch/av_hubert"
      ],
      "assumptions": [
        "Conceptual AV-HuBERT-style pretraining; clean fused features represent the offline target pipeline, whose clustering is refined across iterations.",
        "Frontends, temporal resampling, and fusion widths are symbolic."
      ],
      "tags": [
        "audio-visual",
        "speech",
        "AV-HuBERT",
        "masked-prediction"
      ],
      "nodes": 10,
      "edges": 10,
      "source_file": "multimodal-09-audiovisual-speech-fusion.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-09-audiovisual-speech-fusion.json",
      "svg": "gallery/atlas/multimodal-09-audiovisual-speech-fusion.svg",
      "png": "gallery/atlas/multimodal-09-audiovisual-speech-fusion.png",
      "pdf": "gallery/atlas/multimodal-09-audiovisual-speech-fusion.pdf",
      "tex": "gallery/atlas/multimodal-09-audiovisual-speech-fusion.tex"
    },
    {
      "id": "multimodal-10-early-versus-late-fusion",
      "title": "Early fusion versus late fusion",
      "family": "multimodal",
      "description": "Side-by-side comparison of aligned input fusion before a joint model and weighted probability fusion after unimodal models.",
      "caption": "Early fusion exposes cross-modal interactions to one model; late fusion combines independently produced decision values.",
      "sources": [
        "https://arxiv.org/abs/1705.09406",
        "https://ai.stanford.edu/~ang/papers/icml11-MultimodalDeepLearning.pdf"
      ],
      "assumptions": [
        "Conceptual fusion comparison; concatenation and weighted averaging are illustrative design choices, with 0 <= lambda <= 1.",
        "Inputs are assumed aligned when early concatenation requires correspondence."
      ],
      "tags": [
        "early-fusion",
        "late-fusion",
        "comparison"
      ],
      "nodes": 10,
      "edges": 8,
      "source_file": "multimodal-10-early-versus-late-fusion.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-10-early-versus-late-fusion.json",
      "svg": "gallery/atlas/multimodal-10-early-versus-late-fusion.svg",
      "png": "gallery/atlas/multimodal-10-early-versus-late-fusion.png",
      "pdf": "gallery/atlas/multimodal-10-early-versus-late-fusion.pdf",
      "tex": "gallery/atlas/multimodal-10-early-versus-late-fusion.tex"
    },
    {
      "id": "multimodal-11-vision-language-action",
      "title": "Vision-language-action policy",
      "family": "multimodal",
      "description": "A closed-loop vision-language-action policy with visual and language branches, action-token decoding, and environment feedback.",
      "caption": "The policy emits discrete action tokens, which are decoded into a control command before the next observation arrives.",
      "sources": [
        "https://arxiv.org/abs/2307.15818",
        "https://proceedings.mlr.press/v229/zitkovich23a.html"
      ],
      "assumptions": [
        "Conceptual RT-2-style inference loop; action symbols are schematic and do not specify exact tokenization or robot degrees of freedom.",
        "Web-data co-fine-tuning and robotics training trajectories are outside this inference view."
      ],
      "tags": [
        "VLA",
        "RT-2",
        "robotics",
        "closed-loop"
      ],
      "nodes": 8,
      "edges": 8,
      "source_file": "multimodal-11-vision-language-action.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-11-vision-language-action.json",
      "svg": "gallery/atlas/multimodal-11-vision-language-action.svg",
      "png": "gallery/atlas/multimodal-11-vision-language-action.png",
      "pdf": "gallery/atlas/multimodal-11-vision-language-action.pdf",
      "tex": "gallery/atlas/multimodal-11-vision-language-action.tex"
    },
    {
      "id": "multimodal-12-rgb-depth-fusion",
      "title": "RGB-depth fusion at multiple scales",
      "family": "multimodal",
      "description": "Registered RGB and depth encoders with repeated same-scale additive feature fusion and a dense semantic decoder.",
      "caption": "Depth and RGB features are summed at corresponding scales; the fused appearance stream supplies a dense decoder.",
      "sources": [
        "https://github.com/tum-vision/fusenet",
        "https://cvai.cit.tum.de/_media/spezial/bib/hazirbasma2016fusenet.pdf"
      ],
      "assumptions": [
        "Conceptual FuseNet-style pattern with three representative scales; the source architecture contains additional stages and decoder detail.",
        "RGB and depth are assumed registered; symbolic feature channels are compatible at each sum."
      ],
      "tags": [
        "RGB-D",
        "FuseNet",
        "dense-prediction",
        "multiscale-fusion"
      ],
      "nodes": 13,
      "edges": 14,
      "source_file": "multimodal-12-rgb-depth-fusion.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-12-rgb-depth-fusion.json",
      "svg": "gallery/atlas/multimodal-12-rgb-depth-fusion.svg",
      "png": "gallery/atlas/multimodal-12-rgb-depth-fusion.png",
      "pdf": "gallery/atlas/multimodal-12-rgb-depth-fusion.pdf",
      "tex": "gallery/atlas/multimodal-12-rgb-depth-fusion.tex"
    },
    {
      "id": "multimodal-13-document-layout-language-vision",
      "title": "Document language-layout-vision fusion",
      "family": "multimodal",
      "description": "OCR words and segment boxes plus linear image patches are fused by a shared document transformer with three pretraining heads.",
      "caption": "Text, patch, and word-patch objectives train one multimodal encoder while layout coordinates remain available.",
      "sources": [
        "https://arxiv.org/abs/2204.08387",
        "https://arxiv.org/html/2204.08387v3"
      ],
      "assumptions": [
        "Conceptual LayoutLMv3-style graph; image targets are discrete visual tokens and WPA predicts corresponding patch masking.",
        "Mask selection and visual tokenizer target generation are omitted; all dimensions are symbolic."
      ],
      "tags": [
        "document-AI",
        "LayoutLMv3",
        "layout",
        "pretraining"
      ],
      "nodes": 10,
      "edges": 11,
      "source_file": "multimodal-13-document-layout-language-vision.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-13-document-layout-language-vision.json",
      "svg": "gallery/atlas/multimodal-13-document-layout-language-vision.svg",
      "png": "gallery/atlas/multimodal-13-document-layout-language-vision.png",
      "pdf": "gallery/atlas/multimodal-13-document-layout-language-vision.pdf",
      "tex": "gallery/atlas/multimodal-13-document-layout-language-vision.tex"
    },
    {
      "id": "multimodal-14-retrieval-augmented-generation",
      "title": "Retrieval-augmented multimodal generation",
      "family": "multimodal",
      "description": "Multimodal retrieval-augmented generation with offline memory keys, payload storage, top-k search, and a direct query context path.",
      "caption": "Offline keys support nearest-neighbor search; retrieved identifiers fetch multimodal evidence for query-conditioned generation.",
      "sources": [
        "https://aclanthology.org/2022.emnlp-main.375/",
        "https://arxiv.org/abs/2210.02928"
      ],
      "assumptions": [
        "Conceptual MuRAG-inspired system; the key index and payload store are logical roles and may share one implementation.",
        "The figure describes inference and memory construction; contrastive and generative pretraining objectives are omitted."
      ],
      "tags": [
        "multimodal-RAG",
        "retrieval",
        "MuRAG",
        "memory"
      ],
      "nodes": 10,
      "edges": 11,
      "source_file": "multimodal-14-retrieval-augmented-generation.tex",
      "width_cm": 18,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-14-retrieval-augmented-generation.json",
      "svg": "gallery/atlas/multimodal-14-retrieval-augmented-generation.svg",
      "png": "gallery/atlas/multimodal-14-retrieval-augmented-generation.png",
      "pdf": "gallery/atlas/multimodal-14-retrieval-augmented-generation.pdf",
      "tex": "gallery/atlas/multimodal-14-retrieval-augmented-generation.tex"
    },
    {
      "id": "multimodal-15-mixture-of-experts",
      "title": "Multimodal mixture-of-experts routing",
      "family": "multimodal",
      "description": "Shared multimodal token processing with sparse content-dependent routing, a common expert bank, routing regularization, and residual recombination.",
      "caption": "A sparse router dispatches each token to selected experts; weighted outputs rejoin the residual stream.",
      "sources": [
        "https://arxiv.org/abs/2206.02770",
        "https://proceedings.neurips.cc/paper_files/paper/2022/file/3e67e84abf900bb2c7cbd5759bfce62d-Paper-Conference.pdf"
      ],
      "assumptions": [
        "Conceptual LIMoE-inspired expert block; the expert count and top-k selection are illustrative and not asserted as an exact model configuration.",
        "Image and text sequences can be encoded separately through shared weights; the display juxtaposes token sources rather than asserting cross-modal joint attention."
      ],
      "tags": [
        "MoE",
        "LIMoE",
        "sparse-routing",
        "shared-experts"
      ],
      "nodes": 10,
      "edges": 12,
      "source_file": "multimodal-15-mixture-of-experts.tex",
      "width_cm": 19,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/multimodal-15-mixture-of-experts.json",
      "svg": "gallery/atlas/multimodal-15-mixture-of-experts.svg",
      "png": "gallery/atlas/multimodal-15-mixture-of-experts.png",
      "pdf": "gallery/atlas/multimodal-15-mixture-of-experts.pdf",
      "tex": "gallery/atlas/multimodal-15-mixture-of-experts.tex"
    },
    {
      "id": "agents-01-react-loop",
      "title": "ReAct: interleaved reasoning, action, and observation",
      "family": "agents",
      "description": "A ReAct-style agent explicitly feeds tool observations back into its trajectory context, with a separate finish path.",
      "caption": "Each observation updates the trajectory before another action or a final response is selected.",
      "sources": [
        "https://arxiv.org/abs/2210.03629"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "The diagram abstracts the paper's thought/action/observation sequence and does not expose or prescribe private model reasoning.",
        "The finish criterion is task dependent; no convergence or correctness guarantee is implied."
      ],
      "tags": [
        "agent",
        "ReAct",
        "feedback",
        "tools"
      ],
      "nodes": 7,
      "edges": 7,
      "source_file": "agents-01-react-loop.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-01-react-loop.json",
      "svg": "gallery/atlas/agents-01-react-loop.svg",
      "png": "gallery/atlas/agents-01-react-loop.png",
      "pdf": "gallery/atlas/agents-01-react-loop.pdf",
      "tex": "gallery/atlas/agents-01-react-loop.tex"
    },
    {
      "id": "agents-02-plan-execute",
      "title": "Plan and execute with progress-aware replanning",
      "family": "agents",
      "description": "An original U-shaped view of the official plan-and-execute pattern, separating planner, ordered plan, executor, and progress-based replanning.",
      "caption": "An explicit plan drives execution; completed-step evidence supports either replanning or a final response.",
      "sources": [
        "https://www.langchain.com/blog/planning-agents",
        "https://arxiv.org/abs/2305.04091"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Illustrates serial plan steps, not a dependency scheduler.",
        "Progress is passed to a replan/finish controller; criteria and iteration bounds are application choices."
      ],
      "tags": [
        "agent",
        "planning",
        "execution",
        "state"
      ],
      "nodes": 8,
      "edges": 8,
      "source_file": "agents-02-plan-execute.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-02-plan-execute.json",
      "svg": "gallery/atlas/agents-02-plan-execute.svg",
      "png": "gallery/atlas/agents-02-plan-execute.png",
      "pdf": "gallery/atlas/agents-02-plan-execute.pdf",
      "tex": "gallery/atlas/agents-02-plan-execute.tex"
    },
    {
      "id": "agents-03-tool-protocol",
      "title": "Tool-call and result protocol",
      "family": "agents",
      "description": "An original three-lane sequence diagram of the OpenAI function-call/output contract, with application-side execution authority and call-id linkage.",
      "caption": "The application executes the function and returns output linked to the model's call identifier.",
      "sources": [
        "https://developers.openai.com/api/docs/guides/function-calling"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Uses generic names for a single illustrative function call; concrete API item types differ by API.",
        "Validation and execution policy are application responsibilities and are shown as explicit application steps."
      ],
      "tags": [
        "protocol",
        "tool calling",
        "sequence",
        "application boundary"
      ],
      "nodes": 3,
      "edges": 6,
      "source_file": "agents-03-tool-protocol.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-03-tool-protocol.json",
      "svg": "gallery/atlas/agents-03-tool-protocol.svg",
      "png": "gallery/atlas/agents-03-tool-protocol.png",
      "pdf": "gallery/atlas/agents-03-tool-protocol.pdf",
      "tex": "gallery/atlas/agents-03-tool-protocol.tex"
    },
    {
      "id": "agents-04-bounded-reflection",
      "title": "Bounded reflection and revision",
      "family": "agents",
      "description": "An original bounded refinement controller inspired by Self-Refine, with candidate, self-feedback, revision, and explicit stop/budget paths.",
      "caption": "Feedback can guide a revision, while a stopping rule or revision budget bounds the loop; feedback may itself be wrong.",
      "sources": [
        "https://arxiv.org/abs/2303.17651"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "The finite revision budget and recorded stop reason are explicit design additions, not claimed paper guarantees.",
        "Task and rubric remain available to generation, feedback, and revision; arrows emphasize changing artifacts."
      ],
      "tags": [
        "agent",
        "self-refine",
        "reflection",
        "bounded loop"
      ],
      "nodes": 7,
      "edges": 8,
      "source_file": "agents-04-bounded-reflection.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-04-bounded-reflection.json",
      "svg": "gallery/atlas/agents-04-bounded-reflection.svg",
      "png": "gallery/atlas/agents-04-bounded-reflection.png",
      "pdf": "gallery/atlas/agents-04-bounded-reflection.pdf",
      "tex": "gallery/atlas/agents-04-bounded-reflection.tex"
    },
    {
      "id": "agents-05-supervisor",
      "title": "Supervisor with tool-wrapped specialist agents",
      "family": "agents",
      "description": "An original supervisor-centered topology showing scoped specialist invocation, result returns, main-agent conversation state, and local tool boundaries.",
      "caption": "The supervisor supplies scoped tasks and combines returned results; specialists do not directly answer the user.",
      "sources": [
        "https://docs.langchain.com/oss/python/langchain/multi-agent/subagents"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Specialists are tool wrapped and return to the supervisor; no direct specialist-to-user path is shown.",
        "Local tool-call/result detail is abstracted; specialties are illustrative."
      ],
      "tags": [
        "multi-agent",
        "supervisor",
        "state",
        "boundaries"
      ],
      "nodes": 10,
      "edges": 13,
      "source_file": "agents-05-supervisor.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-05-supervisor.json",
      "svg": "gallery/atlas/agents-05-supervisor.svg",
      "png": "gallery/atlas/agents-05-supervisor.png",
      "pdf": "gallery/atlas/agents-05-supervisor.pdf",
      "tex": "gallery/atlas/agents-05-supervisor.tex"
    },
    {
      "id": "agents-06-parallel-research",
      "title": "Parallel research with evidence reduction",
      "family": "agents",
      "description": "An original fan-out/fan-in research design with scoped parallel workers, explicit evidence packets, and a reducer before final synthesis.",
      "caption": "Scoped research branches return source-linked claims; the reducer checks coverage and resolves conflicts before synthesis.",
      "sources": [
        "https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/",
        "https://docs.langchain.com/oss/python/langgraph/workflows-agents"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Applies map/reduce and orchestrator/worker ideas to research; this is not a reproduction of the MapReduce system architecture.",
        "Coverage checks and conflict resolution are application steps; shared source bias can remain."
      ],
      "tags": [
        "multi-agent",
        "parallel",
        "research",
        "reducer"
      ],
      "nodes": 10,
      "edges": 11,
      "source_file": "agents-06-parallel-research.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-06-parallel-research.json",
      "svg": "gallery/atlas/agents-06-parallel-research.svg",
      "png": "gallery/atlas/agents-06-parallel-research.png",
      "pdf": "gallery/atlas/agents-06-parallel-research.pdf",
      "tex": "gallery/atlas/agents-06-parallel-research.tex"
    },
    {
      "id": "agents-07-debate-adjudicator",
      "title": "Debate with an explicit adjudicator",
      "family": "agents",
      "description": "An original two-round debate topology with transcript exchange followed by a distinct adjudicator, rather than assuming consensus is correct.",
      "caption": "Agents revise after reading both arguments; a separate adjudicator records a decision and any unresolved disagreement.",
      "sources": [
        "https://arxiv.org/abs/2305.14325"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "A separate adjudicator and explicit disagreement output are design additions inspired by the debate pattern.",
        "Two rounds are illustrative; correlated mistakes and adjudicator errors remain possible."
      ],
      "tags": [
        "multi-agent",
        "debate",
        "adjudication",
        "transcript"
      ],
      "nodes": 7,
      "edges": 8,
      "source_file": "agents-07-debate-adjudicator.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-07-debate-adjudicator.json",
      "svg": "gallery/atlas/agents-07-debate-adjudicator.svg",
      "png": "gallery/atlas/agents-07-debate-adjudicator.png",
      "pdf": "gallery/atlas/agents-07-debate-adjudicator.pdf",
      "tex": "gallery/atlas/agents-07-debate-adjudicator.tex"
    },
    {
      "id": "agents-08-rag-lifecycles",
      "title": "RAG: separate indexing from per-query generation",
      "family": "agents",
      "description": "An original two-lane RAG architecture separating document indexing from query-time encoding, retrieval, and generation, including an explicit query-to-generator path.",
      "caption": "Indexing writes document representations; a query retrieves passages that condition the generator alongside the query.",
      "sources": [
        "https://arxiv.org/abs/2005.11401"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Uses a dense retrieval abstraction; training, index refresh, ranking, and passage storage implementations are omitted.",
        "Linked passages are included in the retrieval-index abstraction; no index size or exact tensor dimension is asserted."
      ],
      "tags": [
        "RAG",
        "indexing",
        "retrieval",
        "generation"
      ],
      "nodes": 9,
      "edges": 11,
      "source_file": "agents-08-rag-lifecycles.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-08-rag-lifecycles.json",
      "svg": "gallery/atlas/agents-08-rag-lifecycles.svg",
      "png": "gallery/atlas/agents-08-rag-lifecycles.png",
      "pdf": "gallery/atlas/agents-08-rag-lifecycles.pdf",
      "tex": "gallery/atlas/agents-08-rag-lifecycles.tex"
    },
    {
      "id": "agents-09-hybrid-fusion",
      "title": "Hybrid retrieval with reciprocal rank fusion",
      "family": "agents",
      "description": "An original two-branch hybrid retrieval diagram that fuses lexical and vector rank lists with the reciprocal-rank formula and a document-id merge.",
      "caption": "Fuse document ranks from lexical and dense retrieval, deduplicate by document id, then select the context window.",
      "sources": [
        "https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion",
        "https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Two equal-weight child lists and illustrative document ids are shown; retrieval scores are not added directly.",
        "The rank constant and rank-window sizes are implementation choices; no quality guarantee is implied."
      ],
      "tags": [
        "retrieval",
        "hybrid",
        "RRF",
        "fusion"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "agents-09-hybrid-fusion.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-09-hybrid-fusion.json",
      "svg": "gallery/atlas/agents-09-hybrid-fusion.svg",
      "png": "gallery/atlas/agents-09-hybrid-fusion.png",
      "pdf": "gallery/atlas/agents-09-hybrid-fusion.pdf",
      "tex": "gallery/atlas/agents-09-hybrid-fusion.tex"
    },
    {
      "id": "agents-10-corrective-rag",
      "title": "Corrective RAG with route-dependent evidence",
      "family": "agents",
      "description": "An original CRAG logic view with a retrieval evaluator controlling refined-corpus, web-search, and combined-evidence paths into generation.",
      "caption": "The evaluator selects refined retrieved evidence, web evidence, or both; its routing decisions can still be wrong.",
      "sources": [
        "https://arxiv.org/abs/2401.15884",
        "https://arxiv.org/html/2401.15884v3"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Correct/incorrect/ambiguous route semantics follow CRAG; evaluator internals and knowledge-refinement internals are abstracted.",
        "The query is shared request context for evaluation, rewriting, and generation; branch arrows emphasize evidence and route control.",
        "Evidence assembly consumes only route-selected inputs; it does not wait for a branch that was not executed."
      ],
      "tags": [
        "RAG",
        "CRAG",
        "corrective retrieval",
        "conditional control"
      ],
      "nodes": 8,
      "edges": 8,
      "source_file": "agents-10-corrective-rag.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-10-corrective-rag.json",
      "svg": "gallery/atlas/agents-10-corrective-rag.svg",
      "png": "gallery/atlas/agents-10-corrective-rag.png",
      "pdf": "gallery/atlas/agents-10-corrective-rag.pdf",
      "tex": "gallery/atlas/agents-10-corrective-rag.tex"
    },
    {
      "id": "agents-11-memory-scopes",
      "title": "Thread state and cross-session memory",
      "family": "agents",
      "description": "An original two-boundary memory diagram showing current-thread state reads and feedback updates, plus selected writes and cross-session reads of a namespaced long-term store.",
      "caption": "Thread-scoped history supports the current run; namespaced long-term memory is read and updated across sessions.",
      "sources": [
        "https://docs.langchain.com/oss/python/concepts/memory",
        "https://arxiv.org/abs/2310.08560"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "The memory write policy is an illustrative application component, not an automatic guarantee of accurate memories.",
        "Memory recall is an explicit data retrieval operation; no online model training is shown."
      ],
      "tags": [
        "agent",
        "memory",
        "state",
        "session boundaries"
      ],
      "nodes": 7,
      "edges": 8,
      "source_file": "agents-11-memory-scopes.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-11-memory-scopes.json",
      "svg": "gallery/atlas/agents-11-memory-scopes.svg",
      "png": "gallery/atlas/agents-11-memory-scopes.png",
      "pdf": "gallery/atlas/agents-11-memory-scopes.pdf",
      "tex": "gallery/atlas/agents-11-memory-scopes.tex"
    },
    {
      "id": "agents-12-event-workflow",
      "title": "Event-driven agent workflow with durable state",
      "family": "agents",
      "description": "An original asynchronous agent coordinator with event inbox, deduplication identity, append-only log, state checkpoint, task outbox, worker, and completion-event feedback.",
      "caption": "Events drive state transitions and task dispatch; deduplication and recovery depend on persistence and worker semantics.",
      "sources": [
        "https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing",
        "https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "An original event-driven agent design informed by event-sourcing and asynchronous request/reply patterns; no exactly-once guarantee is claimed.",
        "The figure does not prescribe a distributed transaction between event log, checkpoint, and outbox; consistency and retry behavior require implementation choices."
      ],
      "tags": [
        "agent",
        "events",
        "asynchronous",
        "durable state"
      ],
      "nodes": 10,
      "edges": 11,
      "source_file": "agents-12-event-workflow.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-12-event-workflow.json",
      "svg": "gallery/atlas/agents-12-event-workflow.svg",
      "png": "gallery/atlas/agents-12-event-workflow.png",
      "pdf": "gallery/atlas/agents-12-event-workflow.pdf",
      "tex": "gallery/atlas/agents-12-event-workflow.tex"
    },
    {
      "id": "agents-13-human-approval",
      "title": "Human approval checkpoint before side effects",
      "family": "agents",
      "description": "An original pause-and-resume approval architecture with persisted proposal state, a human review boundary, and explicit approve/execute and reject/cancel paths.",
      "caption": "Persist the proposal and paused state, obtain a human decision, then resume to execute or cancel.",
      "sources": [
        "https://docs.langchain.com/oss/python/langgraph/interrupts"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Illustrates a workflow configured to interrupt before the side effect; the checkpoint is not a general guarantee of all tool safety.",
        "Authentication, proposal freshness, and replay/side-effect idempotency are application concerns beyond this conceptual figure."
      ],
      "tags": [
        "agent",
        "human in the loop",
        "approval",
        "checkpoint"
      ],
      "nodes": 8,
      "edges": 8,
      "source_file": "agents-13-human-approval.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-13-human-approval.json",
      "svg": "gallery/atlas/agents-13-human-approval.svg",
      "png": "gallery/atlas/agents-13-human-approval.png",
      "pdf": "gallery/atlas/agents-13-human-approval.pdf",
      "tex": "gallery/atlas/agents-13-human-approval.tex"
    },
    {
      "id": "agents-14-sandbox-execution",
      "title": "Sandboxed code execution with explicit result capture",
      "family": "agents",
      "description": "An original execution-service workflow with request validation, configured runtime launch, resource/access policy, sandboxed process, ephemeral files, and captured-result feedback.",
      "caption": "Validate and launch code under an explicit runtime policy; return captured outputs and deliberately exported artifacts.",
      "sources": [
        "https://gvisor.dev/docs/architecture_guide/intro/",
        "https://gvisor.dev/docs/user_guide/quick_start/docker/"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "The generic workflow is informed by gVisor's runtime isolation boundary; it is not a diagram of the Sentry/Gofer internals.",
        "Resource limits, mounts, network access, and artifact export are illustrative configured controls; no perfect-containment guarantee is implied."
      ],
      "tags": [
        "agent",
        "sandbox",
        "code execution",
        "security boundary"
      ],
      "nodes": 7,
      "edges": 9,
      "source_file": "agents-14-sandbox-execution.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-14-sandbox-execution.json",
      "svg": "gallery/atlas/agents-14-sandbox-execution.svg",
      "png": "gallery/atlas/agents-14-sandbox-execution.png",
      "pdf": "gallery/atlas/agents-14-sandbox-execution.pdf",
      "tex": "gallery/atlas/agents-14-sandbox-execution.tex"
    },
    {
      "id": "agents-15-distributed-serving",
      "title": "Distributed inference with tensor-parallel serving",
      "family": "agents",
      "description": "An original distributed inference serving topology with a request queue, active-batch scheduler, a two-rank tensor-parallel replica, per-rank KV state, collective communication, and a client response stream.",
      "caption": "A scheduler dispatches active sequences to a tensor-parallel replica; local KV state supports iterative token generation.",
      "sources": [
        "https://docs.vllm.ai/en/latest/serving/parallelism_scaling/",
        "https://arxiv.org/abs/2309.06180"
      ],
      "assumptions": [
        "Conceptual original schematic; implementation details and dimensions vary.",
        "Two ranks are illustrative; exact placement, parallelism degree, batch policy, and KV-cache management vary.",
        "A representative leader output path is shown; sampling/detokenization and backend-specific control/data exchange are abstracted.",
        "KV state arrows indicate state access, not a claim that one rank only reads while another only writes."
      ],
      "tags": [
        "serving",
        "distributed inference",
        "tensor parallelism",
        "KV cache"
      ],
      "nodes": 9,
      "edges": 11,
      "source_file": "agents-15-distributed-serving.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/agents-15-distributed-serving.json",
      "svg": "gallery/atlas/agents-15-distributed-serving.svg",
      "png": "gallery/atlas/agents-15-distributed-serving.png",
      "pdf": "gallery/atlas/agents-15-distributed-serving.pdf",
      "tex": "gallery/atlas/agents-15-distributed-serving.tex"
    },
    {
      "id": "rg01-perception-action-loop",
      "title": "Perception--action closed loop",
      "family": "robotics-graphs",
      "description": "A closed physical feedback cycle with an external task reference and an explicit actuation boundary.",
      "caption": "Conceptual sensing, estimation, control, and physical feedback; ROS control documentation informs the control interface.",
      "sources": [
        "https://control.ros.org/jazzy/doc/getting_started/getting_started.html"
      ],
      "assumptions": [
        "Perception and estimation are conceptual additions around the documented controller/hardware interface.",
        "Discrete-time notation is illustrative; no timing, stability, or safety guarantee is implied."
      ],
      "tags": [
        "robotics",
        "feedback",
        "perception",
        "control"
      ],
      "nodes": 6,
      "edges": 5,
      "source_file": "rg01-perception-action-loop.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg01-perception-action-loop.json",
      "svg": "gallery/atlas/rg01-perception-action-loop.svg",
      "png": "gallery/atlas/rg01-perception-action-loop.png",
      "pdf": "gallery/atlas/rg01-perception-action-loop.pdf",
      "tex": "gallery/atlas/rg01-perception-action-loop.tex"
    },
    {
      "id": "rg02-hierarchical-policy",
      "title": "Hierarchical robot policy",
      "family": "robotics-graphs",
      "description": "A three-skill options hierarchy showing discrete option selection, primitive action emission, and termination feedback.",
      "caption": "Conceptual options hierarchy after Sutton, Precup, and Singh (1999); only the selected option emits primitive actions.",
      "sources": [
        "https://doi.org/10.1016/S0004-3702(99)00052-1"
      ],
      "assumptions": [
        "Navigate, Reach, and Grasp are illustrative robot skill names, not a reported system from the source.",
        "State input to each option is implicit; arrows from options denote mutually exclusive active-option routing."
      ],
      "tags": [
        "robotics",
        "hierarchical-policy",
        "options",
        "temporal-abstraction"
      ],
      "nodes": 6,
      "edges": 8,
      "source_file": "rg02-hierarchical-policy.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg02-hierarchical-policy.json",
      "svg": "gallery/atlas/rg02-hierarchical-policy.svg",
      "png": "gallery/atlas/rg02-hierarchical-policy.png",
      "pdf": "gallery/atlas/rg02-hierarchical-policy.pdf",
      "tex": "gallery/atlas/rg02-hierarchical-policy.tex"
    },
    {
      "id": "rg03-model-predictive-control",
      "title": "Model-predictive control",
      "family": "robotics-graphs",
      "description": "An MPC feedback loop paired with a time-indexed planned-input strip that distinguishes first-action execution from future controls.",
      "caption": "Conceptual MPC after Rawlings, Mayne, and Diehl: optimize a horizon, execute its first input, and replan from the next estimate.",
      "sources": [
        "https://sites.engineering.ucsb.edu/~jbraw/mpc/"
      ],
      "assumptions": [
        "The state estimator, objective, constraints, dynamics, and horizon are problem-specific and shown abstractly.",
        "Feasibility, closed-loop stability, runtime, and safety are not established by this schematic."
      ],
      "tags": [
        "robotics",
        "mpc",
        "optimization",
        "receding-horizon"
      ],
      "nodes": 4,
      "edges": 4,
      "source_file": "rg03-model-predictive-control.tex",
      "width_cm": 16,
      "height_cm": 9.3,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg03-model-predictive-control.json",
      "svg": "gallery/atlas/rg03-model-predictive-control.svg",
      "png": "gallery/atlas/rg03-model-predictive-control.png",
      "pdf": "gallery/atlas/rg03-model-predictive-control.pdf",
      "tex": "gallery/atlas/rg03-model-predictive-control.tex"
    },
    {
      "id": "rg04-sim-to-real",
      "title": "Simulation training and robot deployment",
      "family": "robotics-graphs",
      "description": "A grid of randomized simulators feeds a learner; only a checkpoint crosses into the isolated physical deployment loop.",
      "caption": "Conceptual sim-to-real separation after Peng et al. (2018); randomized training does not guarantee successful physical transfer.",
      "sources": [
        "https://arxiv.org/abs/1710.06537"
      ],
      "assumptions": [
        "Parallel simulator grid and a frozen checkpoint are conceptual implementation choices.",
        "The figure omits the source method's recurrent policy, omniscient critic, and task-specific training details.",
        "No physical transfer, reliability, timing, or safety guarantee is implied."
      ],
      "tags": [
        "robotics",
        "sim-to-real",
        "domain-randomization",
        "training-deployment"
      ],
      "nodes": 9,
      "edges": 12,
      "source_file": "rg04-sim-to-real.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg04-sim-to-real.json",
      "svg": "gallery/atlas/rg04-sim-to-real.svg",
      "png": "gallery/atlas/rg04-sim-to-real.png",
      "pdf": "gallery/atlas/rg04-sim-to-real.pdf",
      "tex": "gallery/atlas/rg04-sim-to-real.tex"
    },
    {
      "id": "rg05-sensor-fusion",
      "title": "Robot sensor fusion",
      "family": "robotics-graphs",
      "description": "Three measurement streams converge into a recursive prediction/correction estimator and expose both state and uncertainty.",
      "caption": "Conceptual predict--correct fusion informed by robot_localization documentation; frame and covariance treatment are essential.",
      "sources": [
        "https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/doc/state_estimation_nodes.rst",
        "https://index.ros.org/p/robot_localization/"
      ],
      "assumptions": [
        "The three selected sensor sources and the layout are illustrative, not a package launch configuration.",
        "Time/frame handling is conceptual; the diagram does not require simultaneous arrival or claim an explicit synchronization node.",
        "The estimator may use an EKF or UKF; equations intentionally omit filter-specific details."
      ],
      "tags": [
        "robotics",
        "sensor-fusion",
        "state-estimation",
        "uncertainty"
      ],
      "nodes": 9,
      "edges": 9,
      "source_file": "rg05-sensor-fusion.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg05-sensor-fusion.json",
      "svg": "gallery/atlas/rg05-sensor-fusion.svg",
      "png": "gallery/atlas/rg05-sensor-fusion.png",
      "pdf": "gallery/atlas/rg05-sensor-fusion.pdf",
      "tex": "gallery/atlas/rg05-sensor-fusion.tex"
    },
    {
      "id": "rg06-graph-message-passing",
      "title": "Graph message passing",
      "family": "robotics-graphs",
      "description": "A true local graph neighborhood accompanies explicit edge-message, symmetric aggregation, and node-update equations.",
      "caption": "Conceptual MPNN update after Gilmer et al. (2017); the same local rule is applied across graph nodes.",
      "sources": [
        "https://arxiv.org/abs/1704.01212"
      ],
      "assumptions": [
        "The small graph and sum aggregator are illustrative instances of the MPNN framework.",
        "Undirected context edges are shown without arrows; directed arrows indicate messages into the selected node only."
      ],
      "tags": [
        "graph-learning",
        "message-passing",
        "aggregation",
        "gnn"
      ],
      "nodes": 8,
      "edges": 8,
      "source_file": "rg06-graph-message-passing.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg06-graph-message-passing.json",
      "svg": "gallery/atlas/rg06-graph-message-passing.svg",
      "png": "gallery/atlas/rg06-graph-message-passing.png",
      "pdf": "gallery/atlas/rg06-graph-message-passing.pdf",
      "tex": "gallery/atlas/rg06-graph-message-passing.tex"
    },
    {
      "id": "rg07-graph-attention",
      "title": "Graph attention",
      "family": "robotics-graphs",
      "description": "A masked graph neighborhood, self-attention loop, local softmax, and parallel attention-head fanout/merge.",
      "caption": "Conceptual GAT layer after Veličković et al. (2018); each head normalizes attention over the permitted neighborhood.",
      "sources": [
        "https://arxiv.org/abs/1710.10903"
      ],
      "assumptions": [
        "The depicted layer uses concatenated heads; the source also describes head averaging in a final layer.",
        "Self-loops are included in the conceptual permitted neighborhood.",
        "Head count and graph size are symbolic rather than a reported benchmark configuration."
      ],
      "tags": [
        "graph-learning",
        "attention",
        "gat",
        "multihead"
      ],
      "nodes": 10,
      "edges": 9,
      "source_file": "rg07-graph-attention.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg07-graph-attention.json",
      "svg": "gallery/atlas/rg07-graph-attention.svg",
      "png": "gallery/atlas/rg07-graph-attention.png",
      "pdf": "gallery/atlas/rg07-graph-attention.pdf",
      "tex": "gallery/atlas/rg07-graph-attention.tex"
    },
    {
      "id": "rg08-graph-readout",
      "title": "Graph-level readout",
      "family": "robotics-graphs",
      "description": "An encoded graph is treated as an unordered set of node states and pooled into a graph embedding and graph-level output.",
      "caption": "Conceptual graph readout after Gilmer et al. (2017); a symmetric set aggregation produces one graph representation.",
      "sources": [
        "https://arxiv.org/abs/1704.01212"
      ],
      "assumptions": [
        "The sum-of-transformed-states readout is an illustrative invariant instance, not the complete readout used in every MPNN.",
        "Only node states are visualized; tasks may also use edge or global attributes."
      ],
      "tags": [
        "graph-learning",
        "readout",
        "graph-level",
        "permutation-invariance"
      ],
      "nodes": 12,
      "edges": 12,
      "source_file": "rg08-graph-readout.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg08-graph-readout.json",
      "svg": "gallery/atlas/rg08-graph-readout.svg",
      "png": "gallery/atlas/rg08-graph-readout.png",
      "pdf": "gallery/atlas/rg08-graph-readout.pdf",
      "tex": "gallery/atlas/rg08-graph-readout.tex"
    },
    {
      "id": "rg09-heterogeneous-graph",
      "title": "Heterogeneous graph network",
      "family": "robotics-graphs",
      "description": "A typed author/paper/venue graph is paired with three relation-specific message channels and a self-term node update.",
      "caption": "Conceptual relational GNN after Schlichtkrull et al. (2018); each relation has its own transform before node aggregation.",
      "sources": [
        "https://arxiv.org/abs/1703.06103"
      ],
      "assumptions": [
        "The author/paper/venue schema is an original illustrative graph, not a source benchmark.",
        "Inverse published-in relations are explicitly assumed to permit venue-to-paper messages.",
        "Relation normalization c_(i,r) is symbolic and each sum is restricted to the named incoming relation; basis decomposition and training objectives are omitted."
      ],
      "tags": [
        "graph-learning",
        "heterogeneous-graph",
        "relations",
        "rgcn"
      ],
      "nodes": 9,
      "edges": 8,
      "source_file": "rg09-heterogeneous-graph.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg09-heterogeneous-graph.json",
      "svg": "gallery/atlas/rg09-heterogeneous-graph.svg",
      "png": "gallery/atlas/rg09-heterogeneous-graph.png",
      "pdf": "gallery/atlas/rg09-heterogeneous-graph.pdf",
      "tex": "gallery/atlas/rg09-heterogeneous-graph.tex"
    },
    {
      "id": "rg10-spatiotemporal-graph",
      "title": "Spatiotemporal graph forecasting",
      "family": "robotics-graphs",
      "description": "A graph-by-time lattice feeds an encoder state, a recurrent decoder, and a node-by-horizon forecast grid.",
      "caption": "Conceptual graph-recurrent forecasting after Li et al. (2018); topology and temporal state inform node forecasts.",
      "sources": [
        "https://arxiv.org/abs/1707.01926"
      ],
      "assumptions": [
        "The three-node chain, three observed times, and two forecast steps are illustrative and not DCRNN's reported dimensions.",
        "Cells denote hidden states; per-time observation injection, diffusion filters, gates, and scheduled sampling are omitted.",
        "Undirected vertical lines abstract spatial neighborhoods; the source DCRNN uses directed-graph diffusion.",
        "This is a conceptual family diagram rather than an exact DCRNN computational graph."
      ],
      "tags": [
        "graph-learning",
        "spatiotemporal",
        "forecasting",
        "graph-recurrent"
      ],
      "nodes": 17,
      "edges": 16,
      "source_file": "rg10-spatiotemporal-graph.tex",
      "width_cm": 16,
      "height_cm": 9,
      "mode": "native-tikz",
      "source": "gallery/atlas/rg10-spatiotemporal-graph.json",
      "svg": "gallery/atlas/rg10-spatiotemporal-graph.svg",
      "png": "gallery/atlas/rg10-spatiotemporal-graph.png",
      "pdf": "gallery/atlas/rg10-spatiotemporal-graph.pdf",
      "tex": "gallery/atlas/rg10-spatiotemporal-graph.tex"
    }
  ]
};
