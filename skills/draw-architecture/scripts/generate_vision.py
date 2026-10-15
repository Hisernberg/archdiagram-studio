#!/usr/bin/env python3
"""Twenty original concept-level computer-vision TikZ architecture figures."""
from pathlib import Path
import json
from atlaslib import Figure

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'atlas' / 'vision'
INDEX = []

def make(title, width=18, height=9, caption=''):
    return Figure(title, width, height,
                  subtitle='Conceptual architecture | original schematic | symbolic dimensions',
                  caption=caption)

def save(f, slug, description, sources, tags, assumptions=None):
    INDEX.append(f.write(OUT, 'vision-' + slug, 'vision', description, sources,
                         assumptions=assumptions, tags=tags))

def grid(f, x, y, n, m=None, cell=.5, fills=None, heavy=(), labels=None):
    m = m or n
    fills = fills or {}
    for (r,c), gray in fills.items():
        f.raw(fr'\fill[black!{gray}] ({x+c*cell},{y+r*cell}) rectangle ({x+(c+1)*cell},{y+(r+1)*cell});')
    f.raw(fr'\draw[ink,line width=.45pt] ({x},{y}) rectangle ({x+m*cell},{y+n*cell});')
    for c in range(1,m):
        f.raw(fr'\draw[ink,line width=.45pt] ({x+c*cell},{y}) -- ({x+c*cell},{y+n*cell});')
    for r in range(1,n):
        f.raw(fr'\draw[ink,line width=.45pt] ({x},{y+r*cell}) -- ({x+m*cell},{y+r*cell});')
    for orient, k in heavy:
        if orient == 'v':
            f.raw(fr'\draw[ink,line width=1.25pt] ({x+k*cell},{y}) -- ({x+k*cell},{y+n*cell});')
        else:
            f.raw(fr'\draw[ink,line width=1.25pt] ({x},{y+k*cell}) -- ({x+m*cell},{y+k*cell});')
    for (r,c),label in (labels or {}).items():
        f.raw(fr'\node[font=\scriptsize] at ({x+(c+.5)*cell},{y+(r+.5)*cell}) {{{label}}};')

def note(f, text, x, y, width=5):
    f.raw(fr'\node[annotation,text width={width}cm] at ({x},{y}) {{{text}}};')


# 01: A spatial operator, with a receptive field rather than a generic layer chain.
f = make('Spatial convolution: one local response', 16, 9,
         'A kernel is reused at each spatial location; channel sums create each output channel.')
grid(f, 1.0, 2.0, 5, cell=.56, fills={(r,c):15 for r in range(3) for c in range(3)})
f.raw(r'\draw[ink,line width=1.1pt] (1,2) rectangle (2.68,3.68);')
grid(f, 6.0, 2.55, 3, cell=.56,
     labels={(r,c):fr'$w_{{{r+1}{c+1}}}$' for r in range(3) for c in range(3)})
grid(f, 11.0, 2.55, 3, cell=.56, fills={(0,0):30})
f.raw(r'\draw[flow] (3.9,3.4) -- node[above,font=\scriptsize] {local patch} (5.65,3.4);')
f.raw(r'\draw[flow] (8.0,3.4) -- node[above,font=\scriptsize] {multiply, sum} (10.6,3.4);')
f.node('input', r'Input $X$\par $5\times5$ illustration', 2.4, 5.35, 3, .7, 'plain')
f.node('kernel', r'Shared kernel $W$\par $3\times3$', 6.84, 5.35, 2.6, .7, 'plain')
f.node('output', r'Output $Y$\par valid padding, unit stride', 11.84, 5.35, 3.5, .7, 'plain')
f.node('equation', r'$Y_{o,i,j}=b_o+\displaystyle\sum_{c,u,v} W_{o,c,u,v}X_{c,i+u,j+v}$', 8, 7.0, 13, 1.0)
save(f, 'convolution', 'A shared spatial kernel, its receptive field, and the multi-channel convolution equation.',
     ['https://docs.pytorch.org/docs/2.14/generated/torch.nn.Conv2d.html'], ['cnn','convolution','receptive-field'],
     ['The illustrated spatial sizes are pedagogical; no model checkpoint is specified.', 'The equation follows the cross-correlation convention used by common deep-learning libraries.'])

# 02: The identity originates at x, before both residual convolutions.
f = make('Residual block: preserve an identity route', 18, 9,
         'The residual branch learns a correction; an identity shortcut reaches the same addition node.')
for args in [
    ('x',r'$x$',1.1,4.6,1.0,.9,'tensor'),
    ('c1',r'$3\times3$ conv\\BN, ReLU',4.0,4.6,2.5,1.15,'block'),
    ('c2',r'$3\times3$ conv\\BN',7.6,4.6,2.5,1.15,'block'),
    ('sum',r'$+$',10.9,4.6,.65,.65,'circle'),
    ('relu','ReLU',13.4,4.6,2,.85,'block'),
    ('y',r'$y$',16.5,4.6,1.2,.9,'tensor')]: f.node(*args)
for a,b in [('x','c1'),('c1','c2'),('c2','sum'),('sum','relu'),('relu','y')]: f.edge(a,b)
f.edge('x','sum',r'identity $x$',side='north',to_side='north',via=[(1.1,2.3),(10.9,2.3)],style='skip')
note(f,r'$y=\operatorname{ReLU}(F(x)+x)$',9,7.0,8)
save(f,'residual-block','A post-activation two-convolution residual block with an explicit identity shortcut.',
     ['https://arxiv.org/abs/1512.03385'],['cnn','residual','identity'],
     ['An identity shortcut assumes matching tensor shapes; projection shortcuts are outside this concept view.'])

