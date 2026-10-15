#!/usr/bin/env python3
"""Generate the original, conceptual language/sequence family of the atlas."""
from pathlib import Path
import json
from atlaslib import Figure

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "atlas" / "text"
ATTN = "https://arxiv.org/abs/1706.03762"
PRELN = "https://arxiv.org/abs/2002.04745"
SEQ = "https://arxiv.org/abs/1409.3215"


def fig(title, caption, height=9, subtitle="Conceptual schematic; symbolic dimensions; batch axis omitted"):
    return Figure(title, width=16, height=height, subtitle=subtitle, caption=caption)


def n(f, name, label, x, y, w=2.5, h=.8, kind="block"):
    return f.node(name, label, x, y, w, h, kind)


def e(f, a, b, label="", **kwargs):
    f.edge(a, b, label, **kwargs)


def note(f, label, x, y, w=5, h=.5):
    return n(f, "note" + str(len(f.nodes)), label, x, y, w, h, "plain")


def save(f, id, description, sources, assumptions=None, tags=None):
    return f.write(OUT, id, "text", description, sources, assumptions, tags)


def token_embedding():
    f = fig("Subword tokenization and embedding lookup", "Token boundaries and identifiers are illustrative; a learned table maps each token to a model-width vector.")
    n(f,"text",r"Raw text\\\texttt{replaying}",2,2.1,3,.9)
    n(f,"tok",r"Subword tokenizer\\fixed vocabulary",5.7,2.1,3.2,.9)
    n(f,"pieces",r"Illustrative pieces\\\texttt{re} $\mid$ \texttt{play} $\mid$ \texttt{ing}",10.7,2.1,4.5,.9)
    n(f,"ids",r"Token identifiers\\$t_1,t_2,\ldots,t_T$",10.7,3.8,4.5,.9,"tensor")
    n(f,"vocab",r"Vocabulary\\piece $\leftrightarrow$ identifier",2,5.3,3,1.2,"store")
    n(f,"table",r"Learned table\\$E\in\mathbb{R}^{|\mathcal V|\times d}$",5.7,5.3,3.2,1.2,"store")
    n(f,"lookup",r"Gather rows\\$e_i=E[t_i]$",10.7,5.3,4.5,1.0)
    n(f,"pos",r"Position vectors\\$P\in\mathbb{R}^{T\times d}$",5.7,7.4,3.2,.9,"tensor")
    n(f,"out",r"Sequence representation\\$X_i=e_i+P_i\quad X\in\mathbb{R}^{T\times d}$",10.7,7.4,4.5,.9,"tensor")
    e(f,"text","tok"); e(f,"tok","pieces"); e(f,"pieces","ids"); e(f,"ids","lookup")
    e(f,"vocab","tok",side="north",to_side="south",via=[(2,3.5),(5.7,3.5)])
    e(f,"vocab","table"); e(f,"table","lookup"); e(f,"lookup","out"); e(f,"pos","out","add")
    return save(f,"text_01_token_embedding","Subword segmentation, vocabulary identifiers, learned embedding lookup, and additive position vectors.",["https://arxiv.org/abs/1508.07909",ATTN],["Illustrative segmentation is not the output of a particular trained tokenizer.","Additive position vectors are a chosen example; RoPE is a different mechanism."],["tokenization","embedding","subword"])


def causal_decoder():
    f = fig("Causal decoder with pre-normalized residual blocks", "Each residual starts before its normalization; the block repeats with distinct parameters across layers.")
    n(f,"tokens",r"Input tokens $x_{1:T}$",2.7,1.7,3.7,.7,"tensor")
    n(f,"embed",r"Embedding and\\position mechanism",2.7,3.0,3.7,.9)
    n(f,"block",r"Pre-norm decoder block\\causal attention $+$ FFN",2.7,4.6,3.7,1.15)
    n(f,"norm",r"Final norm",2.7,6.3,3.7,.8)
    n(f,"head",r"Vocabulary projection; softmax\\$p(x_{t+1}\mid x_{\leq t})$",2.7,7.65,4.2,.95)
    for a,b in [("tokens","embed"),("embed","block"),("block","norm"),("norm","head")]: e(f,a,b)
    f.raw(r"\draw[decorate,decoration={brace,amplitude=4pt},draw=ink] (5.0,5.2)--(5.0,4.0) node[midway,right=5pt,font=\small] {$L$};")
    f.group(r"Block detail",6.5,1.3,8.8,6.95)
    n(f,"x",r"$H^{\ell-1}$",10.5,1.7,3.3,.65,"tensor")
    n(f,"attn",r"Norm $\rightarrow$ causal self-attention\\query $i$ sees keys $j\leq i$",10.5,2.95,4.3,1.0)
    n(f,"add1",r"$+$",10.5,4.15,.65,.65)
    n(f,"ffn",r"Norm $\rightarrow$ positionwise FFN",10.5,5.35,4.3,.9)
    n(f,"add2",r"$+$",10.5,6.55,.65,.65)
    n(f,"h",r"$H^\ell\in\mathbb{R}^{T\times d}$",10.5,7.65,4.3,.65,"tensor")
    for a,b in [("x","attn"),("attn","add1"),("add1","ffn"),("ffn","add2"),("add2","h")]: e(f,a,b)
    e(f,"x","add1","identity",side="west",to_side="west",via=[(7.4,1.7),(7.4,4.15)],style="skip",label_side="left")
    e(f,"add1","add2","identity",side="east",to_side="east",via=[(14.2,4.15),(14.2,6.55)],style="skip",label_side="right")
    f.raw(r"\draw[draw=soft,dashed,line width=.45pt] (block.east)--(6.25,4.6);\node[annotation] at (5.75,4.35) {detail};")
    return save(f,"text_02_causal_decoder","Pre-normalized causal decoder block with two correctly originated identity residuals and a language-model readout.",[ATTN,PRELN],["Conceptual pre-normalized decoder; no particular model's layer count, norm type, or position method is implied."],["decoder","causal","residual","pre-norm"])


