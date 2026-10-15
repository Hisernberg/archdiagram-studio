#!/usr/bin/env python3
"""Author fifteen original, conceptual monochrome multimodal TikZ figures."""
from pathlib import Path
import json
from atlaslib import Figure

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'atlas' / 'multimodal'
INDEX = []


def figure(title, subtitle, caption, width=18, height=9):
    return Figure(title, width=width, height=height, subtitle=subtitle, caption=caption)


def n(f, name, label, x, y, w=2.5, h=.9, kind='block'):
    return f.node(name, label, x, y, w, h, kind)


def e(f, a, b, label='', **kw):
    f.edge(a, b, label, **kw)


def boundary(f, label, x, y, w, h):
    # Transparent boundaries preserve the background-layer data arrows.
    f.raw(r'\draw[draw=soft,dashed,line width=.45pt] '
          f'({x},{y}) rectangle ({x+w},{y+h});\n'
          r'\node[anchor=west,font=\scriptsize,fill=white,inner sep=2pt] '
          f'at ({x+.15},{y}) {{{label}}};')


def note(f, label, x, y, width=4):
    f.raw(r'\node[annotation,text width=' + str(width) + 'cm] at '
          f'({x},{y}) {{{label}}};')


def save(f, id, description, sources, assumptions=None, tags=None):
    assert len(f.caption) <= 140, (id, len(f.caption))
    INDEX.append(f.write(OUT, id, 'multimodal', description, sources,
                         assumptions or ['Original conceptual schematic; all dimensions are symbolic and implementation dependent.'],
                         tags or []))


def clip():
    f = figure('CLIP contrastive dual encoder',
        'Conceptual training graph: paired examples share a batch index, not encoder parameters.',
        'The diagonal of the cross-modal similarity matrix supplies positives for two directional classification losses.')
    for name, label, x, y, w, h, kind in [
        ('images',r'Image batch\\$\{I_i\}_{i=1}^{B}$',1.6,2.6,2.4,1,'tensor'),
        ('texts',r'Text batch\\$\{T_i\}_{i=1}^{B}$',1.6,5.8,2.4,1,'tensor'),
        ('vision',r'Image encoder\\$f_{\theta}$',4.7,2.6,2.4,1,'block'),
        ('language',r'Text encoder\\$g_{\phi}$',4.7,5.8,2.4,1,'block'),
        ('u',r'Project, normalize\\$U\in\mathbb{R}^{B\times d}$',8.0,2.6,2.7,1,'tensor'),
        ('v',r'Project, normalize\\$V\in\mathbb{R}^{B\times d}$',8.0,5.8,2.7,1,'tensor'),
        ('sim',r'$S=UV^{\top}/\tau$\\$\begin{bmatrix}\blacksquare&\circ&\circ\\\circ&\blacksquare&\circ\\\circ&\circ&\blacksquare\end{bmatrix}$\\$S\in\mathbb{R}^{B\times B}$',11.9,4.2,3.1,2.5,'tensor'),
        ('row',r'Image-to-text CE\\$\mathcal L_{I\to T}$',15.8,2.9,3.0,1,'block'),
        ('col',r'Text-to-image CE\\$\mathcal L_{T\to I}$',15.8,5.4,3.0,1,'block'),
        ('loss',r'Symmetric objective\\$\frac12(\mathcal L_{I\to T}+\mathcal L_{T\to I})$',15.8,7.4,3.4,.9,'block'),
    ]: n(f,name,label,x,y,w,h,kind)
    e(f,'images','vision');e(f,'texts','language');e(f,'vision','u');e(f,'language','v')
    e(f,'u','sim',side='east',to_side='north',via=[(11.9,2.6)])
    e(f,'v','sim',side='east',to_side='south',via=[(11.9,5.8)])
    e(f,'sim','row',r'rows',side='east',to_side='west',via=[(13.8,4.2),(13.8,2.9)])
    e(f,'sim','col',r'columns',side='east',to_side='west',via=[(14.2,4.2),(14.2,5.4)])
    e(f,'row','loss',side='east',to_side='east',via=[(17.6,2.9),(17.6,7.4)])
    e(f,'col','loss')
    note(f,r'$\blacksquare$: matched pair\qquad $\circ$: in-batch negative',7.8,7.6,7.0)
    save(f,'multimodal-01-clip-dual-encoder','Dual encoder contrastive pretraining with normalized embeddings, a batch similarity matrix, and symmetric losses.',
         ['https://proceedings.mlr.press/v139/radford21a.html'],tags=['contrastive','dual-encoder','CLIP','training'])


