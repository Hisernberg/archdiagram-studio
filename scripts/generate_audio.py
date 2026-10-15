#!/usr/bin/env python3
"""Generate 20 original, conceptual, monochrome audio architecture plates."""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/draw-architecture/scripts"))
from atlaslib import Figure

OUT = ROOT / "skills/draw-architecture/assets/atlas/audio"
INDEX = []

SOURCES = {
    "stft": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html",
    "cnn": "https://arxiv.org/abs/1912.10211",
    "ctc": "https://www.cs.toronto.edu/~graves/icml_2006.pdf",
    "rnnt": "https://arxiv.org/abs/1211.3711",
    "las": "https://arxiv.org/abs/1508.01211",
    "conformer": "https://arxiv.org/abs/2005.08100",
    "whisper": "https://cdn.openai.com/papers/whisper.pdf",
    "w2v": "https://arxiv.org/abs/2006.11477",
    "hubert": "https://arxiv.org/abs/2106.07447",
    "xvector": "https://www.danielpovey.com/files/2018_icassp_xvectors.pdf",
    "diarization": "https://arxiv.org/abs/2012.14952",
    "tacotron": "https://arxiv.org/abs/1712.05884",
    "fastspeech": "https://arxiv.org/abs/2006.04558",
    "vits": "https://arxiv.org/abs/2106.06103",
    "hifigan": "https://arxiv.org/abs/2010.05646",
    "diffwave": "https://arxiv.org/abs/2009.09761",
    "enhance": "https://arxiv.org/abs/2008.00264",
    "codec": "https://arxiv.org/abs/2107.03312",
}


def plate(title, caption, height=9):
    return Figure(title, 16, height,
                  subtitle="Audio and speech atlas | Original conceptual schematic",
                  caption=caption)


def save(f, ident, description, keys, assumptions=None, tags=None):
    notes = ["Conceptual original schematic; layer counts, widths, and signal lengths are illustrative."]
    notes.extend(assumptions or [])
    INDEX.append(f.write(OUT, ident, "audio", description,
                         [SOURCES[k] for k in keys], notes, tags or []))


def label(f, text, x, y, width=4, size="scriptsize", color="ink", anchor="center"):
    # Preserve normal mathematical spacing inside TikZ text-width paragraphs.
    text = re.sub(r"\$[^$]*\$", lambda m: r"\mbox{" + m.group() + "}", text)
    f.raw(r"\node[align=center,anchor=" + anchor + ",font=\\" + size + ",text=" + color +
          f",text width={width}cm] at ({x},{y}) {{{text}}};")


def wave(f, x, y, width, amplitude=.4, phase=0, noise=False):
    pts = []
    for i in range(201):
        t = i / 200
        envelope = .32 + .52 * math.sin(math.pi * t) ** 2
        value = math.sin(2 * math.pi * (8 * t + 2 * t * t) + phase)
        value += .25 * math.sin(2 * math.pi * 29 * t + .7)
        if noise:
            value += .24 * math.sin(2 * math.pi * 53 * t + 1.1)
        pts.append(f"({x + width * t:.3f},{y + amplitude * envelope * value:.3f})")
    f.raw(r"\draw[soft,line width=.35pt] " + f"({x},{y}) -- ({x+width},{y});")
    f.raw(r"\draw[ink,line width=.55pt] plot coordinates {" + " ".join(pts) + "};")


def grid(f, x, y, width, height, cols=12, rows=8, outline=True):
    """An original illustrative energy map, explicitly not measured audio."""
    cw, rh = width / cols, height / rows
    for c in range(cols):
        for r in range(rows):
            val = 8 + int(74 * abs(math.sin(.64 * c + .39 * r) * math.cos(.73 * r - .21 * c)))
            f.raw(f"\\fill[black!{val}] ({x+c*cw:.3f},{y+r*rh:.3f}) rectangle "
                  f"({x+(c+1)*cw:.3f},{y+(r+1)*rh:.3f});")
    if outline:
        f.raw(f"\\draw[ink,line width=.5pt] ({x},{y}) rectangle ({x+width},{y+height});")


def arrow(f, points, text="", at=None, style=""):
    f.raw(r"\draw[flow" + style + "] " + " -- ".join(f"({x},{y})" for x, y in points) + ";")
    if text and at:
        label(f, text, at[0], at[1], 3, color="soft")


# 01 -- waveform framing: overlapping windows and separate local coordinates.
f = plate("Waveform framing and windowing", "Overlapping slices preserve local time structure before spectral analysis.")
wave(f, 1.0, 2.65, 14, .62)
label(f, r"Sampled waveform $x[n]$", 1.8, 1.6, 2.5)
for i, start in enumerate((2.5, 5.0, 7.5)):
    f.raw(f"\\draw[ink,{'dashed,' if i else ''}line width=.6pt] ({start},1.95) rectangle ({start+4},3.35);")
    label(f, f"$m={i}$", start + 2, 3.65, 1)
arrow(f, [(5, 1.78), (7.5, 1.78)], r"hop $H$", (6.25, 1.5))
for i, x in enumerate((3, 8, 13)):
    f.node(f"frame{i}", rf"Frame $m={i}$\\$x_m[n]=x[n+{i}H]$", x, 5.0, 3.7, .95, "tensor")
    arrow(f, [(4.5+2.5*i, 3.4), (4.5+2.5*i, 4.0), (x,4.0), (x,4.52)])
    wave(f, x-1.55, 6.65, 3.1, .45, i*.8)
    # The enclosing smooth window is a conceptual Hann window, not data.
    pts = " ".join(f"({x-1.55+3.1*j/60:.3f},{6.65-.78*math.sin(math.pi*j/60)**2:.3f})" for j in range(61))
    f.raw(r"\draw[soft,dashed,line width=.5pt] plot coordinates {"+pts+"};")
    label(f, r"$0\leq n<L$", x, 7.3, 2)
label(f, r"Windowed frame: $\widetilde{x}_m[n]=w[n]x[n+mH]$,\quad $0<H<L$", 8, 8.0, 14, "small")
save(f, "audio-01-waveform-framing", "Overlapping sampled frames and a shared window in local frame coordinates.", ["stft"],
     ["Displayed waveforms and windows are illustrative; no sampling rate or frame length is asserted."], ["waveform", "framing", "window"])