def encoder_decoder():
    f = fig("Encoder--decoder Transformer", "Encoder memory supplies keys and values to every decoder cross-attention layer.",10)
    f.group(r"Encoder layer $\times L_e$",1.6,3.85,4.9,3.3)
    f.group(r"Decoder layer $\times L_d$",9.0,3.85,5.1,4.45)
    n(f,"src",r"Source tokens $s_{1:S}$",4,1.8,3.8,.8,"tensor")
    n(f,"se",r"Token embedding\\$+$ source positions",4,3,3.8,.9)
    n(f,"sa",r"Full self-attention\\residual, then norm",4,4.6,3.8,1.0)
    n(f,"sf",r"Positionwise FFN\\residual, then norm",4,6.25,3.8,1.0)
    n(f,"mem",r"Encoder memory\\$M\in\mathbb{R}^{S\times d}$",4,8.1,3.8,1.0,"tensor")
    n(f,"tgt",r"Shifted target tokens\\$\langle\mathrm{BOS}\rangle,y_{<t}$",11.55,1.8,4.0,.8,"tensor")
    n(f,"te",r"Token embedding\\$+$ target positions",11.55,3,4.0,.9)
    n(f,"ta",r"Masked self-attention\\residual, then norm",11.55,4.6,4.0,1.0)
    n(f,"cross",r"Cross-attention\\$Q$: decoder; $K,V$: memory\\residual, then norm",11.55,6.1,4.0,1.15)
    n(f,"tf",r"Positionwise FFN\\residual, then norm",11.55,7.65,4.0,1.0)
    n(f,"out",r"Vocabulary projection and softmax\\$p(y_t\mid y_{<t},s)$",11.55,8.95,4.0,.85)
    for a,b in [("src","se"),("se","sa"),("sa","sf"),("sf","mem"),("tgt","te"),("te","ta"),("ta","cross"),("cross","tf"),("tf","out")]:e(f,a,b)
    e(f,"mem","cross","$K,V$",side="east",to_side="west",via=[(7.6,8.1),(7.6,6.1)])
    note(f,r"Source and target lengths $S,T$ may differ.",4,9.05,5.5,.5)
    return save(f,"text_03_encoder_decoder","Paired encoder and autoregressive decoder stacks with source memory connected only to decoder cross-attention keys and values.",[ATTN],["Original post-norm ordering is summarized in labels; residual wires are not expanded.","Layer repeat counts are symbolic."],["transformer","encoder-decoder","cross-attention"])


def self_attention():
    f = fig("Scaled dot-product self-attention", "Rows are queries, columns are keys; normalization runs over allowed key positions for each query.")
    n(f,"x",r"One sequence $X\in\mathbb{R}^{T\times d}$",8,1.7,5.3,.8,"tensor")
    n(f,"q",r"$Q=XW_Q$\\$T\times d_k$",3,3.1,3,.9,"tensor")
    n(f,"k",r"$K=XW_K$\\$T\times d_k$",7.5,3.1,3,.9,"tensor")
    n(f,"v",r"$V=XW_V$\\$T\times d_v$",12.8,3.1,3,.9,"tensor")
    n(f,"score",r"Pairwise scores\\$QK^\top/\sqrt{d_k}$",4.9,4.8,3.4,.95)
    n(f,"softmax",r"Add mask $M$\\rowwise softmax",8.8,4.8,3.0,.95)
    n(f,"a",r"$A_{ij}=p(j\mid i)$\\$A\in\mathbb{R}^{T\times T}$",8.8,6.9,3.0,.95,"tensor")
    n(f,"y",r"Weighted values\\$Y=AV\in\mathbb{R}^{T\times d_v}$",12.8,6.9,3.6,.95,"tensor")
    for t in ["q","k","v"]:e(f,"x",t)
    e(f,"q","score",side="south",to_side="west",via=[(3,4.8)])
    e(f,"k","score",side="south",to_side="north",via=[(7.5,4.1),(4.9,4.1)])
    e(f,"score","softmax");e(f,"softmax","a");e(f,"a","y");e(f,"v","y")
    f.raw(r"\node[annotation] at (2.1,5.55) {Illustrative causal mask};")
    for i in range(4):
        for j in range(4):
            x,y=1+j*.55,5.9+i*.55
            f.raw(r"\draw[draw=soft,line width=.35pt,fill="+("wash" if j<=i else "gray!35")+f"] ({x},{y}) rectangle ({x+.55},{y+.55});")
    f.raw(r"\node[annotation] at (2.1,8.25) {key index $j$ $\rightarrow$};\node[annotation,rotate=90] at (.35,7) {query index $i$};\draw[flow] (.7,5.9)--(.7,8.1);")
    note(f,r"$M_{ij}=0$ for $j\leq i$; $M_{ij}=-\infty$ otherwise.",5.8,8.1,5.2,.5)
    return save(f,"text_04_scaled_self_attention","Self-attention factorization with symbolic query/key/value shapes, correct attention axes, and an illustrative causal mask.",[ATTN],["Single attention head; the batch axis is omitted.","Causal masking is the selected example; full self-attention omits that mask."],["attention","mask","tensor-shapes"])