def vqa():
    f=figure('Visual question answering',
        'Conceptual region-attention model: the question selects visual evidence and also enters answer fusion.',
        'Question-conditioned weights pool region values; a separate question path preserves linguistic context.')
    n(f,'image','Image',1.6,2.6,2.2,1,'tensor')
    n(f,'regions',r'Region encoder\\$R\in\mathbb{R}^{N\times d_v}$',4.9,2.6,2.7,1.1)
    n(f,'question',r'Question\\$x_{1:L}$',1.6,6.4,2.2,1,'tensor')
    n(f,'qenc',r'Question encoder\\$q\in\mathbb{R}^{d_q}$',4.9,6.4,2.7,1.1)
    n(f,'att',r'Score and softmax\\$\alpha_i=\mathrm{softmax}_i\,s(R_i,q)$',8.3,4.3,2.8,1.3)
    n(f,'pool',r'Weighted visual pool\\$v=\sum_i\alpha_iR_i$',11.8,2.6,2.8,1.1)
    n(f,'fuse',r'Joint fusion\\$z=F(v,q)$',11.8,6.4,2.8,1.1)
    n(f,'answer',r'Answer classifier\\$p(a\mid I,x)$',15.5,6.4,3.0,1.1)
    n(f,'target',r'Answer supervision\\$a^{\star}$',15.5,2.6,3.0,1)
    n(f,'loss',r'Classification loss',15.5,4.4,3.0,.8)
    e(f,'image','regions');e(f,'question','qenc')
    e(f,'regions','att',r'keys',side='east',to_side='north',via=[(8.3,2.6)])
    e(f,'qenc','att',r'query',side='east',to_side='south',via=[(8.3,6.4)])
    e(f,'regions','pool',r'values',side='north',to_side='north',via=[(4.9,1.6),(11.8,1.6)])
    e(f,'att','pool',r'$\alpha$',side='east',to_side='west',via=[(9.9,4.3),(9.9,2.6)])
    e(f,'pool','fuse');e(f,'qenc','fuse',r'linguistic context')
    e(f,'fuse','answer');e(f,'target','loss');e(f,'answer','loss',side='north',to_side='south')
    save(f,'multimodal-02-visual-question-answering','Region-based question answering with question-conditioned attention, weighted visual pooling, and answer supervision.',
        ['https://openaccess.thecvf.com/content_cvpr_2018/html/Anderson_Bottom-Up_and_Top-Down_CVPR_2018_paper.html'],tags=['VQA','attention','fusion'])


def captioning():
    f=figure('Attention-based image captioning',
        'Conceptual recurrent decoder: image attention is recomputed as the generated prefix grows.',
        'Visual memory is reused at each token step; the hidden state controls attention and sampled words feed the decoder.')
    n(f,'image',r'Image\\$I$',1.5,4.9,2.2,1,'tensor')
    n(f,'features',r'Visual encoder\\$A=\{a_i\}_{i=1}^{N}$',4.6,4.9,2.6,1.1)
    n(f,'att',r'Soft visual attention\\$c_t=\sum_i\alpha_{t,i}a_i$',8.0,4.9,2.8,1.1)
    n(f,'dec',r'Recurrent decoder\\$h_t=\mathrm{RNN}(h_{t-1},e_{t-1},c_t)$',11.6,4.9,3.0,1.3)
    n(f,'softmax',r'Vocabulary head\\$p(y_t\mid y_{<t},I)$',15.3,4.9,3.0,1.1)
    n(f,'target',r'Reference token\\$y_t^{\star}$',15.3,1.9,2.8,.9)
    n(f,'loss',r'Token cross-entropy',15.3,3.2,2.8,.8)
    n(f,'token',r'Decode token\\$\hat y_t$',15.3,7.3,2.8,.9)
    n(f,'embed',r'Embedding for step $t+1$\\$e_t=E(\hat y_t)$',11.6,7.3,3.0,.9)
    e(f,'image','features');e(f,'features','att');e(f,'att','dec');e(f,'dec','softmax')
    e(f,'target','loss');e(f,'softmax','loss',side='north',to_side='south')
    e(f,'softmax','token');e(f,'token','embed',side='west',to_side='east')
    e(f,'embed','dec',r'next step',side='north',to_side='south',style='feedback')
    e(f,'dec','att',r'next-step state $h_t$',side='north',to_side='north',via=[(11.6,2.8),(8.0,2.8)],style='feedback')
    note(f,r'Training may supply $E(y_{t-1}^{\star})$ through teacher forcing.',5.6,7.4,7)
    save(f,'multimodal-03-image-captioning','Image captioning with recurrent visual attention, a token likelihood objective, and an autoregressive word feedback loop.',
        ['https://proceedings.mlr.press/v37/xuc15.html'],tags=['captioning','autoregressive','visual-attention'])