# 02 -- STFT has a mathematical operator and a time-frequency output.
f = plate("Short-time Fourier transform", "One DFT per windowed frame becomes one column in a time--frequency array.")
wave(f, .8, 2.7, 3.5, .55)
label(f, r"$x[n]$", 2.5, 3.55, 2)
f.node("frames", r"Frame and window\\$\widetilde{x}_m[n]$", 6, 2.7, 2.5, 1)
f.node("dft", r"DFT over $n$\\$X[m,k]$", 9.4, 2.7, 2.5, 1)
f.node("mag", r"Magnitude or power\\$|X[m,k]|^p$", 13.1, 2.7, 2.8, 1)
arrow(f, [(4.35,2.7),(4.75,2.7)])
f.edge("frames", "dft")
f.edge("dft", "mag")
grid(f, 9.1, 4.8, 5.5, 2.65, 16, 10)
arrow(f, [(13.1,3.2),(13.1,4.2),(11.85,4.2),(11.85,4.7)])
f.raw(r"\draw[ink,dashed,line width=.7pt] (11.16,4.75) rectangle (11.51,7.5);")
arrow(f, [(9.1,7.7),(14.6,7.7)], "$m$ (time)", (11.9,8.0))
arrow(f, [(8.8,7.45),(8.8,4.8)], "$k$", (8.35,6.1))
label(f, r"$X[m,k]=\displaystyle\sum_{n=0}^{L-1}x[n+mH]w[n]e^{-j2\pi kn/L}$", 4.35, 5.8, 7.8, "small")
label(f, r"Column $m$: spectrum of one local frame", 4.3, 7.1, 7, color="soft")
save(f, "audio-02-stft-spectrogram", "Windowed Fourier analysis maps time samples into a spectrogram grid.", ["stft"],
     ["The energy grid is synthetic. The exponent p may be 1 (magnitude) or 2 (power)."], ["STFT", "spectrogram", "Fourier"])

# 03 -- local receptive fields, changing map geometry, and global clip tagging.
f = plate("Spectrogram convolutional classifier", "Local time--frequency filters feed progressively pooled features and clip-level tags.")
grid(f, .8, 2.15, 3.3, 3.5, 11, 10)
f.raw(r"\draw[white,line width=1.6pt] (1.4,3.2) rectangle (2.3,4.25);\draw[ink,line width=.6pt] (1.4,3.2) rectangle (2.3,4.25);")
f.node("spec", "", 2.45, 3.9, 3.3, 3.5, "plain")
label(f, r"Log-mel input\\$T\times F$", 2.45, 6.2, 3.5)
f.node("conv1", r"Conv\\BN\\ReLU", 5.65, 3.9, 1.7, 2.6, "tensor")
f.node("conv2", r"Conv\\pool", 8.15, 3.9, 1.7, 1.95, "tensor")
f.node("conv3", r"Conv\\pool", 10.65, 3.9, 1.7, 1.25, "tensor")
f.node("global", r"Global pooling\\over time and frequency", 13.65, 3.9, 2.6, 1.15)
f.node("tags", r"Linear + sigmoid\\$p(\text{tag}_i\mid x)$", 13.65, 6.4, 2.6, 1.05)
for a,b in [("spec","conv1"),("conv1","conv2"),("conv2","conv3"),("conv3","global"),("global","tags")]:
    f.edge(a,b)
label(f, r"A shared kernel scans local patches", 5.1, 1.75, 5, color="soft")
label(f, r"Spatial extent decreases; learned channels need not decrease", 8.2, 7.7, 10, color="soft")
save(f, "audio-03-spectrogram-cnn", "A conceptual PANNs-inspired spectrogram CNN for multilabel audio tagging.", ["cnn"],
     ["This is a generic spectrogram CNN, not the exact CNN14 layer inventory. Tensor depths are illustrative."], ["CNN", "audio tagging", "receptive field"])

# 04 -- explicit CTC path, collapse, and sum over possible alignments.
f = plate("CTC speech recognition", "CTC sums frame paths during training; a collapse map removes repeats and blank symbols.")
f.node("input", r"Acoustic frames\\$x_{1:T}$", 2, 2.2, 2.6, .9, "tensor")
f.node("encoder", r"Sequence encoder", 5.6, 2.2, 2.7, .9)
f.node("post", r"Frame posteriors\\$p(\pi_t\mid x)$", 9.4, 2.2, 2.9, .9)
f.node("loss", r"CTC loss\\$-\log p(y\mid x)$", 13.4, 2.2, 2.9, .9)
for a,b in [("input","encoder"),("encoder","post"),("post","loss")]: f.edge(a,b)
tokens = [r"\varnothing", "c", "c", r"\varnothing", "a", "a", "t", r"\varnothing"]
for i,tok in enumerate(tokens):
    x = 1.4 + 1.85*i
    f.raw(f"\\draw[ink,fill={'wash' if tok==r'\varnothing' else 'white'}] ({x-.68},4.15) rectangle ({x+.68},5.15);")
    label(f, f"${tok}$", x, 4.65, 1, "small")
    label(f, f"$t={i+1}$", x, 5.5, 1)
arrow(f, [(9.4,2.65),(9.4,3.5),(7.9,3.5),(7.9,4.05)])
label(f, r"One possible frame path $\pi$", 3.2, 3.7, 5, color="soft")
f.node("collapse", r"Collapse $\mathcal{B}$", 7.9, 6.4, 3.2, .7)
f.node("text", r"$y=\texttt{cat}$", 12.2, 6.4, 2.6, .7, "plain")
arrow(f, [(7.9,5.65),(7.9,6.0)])
f.edge("collapse","text")
label(f, r"$p(y\mid x)=\displaystyle\sum_{\pi:\,\mathcal{B}(\pi)=y}\prod_{t=1}^{T}p(\pi_t\mid x)$", 8, 7.8, 14, "small")
save(f, "audio-04-ctc-recognition", "Framewise CTC probabilities, an explicit repeated-and-blank path, and the collapse map.", ["ctc"],
     ["The displayed path is illustrative; recognition may use beam search rather than greedy decoding."], ["ASR", "CTC", "alignment"])