def cross_attention():
    f = fig("Cross-attention with a query-stream residual", "The output has the query length; the identity path starts at the decoder state, before query projection.")
    n(f,"h",r"Decoder states\\$H\in\mathbb{R}^{T\times d}$",3.0,1.9,3.6,.9,"tensor")
    n(f,"m",r"Source memory\\$M\in\mathbb{R}^{S\times d}$",11.0,1.9,5.0,.9,"tensor")
    n(f,"q",r"$Q=HW_Q$\\$T\times d_k$",3.0,3.5,3.0,.9)
    n(f,"k",r"$K=MW_K$\\$S\times d_k$",9.0,3.5,3.0,.9)
    n(f,"v",r"$V=MW_V$\\$S\times d_v$",13.0,3.5,3.0,.9)
    n(f,"score",r"$A=\operatorname{softmax}_{j}(QK^\top/\sqrt{d_k})$\\$A\in\mathbb{R}^{T\times S}$",6.7,5.4,5.8,1.0)
    n(f,"out",r"$O=AVW_O$\\$T\times d$",11.6,6.9,3.2,1.0)
    n(f,"add",r"Add\\$H+O$",14.3,6.9,1.8,1.0)
    e(f,"h","q");e(f,"m","k");e(f,"m","v")
    e(f,"q","score",side="south",to_side="west",via=[(3,5.4)])
    e(f,"k","score",side="south",to_side="north",via=[(9,4.55),(6.7,4.55)])
    e(f,"score","out",side="east",to_side="west",via=[(10,5.4),(10,6.9)])
    e(f,"v","out",side="south",to_side="north",via=[(13,6.0),(11.6,6.0)])
    e(f,"out","add")
    e(f,"h","add",side="west",to_side="south",via=[(.55,1.9),(.55,7.9),(14.3,7.9)],style="skip")
    for i in range(3):
        for j in range(5):
            x,y=1.3+j*.4,6.2+i*.4
            f.raw(f"\\draw[draw=soft,fill=wash,line width=.35pt] ({x},{y}) rectangle ({x+.4},{y+.4});")
    f.raw(r"\node[annotation] at (2.3,6.0) {$S$ source keys};\node[annotation,rotate=90] at (.95,6.8) {$T$ queries};")
    return save(f,"text_05_cross_attention","Cross-attention with rectangular T-by-S weights and a residual that originates from the decoder query stream.",[ATTN],["Single head shown; output projection restores the query stream width d.","Normalization wrapper omitted to isolate attention and residual origin."],["cross-attention","residual","query-memory"])


def multi_head():
    f = fig("Multi-head attention: separate projections, joined outputs", "Each head computes its own attention map; concatenation precedes the shared output projection.")
    n(f,"x",r"$X\in\mathbb{R}^{T\times d}$",8,1.7,4,.8,"tensor")
    for ident,x,label in [("a",3,r"1"),("b",8,r"i"),("c",13,r"h")]:
        f.group(r"Head $"+label+r"$",x-2.0,2.6,4.0,3.85)
        n(f,"proj"+ident,r"$Q_{"+label+r"},K_{"+label+r"},V_{"+label+r"}$\\head-specific $W$",x,3.3,3.4,.9)
        n(f,"attn"+ident,r"$S_{"+label+r"}=Q_{"+label+r"}K_{"+label+r"}^{\top}/\sqrt{d_k}$\\$A_{"+label+r"}=\operatorname{softmax}(S_{"+label+r"})$\\$O_{"+label+r"}=A_{"+label+r"}V_{"+label+r"}$",x,4.75,3.4,1.15)
        n(f,"o"+ident,r"$O_{"+label+r"}\in\mathbb{R}^{T\times d_v}$",x,6.1,3.4,.65,"tensor")
        e(f,"x","proj"+ident);e(f,"proj"+ident,"attn"+ident);e(f,"attn"+ident,"o"+ident)
    n(f,"cat",r"Concatenate features\\$[O_1;\ldots;O_h]$",7,7.5,4,.9)
    n(f,"wo",r"Output projection\\$W_O\in\mathbb{R}^{h d_v\times d}$",12.2,7.5,4.1,.9)
    for ident,x in [("a",3),("b",8),("c",13)]:
        e(f,"o"+ident,"cat",side="south",to_side="north",via=[(x,6.8),(7,6.8)])
    e(f,"cat","wo")
    note(f,r"Only representative heads are drawn; $h$ is symbolic.",3.0,8.2,5.2,.4)
    return save(f,"text_06_multi_head_attention","Parallel head-specific query/key/value projections and attention maps followed by feature concatenation and output projection.",[ATTN],["Representative heads 1, i, and h stand for an arbitrary number of heads.","Feature widths are symbolic and need not be assigned numeric values."],["multi-head","attention","parallel-branches"])


def grouped_query():
    f = fig("Grouped-query attention: several queries share keys and values", "A query head uses the key/value head of its assigned group; head outputs are then concatenated.")
    for g,left,qs in [("g",.7,[("j",2.8),("k",6.0)]),("g'",8.6,[("r",10.7),("s",13.9)])]:
        f.group(r"KV group $"+g+r"$",left,1.8,6.7,4.65)
        for q,x in qs:
            n(f,"q"+q,r"$Q_{"+q+r"}=XW_{Q,"+q+r"}$",x,2.6,2.6,.8,"tensor")
            n(f,"a"+q,r"Attention\\$Q_{"+q+r"},K_{"+g+r"},V_{"+g+r"}$",x,5.45,2.6,1.0)
            e(f,"q"+q,"a"+q,side="south",to_side="north")
        mid=(qs[0][1]+qs[1][1])/2
        kv_id="kv"+qs[0][0]
        n(f,kv_id,r"Shared $K_{"+g+r"},V_{"+g+r"}$\\from $X$",mid,3.95,2.6,.85,"tensor")
        for pos,(q,x) in enumerate(qs):
            port=x+(.65 if pos==0 else -.65)
            f.raw(r"\draw[flow] ("+kv_id+f".south)--({mid},4.6)--({port},4.6)--({port},4.95);")
    n(f,"cat",r"Concatenate all query-head outputs; apply $W_O$",8,7.6,8.5,.9)
    for q,x in [("j",2.8),("k",6),("r",10.7),("s",13.9)]:
        e(f,"a"+q,"cat",side="south",to_side="north",via=[(x,6.9),(8,6.9)])
    return save(f,"text_07_grouped_query_attention","Grouped-query attention shows explicitly shared K/V tensors within groups and distinct query-head attention computations.",["https://arxiv.org/abs/2305.13245"],["Two representative groups with two representative queries each are a schematic partition, not a fixed model configuration.","All projections are from the same sequence X."],["GQA","attention","shared-KV"])


