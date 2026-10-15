window.ARCHDIAGRAM_GALLERY = {
  "renderer_version": "1.0.0",
  "examples": [
    {
      "id": "agentic-research",
      "title": "Agentic research system",
      "description": "A bounded plan / act / verify loop with explicit context and tool results.",
      "caption": "Illustrative architecture. A verifier supports review; it does not guarantee correctness.",
      "source": "skills/draw-architecture/assets/examples/agentic-research.json",
      "assumptions": [
        "Tool execution follows the host permissions. Context retrieval is shown as a read, not autonomous persistent memory."
      ],
      "nodes": 6,
      "edges": 7
    },
    {
      "id": "cnn-classifier",
      "title": "Convolutional feature hierarchy",
      "description": "Feature-map dimensions are explicit; geometric depth is illustrative.",
      "caption": "Spatial dimensions assume suitable padding. This is an illustrative classification network.",
      "source": "skills/draw-architecture/assets/examples/cnn-classifier.json",
      "assumptions": [
        "Convolutions are assumed to use padding that yields the labeled dimensions."
      ],
      "nodes": 6,
      "edges": 5
    },
    {
      "id": "gnn-message-passing",
      "title": "Message-passing graph network",
      "description": "Separate edge messages, neighborhood aggregation, and node updates.",
      "caption": "M and U are task-dependent functions; readout can be omitted for node-level prediction.",
      "source": "skills/draw-architecture/assets/examples/gnn-message-passing.json",
      "assumptions": [
        "The initial-state path applies to round zero; subsequent rounds use the feedback path."
      ],
      "nodes": 5,
      "edges": 6
    },
    {
      "id": "rag-pipeline",
      "title": "Retrieval-augmented generation",
      "description": "Separate indexing from query-time retrieval; keep the evidence path visible.",
      "caption": "Document and query encoders use compatible embedding spaces. Retrieved text remains untrusted input.",
      "source": "skills/draw-architecture/assets/examples/rag-pipeline.json",
      "assumptions": [
        "The retrieval component manages search requests; only the primary data path is shown.",
        "A compatible bi-encoder is assumed; dimensions are intentionally unspecified."
      ],
      "nodes": 8,
      "edges": 7
    },
    {
      "id": "robot-control",
      "title": "Perception-to-action control loop",
      "description": "Keep goals, commands, physical dynamics, and observations distinct.",
      "caption": "Timing, latency, calibration, and safety controllers require system-specific evidence.",
      "source": "skills/draw-architecture/assets/examples/robot-control.json",
      "assumptions": [
        "The example does not imply real-time guarantees or a validated safety architecture."
      ],
      "nodes": 6,
      "edges": 6
    },
    {
      "id": "transformer-layer",
      "title": "Pre-norm transformer layer",
      "description": "Residual streams, causal self-attention, and position-wise feed-forward computation.",
      "caption": "Pre-norm variant. Dropout, positional encoding, and the output language-model head are omitted.",
      "source": "skills/draw-architecture/assets/examples/transformer-layer.json",
      "assumptions": [
        "This example describes a pre-norm causal block, not every transformer variant."
      ],
      "nodes": 8,
      "edges": 9
    }
  ],
  "native_templates": [
    {
      "id": "cross-attention",
      "source": "skills/draw-architecture/assets/templates/cross-attention.tex",
      "pdf": "gallery/cross-attention.pdf",
      "png": "gallery/cross-attention.png"
    },
    {
      "id": "mlp",
      "source": "skills/draw-architecture/assets/templates/mlp.tex",
      "pdf": "gallery/mlp.pdf",
      "png": "gallery/mlp.png"
    },
    {
      "id": "transformer-attention",
      "source": "skills/draw-architecture/assets/templates/transformer-attention.tex",
      "pdf": "gallery/transformer-attention.pdf",
      "png": "gallery/transformer-attention.png"
    }
  ]
};