# 05 -- two input axes and the transducer alignment lattice.
f = plate("RNN-T transducer", "The joint distribution depends on both acoustic time and the emitted-label prefix.")
f.node("audio", r"Acoustic frames\\$x_{1:T}$", 1.9, 2.2, 2.6, .85, "tensor")
f.node("encoder", r"Encoder\\$h_t$", 5.2, 2.2, 2.6, .85)
f.node("prefix", r"Label prefix\\$y_{<u}$", 1.9, 4.2, 2.6, .85, "tensor")
f.node("predict", r"Prediction network\\$g_u$", 5.2, 4.2, 2.6, .85)
f.node("joint", r"Joint network\\$h_t,g_u$", 8.9, 3.2, 2.6, 1.1)
f.node("dist", r"Softmax\\$p(k\mid t,u)$", 12.9, 3.2, 2.8, 1.1)
for a,b in [("audio","encoder"),("prefix","predict"),("encoder","joint"),("predict","joint"),("joint","dist")]: f.edge(a,b)
label(f, r"Blank: advance acoustic time $t$\\Label: extend prefix, advance $u$", 3.9, 6.4, 6.5, "small")
for i in range(5):
    for j in range(3):
        x,y=8.8+1.25*i,7.55-.75*j
        f.raw(f"\\fill[ink] ({x},{y}) circle (.045);")
        if i<4: arrow(f,[(x+.08,y),(x+1.17,y)],style=",draw=soft")
        if j<2: arrow(f,[(x,y-.08),(x,y-.67)],style=",draw=soft")
arrow(f, [(8.8,7.55),(10.05,7.55),(10.05,6.8),(11.3,6.8),(12.55,6.8),(12.55,6.05),(13.8,6.05)], style=",line width=1.2pt")
label(f, r"$t\rightarrow$", 11.3, 8.05, 3)
label(f, r"$u$", 8.35, 6.8, .5)
label(f, r"Alignment lattice (one path emphasized)", 11.4, 5.45, 6, color="soft")
save(f, "audio-05-rnnt-transducer", "Acoustic encoder and label-prefix predictor meet at a joint distribution over blank and labels.", ["rnnt"],
     ["The small lattice is illustrative. Blank transitions move right and label transitions move upward."], ["ASR", "RNN-T", "lattice"])

# 06 -- listener memory, attention context, and autoregressive speller state.
f = plate("Attention-based speech recognition", "A listener encodes audio; the speller queries its memory for each output character.")
f.group("Listener", .7, 1.55, 5.5, 4.9)
f.node("features", r"Filter-bank features", 3.45, 2.4, 4.4, .8, "tensor")
f.node("listener", r"Pyramidal recurrent encoder", 3.45, 3.95, 4.4, .95)
f.node("memory", r"$h_1\quad h_2\quad\cdots\quad h_{T'}$", 3.45, 5.55, 4.4, .8, "tensor")
f.node("attn", r"Attention\\$\alpha_{u,t}$", 8.35, 4.4, 2.35, .95)
f.node("context", r"Context\\$c_u=\sum_t\alpha_{u,t}h_t$", 11.9, 4.4, 3.0, .95)
f.node("decoder", r"Recurrent speller\\state $s_u$", 11.9, 6.5, 3.0, .95)
f.node("prev", r"Previous character\\$y_{u-1}$", 8.35, 6.5, 2.35, .95)
f.node("char", r"Character\\$y_u$", 14.85, 6.5, 1.8, .85, "plain")
for a,b in [("features","listener"),("listener","memory"),("memory","attn"),("attn","context"),("context","decoder"),("prev","decoder"),("decoder","char")]: f.edge(a,b)
f.edge("decoder","attn",side="north",to_side="north",via=[(11.9,5.5),(14.0,5.5),(14.0,3.0),(8.35,3.0)],style="feedback")
f.edge("char","prev",side="south",to_side="south",via=[(14.85,7.4),(8.35,7.4)],style="feedback")
label(f, r"query from previous state $s_{u-1}$", 11.3, 2.65, 6, color="soft")
label(f, r"$p(y\mid x)=\prod_u p(y_u\mid y_{<u},x)$", 8.1, 7.95, 13, "small")
save(f, "audio-06-attention-asr", "A LAS-inspired listener, attention memory, and recurrent character speller.", ["las"],
     ["The listener is conceptual; its pyramid depth and temporal reduction factor are omitted."], ["ASR", "attention", "LAS"])

# 07 -- four residual sublayers and a convolutional submodule callout.
f = plate("Conformer encoder block", "Macaron feed-forward halves surround global self-attention and a local convolution module.")
f.node("input", r"$x$", .5, 3.0, .8, .65, "plain")
stages=[("ff1",r"$\tfrac12\,\mathrm{FFN}$",2.05,3.55),("mhsa",r"Multi-head\\self-attention",5.25,6.75),("conv",r"Convolution\\module",8.45,9.95),("ff2",r"$\tfrac12\,\mathrm{FFN}$",11.65,13.15)]
prev="input"
for name,txt,x,sx in stages:
    f.node(name,txt,x,3.0,2.05,.95)
    f.node(name+"sum",r"$+$",sx,3.0,.55,.55,"circle")
    f.edge(prev,name)
    f.edge(name,name+"sum")
    originx = .95 if prev=="input" else f.nodes[prev].x+.43
    arrow(f,[(originx,3.0),(originx,1.8),(sx,1.8),(sx,2.64)],style=",dashed")
    prev=name+"sum"