def kv_cache():
    f = fig("Autoregressive decoding with a per-layer KV cache", "Only the current query is evaluated against the enlarged cache; past keys and values are reused.")
    n(f,"x",r"Current hidden state\\$x_t\in\mathbb{R}^{1\times d}$",1.8,2.2,3.1,1.0,"tensor")
    n(f,"proj",r"Head projections\\$W_Q,W_K,W_V$",5.3,2.2,3.0,1.0)
    n(f,"q",r"Current query $q_t$",9,2.2,2.8,.9,"tensor")
    n(f,"attn",r"Attend\\$a_t=\operatorname{softmax}(q_t K_{1:t}^{\top}/\sqrt{d_k})$\\$o_t=a_tV_{1:t}$",12.8,2.2,4.0,1.3)
    n(f,"new",r"Current $k_t,v_t$",8,4.35,3,.9,"tensor")
    n(f,"old",r"Previous cache\\$K_{1:t-1},V_{1:t-1}$",3.5,6.7,4.4,1.25,"store")
    n(f,"append",r"Append at\\position $t$",8,6.7,2.7,1.0)
    n(f,"cache",r"Updated cache\\$K_{1:t},V_{1:t}$",12.8,6.7,3.6,1.25,"store")
    n(f,"out",r"Head result at $t$",12.8,4.3,3.6,.85,"tensor")
    e(f,"x","proj");e(f,"proj","q");e(f,"q","attn");e(f,"attn","out")
    e(f,"proj","new",side="south",to_side="west",via=[(5.3,4.35)])
    e(f,"new","append");e(f,"old","append");e(f,"append","cache");e(f,"cache","attn","read",side="east",to_side="east",via=[(15.3,6.7),(15.3,2.2)])
    note(f,r"Cache sequence axis grows from $t-1$ to $t$; old queries are not stored here.",6.7,8.1,11,.5)
    return save(f,"text_08_kv_cache","Single-step autoregressive attention with separate current Q and new K/V, explicit cache append, and cache read.",["https://arxiv.org/abs/1911.02150",ATTN],["One layer and representative head shown; implementations may pack or page the cache differently.","Projection and attention normalization wrappers omitted."],["KV-cache","decoding","storage"])


def rope():
    f = fig("Rotary positions act on query and key feature pairs", "Position rotations change query--key dot products through relative position; values follow their ordinary projection path.")
    n(f,"q",r"Unrotated query\\$q_m=W_Qx_m$",2.4,2.5,3.4,1.0,"tensor")
    n(f,"k",r"Unrotated key\\$k_n=W_Kx_n$",2.4,5.4,3.4,1.0,"tensor")
    n(f,"rq",r"Rotate feature pairs\\$R_m$",6.4,2.5,3.2,1.0)
    n(f,"rk",r"Rotate feature pairs\\$R_n$",6.4,5.4,3.2,1.0)
    n(f,"oq",r"$\widetilde q_m=R_m q_m$",10.4,2.5,3.3,.9,"tensor")
    n(f,"ok",r"$\widetilde k_n=R_n k_n$",10.4,5.4,3.3,.9,"tensor")
    n(f,"dot",r"Dot product\\$\widetilde q_m^{\top}\widetilde k_n$",14.1,4.0,3.0,1.05)
    e(f,"q","rq");e(f,"rq","oq");e(f,"k","rk");e(f,"rk","ok")
    e(f,"oq","dot",side="east",to_side="north",via=[(14.1,2.5)])
    e(f,"ok","dot",side="east",to_side="south",via=[(14.1,5.4)])
    note(f,r"Each feature-pair block: $R_m^{(a)}=\begin{bmatrix}\cos(m\theta_a)&-\sin(m\theta_a)\\\sin(m\theta_a)&\cos(m\theta_a)\end{bmatrix}$",8,7.0,13,1.0)
    note(f,r"$\widetilde q_m^{\top}\widetilde k_n=q_m^{\top}R_{n-m}k_n$",8,8.1,13,.5)
    return save(f,"text_09_rotary_positions","Separate position-indexed rotations of query and key feature pairs and their relative-position dot-product identity.",["https://arxiv.org/abs/2104.09864"],["Column-vector convention is used in this figure; model-wide row-vector notation is equivalent after transposition.","Pair-specific frequencies theta_a are symbolic; value rotation is not shown."],["RoPE","position","rotation"])


def swiglu():
    f = fig("SwiGLU feed-forward network", "A SiLU-transformed gate modulates the parallel up-projection before the down-projection restores model width.")
    n(f,"x",r"$X\in\mathbb{R}^{T\times d}$",1.7,4.5,2.8,1.0,"tensor")
    n(f,"wg",r"Gate projection\\$G=XW_g$",5.0,2.5,3.0,1.0)
    n(f,"wu",r"Up-projection\\$U=XW_u$",5.0,6.5,3.0,1.0)
    n(f,"silu",r"$\operatorname{SiLU}(G)$\\$G\odot\sigma(G)$",8.6,2.5,3.0,1.0)
    n(f,"mul",r"$\odot$",8.6,4.5,.75,.75)
    n(f,"wd",r"Down-projection\\$W_d\in\mathbb{R}^{d_f\times d}$",11.4,4.5,3.2,1.0)
    n(f,"out",r"$Y$\\$T\times d$",14.6,4.5,1.8,1.0,"tensor")
    e(f,"x","wg",side="north",to_side="west",via=[(1.7,2.5)])
    e(f,"x","wu",side="south",to_side="west",via=[(1.7,6.5)])
    e(f,"wg","silu");e(f,"silu","mul");e(f,"wu","mul",side="east",to_side="south",via=[(8.6,6.5)])
    e(f,"mul","wd");e(f,"wd","out")
    note(f,r"$W_g,W_u\in\mathbb{R}^{d\times d_f}$; the elementwise product preserves $T\times d_f$.",8,7.85,12.8,.6)
    return save(f,"text_10_swiglu_ffn","Two-branch SwiGLU feed-forward network with SiLU gate, elementwise multiplication, and output projection.",["https://arxiv.org/abs/2002.05202"],["Biases and residual/norm wrappers are omitted to isolate the feed-forward transformation.","The intermediate width d_f is symbolic."],["SwiGLU","FFN","gating"])