# 03: Concatenated feature banks grow; they are not additive residual merges.
f=make('Dense block: accumulate earlier feature maps',18,9,
       'Each transform reads the complete feature bank; concatenation appends its new channels.')
f.node('x0',r'$x_0$',1.1,4.1,1.1,.9,'tensor')
f.node('h1',r'$H_1$\\BN--ReLU--Conv',3.5,4.1,2.2,1.0)
f.node('b1',r'Concat\\$[x_0,x_1]$',6.0,4.1,1.9,1.1,'tensor')
f.node('h2',r'$H_2$\\BN--ReLU--Conv',8.6,4.1,2.2,1.0)
f.node('b2',r'Concat\\$[x_0,x_1,x_2]$',11.2,4.1,2.1,1.1,'tensor')
f.node('h3',r'$H_3$\\BN--ReLU--Conv',13.8,4.1,2.2,1.0)
f.node('b3',r'Concat\\$[x_0,x_1,x_2,x_3]$',16.4,4.1,2.7,1.25,'tensor')
for a,b,label in [('x0','h1',''),('h1','b1',r'$x_1$'),('b1','h2',''),('h2','b2',r'$x_2$'),('b2','h3',''),('h3','b3',r'$x_3$')]: f.edge(a,b,label)
f.edge('x0','b1',side='south',to_side='south',via=[(1.1,6.2),(6,6.2)],style='skip')
f.edge('b1','b2',side='south',to_side='south',via=[(6,6.8),(11.2,6.8)],style='skip')
f.edge('b2','b3',side='south',to_side='south',via=[(11.2,7.4),(16.4,7.4)],style='skip')
note(f,r'$x_\ell=H_\ell([x_0,\ldots,x_{\ell-1}])$; dashed routes carry the accumulated bank.',8.7,2.1,12)
save(f,'dense-block','A three-layer DenseNet concept with explicit growing feature banks and reuse routes.',
     ['https://arxiv.org/abs/1608.06993'],['cnn','densenet','concatenation'])

# 04: A symmetric spatial hierarchy with lateral concatenations.
f=make('U-Net: contract for context, expand for localization',18,10,
       'Skip features are aligned and concatenated with the upsampled decoder stream at matching scales.')
f.node('x','Image',1.1,2.8,1.5,1.05,'tensor')
f.node('e1',r'Conv block\\fine scale',3.6,2.8,2.2,1.05)
f.node('e2',r'Conv block\\coarser scale',6.2,4.9,2.3,1.05)
f.node('b',r'Bottleneck\\context',9.0,7.1,2.4,1.05)
f.node('d2',r'Concat + conv\\coarser scale',12.0,4.9,2.6,1.05)
f.node('d1',r'Concat + conv\\fine scale',14.6,2.8,2.5,1.05)
f.node('y',r'$1\times1$ conv\\pixel logits',17.0,2.8,1.8,1.05,'tensor')
f.edge('x','e1')
f.edge('e1','e2','pool',side='south',to_side='west',via=[(3.6,4.9)])
f.edge('e2','b','pool',side='south',to_side='west',via=[(6.2,7.1)])
f.edge('b','d2','upsample',side='east',to_side='south',via=[(12,7.1)])
f.edge('d2','d1','upsample',side='east',to_side='south',via=[(14.6,4.9)])
f.edge('e2','d2','align + concatenate',style='skip')
f.edge('e1','d1','align + concatenate',side='north',to_side='north',via=[(3.6,1.7),(14.6,1.7)],style='skip')
f.edge('d1','y')
note(f,'Contracting path',3.3,7.8,4)
note(f,'Expanding path',14.3,7.8,4)
save(f,'unet','A reduced U-Net hierarchy with contracting and expanding paths and aligned skip concatenations.',
     ['https://arxiv.org/abs/1505.04597'],['segmentation','unet','encoder-decoder'],
     ['Two resolution changes illustrate the topology rather than reproduce the depth of a published checkpoint.', 'Alignment represents the cropping required by the original valid-convolution formulation.'])

# 05: Bottom-up features and a top-down semantic pathway are kept distinct.
f=make('Feature pyramid: bottom-up detail, top-down semantics',18,10.5,
       'Lateral projections combine backbone features with upsampled coarse features before spatial smoothing.')
f.group('Bottom-up backbone',1.6,1.6,3.0,7.1)
f.group('Top-down pyramid',6.0,1.6,10.5,7.1)
levels=[(5,2.6),(4,4.3),(3,6.0),(2,7.7)]
for level,y in levels:
    f.node(f'c{level}',fr'$C_{level}$',3.1,y,2.0,.9,'tensor')
    f.node(f'l{level}',r'$1\times1$ conv',7.4,y,2.1,.8)
    f.node(f'm{level}',r'$+$' if level!=5 else r'$\rightarrow$',10.6,y,.65,.65,'circle')
    f.node(f'p{level}',fr'$3\times3$ conv\\$P_{level}$',14.0,y,2.6,1.0,'tensor')
    f.edge(f'c{level}',f'l{level}')
    f.edge(f'l{level}',f'm{level}')
    f.edge(f'm{level}',f'p{level}')