def llava():
    f=figure('Vision-language projection bridge',
        'LLaVA-style conceptual graph: project visual patch features into the language-model embedding space.',
        'Projected image tokens and text embeddings enter one causal sequence; response tokens carry the language objective.')
    n(f,'image',r'Image\\$I$',1.5,2.8,2.1,1,'tensor')
    n(f,'vision',r'Pretrained vision encoder\\$Z_v\in\mathbb{R}^{N_v\times d_v}$',4.7,2.8,2.9,1.2)
    n(f,'proj',r'Trainable projector\\$Z=Z_vW$\\$N_v\times d_{\mathrm{LM}}$',8.1,2.8,2.8,1.4)
    n(f,'instruction',r'Instruction / prefix\\$x_{1:L}$',1.7,6.4,2.5,1,'tensor')
    n(f,'tokenize',r'Tokenize and embed\\$E(x_{1:L})$',5.1,6.4,3.0,1.1)
    n(f,'sequence',r'Causal input sequence\\$[Z;E(x);E(y_{<t})]$\\$(N_v+L+t-1)\times d_{\mathrm{LM}}$',11.5,4.6,3.2,1.8,'tensor')
    n(f,'lm',r'Language model\\$p(y_t\mid I,x,y_{<t})$',15.4,4.6,3.0,1.2)
    n(f,'loss',r'Response-token loss\\$-\sum_t\log p(y_t^{\star}\mid\cdot)$',15.4,2.0,3.2,1.0)
    n(f,'response',r'Generated response\\$y_{1:T}$',15.4,7.0,3.0,.9)
    e(f,'image','vision');e(f,'vision','proj');e(f,'instruction','tokenize')
    e(f,'proj','sequence',side='east',to_side='north',via=[(11.5,2.8)])
    e(f,'tokenize','sequence',side='east',to_side='south',via=[(11.5,6.4)])
    e(f,'sequence','lm');e(f,'lm','loss',side='north',to_side='south');e(f,'lm','response')
    note(f,r'Conceptual projector shown as a linear map. Training stages determine which pretrained weights are updated.',6.1,7.7,9.8)
    save(f,'multimodal-04-vision-language-projector','LLaVA-style alignment of image encoder patch features with a causal language model through a learned projection.',
        ['https://arxiv.org/abs/2304.08485','https://github.com/haotian-liu/LLaVA'],
        ['Conceptual LLaVA-style bridge; the linear projector follows the initial formulation, while later versions may use an MLP.','Visual token counts and embedding widths are symbolic; the diagram does not fix training-stage freeze policies.'],
        ['LLaVA','projector','vision-language','causal-LM'])


def flamingo():
    f=figure('Resampling with gated visual cross-attention',
        'Flamingo-style conceptual block: a fixed latent set connects variable visual inputs to a pretrained language stream.',
        'Learned latent queries resample vision features; text queries read those latents through a gated residual path.')
    n(f,'images',r'Image / video features\\variable visual extent',1.7,2.6,2.7,1.1,'tensor')
    n(f,'vision',r'Vision encoder\\$V\in\mathbb{R}^{N\times d_v}$',4.9,2.6,2.7,1.1)
    n(f,'resample',r'Perceiver resampler\\$N\longrightarrow M$',8.2,2.6,2.7,1.1)
    n(f,'latents',r'Visual latent memory\\$Z\in\mathbb{R}^{M\times d}$',11.8,2.6,3.0,1.1,'tensor')
    n(f,'queries',r'Learned latent queries\\$Q_0\in\mathbb{R}^{M\times d}$',8.2,4.3,2.8,.9)
    n(f,'text',r'Text tokens\\$x_{1:L}$',1.6,6.5,2.2,.9,'tensor')
    n(f,'lm1',r'Language block\\$H$',4.7,6.5,2.6,1.0)
    n(f,'xatt',r'Gated cross-attention\\{\scriptsize $\tanh(\gamma)\,\mathrm{Attn}(H,Z)$}',8.2,6.5,2.9,1.1)
    n(f,'sum',r'$+$',10.5,6.5,.55,.55)
    n(f,'lm2',r'Next language block\\$H^{\prime}$',12.6,6.5,2.7,1.0)
    n(f,'out',r'Next-token scores',16.0,6.5,2.8,.9)
    e(f,'images','vision');e(f,'vision','resample');e(f,'resample','latents');e(f,'queries','resample',side='north',to_side='south')
    e(f,'text','lm1');e(f,'lm1','xatt');e(f,'xatt','sum');e(f,'sum','lm2');e(f,'lm2','out')
    e(f,'latents','xatt',side='south',to_side='north',via=[(11.8,5.1),(8.2,5.1)])
    e(f,'lm1','sum',side='south',to_side='south',via=[(4.7,7.4),(10.5,7.4)],style='skip')
    boundary(f,'interleaved language block',3.1,5.8,11.1,2.0)
    note(f,r'Visual keys and values',13.2,4.2,3.0)
    save(f,'multimodal-05-resampler-cross-attention','Flamingo-style learned visual resampling and gated cross-attention inserted between language model blocks.',
        ['https://arxiv.org/abs/2204.14198'],tags=['Flamingo','Perceiver','cross-attention','gated-residual'])


