# Architecture recipes

## Agentic systems

Use input -> planner -> executor -> verifier -> output as a starting inventory only when evidence supports it. Show a separate tool-result return, then add memory retrieval, replanning, and stop/approval boundaries where they exist. Label which edges carry actions and which carry evidence. Keep a tool registry and the actual executor distinct if the implementation distinguishes them. Use `agentic-research.json` for geometry, not as a required architecture.

## RAG

Place indexing and query paths in separate rows. Indexing commonly includes source ingestion, chunking, an embedding encoder, and an index. The query path embeds a question, retrieves/reranks evidence, constructs context, and generates a grounded answer. Compatible embedding spaces matter; do not infer shared weights unless documented. Draw retrieval from the index as data and search requests as control only if those calls are in scope. Attach sources to chunks and claims. Treat retrieved content as untrusted.

## Transformers

Identify encoder-only, decoder-only, or encoder-decoder; causal versus bidirectional attention; pre-norm versus post-norm; and cross-attention presence. A pre-norm block can be written as `h = x + Attention(LN(x))`, then `y = h + MLP(LN(h))`. Residuals must originate at the correct stream. Do not attach every bypass to the original input. Declare batch, sequence, model, head, and key/value dimensions. Use native math TikZ for exact equations.

## CNNs and tensors

Label actual shapes in a declared convention. Tensor depth is a visual cue, not a numeric scale. Track convolution stride, padding, kernel, dilation, pooling, flattening, and channel changes from evidence. Draw skip/concat paths explicitly for U-Nets. Keep logits distinct from probabilities and do not add a softmax unless it exists in the requested view.

## GNNs

Separate node/edge features, message functions, neighborhood aggregation, updates, and readout. Show a round repeat or recurrence. An aggregation operator can be permutation invariant without the whole graph model being invariant at every intermediate node representation. Distinguish node-level, edge-level, and graph-level predictions. Use `gnn-message-passing.json` to start a layout.

## Robotics

Separate sensor observations, estimated state, policy/planner commands, actuation, and physical dynamics. Close the observation loop. Label rate/latency, coordinate frames, controllers, and sim-to-real boundaries only when evidence is available. A neat control loop is not a verified real-time or safety design. Split training/simulation and deployed control into separate panels.