f.node("ln",r"Layer\\norm",14.2,3.0,1.05,.95)
f.node("out",r"$y$",15.35,3.0,.8,.65,"plain")
f.edge(prev,"ln");f.edge("ln","out")
for i,x in enumerate((3.55,6.75,9.95),1):label(f,rf"$x_{i}$",x,3.7,1)
f.group("Convolution module detail",2.55,4.55,12.8,1.95)
detail=[("cln",r"Layer norm",3.8,1.8),("glu",r"Pointwise\\conv + GLU",6.35,2.2),("dw",r"Depthwise\\conv",9.1,2.2),("bn",r"Batch norm\\+ Swish",11.85,2.2),("pw",r"Pointwise\\conv",14.3,1.6)]
for name,txt,x,w in detail:f.node(name,txt,x,5.55,w,.95)
for a,b in zip(detail,detail[1:]):f.edge(a[0],b[0])
f.edge("conv","dw",side="south",to_side="north",via=[(8.45,4.1),(9.1,4.1)],style="control")
label(f, r"$y=\mathrm{LN}\!\left(x_3+\tfrac12\mathrm{FFN}(x_3)\right)$", 8, 7.45, 12, "small")
label(f, "Dropout and internal normalization details are suppressed outside the callout.", 8, 8.05, 13, color="soft")
save(f,"audio-07-conformer-block","A Conformer block with explicit residual origins, half-step FFNs, and expanded convolution module.",["conformer"],
     ["Pre-normalization is implicit in the attention and FFN boxes. The convolution callout omits dropout."],["Conformer","residual","convolution"])

# 08 -- encoder-decoder with distinct audio memory and task-prefix inputs.
f = plate("Whisper-style encoder--decoder", "Audio memory conditions a causal text decoder; task tokens select the decoding objective.")
wave(f,.9,2.2,3.1,.5)
f.node("mel",r"Log-mel\\spectrogram",2.45,4.1,2.9,1.0,"tensor")
arrow(f,[(2.45,2.85),(2.45,3.55)])
f.group("Audio encoder",4.7,1.55,3.6,4.9)
f.node("conv",r"Convolutional\\frontend",6.5,2.55,2.8,.95)
f.node("pos",r"Add position\\information",6.5,4.05,2.8,.85)
f.node("enc",r"Transformer\\encoder",6.5,5.55,2.8,.95)
f.edge("mel","conv",side="east",to_side="west",via=[(4.25,4.1),(4.25,2.55)])
f.edge("conv","pos");f.edge("pos","enc")
f.group("Causal text decoder",9.0,1.55,6.2,4.9)
f.node("tokens",r"Task prefix and\\previous tokens $y_{<u}$",12.1,2.55,4.6,.95,"tensor")
f.node("embed",r"Token + position\\embeddings",12.1,4.05,4.6,.85)
f.node("dec",r"Masked self-attention\\Cross-attention to audio\\Feed-forward network",12.1,5.55,4.6,1.05)
f.node("out",r"Text / timestamp tokens\\$p(y_u\mid y_{<u},x)$",12.1,7.5,4.6,.95)
f.edge("tokens","embed");f.edge("embed","dec");f.edge("enc","dec",label="audio memory")
f.edge("dec","out")
f.edge("out","tokens",side="east",to_side="east",via=[(15.6,7.5),(15.6,2.55)],style="feedback")
label(f, "Depth, head counts, and vocabulary are intentionally unspecified.",5.4,7.65,7,color="soft")
save(f,"audio-08-whisper-encoder-decoder","A conceptual Whisper-style audio encoder and autoregressive task-conditioned text decoder.",["whisper"],
     ["This is an architecture overview. Exact model sizes and positional-embedding choices are omitted."],["Whisper","ASR","encoder-decoder"])

# 09 -- learned quantized targets branch before latent span masking.
f=plate("wav2vec 2.0 pretraining","Latent span masking feeds contextual prediction; an unmasked branch supplies learned quantized targets.")
f.node("wave",r"Raw audio\\$x$",1.9,2.2,2.6,.85,"tensor")
f.node("cnn",r"Convolutional\\feature encoder",5.2,2.2,2.7,.95)
f.node("latent",r"Latent sequence\\$z_{1:T}$",8.7,2.2,2.7,.85,"tensor")
f.node("mask",r"Mask spans\\of $z_t$",8.7,4.25,2.7,.85)
f.node("context",r"Context Transformer\\$c_{1:T}$",12.5,4.25,3.0,.95)
f.node("quant",r"Learned product\\quantization",4.5,6.6,3.0,1.0)
f.node("target",r"Target $q_t$ and\\distractor targets",8.5,6.6,3.0,1.0,"tensor")
f.node("loss",r"Contrastive loss\\at masked steps",12.5,6.6,3.0,1.0)
for a,b in [("wave","cnn"),("cnn","latent"),("latent","mask"),("mask","context"),("quant","target"),("target","loss"),("context","loss")]:f.edge(a,b)
f.edge("latent","quant",side="south",to_side="north",via=[(8.7,3.25),(4.5,3.25)],label="unmasked latents")
label(f,r"Codebook diversity regularization",4.5,7.8,5,color="soft")
label(f,r"$c_t$ identifies the true $q_t$ among distractors",10.8,8.05,8,color="soft")
save(f,"audio-09-wav2vec2-pretraining","Latent masking, contextual representations, product-quantized contrastive targets, and diversity regularization.",["w2v"],
     ["Only the pretraining graph is shown. Codebook counts and distractor-sampling details are omitted."],["self-supervised","wav2vec2","contrastive"])

# 10 -- offline teacher and masked student are separate computation lanes.
f=plate("HuBERT masked-unit pretraining","An offline clustering teacher supplies discrete units; the student predicts masked units from context.")
f.group("Offline target generation",.7,1.55,14.6,2.0)
top=[("audioT",r"Unlabelled audio",2.3,2.55), ("feat",r"Acoustic features\\or prior hidden states",5.8,2.55), ("cluster",r"Offline $k$-means",9.3,2.55), ("units",r"Discrete unit targets\\$q_{1:T}$",12.8,2.55)]
for name,txt,x,y in top:f.node(name,txt,x,y,2.8,.95,"tensor" if name in {"audioT","units"} else "block")
for a,b in zip(top,top[1:]):f.edge(a[0],b[0])
f.group("Masked prediction student",.7,4.65,14.6,2.1)
bot=[("audioS",r"Same audio",2.3,5.7),("cnn",r"Convolutional\\feature encoder",5.8,5.7),("mask",r"Mask latent spans",9.3,5.7),("trans",r"Transformer\\unit prediction",12.8,5.7)]
for name,txt,x,y in bot:f.node(name,txt,x,y,2.8,.95,"tensor" if name=="audioS" else "block")
for a,b in zip(bot,bot[1:]):f.edge(a[0],b[0])
f.node("loss",r"Masked-step cross-entropy\\$-\sum_{t\in M}\log p(q_t\mid \widetilde{x})$",10.8,7.9,5.0,.85)
f.edge("trans","loss",side="south",to_side="north",via=[(12.8,7.15),(10.8,7.15)])
f.edge("units","loss",side="east",to_side="east",via=[(15.65,2.55),(15.65,7.9)])
f.edge("trans","feat",side="north",to_side="south",via=[(12.8,4.05),(5.8,4.05)],style="feedback")
label(f,"Optional next clustering round",9.25,3.82,6,color="soft")
label(f,"Teacher labels are fixed within a round.",4.0,7.85,5.6,color="soft")
save(f,"audio-10-hubert-pretraining","Offline discrete-unit clustering and masked student prediction with optional iterative reclustering.",["hubert"],
     ["The teacher feature type changes across training iterations; one generic offline lane represents these choices."],["HuBERT","self-supervised","masked prediction"])