def clap():
    f=figure('Audio-text contrastive learning and zero-shot scoring',
        'CLAP-style conceptual view: learn a common embedding space, then score natural-language class descriptions.',
        'Training aligns paired audio and descriptions; zero-shot inference ranks candidate text embeddings by cosine similarity.')
    n(f,'audio',r'Audio clips\\variable duration',1.8,2.4,2.7,.9,'tensor')
    n(f,'aenc',r'Audio encoder + pool\\$a_i\in\mathbb{R}^{d_a}$',5.2,2.4,3.0,1.0)
    n(f,'aproj',r'Project and normalize\\$u_i\in\mathbb{R}^{d}$',8.9,2.4,3.0,1.0)
    n(f,'desc',r'Paired descriptions',1.8,4.1,2.7,.9,'tensor')
    n(f,'tenc',r'Text encoder + pool\\$t_i\in\mathbb{R}^{d_t}$',5.2,4.1,3.0,1.0)
    n(f,'tproj',r'Project and normalize\\$v_i\in\mathbb{R}^{d}$',8.9,4.1,3.0,1.0)
    n(f,'align',r'Contrastive alignment\\$\mathrm{sim}(u_i,v_i)$ vs. $\mathrm{sim}(u_i,v_j)$',14.0,3.2,4.8,1.5)
    e(f,'audio','aenc');e(f,'aenc','aproj');e(f,'desc','tenc');e(f,'tenc','tproj')
    e(f,'aproj','align',side='east',to_side='north',via=[(14.0,2.4)])
    e(f,'tproj','align',side='east',to_side='south',via=[(14.0,4.1)])
    boundary(f,'paired pretraining',.3,1.6,17.2,3.2)
    n(f,'query',r'Query audio embedding\\$u$',2.7,6.7,3.7,1.0,'tensor')
    n(f,'candidates',r'Candidate text embeddings\\$\{v_c\}_{c\in\mathcal C}$',8.3,7.6,3.9,.9)
    n(f,'score',r'Cosine scores\\$s_c=u^{\top}v_c$',8.3,5.7,3.9,.9)
    n(f,'rank',r'Rank / select description\\$\hat c=\arg\max_c s_c$',14.2,6.7,4.7,1.1)
    e(f,'query','score',side='east',to_side='west',via=[(5.3,6.7),(5.3,5.7)])
    e(f,'candidates','score',side='north',to_side='south');e(f,'score','rank',side='east',to_side='west',via=[(10.8,5.7),(10.8,6.7)])
    save(f,'multimodal-06-clap-audio-text','Audio-text contrastive pretraining with duration pooling and a distinct zero-shot text-label retrieval panel.',
        ['https://arxiv.org/abs/2206.04769','https://www.microsoft.com/en-us/research/publication/clap-learning-audio-concepts-from-natural-language-supervision/'],
        tags=['CLAP','audio-text','contrastive','zero-shot'])


def speech_bridge():
    f=figure('Speech-to-language-model bridge',
        'SALMONN-style conceptual path: aligned speech and general-audio representations become a short language prefix.',
        'A windowed query adapter compresses aligned encoder features; prompt embeddings and audio tokens condition text generation.')
    n(f,'wave',r'Audio waveform\\$x_{1:T}$',1.5,4.5,2.2,1.0,'tensor')
    n(f,'speech',r'Speech encoder\\$S\in\mathbb{R}^{T_s\times d_s}$',4.6,2.5,2.8,1.1)
    n(f,'sound',r'General-audio encoder\\$A\in\mathbb{R}^{T_a\times d_a}$',4.6,6.4,2.8,1.1)
    n(f,'align',r'Time-align + concatenate\\$H\in\mathbb{R}^{T_h\times(d_s+d_a)}$',7.9,4.5,2.8,1.3)
    n(f,'adapter',r'Windowed Q-Former\\+ projection\\$Z\in\mathbb{R}^{M\times d_{\mathrm{LM}}}$',11.2,4.5,2.9,1.5)
    n(f,'query',r'Learned queries\\per time window',11.2,2.0,2.9,.9)
    n(f,'lm',r'Language model\\$p(y_t\mid Z,x_{\mathrm{prompt}},y_{<t})$',14.6,4.5,2.9,1.3)
    n(f,'prompt',r'Prompt embeddings\\``Transcribe the speech''',14.6,7.1,3.0,1)
    n(f,'text',r'Text tokens\\$y_{1:L}$',17.2,4.5,1.5,1,'tensor')
    e(f,'wave','speech',side='north',to_side='west',via=[(1.5,2.5)])
    e(f,'wave','sound',side='south',to_side='west',via=[(1.5,6.4)])
    e(f,'speech','align',side='east',to_side='north',via=[(7.9,2.5)])
    e(f,'sound','align',side='east',to_side='south',via=[(7.9,6.4)])
    e(f,'align','adapter');e(f,'query','adapter');e(f,'adapter','lm');e(f,'prompt','lm',side='north',to_side='south');e(f,'lm','text')
    note(f,r'Text supervision: $\mathcal L_{\mathrm{text}}=-\sum_t\log p(y_t^{\star}\mid Z,x_{\mathrm{prompt}},y_{<t}^{\star})$.',7.6,7.8,12)
    save(f,'multimodal-07-speech-language-bridge','SALMONN-style speech and audio encoder fusion through a window-level query adapter into a language model.',
        ['https://arxiv.org/abs/2310.13289','https://github.com/bytedance/SALMONN'],
        ['Conceptual SALMONN-style bridge, shown for transcription; encoder alignment, query counts, and widths remain symbolic.','The figure omits low-rank adaptation and detailed training stages.'],
        ['speech','audio','Q-Former','language-model','adapter'])