def moe():
    f = fig("Sparse mixture-of-experts decoder and routing detail", "The router selects experts per token; only selected experts receive data and contribute weighted outputs.",10)
    n(f,"tokens",r"Token embeddings",2.4,1.8,3.6,.85,"tensor")
    n(f,"attn",r"Causal attention\\residual sublayer",2.4,3.5,3.6,1.1)
    n(f,"moe",r"Sparse MoE\\residual sublayer",2.4,5.6,3.6,1.1)
    n(f,"head",r"Final norm and\\language-model head",2.4,7.8,3.6,1.0)
    for a,b in [("tokens","attn"),("attn","moe"),("moe","head")]:e(f,a,b)
    f.raw(r"\draw[decorate,decoration={brace,amplitude=4pt},draw=ink] (4.6,6.2)--(4.6,2.9) node[midway,right=5pt,font=\small] {$L$};")
    f.group(r"One sparse MoE transformation",6.0,1.5,9.5,7.5)
    n(f,"x",r"Token state $x_t$",8.0,2.5,3.0,.9,"tensor")
    n(f,"router",r"Router\\$r_t=W_rx_t$",11.3,2.5,2.7,.9)
    n(f,"topk",r"Select $\mathcal S_t$\\weights $g_{t,e}$",14.1,2.5,2.5,.9)
    n(f,"ea",r"Expert $e_a$\\selected",8.4,5.2,2.5,1.0)
    n(f,"eb",r"Expert $e_b$\\selected",11.4,5.2,2.5,1.0)
    n(f,"er",r"Expert $e_r$\\inactive",14.2,5.2,2.3,1.0)
    n(f,"sum",r"Weighted sum\\$y_t=\sum_{e\in\mathcal S_t}g_{t,e}E_e(x_t)$",11.4,7.65,7.1,1.2)
    e(f,"x","router");e(f,"router","topk")
    e(f,"x","ea",side="south",to_side="north",via=[(8,4.05),(8.4,4.05)])
    e(f,"x","eb",side="south",to_side="north",via=[(8,4.05),(11.4,4.05)])
    e(f,"topk","ea",side="south",to_side="west",via=[(14.1,3.5),(6.7,3.5),(6.7,5.2)],style="control")
    e(f,"topk","eb",side="south",to_side="east",via=[(14.1,3.5),(12.95,3.5),(12.95,5.2)],style="control")
    e(f,"topk","sum",r"$g_{t,e}$",side="east",to_side="east",via=[(15.65,2.5),(15.65,7.65)],style="control",label_side="above")
    e(f,"ea","sum",side="south",to_side="north",via=[(8.4,6.65),(11.4,6.65)])
    e(f,"eb","sum")
    f.raw(r"\draw[draw=soft,dashed,line width=.45pt] (moe.east)--(5.85,5.6);\node[annotation] at (5.35,5.3) {detail};")
    note(f,r"Expert count and selected-set size are symbolic.",10.9,8.65,8.7,.4)
    return save(f,"text_11_sparse_moe","Per-token sparse expert selection, dispatch to active experts, and gate-weighted aggregation, with an explicitly inactive expert.",["https://arxiv.org/abs/1701.06538"],["The two selected experts are illustrative, not a universal routing configuration.","Capacity limits, auxiliary losses, and distributed expert placement are outside this layer-level view."],["MoE","routing","sparse"])


def lora():
    f = fig("LoRA: a frozen dense path plus a trainable low-rank update", "The adapter branch has a rank bottleneck; its scaled output adds to the frozen base-layer output.")
    n(f,"x",r"Input $x$\\$\mathbb{R}^{d_{\rm in}}$",1.7,4.0,2.8,1.0,"tensor")
    n(f,"base",r"Frozen base matrix\\$W_0\in\mathbb{R}^{d_{\rm out}\times d_{\rm in}}$",7.0,2.5,5.0,1.15)
    n(f,"a",r"Trainable $A$\\$r\times d_{\rm in}$",5.1,5.6,3.0,1.0)
    n(f,"b",r"Trainable $B$\\$d_{\rm out}\times r$",8.7,5.6,3.0,1.0)
    n(f,"scale",r"Scale\\$s=\alpha/r$",12,5.6,2.5,1.0)
    n(f,"add",r"$+$",13.6,2.5,.65,.65)
    n(f,"out",r"$y$",15,2.5,1.0,.8,"tensor")
    e(f,"x","base",side="north",to_side="west",via=[(1.7,2.5)])
    e(f,"x","a",side="south",to_side="west",via=[(1.7,5.6)])
    e(f,"base","add");e(f,"a","b");e(f,"b","scale")
    e(f,"scale","add",side="east",to_side="south",via=[(13.6,5.6)])
    e(f,"add","out")
    note(f,r"$y=W_0x+sBAx$; $\Delta W=sBA$ and $r\ll\min(d_{\rm in},d_{\rm out})$.",8,7.7,13.8,.7)
    return save(f,"text_12_lora","Low-rank trainable matrices A and B operate in parallel with a frozen base layer, then add at the output.",["https://arxiv.org/abs/2106.09685"],["Column-vector convention; A maps input width to rank r and B maps r to output width.","The common alpha/r scaling convention is shown; bias and optimizer details are omitted."],["LoRA","adapter","low-rank"])