# 11 -- x-vector statistics pooling and distinct training / comparison uses.
f=plate("Speaker embedding with statistics pooling","Frame-level representations become a fixed-size segment embedding through mean and standard-deviation pooling.")
f.node("features",r"Variable-length\\speech features",1.8,3.1,2.5,1.0,"tensor")
f.node("tdnn",r"Frame-level\\TDNN stack",5.0,3.1,2.6,1.0)
f.node("mean",r"Temporal mean\\$\mu=\frac1T\sum_t h_t$",8.2,2.25,2.7,1.0)
f.node("std",r"Temporal std.\\$\sigma=\sqrt{\frac1T\sum_t(h_t-\mu)^2}$",8.2,4.05,2.7,1.0)
f.node("concat",r"Concatenate\\$[\mu;\sigma]$",11.45,3.1,2.3,1.0)
f.node("embed",r"Segment layers\\embedding $e$",14.3,3.1,2.4,1.0,"tensor")
f.edge("features","tdnn");f.edge("tdnn","mean");f.edge("tdnn","std")
f.edge("mean","concat");f.edge("std","concat");f.edge("concat","embed")
f.node("enroll",r"Enrollment\\embedding $e'$",7.7,6.2,2.6,.95,"tensor")
f.node("score",r"Similarity /\\backend scoring",11.45,6.2,2.7,.95)
f.node("decision",r"Same-speaker\\score",14.3,6.2,2.4,.95)
f.node("train",r"Speaker-ID classifier (training)",11.9,7.9,5.9,.7)
f.edge("enroll","score");f.edge("embed","score",side="south",to_side="north",via=[(14.3,4.95),(11.45,4.95)])
f.edge("score","decision")
f.edge("embed","train",side="east",to_side="east",via=[(15.8,3.1),(15.8,7.9)],style="control")
label(f,"Utterance duration changes $T$, not embedding size.",4.2,7.75,7,color="soft")
save(f,"audio-11-speaker-embedding","An x-vector-style TDNN, temporal statistics pooling, segment embedding, and scoring backend.",["xvector"],
     ["The diagram does not prescribe a particular scoring backend. The classifier is training-only."],["speaker recognition","x-vector","statistics pooling"])

# 12 -- diarization culminates in a multi-row temporal annotation.
f=plate("Speaker diarization by embedding clustering","Speech turns are segmented, embedded, clustered, and placed back on the recording timeline.")
nodes=[("audio",r"Recording",1.65),("vad",r"Voice activity\\detection",4.8),("seg",r"Speech windows",7.95),("emb",r"Speaker\\embeddings",11.1),("cluster",r"Cluster +\\temporal refine",14.25)]
for name,txt,x in nodes:f.node(name,txt,x,2.35,2.6,.95,"tensor" if name=="audio" else "block")
for a,b in zip(nodes,nodes[1:]):f.edge(a[0],b[0])
wave(f,1.8,4.2,12.6,.35)
arrow(f,[(1.8,4.75),(14.4,4.75)],"recording time",(8.1,5.03))
turns={"A":[(1.8,4.4),(9.1,11.5)],"B":[(4.4,6.9),(12.1,14.4)],"C":[(7.2,9.1)]}
for row,(spk,intervals) in enumerate(turns.items()):
    y=5.7+.85*row
    label(f,"Speaker "+spk,.85,y,1.6)
    f.raw(f"\\draw[soft,line width=.3pt] (1.8,{y+.28}) -- (14.4,{y+.28});")
    for a,b in intervals:
        f.raw(f"\\draw[ink,fill=black!{12+row*13}] ({a},{y-.23}) rectangle ({b},{y+.23});")
f.edge("cluster","emb",side="south",to_side="south",via=[(14.25,3.35),(11.1,3.35)],style="feedback",label="refine assignments",label_side="below")
arrow(f,[(14.25,2.83),(15.65,2.83),(15.65,7.8),(14.4,7.8)])
label(f,"Gaps represent non-speech; letter labels are recording-local identities.",8.2,8.15,13,color="soft")
save(f,"audio-12-speaker-diarization","A conceptual embedding-clustering diarization pipeline and speaker activity timeline.",["diarization"],
     ["The timeline is invented. Overlapping speech handling is outside this simplified clustering schematic."],["diarization","timeline","clustering"])

# 13 -- two-stage synthesis overview with explicit conditioning branches.
f=plate("Text-to-speech: two-stage synthesis","A linguistic frontend and acoustic model predict an intermediate representation for a neural vocoder.")
main=[("text",r"Text",1.5,1.8),("front",r"Normalize text\\and phonemize",4.35,2.6),("acoustic",r"Acoustic model",7.75,2.7),("mel",r"Mel frames",10.8,2.0),("vocoder",r"Neural vocoder",13.65,2.6)]
for name,txt,x,w in main:f.node(name,txt,x,3.0,w,1.0,"tensor" if name in {"text","mel"} else "block")
for a,b in zip(main,main[1:]):f.edge(a[0],b[0])
f.node("speaker",r"Speaker / style\\conditioning",4.35,6.2,2.8,1.0)
f.node("prosody",r"Duration, pitch,\\and energy controls",7.75,6.2,2.8,1.0)
f.edge("speaker","acoustic",side="north",to_side="south",via=[(4.35,4.8),(7.15,4.8)],style="control")
f.edge("prosody","acoustic",side="north",to_side="south",style="control")
wave(f,11.55,6.25,3.9,.6)
arrow(f,[(13.65,3.5),(13.65,5.35)])
label(f,r"Waveform $\widehat{x}[n]$",13.5,7.3,3.7,"small")
label(f,"Conditioning is model-dependent and may be implicit.",5.8,7.8,8,color="soft")
save(f,"audio-13-tts-overview","A two-stage text-to-speech overview with linguistic, acoustic, and waveform-generation interfaces.",["tacotron","fastspeech"],
     ["Phonemization and explicit prosody controls are common design choices, not claims about all TTS systems."],["TTS","vocoder","conditioning"])