def video():
    f=figure('Video temporal encoder',
        'ViViT-style factorized encoder (conceptual): shared spatial processing precedes attention across time.',
        'Each frame contributes a spatial summary; temporal position codes preserve order before the video-level readout.')
    for i,(x,t) in enumerate([(2.7,'1'),(6.9,'2'),(11.1,'T')],1):
        n(f,f'frame{i}',rf'Frame $I_{{{t}}}$\\$H\times W\times C$',x,2.0,2.9,1.0,'tensor')
        n(f,f'spatial{i}',r'Patch embedding\\+ spatial transformer',x,3.9,3.3,1.1)
        n(f,f'sum{i}',rf'Frame summary $z_{{{t}}}$\\$\in\mathbb{{R}}^d$',x,5.5,3.1,.9,'tensor')
        e(f,f'frame{i}',f'spatial{i}');e(f,f'spatial{i}',f'sum{i}')
    n(f,'temporal',r'Temporal transformer\\$[z_1+p_1,\ldots,z_T+p_T]\in\mathbb{R}^{T\times d}$',6.9,7.4,7.6,1.1)
    n(f,'readout',r'Video readout\\$z_{\mathrm{video}}\in\mathbb{R}^{d}$',15.0,7.4,3.6,1.1)
    for i,x in enumerate([2.7,6.9,11.1],1):
        e(f,f'sum{i}','temporal',side='south',to_side='north',via=[(x,6.5),(6.9,6.5)])
    e(f,'temporal','readout')
    note(f,r'Shared spatial weights across frames',15.0,3.2,3.5)
    note(f,r'$\cdots$ sampled time steps $\cdots$',8.9,1.25,5.5)
    save(f,'multimodal-08-video-temporal-encoder','A factorized video encoder with shared spatial frame encoders, frame summaries, temporal positions, and temporal attention.',
        ['https://openaccess.thecvf.com/content/ICCV2021/html/Arnab_ViViT_A_Video_Vision_Transformer_ICCV_2021_paper.html'],
        ['Conceptual frame-level factorized encoder inspired by ViViT; temporal tubelets and other ViViT variants are not shown.','All frame counts, sequence lengths, and channel widths are symbolic.'],
        ['video','temporal-attention','factorized-encoder','ViViT'])


def audiovisual():
    f=figure('Audio-visual speech fusion',
        'AV-HuBERT-style conceptual pretraining: synchronized sound and lip motion predict masked speech units.',
        'Aligned audio and visual streams feed a masked joint encoder; discrete cluster targets supervise only selected positions.')
    n(f,'audio',r'Audio frames\\$x^a_{1:T_a}$',1.7,2.4,2.6,1,'tensor')
    n(f,'video',r'Mouth-region frames\\$x^v_{1:T_v}$',1.7,5.4,2.6,1,'tensor')
    n(f,'aenc',r'Audio frontend\\$A$',4.9,2.4,2.6,1)
    n(f,'venc',r'Visual frontend\\$V$',4.9,5.4,2.6,1)
    n(f,'align',r'Synchronize + fuse\\$H_t=[A_t;V_t]$',8.1,3.9,2.7,1.2)
    n(f,'mask',r'Mask selected spans\\$\widetilde H_{1:T}$',11.2,3.9,2.6,1.1)
    n(f,'joint',r'Joint transformer\\$Z_{1:T}$',14.3,3.9,2.6,1.1)
    n(f,'pred',r'Unit head\\$p(k_t\mid\widetilde H)$',17.0,3.9,1.8,1.1)
    n(f,'clusters',r'Offline clustering\\targets $k_{1:T}$',8.1,7.2,3.0,1.0)
    n(f,'loss',r'Masked-unit objective\\$-\sum_{t\in\mathcal M}\log p(k_t\mid\widetilde H)$',15.1,7.2,4.5,1.0)
    e(f,'audio','aenc');e(f,'video','venc')
    e(f,'aenc','align',side='east',to_side='north',via=[(8.1,2.4)])
    e(f,'venc','align',side='east',to_side='west',via=[(6.5,5.4),(6.5,3.9)])
    e(f,'align','mask');e(f,'mask','joint');e(f,'joint','pred')
    e(f,'align','clusters',r'clean fused features',side='south',to_side='north')
    e(f,'clusters','loss',r'discrete targets');e(f,'pred','loss',side='south',to_side='north',via=[(17.0,6.2),(15.1,6.2)])
    note(f,r'Selected positions $\mathcal M$; modality dropout and iterative target refinement omitted.',11.3,1.8,9.5)
    save(f,'multimodal-09-audiovisual-speech-fusion','Synchronized audio-visual speech fusion with masked multimodal representations and discrete cluster prediction.',
        ['https://arxiv.org/abs/2201.02184','https://github.com/facebookresearch/av_hubert'],
        ['Conceptual AV-HuBERT-style pretraining; clean fused features represent the offline target pipeline, whose clustering is refined across iterations.','Frontends, temporal resampling, and fusion widths are symbolic.'],
        ['audio-visual','speech','AV-HuBERT','masked-prediction'])