def qlora():
    f = fig("QLoRA: quantized base storage, higher-precision computation", "Quantized base parameters stay frozen; adapters receive parameter updates while gradients can pass through the computation.")
    n(f,"qw",r"Frozen quantized storage\\$Q(W_0)$ and quantization metadata",3.4,2.2,4.5,1.1,"store")
    n(f,"dq",r"Dequantize for\\matrix computation",8,2.2,3.4,1.1)
    n(f,"base",r"Base matmul\\$\widehat W_0x$",11.6,2.2,3.0,1.1)
    n(f,"x",r"Input $x$",1.5,5.2,2.3,.9,"tensor")
    n(f,"a",r"Trainable $A$\\$r\times d_{\rm in}$",5.2,5.2,3.0,1.0)
    n(f,"b",r"Trainable $B$\\$d_{\rm out}\times r$",8.8,5.2,3.0,1.0)
    n(f,"scale",r"Scale $s$",11.7,5.2,2.1,.9)
    n(f,"add",r"$+$",14.1,3.6,.65,.65)
    n(f,"out",r"Output $y$",14.1,6.5,2.8,.9,"tensor")
    e(f,"qw","dq");e(f,"dq","base")
    e(f,"x","base",side="north",to_side="south",via=[(1.5,3.9),(11.6,3.9)])
    e(f,"x","a");e(f,"a","b");e(f,"b","scale")
    e(f,"base","add",side="east",to_side="north",via=[(14.1,2.2)])
    e(f,"scale","add",side="east",to_side="south",via=[(14.1,5.2)])
    e(f,"add","out",side="east",to_side="east",via=[(15.6,3.6),(15.6,6.5)])
    note(f,r"$\widehat W_0=\operatorname{dequant}(Q(W_0))$,\qquad $y=\widehat W_0x+sBAx$",7.5,7.8,13,.7)
    return save(f,"text_13_qlora","Conceptual QLoRA base-weight storage and dequantization path, alongside a trainable low-rank adapter branch.",["https://arxiv.org/abs/2305.14314"],["Quantizer, storage bit width, compute dtype, and optimizer are unspecified in this conceptual view.","Frozen parameters do not mean that the base matmul blocks gradients to its inputs."],["QLoRA","quantization","adapter"])


def beam_search():
    f = fig("Beam search expands prefixes, then prunes globally", "An illustrative beam of two prefixes survives each step; every expansion accumulates its parent prefix score.")
    n(f,"seed",r"Prefix $u$\\score $s(u)$",1.5,4.5,2.5,1.0)
    for name,y,label in [("a",2.2,r"$ua$ retained"),("b",4.5,r"$ub$ retained"),("c",6.8,r"$uc$ pruned")]:
        n(f,name,label,4.6,y,2.7,.9)
        e(f,"seed",name)
    for name,y,label in [("aa",1.8,r"$uaa$"),("ab",3.1,r"$uab$"),("ba",4.6,r"$uba$"),("bb",5.9,r"$ubb$")]:
        n(f,name,label,8.0,y,2.2,.8)
    e(f,"a","aa");e(f,"a","ab");e(f,"b","ba");e(f,"b","bb")
    n(f,"rank",r"Rank all expanded\\prefixes; keep top $B$",11.6,3.9,3.1,1.2)
    for name in ["aa","ab","ba","bb"]:e(f,name,"rank")
    n(f,"s1",r"Survivor $v_1$",14.4,2.6,2.4,.9)
    n(f,"s2",r"Survivor $v_2$",14.4,5.2,2.4,.9)
    e(f,"rank","s1",side="north",to_side="west",via=[(11.6,2.6)])
    e(f,"rank","s2",side="south",to_side="west",via=[(11.6,5.2)])
    note(f,r"$s(uv)=s(u)+\log p(v\mid u)$; complete hypotheses may be handled separately.",8,7.95,13.5,.6)
    return save(f,"text_14_beam_search","A prefix tree with local candidate expansion and global top-B pruning, including a visibly discarded branch.",[SEQ],["B=2 is an illustrative search setting, not an architecture claim.","The score is unnormalized cumulative log probability; length penalties and EOS bookkeeping are omitted."],["beam-search","decoding","tree"])


def speculative():
    f = fig("Speculative decoding: propose, verify, accept a prefix", "Draft proposals are sequential; the target scores their conditional positions together, then corrected sampling preserves its distribution.",9.5)
    n(f,"prefix",r"Committed prefix\\$x_{\leq t}$",1.8,2.5,2.8,1.0,"tensor")
    n(f,"draft",r"Draft model $q$\\autoregressive proposal",5.1,2.5,3.2,1.0)
    n(f,"cand",r"Proposed tokens\\$d_1,d_2,\ldots,d_\gamma$",9.0,2.5,3.7,1.0,"tensor")
    n(f,"target",r"Target model $p$\\one verification pass",13.2,2.5,3.4,1.0)
    n(f,"draftscores",r"Draft conditionals\\$q_1,\ldots,q_\gamma$",5.1,4.5,3.2,.9)
    n(f,"scores",r"Target conditionals\\$p_1,\ldots,p_{\gamma+1}$",13.2,4.5,3.4,1.0)
    n(f,"accept",r"Sequential acceptance\\$a_i=\min\{1,p_i(d_i)/q_i(d_i)\}$\\stop at first rejection",8.8,6.5,4.3,1.3)
    n(f,"correct",r"If rejected: sample from\\$\operatorname{norm}([p_i-q_i]_+)$",13.3,7.3,4.1,1.1)
    n(f,"commit",r"Commit accepted draft prefix\\plus correction, or an extra target token",3.5,6.5,4.3,1.3)
    e(f,"prefix","draft");e(f,"draft","cand");e(f,"cand","target");e(f,"target","scores")
    e(f,"draft","draftscores")
    f.raw(r"\draw[flow] (draftscores.south)--(5.1,5.35)--(7.8,5.35)--(7.8,5.85);")
    f.raw(r"\draw[flow] (scores.south)--(13.2,5.35)--(9.8,5.35)--(9.8,5.85);")
    e(f,"accept","commit",side="west",to_side="east")
    e(f,"accept","correct",side="east",to_side="west")
    e(f,"correct","commit","corrected token",side="south",to_side="south",via=[(13.3,8.5),(3.5,8.5)])
    e(f,"commit","draft","next round",side="west",to_side="north",via=[(.4,6.5),(.4,1.3),(5.1,1.3)],style="feedback",label_side="above")
    return save(f,"text_15_speculative_decoding","Speculative sampling separates draft proposal, target verification, prefix acceptance, corrected rejection sampling, and next-round feedback.",["https://arxiv.org/abs/2211.17192"],["This is the exact sampling form with normalized positive-part correction, rather than a greedy matching variant.","If all proposals are accepted, the extra token is sampled from p_(gamma+1)."],["speculative","decoding","verification"])