# 14 -- attention TTS emphasizes output-frame feedback, distinct from ASR.
f=plate("Tacotron-style attention TTS","An autoregressive acoustic decoder attends to text memory and feeds back the preceding mel frame.")
f.node("text",r"Characters",1.65,2.65,2.2,.95,"tensor")
f.node("encoder",r"Embedding +\\text encoder",4.65,2.65,2.6,.95)
f.node("memory",r"Text states\\$h_{1:N}$",7.85,2.65,2.5,.95,"tensor")
f.node("attn",r"Location-sensitive\\attention",11.0,2.65,2.6,.95)
f.node("context",r"Text context\\$c_t$",14.1,2.65,2.3,.95,"tensor")
f.node("prenet",r"Pre-net",7.85,5.15,2.5,.95)
f.node("decoder",r"Recurrent acoustic\\decoder",11.0,5.15,2.6,1.0)
f.node("mel",r"Predicted mel\\frame $m_t$",14.1,5.15,2.3,1.0,"tensor")
f.node("previous",r"Previous frame\\$m_{t-1}$",7.85,7.35,2.5,.95,"tensor")
f.node("post",r"Post-net residual\\refinement",14.1,7.35,2.3,.95)
for a,b in [("text","encoder"),("encoder","memory"),("memory","attn"),("attn","context"),("previous","prenet"),("prenet","decoder"),("decoder","mel")]:f.edge(a,b)
f.edge("decoder","attn",side="north",to_side="south",label="previous state",style="feedback")
f.edge("context","decoder",side="south",to_side="east",via=[(14.1,4.0),(12.8,4.0),(12.8,5.15)])
f.edge("mel","previous",side="south",to_side="east",via=[(14.1,6.25),(10.0,6.25),(10.0,7.35)],style="feedback")
f.edge("mel","post",side="east",to_side="east",via=[(15.65,5.15),(15.65,7.35)])
label(f,"Training may use teacher forcing; inference uses generated frames.",3.9,6.7,6.6,color="soft")
label(f,"A waveform vocoder follows the refined mel sequence.",3.9,7.65,6.6,color="soft")
save(f,"audio-14-tacotron-attention-tts","Text-memory attention, recurrent mel decoding, pre-net feedback, and post-net refinement.",["tacotron"],
     ["Stop-token prediction, decoder frame grouping, and the downstream vocoder are omitted."],["TTS","Tacotron","autoregressive"])

# 15 -- variance branches meet before a duration-controlled length expansion.
f=plate("FastSpeech 2-style variance adaptor","Duration expands token states into frames; pitch and energy embeddings enrich the acoustic representation.")
f.node("text",r"Phonemes",1.6,2.5,1.9,.95,"tensor")
f.node("encoder",r"Text encoder",4.45,2.5,2.4,.95)
f.node("sum",r"$+$",7.2,2.5,.5,.5,"circle")
f.node("reg",r"Length regulator\\repeat by $d_i$",10.0,2.5,2.6,.95)
f.node("decoder",r"Parallel mel\\decoder",13.5,2.5,2.6,.95)
f.node("mel",r"Mel-spectrogram",13.5,4.6,2.6,.85,"tensor")
for a,b in [("text","encoder"),("encoder","sum"),("sum","reg"),("reg","decoder"),("decoder","mel")]:f.edge(a,b)
for name,txt,x in [("energy",r"Energy predictor",2.0),("pitch",r"Pitch predictor",4.9),("duration",r"Duration predictor",8.0)]:
    f.node(name,txt,x,5.2,2.45,.85)
    f.edge("encoder",name,side="south",to_side="north",via=[(4.45,3.75),(x,3.75)])
for name,x in [("energy",2.0),("pitch",4.9)]:
    f.node(name+"emb",name.capitalize()+r"\\embedding",x,7.15,2.45,.85)
    f.edge(name,name+"emb")
f.edge("energyemb","sum",side="west",to_side="north",via=[(.5,7.15),(.5,1.55),(7.2,1.55)],style="control")
f.edge("pitchemb","sum",side="east",to_side="south",via=[(6.4,7.15),(6.4,3.45),(7.2,3.45)],style="control")
f.edge("duration","reg",side="east",to_side="south",via=[(10.0,5.2)],style="control")
for i,ch in enumerate(["a","a","b","c","c","c"]):
    x=10.1+.8*i
    f.raw(f"\\draw[ink,fill=wash] ({x},6.65) rectangle ({x+.72},7.35);")
    label(f,"$"+ch+"$",x+.36,7.0,.6,"small")
label(f,r"Illustrative expansion: $d=(2,1,3)$",12.4,7.85,6,color="soft")
label(f,"Pitch and energy are shown at token level.",4.5,8.15,8,color="soft")
save(f,"audio-15-fastspeech2-variance","Parallel duration, pitch, and energy prediction with explicit length expansion.",["fastspeech"],
     ["This phoneme-level variance-adaptor abstraction does not prescribe every pitch or energy granularity choice."],["TTS","FastSpeech2","duration"])