for coarse in [5,4,3]:
    f.edge(f'c{coarse-1}',f'c{coarse}',side='north',to_side='south')
    f.edge(f'm{coarse}',f'm{coarse-1}','upsample',side='south',to_side='north')
note(f,'Resolution grows downward in the pyramid; each lateral sum has matching channel width.',9,9.25,14)
save(f,'feature-pyramid','A four-scale FPN with lateral 1x1 projections, top-down upsampling, addition, and 3x3 smoothing.',
     ['https://arxiv.org/abs/1612.03144'],['detection','fpn','multiscale'])

# 06: Patchification, token injection and a class-token readout.
f=make('Vision Transformer: an image becomes a token sequence',18,9,
       'Patch embeddings and a learned class token receive positions before repeated global attention blocks.')
f.node('image','',1.5,3.6,2.0,2.0,'plain')
grid(f,.5,2.6,4,cell=.5,heavy=[('v',2),('h',2)],fills={(r,c):12*((r+c)%2) for r in range(4) for c in range(4)})
f.node('patch',r'Flatten\\non-overlapping patches',4.1,3.6,2.5,1.15)
f.node('emb',r'Linear patch\\embedding',7.1,3.6,2.4,1.15)
f.node('seq',r'Class + patch tokens\\$[z_{\rm cls},z_1,\ldots,z_N]$',10.2,3.6,2.9,1.15,'tensor')
f.node('tr',r'Transformer\\encoder $\times L$',13.3,3.6,2.4,1.15)
f.node('head',r'Class-token\\MLP head',16.3,3.6,2.5,1.15)
f.node('cls','Learned class token',10.2,1.8,2.8,.7)
f.node('pos','Position embeddings',7.1,6.3,2.8,.8)
for a,b in [('image','patch'),('patch','emb'),('emb','seq'),('seq','tr'),('tr','head')]:f.edge(a,b)
f.edge('cls','seq',side='south',to_side='north')
f.edge('pos','seq',r'add to every token',side='east',to_side='south',via=[(10.2,6.3)])
note(f,'Global self-attention permits every patch token to exchange information with all other tokens.',12.1,7.5,9.5)
save(f,'vision-transformer','A ViT concept showing a patch grid, embeddings, class and position tokens, repeated encoder, and class readout.',
     ['https://arxiv.org/abs/2010.11929'],['transformer','vit','patches'])

# 07: Window partitions are explicitly shifted rather than renamed attention blocks.
f=make('Shifted-window attention: connect neighboring windows',18,9,
       'Alternating regular and shifted partitions creates cross-window communication without global attention.')