def selective_ssm():
    f = fig("Selective state-space recurrence", "Input-dependent selection changes the state transition across time; this view isolates the recurrence core.",9.5)
    steps=[("a",3,r"t-1"),("b",8,r"t"),("c",13,r"t+1")]
    for key,x,t in steps:
        n(f,"x"+key,r"Input $x_{"+t+r"}$",x,1.9,2.8,.8,"tensor")
        n(f,"sel"+key,r"Select from input\\$\Delta_{"+t+r"},B_{"+t+r"},C_{"+t+r"}$",x,3.4,3.5,1.0)
        n(f,"h"+key,r"Recurrent update\\state $h_{"+t+r"}$",x,5.3,3.5,1.0)
        n(f,"y"+key,r"Readout\\$y_{"+t+r"}=C_{"+t+r"}h_{"+t+r"}$",x,7.2,3.5,1.0)
        e(f,"x"+key,"sel"+key)
        e(f,"x"+key,"h"+key,"$x$",side="west",to_side="west",via=[(x-2.1,1.9),(x-2.1,5.3)])
        e(f,"sel"+key,"h"+key,"discretize",style="control")
        e(f,"h"+key,"y"+key)
        e(f,"sel"+key,"y"+key,"$C$",side="east",to_side="east",via=[(x+2.1,3.4),(x+2.1,7.2)],style="control")
    e(f,"ha","hb","$h_{t-1}$");e(f,"hb","hc","$h_t$")
    note(f,r"$\bar A_t=\exp(\Delta_t A)$,\qquad $h_t=\bar A_t h_{t-1}+\bar B_t x_t$",8,8.5,13,.6)
    return save(f,"text_16_selective_state_space","An unrolled input-selective state-space core with input-dependent discretization and readout parameters, plus a state carried across time.",["https://arxiv.org/abs/2312.00752"],["Channel mixing, convolution, gating, and output skip terms are omitted to isolate the selective recurrence.","Bars denote discretized transition/input parameters; the discretization scheme for B is not fixed in the drawing."],["SSM","Mamba","recurrence","selectivity"])


def hybrid():
    f = fig("Hybrid sequence layer: recurrence and local attention", "Recurrent state summarizes the past; the local attention cache retains explicit recent key/value positions.")
    n(f,"x",r"$x_t$",1.0,4.5,1.4,.9,"tensor")
    n(f,"rec",r"State-space / gated\\recurrent sublayer",4.3,4.5,3.5,1.1)
    n(f,"attn",r"Local causal\\attention sublayer",8.6,4.5,3.5,1.1)
    n(f,"ffn",r"Gated FFN\\sublayer",12.4,4.5,2.8,1.1)
    n(f,"y",r"$y_t$",15,4.5,1.3,.9,"tensor")
    n(f,"prev",r"Previous state\\$s_{t-1}$",4.3,2.1,3.3,1.0,"store")
    n(f,"window",r"Recent KV window\\positions $t-w,\ldots,t-1$",8.6,2.1,3.8,1.0,"store")
    n(f,"next",r"Updated state\\$s_t$",4.3,7.0,3.3,1.0,"store")
    n(f,"newkv",r"Append current KV;\\evict oldest position",8.6,7.0,3.8,1.0)
    e(f,"x","rec");e(f,"rec","attn");e(f,"attn","ffn");e(f,"ffn","y")
    e(f,"prev","rec");e(f,"rec","next");e(f,"window","attn");e(f,"attn","newkv")
    e(f,"next","prev","next step",side="west",to_side="west",via=[(2.25,7),(2.25,2.1)],style="feedback",label_side="left")
    e(f,"newkv","window","next step",side="east",to_side="east",via=[(10.7,7),(10.7,2.1)],style="feedback",label_side="right")
    note(f,r"Conceptual sublayer sequence; residual/norm wrappers and the overall layer schedule are omitted.",8,8.2,14,.4)
    return save(f,"text_17_hybrid_attention_ssm","Conceptual hybrid layer contrasts compressed recurrent state with a finite explicit KV attention window, with per-step updates of each memory.",["https://arxiv.org/abs/2402.19427","https://arxiv.org/abs/2312.00752"],["Conceptual hybrid; this is not an exact reproduction of Griffin or any specified layer schedule.","The window width w is symbolic; residual/norm wrappers are omitted."],["hybrid","SSM","local-attention","memory"])