def early_late():
    f=figure('Early fusion versus late fusion',
        'Comparative conceptual panel: combine aligned inputs before modeling, or combine unimodal decisions afterward.',
        'Early fusion exposes cross-modal interactions to one model; late fusion combines independently produced decision values.')
    boundary(f,'A. early fusion',.4,1.5,8.2,6.6)
    boundary(f,'B. late fusion',9.0,1.5,8.6,6.6)
    n(f,'ea',r'Modality A\\aligned input $x^a$',2.4,2.7,3.0,1)
    n(f,'eb',r'Modality B\\aligned input $x^b$',6.5,2.7,3.0,1)
    n(f,'concat',r'Input concatenation\\$x=[x^a;x^b]$',4.4,4.3,3.3,1.0)
    n(f,'joint',r'Joint predictive model\\$p(y\mid x^a,x^b)$',4.4,5.9,3.5,1.0)
    n(f,'epred',r'Joint decision $\hat y$',4.4,7.4,3.5,.7)
    e(f,'ea','concat',side='south',to_side='west',via=[(2.4,4.3)])
    e(f,'eb','concat',side='south',to_side='east',via=[(6.5,4.3)])
    e(f,'concat','joint');e(f,'joint','epred')
    n(f,'la',r'Modality A\\input $x^a$',11.2,2.7,3.0,1)
    n(f,'lb',r'Modality B\\input $x^b$',15.4,2.7,3.0,1)
    n(f,'amodel',r'Unimodal model A\\$p_a(y\mid x^a)$',11.2,4.8,3.2,1.2)
    n(f,'bmodel',r'Unimodal model B\\$p_b(y\mid x^b)$',15.4,4.8,3.2,1.2)
    n(f,'combine',r'Decision fusion\\$p(y)=\lambda p_a(y)+(1-\lambda)p_b(y)$',13.3,7.1,6.0,1.2)
    e(f,'la','amodel');e(f,'lb','bmodel')
    e(f,'amodel','combine',side='south',to_side='north',via=[(11.2,6.1),(13.3,6.1)])
    e(f,'bmodel','combine',side='south',to_side='north',via=[(15.4,6.1),(13.3,6.1)])
    save(f,'multimodal-10-early-versus-late-fusion','Side-by-side comparison of aligned input fusion before a joint model and weighted probability fusion after unimodal models.',
        ['https://arxiv.org/abs/1705.09406','https://ai.stanford.edu/~ang/papers/icml11-MultimodalDeepLearning.pdf'],
        ['Conceptual fusion comparison; concatenation and weighted averaging are illustrative design choices, with 0 <= lambda <= 1.','Inputs are assumed aligned when early concatenation requires correspondence.'],
        ['early-fusion','late-fusion','comparison'])


def vla():
    f=figure('Vision-language-action policy',
        'RT-2-style conceptual inference loop: visual observations and a language goal condition action symbols.',
        'The policy emits discrete action tokens, which are decoded into a control command before the next observation arrives.')
    n(f,'obs',r'Robot observation\\image $I_t$',1.8,2.7,2.8,1,'tensor')
    n(f,'vision',r'Visual tokens\\$Z_v(I_t)$',5.2,2.7,2.8,1.0)
    n(f,'goal',r'Language goal\\$g$',1.8,6.0,2.8,1,'tensor')
    n(f,'text',r'Text token embeddings\\$E(g)$',5.2,6.0,2.8,1.0)
    n(f,'policy',r'Autoregressive VLA\\$p(a_t^{\mathrm{tok}}\mid I_t,g)$',8.8,4.3,3.1,1.5)
    n(f,'actions',r'Action symbols\\$[\Delta x,\Delta r,\mathrm{grip},\mathrm{stop}]$',12.4,4.3,3.0,1.4,'tensor')
    n(f,'decode',r'Action detokenizer\\$a_t$',16.0,4.3,3.0,1.1)
    n(f,'robot',r'Robot + environment\\execute $a_t$',16.0,6.8,3.0,1.1)
    e(f,'obs','vision');e(f,'goal','text')
    e(f,'vision','policy',side='east',to_side='north',via=[(8.8,2.7)])
    e(f,'text','policy',side='east',to_side='south',via=[(8.8,6.0)])
    e(f,'policy','actions');e(f,'actions','decode');e(f,'decode','robot')
    e(f,'robot','obs',side='south',to_side='west',via=[(16.0,8.1),(.2,8.1),(.2,2.7)],style='feedback')
    note(f,r'Next observation $I_{t+1}$',8.8,7.8,5)
    note(f,r'Action symbols denote quantized controls; the component count and vocabulary vary by robot.',12.6,1.7,9)
    save(f,'multimodal-11-vision-language-action','A closed-loop vision-language-action policy with visual and language branches, action-token decoding, and environment feedback.',
        ['https://arxiv.org/abs/2307.15818','https://proceedings.mlr.press/v229/zitkovich23a.html'],
        ['Conceptual RT-2-style inference loop; action symbols are schematic and do not specify exact tokenization or robot degrees of freedom.','Web-data co-fine-tuning and robotics training trajectories are outside this inference view.'],
        ['VLA','RT-2','robotics','closed-loop'])