grid(f,1.2,1.8,8,cell=.36,heavy=[('v',4),('h',4)],fills={(r,c):12 if (r//4+c//4)%2 else 0 for r in range(8) for c in range(8)})
f.node('shift',r'Shift partition\\by $M/2$',6.6,3.15,2.4,1.0)
grid(f,9.5,1.8,8,cell=.36,heavy=[('v',2),('v',6),('h',2),('h',6)],fills={(r,c):12 if (r//4+c//4)%2 else 0 for r in range(8) for c in range(8)})
f.raw(r'\draw[flow] (4.3,3.15) -- (shift.west);\draw[flow] (shift.east) -- (9.15,3.15);')
note(f,'Regular windows',2.6,4.95,4)
note(f,'Shifted partition; masks prevent invalid wrap-around attention in the efficient cyclic implementation.',11.2,5.0,6.6)
f.node('w',r'Window attention\\residual + MLP',3.4,6.75,3.5,1.05)
f.node('sw',r'Shifted-window attention\\residual + MLP',9.0,6.75,4.0,1.05)
f.node('exchange',r'Neighboring windows\\exchange information',14.7,6.75,3.6,1.05,'tensor')
f.edge('w','sw');f.edge('sw','exchange')
save(f,'shifted-windows','Regular and shifted window grids linked to alternating Swin attention blocks and boundary masking.',
     ['https://arxiv.org/abs/2103.14030'],['transformer','swin','window-attention'],
     ['An eight-by-eight token grid with four-token windows illustrates the two-token partition shift.'])

# 08: The expensive encoder sees only visible tokens; loss is on masked patches.
f=make('Masked autoencoder: encode only visible image patches',18,10,
       'A lightweight decoder restores missing positions; reconstruction loss is evaluated on masked patches.')
f.node('img','',1.5,3.3,2.0,2.0,'plain')
mask={(r,c):55 if (r,c) not in {(0,0),(1,2),(2,1),(3,3)} else 0 for r in range(4) for c in range(4)}
grid(f,.5,2.3,4,cell=.5,fills=mask)
note(f,'Image patches: white visible, gray masked',1.6,1.75,3.0)
f.node('keep',r'Select visible\\patch tokens',4.2,3.3,2.3,1.0)
f.node('enc',r'Large encoder\\visible tokens only',7.2,3.3,2.5,1.1)
f.node('restore',r'Restore positions\\+ mask tokens',10.3,3.3,2.5,1.1)
f.node('dec',r'Small decoder\\all token positions',13.3,3.3,2.5,1.1)
f.node('pred',r'Predict\\patch pixels',16.3,3.3,2.3,1.1,'tensor')
f.node('mask','Learned mask token',10.3,1.7,2.6,.65)
f.node('target',r'Original pixels\\at masked positions',4.2,7.4,3.1,1.0,'tensor')
f.node('loss',r'Masked-patch loss\\$\sum_{i\in\mathcal M}\|\hat x_i-x_i\|^2$',12.1,7.4,5.2,1.2)
for a,b in [('img','keep'),('keep','enc'),('enc','restore'),('restore','dec'),('dec','pred')]:f.edge(a,b)
f.edge('mask','restore',side='south',to_side='north')
f.edge('img','target',side='south',to_side='west',via=[(1.5,7.4)])
f.edge('target','loss')
f.edge('pred','loss',side='south',to_side='east',via=[(16.3,7.4)])
save(f,'masked-autoencoder','An asymmetric masked autoencoder with visible-token encoding, mask-token restoration, and masked-pixel objective.',
     ['https://arxiv.org/abs/2111.06377'],['self-supervised','mae','masking'])

# 09: A deterministic bottleneck and direct reconstruction supervision.
f=make('Deterministic autoencoder: compress and reconstruct',16,9,
       'The compact code is a deterministic function of the input; reconstruction error trains both paths.')
f.node('x',r'Image\\$x$',1.2,4.0,1.3,3.0,'tensor')
f.node('enc',r'Encoder $f_\theta$\\downsample\\and compress',4.4,4.0,2.8,2.0)
f.node('z',r'Code\\$z$',8.0,4.0,1.4,.95,'tensor')
f.node('dec',r'Decoder $g_\phi$\\expand and\\reconstruct',11.6,4.0,2.8,2.0)
f.node('xh',r'Image\\$\hat x$',14.8,4.0,1.3,3.0,'tensor')
f.node('loss',r'Reconstruction objective\\$\mathcal L(x,g_\phi(f_\theta(x)))$',8.0,7.3,5.3,1.0)
for a,b in [('x','enc'),('enc','z'),('z','dec'),('dec','xh')]:f.edge(a,b)
f.edge('x','loss',side='south',to_side='west',via=[(1.2,7.3)])
f.edge('xh','loss',side='south',to_side='east',via=[(14.8,7.3)])
save(f,'deterministic-autoencoder','A deterministic encoder-decoder bottleneck with reconstruction paths from input and output into the objective.',
     ['https://www.cs.toronto.edu/~hinton/absps/science.pdf'],['autoencoder','representation','reconstruction'],
     ['This general image autoencoder concept does not reproduce the layer widths or pretraining of the cited work.'])

# 10: Posterior branches, reparameterization, and the two terms of the VAE bound.
f=make('Variational autoencoder: a distribution at the bottleneck',18,10,
       'Reparameterized samples connect reconstruction learning to a posterior regularized toward the prior.')
f.node('x',r'Image $x$',1.0,4.0,1.5,1.0,'tensor')
f.node('enc',r'Encoder\\$q_\phi(z\mid x)$',3.5,4.0,2.3,1.1)
f.node('mu',r'Mean $\mu_\phi(x)$',6.7,2.6,2.5,.8)
f.node('lv',r'Log-variance\\$\log\sigma_\phi^2(x)$',6.7,5.4,2.5,1.0)
f.node('sample',r'$z=\mu+\sigma\odot\epsilon$',10.3,4.0,3.2,1.05)
f.node('noise',r'$\epsilon\sim\mathcal N(0,I)$',10.3,1.7,3.0,.75,'tensor')
f.node('dec',r'Decoder\\$p_\theta(x\mid z)$',13.7,4.0,2.5,1.1)
f.node('out',r'$\hat x$',16.8,4.0,1.2,1.0,'tensor')
f.node('kl',r'$D_{\rm KL}(q_\phi(z\mid x)\Vert p(z))$',7.2,7.9,4.3,1.0)
f.node('rec',r'$-\mathbb E_q\log p_\theta(x\mid z)$',13.7,6.5,4.2,1.0)
f.node('obj',r'Negative ELBO\\reconstruction + KL',12.4,8.5,4.2,.95)
f.edge('x','enc')
f.edge('enc','mu',side='north',to_side='west',via=[(3.5,2.6)])
f.edge('enc','lv',side='south',to_side='west',via=[(3.5,5.4)])
f.edge('mu','sample',side='east',to_side='west',via=[(8.5,2.6),(8.5,4.0)])
f.edge('lv','sample',side='east',to_side='south',via=[(10.3,5.4)])
f.edge('noise','sample',side='south',to_side='north')
f.edge('sample','dec');f.edge('dec','out')
f.edge('lv','kl',side='south',to_side='north')
f.edge('mu','kl',side='west',to_side='west',via=[(4.9,2.6),(4.9,7.9)])
f.edge('out','rec',side='south',to_side='east',via=[(16.8,6.5)])
f.edge('x','rec',side='south',to_side='west',via=[(1.0,6.5)])
f.edge('kl','obj');f.edge('rec','obj',side='south',to_side='north')
save(f,'variational-autoencoder','A VAE with posterior parameters, noise reparameterization, reconstruction likelihood and KL objective paths.',
     ['https://arxiv.org/abs/1312.6114'],['vae','generative','latent-variable'],
     ['A diagonal Gaussian posterior and standard-normal prior are shown; decoder likelihood is abstract.'])

# 11: Real and generated samples share D; optimization feedback is visibly separate.
f=make('Adversarial generation: two models, one learning game',18,9,
       'The discriminator shares parameters across real and generated examples; gradient feedback updates both players.')
f.node('real',r'Real image\\$x\sim p_{\rm data}$',3.0,2.5,2.6,1.0,'tensor')
f.node('dr',r'Discriminator\\$D_\phi$',10.3,2.5,2.6,1.0)
f.node('sr',r'$D_\phi(x)$',13.4,2.5,1.8,.8,'tensor')
f.node('z',r'$z\sim p(z)$',1.5,5.9,2.0,.9,'tensor')
f.node('g',r'Generator\\$G_\theta$',5.0,5.9,2.4,1.0)
f.node('fake',r'Fake image\\$G_\theta(z)$',8.0,5.9,2.2,1.0,'tensor')
f.node('df',r'Discriminator\\$D_\phi$',11.0,5.9,2.6,1.0)
f.node('sf',r'$D_\phi(G_\theta(z))$',14.1,5.9,2.7,.8,'tensor')
f.node('obj',r'Minimax game\\$\min_\theta\max_\phi V(D,G)$',15.7,4.15,3.8,1.1)
for a,b in [('real','dr'),('dr','sr'),('z','g'),('g','fake'),('fake','df'),('df','sf')]:f.edge(a,b)
f.edge('sr','obj',side='east',to_side='north',via=[(15.7,2.5)])
f.edge('sf','obj',side='east',to_side='south',via=[(17.3,5.9),(17.3,4.9),(15.7,4.9)])
f.edge('dr','df','shared parameters',side='south',to_side='north',style='control')
f.edge('obj','df',side='south',to_side='north east',via=[(15.7,5.0),(12.3,5.0)],style='feedback')
note(f,r'update $\phi$',12.1,4.72,2.0)
f.edge('obj','g',r'update $\theta$',side='south',to_side='south',via=[(15.7,7.7),(5,7.7)],style='feedback')
note(f,r'$V=\mathbb E_x\log D(x)+\mathbb E_z\log(1-D(G(z)))$',6.6,1.5,11)
save(f,'gan','A two-player GAN with shared discriminator calls, real and generated data paths, and generator update feedback.',
     ['https://arxiv.org/abs/1406.2661'],['gan','adversarial','training'],
     ['The original minimax objective is shown; practical generator losses can differ.'])

# 12: Forward and reverse directions plus the epsilon-prediction training graph.
f=make('Denoising diffusion: corrupt forward, learn the reverse',18,10,
       'Training predicts the sampled noise at a random time; generation repeatedly applies the learned reverse transition.')
for id,label,x in [('x0',r'$x_0$\\clean image',2.0),('xm',r'$x_{t-1}$',6.2),('xt',r'$x_t$',10.4),('xT',r'$x_T$\\near-Gaussian',14.6)]:f.node(id,label,x,2.5,2.6,1.0,'tensor')
for a,b in [('x0','xm'),('xm','xt'),('xt','xT')]:
    f.edge(a,b,r'$q$: add noise')
    f.edge(b,a,r'$p_\theta$: denoise',side='south',to_side='south',via=[(f.nodes[b].x,4.0),(f.nodes[a].x,4.0)])
f.node('clean',r'Clean training image $x_0$',2.5,6.5,3.5,.9,'tensor')
f.node('corrupt',r'$x_t=\sqrt{\bar\alpha_t}x_0$\\$+\sqrt{1-\bar\alpha_t}\epsilon$',7.0,6.5,3.7,1.3)
f.node('denoise',r'Noise predictor\\$\epsilon_\theta(x_t,t)$',11.4,6.5,3.0,1.1)
f.node('loss',r'$\|\epsilon-\epsilon_\theta(x_t,t)\|^2$',15.6,6.5,3.5,1.0)
f.node('eps',r'$\epsilon\sim\mathcal N(0,I)$',4.2,8.5,3.0,.8,'tensor')
f.node('time',r'Random time $t$',11.4,8.4,2.7,.8)
f.edge('clean','corrupt');f.edge('corrupt','denoise');f.edge('denoise','loss')
f.edge('eps','corrupt',side='north',to_side='south',via=[(7,8.5)])
f.edge('eps','loss',side='south',to_side='south',via=[(4.2,9.2),(15.6,9.2)])
f.edge('time','denoise',side='north',to_side='south')
save(f,'ddpm','A DDPM forward/reverse timeline and noise-prediction training graph with sampled noise and time.',
     ['https://arxiv.org/abs/2006.11239'],['diffusion','ddpm','denoising'])

# 13: Compression is separate from the latent-space denoising process.
f=make('Latent diffusion: denoise a compressed image representation',18,10,
       'An autoencoder defines latent space; a conditioned denoiser learns there and its reverse process feeds the decoder.')
f.group('Denoiser training in latent space',.3,1.35,17.3,3.2)
f.node('x','Image',1.3,3.2,1.5,1.0,'tensor')
f.node('e',r'Encoder $E$',3.9,3.2,2.0,1.0)
f.node('z0',r'$z_0=E(x)$',6.4,3.2,2.1,1.0,'tensor')
f.node('q',r'Add noise\\$z_0\mapsto z_t$',9.0,3.2,2.3,1.0)
f.node('u',r'U-Net denoiser\\$\epsilon_\theta(z_t,t,c)$',12.3,3.2,3.2,1.0)
f.node('loss',r'Noise loss\\$\|\epsilon-\hat\epsilon\|^2$',16.0,3.2,2.8,1.0)
f.node('cond','Condition embedding $c$',12.3,1.85,3.5,.65)
for a,b in [('x','e'),('e','z0'),('z0','q'),('q','u'),('u','loss')]:f.edge(a,b)
f.edge('cond','u','cross-attention',side='south',to_side='north')
f.group('Sampling',.3,5.35,17.3,3.5)
f.node('zt',r'$z_T\sim\mathcal N(0,I)$',2.0,7.0,3.0,1.0,'tensor')
f.node('rev',r'Iterated reverse diffusion\\same $\epsilon_\theta$',6.3,7.0,3.8,1.1)
f.node('zh',r'Clean latent $\hat z_0$',10.4,7.0,2.9,1.0,'tensor')
f.node('d',r'Decoder $D$',13.7,7.0,2.3,1.0)
f.node('out',r'Image $\hat x$',16.6,7.0,1.9,1.0,'tensor')
f.node('c2','Condition $c$',6.3,5.9,2.8,.65)
for a,b in [('zt','rev'),('rev','zh'),('zh','d'),('d','out')]:f.edge(a,b)
f.edge('c2','rev',side='south',to_side='north')
note(f,'The autoencoder is pretrained before learning the latent denoising model.',9,9.25,14)
save(f,'latent-diffusion','Distinct latent-diffusion training and sampling panels with image compression, conditioning, reverse iteration and decoding.',
     ['https://arxiv.org/abs/2112.10752'],['diffusion','latent-diffusion','conditioning'],
     ['This is a generic latent diffusion concept, not a particular Stable Diffusion checkpoint or conditioning encoder.'])

# 14: Set prediction uses learned query inputs and bipartite supervision.
f=make('DETR: object queries predict an unordered set',18,10,
       'Learned queries attend to encoded image features; bipartite matching assigns predictions to target objects.')
for args in [
    ('x','Image',1.1,3.8,1.5,1.05,'tensor'),('cnn','CNN backbone',3.8,3.8,2.5,1.05,'block'),
    ('enc',r'Transformer\\encoder',6.9,3.8,2.4,1.05,'block'),('dec',r'Transformer\\decoder',10.1,3.8,2.5,1.05,'block'),
    ('head',r'Class + box\\prediction heads',13.4,3.8,2.6,1.05,'block'),('set',r'Object set\\$\{\hat y_i\}_{i=1}^{N}$',16.5,3.8,2.4,1.15,'tensor')]:f.node(*args)
for a,b in [('x','cnn'),('cnn','enc'),('enc','dec'),('dec','head'),('head','set')]:f.edge(a,b)
f.node('pos','Spatial positions',6.9,1.8,2.8,.7)
f.node('queries',r'$N$ learned\\object queries',10.1,1.8,3.2,.7)
f.edge('pos','enc',side='south',to_side='north')
f.edge('queries','dec',side='south',to_side='north')
f.node('gt',r'Ground-truth\\object set',16.0,7.4,2.8,1.0,'tensor')
f.node('match',r'Bipartite matching\\class and box costs',12.3,7.4,3.4,1.1)
f.node('loss',r'Set loss\\class + box terms',8.0,7.4,3.6,1.1)
f.edge('set','match',side='south',to_side='north',via=[(16.5,5.8),(12.3,5.8)])
f.edge('gt','match');f.edge('match','loss')
note(f,'Decoder self-attention relates queries; cross-attention reads the image memory.',5.4,6.0,8.0)
save(f,'detr','A DETR concept with spatial encodings, learned object queries, class/box set prediction and bipartite matching supervision.',
     ['https://arxiv.org/abs/2005.12872'],['detection','detr','set-prediction'])

# 15: Shared backbone features feed both proposal generation and regional recognition.
f=make('Two-stage detection: propose regions, then recognize them',18,9.5,
       'The region proposal network and RoI feature extraction share a backbone feature map.')
f.node('x','Image',1.1,4.1,1.5,1.1,'tensor')
f.node('back','Backbone CNN',3.8,4.1,2.5,1.1)
f.node('feat',r'Shared\\feature map',6.9,4.1,2.3,1.1,'tensor')
f.node('rpn',r'Proposal network\\objectness +\\box deltas',6.9,2.1,3.5,1.25)
f.node('prop',r'Select proposals\\decode boxes\\NMS',11.0,2.1,3.3,1.25)
f.node('roi',r'RoI pooling\\per proposed region',11.0,4.1,3.3,1.1)
f.node('head','Regional head',14.5,4.1,2.5,1.1)
f.node('cls','Classes',16.9,2.9,1.8,.85,'tensor')
f.node('box','Refined boxes',16.9,5.3,1.8,.85,'tensor')
for a,b in [('x','back'),('back','feat'),('feat','roi'),('roi','head')]:f.edge(a,b)
f.edge('feat','rpn',side='north',to_side='south');f.edge('rpn','prop')
f.edge('prop','roi',side='south',to_side='north')
f.edge('head','cls',side='north',to_side='west',via=[(14.5,2.9)])
f.edge('head','box',side='south',to_side='west',via=[(14.5,5.3)])
f.node('loss1',r'Proposal objective\\objectness + box regression',6.9,7.5,4.4,1.0)
f.node('loss2',r'Regional objective\\classification + box regression',13.4,7.5,4.8,1.0)
f.edge('rpn','loss1',side='east',to_side='north',via=[(8.8,2.1),(8.8,6.3),(6.9,6.3)])
f.edge('head','loss2',side='south',to_side='north',via=[(14.5,6.3),(13.4,6.3)])
save(f,'two-stage-detector','A Faster R-CNN concept with shared image features, proposal generation/selection, RoI pooling, and two prediction branches.',
     ['https://arxiv.org/abs/1506.01497'],['detection','faster-rcnn','proposals'],
     ['RoI pooling follows the original Faster R-CNN concept; implementation-specific backbone and anchor counts are omitted.'])

# 16: Dense parallel classification/regression applied independently to pyramid levels.
f=make('One-stage dense detection: predictions at every pyramid level',18,9,
       'Shared classification and box subnets are applied separately to each feature level; focal loss addresses class imbalance.')
f.node('back',r'Image backbone\\+ feature pyramid',2.2,4.5,3.4,1.5)
for level,y in [(3,2.4),(4,4.5),(5,6.6)]:
    f.node(f'p{level}',fr'$P_{level}$',5.6,y,1.7,1.0,'tensor')
    f.edge('back',f'p{level}',side='east',to_side='west',via=[(4.2,4.5),(4.2,y)])
f.node('cls',r'Apply shared $h_c$ per level\\$\{h_c(P_\ell)\}_\ell$\\dense class logits',9.4,3.1,4.1,1.6)
f.node('reg',r'Apply shared $h_b$ per level\\$\{h_b(P_\ell)\}_\ell$\\dense box offsets',9.4,6.1,4.1,1.6)
f.node('fl',r'Focal loss\\classification',15.0,3.1,3.5,1.2)
f.node('bl',r'Box regression\\objective',15.0,6.1,3.5,1.2)
for level in [3,4,5]:
    f.edge(f'p{level}','cls',side='east',to_side='west',via=[(7.0,f.nodes[f'p{level}'].y),(7.0,3.1)])
    f.edge(f'p{level}','reg',side='east',to_side='west',via=[(6.8,f.nodes[f'p{level}'].y),(6.8,6.1)])
f.edge('cls','fl');f.edge('reg','bl')
note(f,r'Illustrated levels are a subset. Each output retains its own spatial locations and anchors.',9,7.85,14)
save(f,'one-stage-detector','A RetinaNet concept with per-level shared dense heads and separate classification/focal and box-regression objectives.',
     ['https://arxiv.org/abs/1708.02002'],['detection','retinanet','focal-loss'],
     ['Three pyramid levels illustrate the repeated mapping; they are not the complete RetinaNet scale configuration.'])

# 17: Twin feature towers explicitly tie weights before a pairwise comparison.
f=make('Siamese image similarity: compare two shared representations',18,9,
       'Both images pass through the same encoder; a learned comparison maps their absolute feature difference to similarity.')
for suffix,y,label in [('a',2.7,r'Image $x_a$'),('b',6.0,r'Image $x_b$')]:
    f.node('x'+suffix,label,1.5,y,2.0,1.1,'tensor')
    f.node('f'+suffix,r'Shared CNN\\$f_\theta$',5.1,y,2.8,1.1)
    f.node('e'+suffix,fr'$f_\theta(x_{suffix})$',8.2,y,2.3,1.1,'tensor')
    f.edge('x'+suffix,'f'+suffix);f.edge('f'+suffix,'e'+suffix)
f.edge('fa','fb',r'same $\theta$',side='south',to_side='north',style='control')
f.node('diff',r'Absolute difference\\$|f_\theta(x_a)-f_\theta(x_b)|$',11.4,4.3,3.1,1.2)
f.node('cmp',r'Weighted sum\\+ sigmoid',14.4,4.3,2.2,1.1)
f.node('score',r'Similarity\\score',16.9,4.3,1.8,1.0,'tensor')
f.edge('ea','diff',side='east',to_side='north',via=[(11.4,2.7)])
f.edge('eb','diff',side='east',to_side='south',via=[(11.4,6.0)])
f.edge('diff','cmp');f.edge('cmp','score')
f.node('pair',r'Same/different\\pair label',11.4,7.6,3.0,.9,'tensor')
f.node('loss',r'Binary classification\\objective',15.4,7.6,3.4,.9)
f.edge('pair','loss');f.edge('score','loss',side='south',to_side='east',via=[(16.9,7.6)])
save(f,'siamese-similarity','A Siamese image pair architecture with tied CNN weights, absolute feature difference, learned similarity and pair supervision.',
     ['https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf'],['siamese','metric-learning','similarity'])

# 18: Spatial filtering is independent by channel, then 1x1 filters mix channels.
f=make('Depthwise separable convolution: split spatial and channel mixing',18,9,
       'Depthwise filters act independently on input channels; pointwise filters combine the resulting channels.')
f.group('Independent spatial filtering',.4,1.6,7.8,6.1)
for c,y in [(1,2.7),(2,4.7),(3,6.7)]:
    f.node(f'x{c}',fr'Channel $x_{c}$',1.7,y,1.8,1.3,'tensor')
    f.node(f'k{c}',fr'$K\times K$\\filter $w_{c}$',4.1,y,1.8,1.2)
    f.node(f'd{c}',fr'$d_{c}$',6.7,y,1.5,1.3,'tensor')
    f.edge(f'x{c}',f'k{c}');f.edge(f'k{c}',f'd{c}')
f.node('pw',r'$1\times1$ pointwise conv\\$y_k=\sum_c v_{kc}d_c$',11.1,4.7,3.8,1.8)
f.node('y',r'Output channels\\$C_{\rm out}$',15.7,4.7,3.0,2.3,'tensor')
for c in [1,2,3]:f.edge(f'd{c}','pw',side='east',to_side='west',via=[(8.6,f.nodes[f'd{c}'].y),(8.6,4.7)])
f.edge('pw','y')
note(f,r'Parameters: $K^2C_{\rm in}+C_{\rm in}C_{\rm out}$, compared with $K^2C_{\rm in}C_{\rm out}$ for a full convolution.',9,8.0,16)
save(f,'depthwise-separable','A channel-explicit depthwise convolution followed by cross-channel pointwise mixing and its parameter expression.',
     ['https://arxiv.org/abs/1704.04861'],['cnn','mobilenet','depthwise'],
     ['Three input channels are drawn as an illustration; channel counts and spatial sizes are symbolic.'])

# 19: Parallel atrous context branches and image-level pooling, not a serial dilation chain.
f=make('Atrous spatial pyramid pooling: parallel scales of context',18,10.5,
       'Dilated convolutions and image-level pooling gather complementary context before concatenation and dense prediction.')
f.node('x','Image',1.0,5.1,1.5,1.0,'tensor')
f.node('back',r'Dilated\\backbone',3.3,5.1,2.1,1.3)
f.edge('x','back')
branches=[('p1',r'$1\times1$ conv',2.1),('a1',r'$3\times3$ atrous\\rate $r_1$',3.65),('a2',r'$3\times3$ atrous\\rate $r_2$',5.2),('a3',r'$3\times3$ atrous\\rate $r_3$',6.75),('pool',r'Image pool\\project + resize',8.3)]
for id,label,y in branches:
    f.node(id,label,6.5,y,2.5,1.0)
    f.edge('back',id,side='east',to_side='west',via=[(4.85,5.1),(4.85,y)])
f.node('cat','Concat',10.0,5.1,1.7,1.25)
f.node('proj',r'$1\times1$\\projection',12.4,5.1,2.0,1.0)
f.node('up',r'Resize to\\image grid',14.8,5.1,2.0,1.0)
f.node('seg',r'Pixel\\logits',17.0,5.1,1.7,1.1,'tensor')
for id,label,y in branches:f.edge(id,'cat',side='east',to_side='west',via=[(8.6,y),(8.6,5.1)])
for a,b in [('cat','proj'),('proj','up'),('up','seg')]:f.edge(a,b)
note(f,r'Atrous rates $r_1,r_2,r_3$ change sampling spacing while retaining the feature grid.',9,9.4,15)
save(f,'atrous-segmentation','A DeepLabv3-style ASPP context module with three atrous branches, a 1x1 branch, image pooling, fusion and resizing.',
     ['https://arxiv.org/abs/1706.05587'],['segmentation','deeplab','aspp','dilated-convolution'],
     ['Dilation rates are symbolic and depend on output stride and implementation.'])

# 20: A real 2x2-to-one rearrangement exposes the spatial/channel trade-off.
f=make('Hierarchical patch merging: trade resolution for channels',18,10,
       'Four neighboring tokens are concatenated, normalized, and projected into one token at the next stage.')
f.group('Whole feature grid',.4,1.5,17.1,3.1)
f.node('input','',1.8,3.0,2.4,2.0,'plain')
grid(f,.6,1.8,4,cell=.6,heavy=[('v',2),('h',2)],fills={(r,c):13 if (r//2+c//2)%2 else 0 for r in range(4) for c in range(4)})
f.node('gather',r'Gather each\\$2\times2$ neighborhood',5.0,3.0,2.7,1.1)
f.node('concat',r'Concatenate\\$H/2\times W/2\times4C$',8.4,3.0,3.3,1.1,'tensor')
f.node('norm','LayerNorm',11.9,3.0,2.2,1.0)
f.node('linear',r'Linear\\$4C\mapsto2C$',14.8,3.0,2.4,1.0)
for a,b in [('input','gather'),('gather','concat'),('concat','norm'),('norm','linear')]:f.edge(a,b)
f.group('One neighborhood',.4,5.35,17.1,3.2)
grid(f,1.5,6.05,2,cell=.65,labels={(0,0):'$a$',(0,1):'$b$',(1,0):'$c$',(1,1):'$d$'})
f.node('local','',2.15,6.7,1.3,1.3,'plain')
f.node('vec',r'$[a;b;c;d]$\\$\in\mathbb R^{4C}$',6.2,6.7,3.1,1.2,'tensor')
f.node('map',r'LayerNorm + linear\\shared at every location',10.8,6.7,4.1,1.2)
f.node('out',r'One coarse token\\$\in\mathbb R^{2C}$',15.3,6.7,3.1,1.2,'tensor')
f.edge('local','vec');f.edge('vec','map');f.edge('map','out')
note(f,r'Global output shape: $(H/2)\times(W/2)\times2C$.',9,9.2,13)
save(f,'patch-merging','A hierarchical patch merging operation with a 2x2 neighborhood grid, 4C concatenation, normalization and 2C projection.',
     ['https://arxiv.org/abs/2103.14030'],['transformer','swin','patch-merging','hierarchy'],
     ['H and W are even. The 4C-to-2C projection follows the original Swin patch-merging formulation.'])

assert len(INDEX)==20
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'index.json').write_text(json.dumps(INDEX,indent=2)+'\n')
print(f'Wrote {len(INDEX)} figures to {OUT}')