def rnn_seq2seq():
    f = fig("Recurrent sequence-to-sequence model", "The encoder's final hidden and cell states initialize the decoder; target inputs are shifted by one position.")
    f.group("Encoder recurrence",.65,2.35,8.95,1.5)
    f.group("Decoder recurrence",6.8,5.25,8.85,1.5)
    for key,x,t in [("a",2.2,"1"),("b",5.2,"i"),("c",8.2,"S")]:
        n(f,"x"+key,r"$s_{"+t+r"}$",x,1.7,2,.6,"tensor")
        n(f,"enc"+key,r"Encoder LSTM\\$(h_{"+t+r"},c_{"+t+r"})$",x,3.1,2.65,1.0)
        e(f,"x"+key,"enc"+key)
    e(f,"enca","encb",r"$\cdots$");e(f,"encb","encc",r"$\cdots$")
    for key,x,t,prev in [("a",8.2,"1",r"\langle\mathrm{BOS}\rangle"),("b",11.2,"2","y_1"),("c",14.2,"3","y_2")]:
        n(f,"dec"+key,r"Decoder LSTM\\$(\widetilde h_{"+t+r"},\widetilde c_{"+t+r"})$",x,6.0,2.65,1.0)
        n(f,"in"+key,r"$"+prev+r"$",x,7.65,2,.7,"tensor")
        n(f,"out"+key,r"Predict $y_{"+t+r"}$",x,4.5,2.65,.7)
        e(f,"in"+key,"dec"+key,side="north",to_side="south");e(f,"dec"+key,"out"+key,side="north",to_side="south")
    e(f,"deca","decb");e(f,"decb","decc")
    e(f,"encc","deca",side="south",to_side="west",via=[(8.2,3.9),(6.4,3.9),(6.4,6.0)])
    note(f,r"Initialize $(h,c)$",5.0,4.5,2.5,.5)
    note(f,r"A fixed-length encoder summary is used here;\\attention is not part of this selected seq2seq variant.",3.3,6.5,5.6,1.0)
    note(f,r"Shifted decoder inputs are teacher-forced during training or generated during inference.",8,8.2,14,.4)
    return save(f,"text_18_rnn_seq2seq","Unrolled LSTM encoder-decoder model with final-state initialization of the decoder and explicitly shifted target inputs.",[SEQ],["Representative source positions and three illustrative target steps are drawn.","The source order is not prescribed; this schematic isolates the fixed-summary encoder-decoder topology."],["RNN","LSTM","seq2seq"])


def bilstm():
    f = fig("Bidirectional LSTM with aligned token readouts", "Forward and backward recurrences run in opposite directions; each readout combines states aligned to the same input.",10)
    steps=[("a",2,"1"),("b",6,"t"),("c",10,"t+1"),("d",14,"T")]
    for key,x,t in steps:
        n(f,"f"+key,r"Forward LSTM\\$\overrightarrow h_{"+t+r"}$",x,2.4,2.7,1.0)
        n(f,"x"+key,r"Input $x_{"+t+r"}$",x,4.5,2.5,.85,"tensor")
        n(f,"b"+key,r"Backward LSTM\\$\overleftarrow h_{"+t+r"}$",x,6.4,2.7,1.0)
        n(f,"y"+key,r"$y_{"+t+r"}=$\\$g([\overrightarrow h_{"+t+r"};\overleftarrow h_{"+t+r"}])$",x,8.7,3.35,1.1)
        e(f,"x"+key,"f"+key,side="north",to_side="south")
        e(f,"x"+key,"b"+key)
        e(f,"b"+key,"y"+key)
        e(f,"f"+key,"y"+key,side="east",to_side="north",via=[(x+1.65,2.4),(x+1.65,7.75),(x,7.75)])
    for a,b in [("a","b"),("b","c"),("c","d")]:
        e(f,"f"+a,"f"+b,r"$\cdots$" if (a,b)!=("b","c") else "")
        e(f,"b"+b,"b"+a,r"$\cdots$" if (a,b)!=("b","c") else "")
    return save(f,"text_19_bidirectional_lstm","Two oppositely directed LSTM state chains share aligned inputs and feed per-position concatenation/readout functions.",["https://www.cs.toronto.edu/~graves/nn_2005.pdf"],["Representative positions are drawn; ellipsis edges summarize intermediate steps.","Cell states and LSTM gates are contained inside the LSTM blocks; this is a noncausal sequence encoder."],["bidirectional","LSTM","sequence-labeling"])


def reranker():
    f = fig("Cross-encoder reranker jointly encodes query and document", "A single encoder allows query--document token interactions; the classification position supplies a relevance score.")
    n(f,"q",r"Query tokens\\$q_1,\ldots,q_m$",3.4,1.8,4.4,.9,"tensor")
    n(f,"d",r"Candidate document tokens\\$d_1,\ldots,d_n$",12.0,1.8,5,.9,"tensor")
    n(f,"pack",r"Pack one pair\\$[\mathrm{CLS}],q_{1:m},[\mathrm{SEP}],d_{1:n},[\mathrm{SEP}]$",8,3.2,11.8,1.0)
    n(f,"embed",r"Token $+$ position $+$ segment embeddings\\$X\in\mathbb{R}^{(m+n+3)\times d}$",8,4.7,11.8,1.0)
    n(f,"enc",r"Shared bidirectional Transformer encoder\\full self-attention across the packed query--document sequence",8,6.2,11.8,1.0)
    n(f,"cls",r"Select classification state\\$h_{\rm CLS}$",3.8,7.85,4.7,.9,"tensor")
    n(f,"head",r"Relevance head\\$w^\top h_{\rm CLS}+b$",9,7.85,4.0,.9)
    n(f,"score",r"Pair relevance\\score",13.8,7.85,3.1,.9,"tensor")
    e(f,"q","pack");e(f,"d","pack");e(f,"pack","embed");e(f,"embed","enc")
    e(f,"enc","cls",side="south",to_side="north",via=[(8,7.05),(3.8,7.05)])
    e(f,"cls","head");e(f,"head","score")
    return save(f,"text_20_cross_encoder_reranker","BERT-style pair packing, joint bidirectional encoding, classification-state extraction, and a document-query relevance head.",["https://arxiv.org/abs/1901.04085","https://arxiv.org/abs/1810.04805"],["Special-token count m+n+3 follows the explicitly shown two-segment BERT packing convention.","The relevance-head activation and loss are task choices; the displayed score is a pre-activation scalar."],["reranking","cross-encoder","BERT"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    builders=[token_embedding,causal_decoder,encoder_decoder,self_attention,cross_attention,multi_head,grouped_query,kv_cache,rope,swiglu,moe,lora,qlora,beam_search,speculative,selective_ssm,hybrid,rnn_seq2seq,bilstm,reranker]
    records=[build() for build in builders]
    assert len(records)==20 and len(list(OUT.glob("*.tex")))==20
    (OUT/"index.json").write_text(json.dumps(records,indent=2)+"\n")
    print(f"Wrote {len(records)} original text figures to {OUT}")


if __name__=="__main__":
    main()