def rgb_depth():
    f=figure('RGB-depth fusion at multiple scales',
        'FuseNet-style conceptual encoder: a depth stream injects registered geometry into the appearance stream.',
        'Depth and RGB features are summed at corresponding scales; the fused appearance stream supplies a dense decoder.')
    n(f,'rgb',r'RGB image\\$H\times W\times3$',1.4,2.9,2.2,1,'tensor')
    n(f,'depth',r'Depth map\\$H\times W\times1$',1.4,6.0,2.2,1,'tensor')
    for i,x in enumerate([4.3,8.2,12.1],1):
        n(f,f'r{i}',rf'RGB stage {i}\\$R_{{{i}}}$',x,2.9,2.0,1.0)
        n(f,f'd{i}',rf'Depth stage {i}\\$D_{{{i}}}$',x,6.0,2.0,1.0)
        n(f,f'plus{i}',r'$+$',x+1.7,2.9,.55,.55)
        e(f,f'r{i}',f'plus{i}')
        e(f,f'd{i}',f'plus{i}',r'geometry',side='north',to_side='south',via=[(x,4.6),(x+1.7,4.6)],label_side='right')
    e(f,'rgb','r1');e(f,'depth','d1')
    for i in [1,2]: e(f,f'plus{i}',f'r{i+1}');e(f,f'd{i}',f'd{i+1}')
    n(f,'dec',r'Dense decoder\\upsample + classify',16.2,2.9,2.8,1.1)
    n(f,'seg',r'Semantic map\\$H\times W\times K$',16.2,6.0,2.8,1.1,'tensor')
    e(f,'plus3','dec');e(f,'dec','seg')
    note(f,r'Registered pixels; channel compatibility is required at every $+$ merge.',8.0,7.6,10.5)
    save(f,'multimodal-12-rgb-depth-fusion','Registered RGB and depth encoders with repeated same-scale additive feature fusion and a dense semantic decoder.',
        ['https://github.com/tum-vision/fusenet','https://cvai.cit.tum.de/_media/spezial/bib/hazirbasma2016fusenet.pdf'],
        ['Conceptual FuseNet-style pattern with three representative scales; the source architecture contains additional stages and decoder detail.','RGB and depth are assumed registered; symbolic feature channels are compatible at each sum.'],
        ['RGB-D','FuseNet','dense-prediction','multiscale-fusion'])


def document():
    f=figure('Document language-layout-vision fusion',
        'LayoutLMv3-style conceptual pretraining: OCR words and coordinates join image patch tokens in one encoder.',
        'Text, patch, and word-patch objectives train one multimodal encoder while layout coordinates remain available.')
    n(f,'page',r'Document image\\$I\in\mathbb{R}^{H\times W\times C}$',1.8,4.3,2.8,1.3,'tensor')
    n(f,'ocr',r'OCR\\words and segment boxes',5.1,2.5,2.8,1.1)
    n(f,'patch',r'Split image patches\\+ linear projection',5.1,6.7,2.8,1.1)
    n(f,'text',r'Text embeddings\\$e_w+e_{1D}+e_{2D}$',8.7,2.5,3.0,1.1)
    n(f,'layout',r'2D layout embeddings\\$(x,y,w,h)$',8.7,4.5,3.0,1.1)
    n(f,'image',r'Image embeddings\\$P\in\mathbb{R}^{N_p\times d}$',8.7,6.7,3.0,1.1,'tensor')
    n(f,'encoder',r'Unified transformer\\$[\mathrm{text};\mathrm{patches}]$\\spatial attention biases',12.4,4.5,3.0,1.8)
    n(f,'mlm',r'Masked language head\\$\mathcal L_{\mathrm{MLM}}$',16.0,2.3,3.1,1.0)
    n(f,'mim',r'Masked image head\\$\mathcal L_{\mathrm{MIM}}$',16.0,4.5,3.1,1.0)
    n(f,'wpa',r'Word-patch alignment\\$\mathcal L_{\mathrm{WPA}}$',16.0,6.7,3.1,1.0)
    e(f,'page','ocr',side='north',to_side='west',via=[(1.8,2.5)])
    e(f,'page','patch',side='south',to_side='west',via=[(1.8,6.7)])
    e(f,'ocr','text',r'words');e(f,'ocr','layout',r'boxes',side='south',to_side='west',via=[(5.1,4.5)])
    e(f,'layout','text',side='north',to_side='south');e(f,'patch','image')
    e(f,'text','encoder',side='east',to_side='north',via=[(12.4,2.5)])
    e(f,'image','encoder',side='east',to_side='south',via=[(12.4,6.7)])
    e(f,'encoder','mlm',side='east',to_side='west',via=[(14.2,4.5),(14.2,2.3)])
    e(f,'encoder','mim');e(f,'encoder','wpa',side='east',to_side='west',via=[(14.2,4.5),(14.2,6.7)])
    save(f,'multimodal-13-document-layout-language-vision','OCR words and segment boxes plus linear image patches are fused by a shared document transformer with three pretraining heads.',
        ['https://arxiv.org/abs/2204.08387','https://arxiv.org/html/2204.08387v3'],
        ['Conceptual LayoutLMv3-style graph; image targets are discrete visual tokens and WPA predicts corresponding patch masking.','Mask selection and visual tokenizer target generation are omitted; all dimensions are symbolic.'],
        ['document-AI','LayoutLMv3','layout','pretraining'])