# 16 -- training / inference reveal the posterior-prior and flow relationship.
f=plate("VITS conceptual training and inference","A text-conditioned prior is matched to a speech posterior; inference samples the prior and inverts the flow.",9.6)
f.group("Training: posterior, alignment, and waveform learning",.5,1.45,15.0,4.1)
f.node("textT",r"Text",1.35,2.35,1.4,.75,"plain")
f.node("prior",r"Text encoder\\prior parameters",3.75,2.35,2.7,.95)
f.node("mas",r"Monotonic\\alignment search",7.15,2.35,2.7,.95)
f.node("dur",r"Stochastic duration\\training",10.6,2.35,2.7,.95)
f.node("gan",r"GAN + feature\\matching + mel\\losses",14.0,2.35,2.7,.95)
f.node("speech",r"Speech\\STFT",1.35,4.5,1.9,.95,"plain")
f.node("posterior",r"Posterior encoder\\sample latent $z$",3.75,4.5,2.7,.95)
f.node("flow",r"Normalizing flow\\$z\mapsto z_p$",7.15,4.5,2.7,.95)
f.node("kl",r"Prior--posterior\\KL term",10.6,4.5,2.7,.95)
f.node("decT",r"Waveform decoder",14.0,4.5,2.7,.95)
for a,b in [("textT","prior"),("prior","mas"),("mas","dur"),("speech","posterior"),("posterior","flow"),("flow","kl"),("flow","mas"),("decT","gan")]:f.edge(a,b)
f.edge("prior","kl",side="north",to_side="east",via=[(3.75,1.65),(12.25,1.65),(12.25,4.5)])
f.edge("posterior","decT",side="south",to_side="south",via=[(3.75,5.25),(14.0,5.25)])
f.group("Inference: synthesize without the posterior encoder",.5,6.25,15.0,2.1)
infer=[("textI",r"Text + sampled\\durations",2.0,2.7),("sample",r"Expand text prior\\and sample $z_p$",5.5,2.7),("inverse",r"Inverse flow\\$z_p\mapsto z$",9.0,2.7),("decI",r"Waveform decoder",12.5,2.7),("audio",r"$\widehat{x}$",15.0,1.0)]
for name,txt,x,w in infer:f.node(name,txt,x,7.3,w,.95,"plain" if name=="audio" else "block")
for a,b in zip(infer,infer[1:]):f.edge(a[0],b[0])
label(f,"Sampled durations select the token-to-frame expansion; alignment search is training-only.",8,8.9,14,color="soft")
save(f,"audio-16-vits-conceptual","Separate training and inference graphs for a variational flow-based end-to-end TTS model.",["vits"],
     ["Training losses and alignment dependencies are aggregated; no specific flow family or decoder depth is asserted."],["TTS","VITS","normalizing flow"])

# 17 -- MRF fans into parallel receptive fields, and discriminator families split.
f=plate("HiFi-GAN neural vocoder","Upsampling and multi-receptive-field fusion generate audio; period and scale discriminator families supervise training.")
main=[("mel",r"Mel frames",1.55,2.0),("pre",r"Input conv",4.2,2.2),("up1",r"Upsample\\+ MRF",7.25,2.4),("up2",r"Further upsampling\\+ MRF stages",10.5,2.7),("wave",r"Output conv\\waveform",14.0,2.5)]
for name,txt,x,w in main:f.node(name,txt,x,2.75,w,.95,"tensor" if name=="mel" else "block")
for a,b in zip(main,main[1:]):f.edge(a[0],b[0])
f.group("One MRF module (conceptual)",.7,4.5,8.5,3.5)
f.node("mrfIn",r"$h$",1.45,6.25,.8,.6,"plain")
for name,txt,y in [("ra",r"Residual convs\\receptive field A",5.25),("rb",r"Residual convs\\receptive field B",6.25),("rc",r"Residual convs\\receptive field C",7.25)]:
    f.node(name,txt,4.85,y,3.0,.75)
    f.edge("mrfIn",name,side="east",to_side="west",via=[(2.55,6.25),(2.55,y)])
f.node("mrfSum",r"$\sum$",8.1,6.25,.7,.7,"circle")
for name in ["ra","rb","rc"]:f.edge(name,"mrfSum",side="east",to_side="west",via=[(7.0,f.nodes[name].y),(7.0,6.25)])
f.edge("up1","ra",side="south",to_side="north",via=[(7.25,4.05),(4.85,4.05)],style="control")
f.node("mpd",r"Multi-period\\discriminators",11.65,5.3,3.1,1.0)
f.node("msd",r"Multi-scale\\discriminators",11.65,7.2,3.1,1.0)
f.node("real",r"Real audio",14.55,6.25,2.1,.85,"tensor")
f.edge("wave","mpd",side="south",to_side="north",via=[(14,4.1),(11.65,4.1)])
f.edge("wave","msd",side="east",to_side="east",via=[(15.7,2.75),(15.7,7.2)])
f.edge("real","mpd",side="west",to_side="east",via=[(13.45,6.25),(13.45,5.3)])
f.edge("real","msd",side="west",to_side="east",via=[(13.45,6.25),(13.45,7.2)])
label(f,"Adversarial, feature-matching, and mel losses train the generator.",8,8.3,14,color="soft")
save(f,"audio-17-hifigan-vocoder","Upsampling generator, parallel MRF receptive fields, and multi-period/multi-scale training discriminators.",["hifigan"],
     ["The MRF branch widths and number of upsampling stages are schematic; discriminator internals are omitted."],["vocoder","HiFi-GAN","GAN"])

# 18 -- separate forward-noising and reverse-sampling paths.
f=plate("Diffusion vocoder", "Forward training noise and reverse conditional denoising run in opposite directions.")
f.group("Forward corruption (training)",.7,1.5,14.6,2.15)
top=[("x0",r"Clean audio\\$x_0$",2.2),("x1",r"$x_1$",5.4),("xk",r"$x_k$",8.6),("xK",r"Nearly Gaussian\\$x_K$",12.7)]
for name,txt,x in top:f.node(name,txt,x,2.55,2.6,.95,"tensor")
for a,b in zip(top,top[1:]):f.edge(a[0],b[0])
label(f,"Progressively add Gaussian noise",8,3.35,10,color="soft")
f.group("Reverse sampling (inference)",.7,4.45,14.6,1.9)
f.node("noise",r"Gaussian sample\\$x_K$",13.8,5.4,2.5,.95,"tensor")
f.node("step",r"Reverse update\\using $\epsilon_\theta(x_k,k,c)$",10.15,5.4,3.0,.95)
f.node("state",r"$x_{k-1}$",6.5,5.4,2.5,.95,"tensor")
f.node("clean",r"Generated audio\\$x_0$",2.5,5.4,2.8,.95,"tensor")
f.edge("noise","step");f.edge("step","state");f.edge("state","clean")
label(f,r"Iterate $k=K,\ldots,1$",3.4,6.8,4.8,color="soft")
f.node("condition",r"Mel conditioning\\$c$",7.3,7.6,2.7,.85,"tensor")
f.node("time",r"Diffusion-step\\embedding $k$",13.4,7.6,2.7,.85)
f.edge("condition","step",side="north",to_side="south",via=[(7.3,6.75),(9.65,6.75)],style="control")
f.edge("time","step",side="north",to_side="south",via=[(13.4,6.75),(10.65,6.75)],style="control")
label(f,r"Train $\epsilon_\theta$ to predict\\the added noise",3.3,7.6,4.8,"small")
save(f,"audio-18-diffusion-vocoder","A DiffWave-inspired conditional waveform diffusion process with forward and reverse lanes.",["diffwave"],
     ["Only the high-level diffusion schedule is shown; step counts and numerical sampler coefficients are unspecified."],["vocoder","diffusion","DiffWave"])