def rag():
    f=figure('Retrieval-augmented multimodal generation',
        'MuRAG-inspired conceptual system: an indexed memory returns text and image evidence to an answer generator.',
        'Offline keys support nearest-neighbor search; retrieved identifiers fetch multimodal evidence for query-conditioned generation.')
    n(f,'corpus',r'Corpus items\\text / image-text pairs',1.8,2.4,2.8,1.1)
    n(f,'keys',r'Memory encoder\\$k_i\in\mathbb{R}^{d}$',5.2,2.4,2.8,1.1)
    n(f,'index',r'Vector index\\$\{k_i,\mathrm{id}_i\}$',8.7,2.4,2.9,1.1)
    n(f,'payload',r'Evidence payloads\\text + image content',12.1,2.4,2.9,1.1)
    n(f,'query',r'User query\\text and/or image',1.8,5.8,2.8,1.1,'tensor')
    n(f,'qenc',r'Query encoder\\$q\in\mathbb{R}^{d}$',5.2,5.8,2.8,1.1)
    n(f,'search',r'Nearest-neighbor search\\$\mathrm{TopK}_i\ q^{\top}k_i$',8.7,5.8,2.9,1.2)
    n(f,'evidence',r'Retrieved evidence\\$\mathcal E_K$',12.1,5.8,2.9,1.1,'tensor')
    n(f,'gen',r'Multimodal generator\\$p(y\mid q,\mathcal E_K)$',15.7,5.8,3.0,1.2)
    n(f,'answer',r'Grounded answer\\$y$',15.7,7.7,3.0,.8)
    e(f,'corpus','keys');e(f,'keys','index')
    e(f,'corpus','payload',r'persist original content',side='north',to_side='north',via=[(1.8,1.5),(12.1,1.5)])
    e(f,'query','qenc');e(f,'qenc','search');e(f,'index','search',side='south',to_side='north')
    e(f,'search','evidence');e(f,'payload','evidence',side='south',to_side='north')
    e(f,'evidence','gen');e(f,'gen','answer')
    e(f,'query','gen',r'query context',side='north',to_side='north',via=[(1.8,4.1),(15.7,4.1)])
    boundary(f,'offline memory construction',.3,1.3,13.5,2.0)
    save(f,'multimodal-14-retrieval-augmented-generation','Multimodal retrieval-augmented generation with offline memory keys, payload storage, top-k search, and a direct query context path.',
        ['https://aclanthology.org/2022.emnlp-main.375/','https://arxiv.org/abs/2210.02928'],
        ['Conceptual MuRAG-inspired system; the key index and payload store are logical roles and may share one implementation.','The figure describes inference and memory construction; contrastive and generative pretraining objectives are omitted.'],
        ['multimodal-RAG','retrieval','MuRAG','memory'])


def moe():
    f=figure('Multimodal mixture-of-experts routing',
        'LIMoE-inspired conceptual block: token content routes image and text streams into one shared expert pool.',
        'A sparse router dispatches each token to selected experts; weighted outputs rejoin the residual stream.',width=19)
    n(f,'image',r'Image patch tokens\\$X_v\in\mathbb{R}^{N_v\times d}$',1.8,2.6,2.9,1.0,'tensor')
    n(f,'text',r'Text tokens\\$X_t\in\mathbb{R}^{N_t\times d}$',1.8,6.1,2.9,1.0,'tensor')
    n(f,'shared',r'Shared attention\\and normalization\\$H\in\mathbb{R}^{N\times d}$',5.3,4.3,2.8,1.5)
    n(f,'router',r'Token router\\$g(h)=\mathrm{TopK}$\\$\bigl(\mathrm{softmax}(Wh)\bigr)$',8.7,4.3,2.8,1.5)
    for i,y in [(1,2.0),(2,4.3),(3,6.6)]:
        n(f,f'expert{i}',rf'Expert $E_{{{i}}}$\\feed-forward network',11.9,y,2.6,1.0)
        e(f,'router',f'expert{i}',side='east',to_side='west',via=[(10.4,4.3),(10.4,y)])
    n(f,'combine',r'Residual recombination\\{\scriptsize $h+\sum_{e\in\mathcal S}g_e(h)E_e(h)$}',15.5,4.3,3.4,1.5)
    n(f,'out',r'Next\\block',18.1,4.3,1.4,1.0)
    n(f,'aux',r'Routing regularization\\entropy / utilization',8.7,7.2,3.0,.9)
    e(f,'image','shared',side='east',to_side='north',via=[(5.3,2.6)])
    e(f,'text','shared',side='east',to_side='south',via=[(5.3,6.1)])
    e(f,'shared','router')
    for i,y in [(1,2.0),(2,4.3),(3,6.6)]:
        e(f,f'expert{i}','combine',side='east',to_side='west',via=[(13.55,y),(13.55,4.3)])
    e(f,'combine','out');e(f,'router','aux',r'training only',side='south',to_side='north',style='control')
    e(f,'shared','combine',r'residual',side='south',to_side='south',via=[(5.3,8.1),(15.5,8.1)],style='skip',label_side='below')
    note(f,r'Experts learn their specialization; no fixed modality assignment is imposed.',5.6,1.55,8.5)
    save(f,'multimodal-15-mixture-of-experts','Shared multimodal token processing with sparse content-dependent routing, a common expert bank, routing regularization, and residual recombination.',
        ['https://arxiv.org/abs/2206.02770','https://proceedings.neurips.cc/paper_files/paper/2022/file/3e67e84abf900bb2c7cbd5759bfce62d-Paper-Conference.pdf'],
        ['Conceptual LIMoE-inspired expert block; the expert count and top-k selection are illustrative and not asserted as an exact model configuration.','Image and text sequences can be encoded separately through shared weights; the display juxtaposes token sources rather than asserting cross-modal joint attention.'],
        ['MoE','LIMoE','sparse-routing','shared-experts'])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for build in [clip,vqa,captioning,llava,flamingo,clap,speech_bridge,video,audiovisual,early_late,vla,rgb_depth,document,rag,moe]:
        build()
    assert len(INDEX)==15
    (OUT/'index.json').write_text(json.dumps(INDEX,indent=2)+'\n')
    print(f'Wrote {len(INDEX)} original figures to {OUT}')


if __name__=='__main__':
    main()