# 19 -- complex-mask enhancement with a true mixture-spectrum bypass.
f=plate("Complex-mask speech enhancement","A complex convolution--recurrent network estimates a mask, then reconstructs the enhanced waveform.")
f.node("noisy",r"Noisy speech\\$x[n]$",1.8,2.6,2.5,.95,"tensor")
f.node("stft",r"STFT\\$X_{t,f}$",5.0,2.6,2.5,.95)
f.node("encoder",r"Complex conv\\encoder",8.3,2.6,2.6,.95)
f.node("rnn",r"Complex recurrent\\bottleneck",11.7,2.6,2.8,.95)
f.node("decoder",r"Complex conv\\decoder",11.7,5.25,2.8,.95)
f.node("mask",r"Complex mask\\$M_{t,f}$",8.3,5.25,2.6,.95,"tensor")
f.node("product",r"Complex\\multiply",5.0,5.25,2.5,.95)
f.node("istft",r"Inverse STFT",1.8,5.25,2.5,.95)
for a,b in [("noisy","stft"),("stft","encoder"),("encoder","rnn"),("rnn","decoder"),("decoder","mask"),("mask","product"),("product","istft")]:f.edge(a,b)
f.edge("stft","product",side="south",to_side="north",label="mixture spectrum")
f.edge("encoder","decoder",side="south",to_side="east",via=[(8.3,3.85),(14.2,3.85),(14.2,5.25)],style="skip")
label(f,"encoder feature skips",11.2,3.57,5.5,color="soft")
wave(f,.55,7.35,3.4,.5)
arrow(f,[(1.8,5.73),(1.8,6.5)])
label(f,r"Enhanced $\widehat{s}[n]$",2.25,8.05,4)
label(f,r"$\widehat{S}_{t,f}=M_{t,f}X_{t,f}$\\$\widehat{s}=\operatorname{iSTFT}(\widehat S)$",9.5,7.4,9,"small")
save(f,"audio-19-speech-enhancement","DCCRN-inspired complex spectral masking with encoder skips and a mixture-spectrum multiplication bypass.",["enhance","stft"],
     ["A single recurrent bottleneck and one skip path stand for repeated implementation-specific layers."],["enhancement","complex mask","DCCRN"])

# 20 -- residual codebooks have explicit subtraction and reconstruction sum.
f=plate("Residual vector-quantized audio codec","Each codebook quantizes the previous residual; summed code vectors reconstruct the encoder latent.")
main=[("audio",r"Audio",1.45,2.0),("enc",r"Neural encoder",4.4,2.5),("latent",r"Latent $z$",7.4,2.0),("rvq",r"Residual vector\\quantizer",10.4,2.5),("dec",r"Neural decoder\\$\widehat{x}$",13.75,2.8)]
for name,txt,x,w in main:f.node(name,txt,x,2.25,w,.95,"tensor" if name in {"audio","latent"} else "block")
for a,b in zip(main,main[1:]):f.edge(a[0],b[0])
f.group("RVQ detail: three illustrative stages",.5,4.15,15.0,4.05)
f.node("r0",r"$r_0=z$",1.2,5.7,1.2,.7,"plain")
for i,x in enumerate((3,7,11),1):
    f.node(f"q{i}",rf"Codebook $Q_{i}$\\$q_{i}=Q_{i}(r_{{{i-1}}})$",x,5.7,2.35,.95)
    f.node(f"sub{i}",r"$-$",x+2,5.7,.55,.55,"circle")
    f.edge(f"q{i}",f"sub{i}")
f.edge("r0","q1")
f.edge("r0","sub1",side="north",to_side="north",via=[(1.2,4.65),(5,4.65)])
f.edge("sub1","q2",label=r"$r_1$")
arrow(f,[(5.43,5.7),(5.43,4.9),(9,4.9),(9,5.34)])
f.edge("sub2","q3",label=r"$r_2$")
arrow(f,[(9.43,5.7),(9.43,4.65),(13,4.65),(13,5.34)])
f.node("sum",r"$\sum$",14.2,7.25,.7,.7,"circle")
f.edge("q1","sum",side="south",to_side="west",via=[(3,7.25)])
f.edge("q2","sum",side="south",to_side="north",via=[(7,6.65),(14.2,6.65)])
f.edge("q3","sum",side="south",to_side="south",via=[(11,7.85),(14.2,7.85)])
arrow(f,[(14.63,7.25),(15.25,7.25)])
label(f,r"$\widehat z$",15.1,6.9,1.0)
label(f,r"Residual update: $r_j=r_{j-1}-q_j$",6.0,8.0,8)
arrow(f,[(10.4,2.725),(10.4,4.05)],style=",dashed")
save(f,"audio-20-residual-vq-codec","A SoundStream-inspired neural codec with expanded residual quantization, subtraction paths, and code-vector summation.",["codec"],
     ["Three codebooks illustrate the recurrence. Codec bandwidth, codebook size, and actual number of stages are unspecified."],["codec","residual VQ","SoundStream"])


assert len(INDEX) == 20
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "index.json").write_text(json.dumps(INDEX, indent=2) + "\n")
print(f"Generated {len(INDEX)} audio figures in {OUT}")
