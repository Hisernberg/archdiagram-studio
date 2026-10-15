#!/usr/bin/env python3
"""Ten original monochrome robotics and graph-learning atlas diagrams.

Primary references are recorded in each figure's metadata and as TeX comments.
The layouts are conceptual schematics, not reproductions of source figures.
"""
from __future__ import annotations

import json
from pathlib import Path

from atlaslib import Figure

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "atlas" / "robotics-graphs"
FAMILY = "robotics-graphs"
INDEX = []

ROS_CONTROL = "https://control.ros.org/jazzy/doc/getting_started/getting_started.html"
OPTIONS = "https://doi.org/10.1016/S0004-3702(99)00052-1"
MPC = "https://sites.engineering.ucsb.edu/~jbraw/mpc/"
SIM_REAL = "https://arxiv.org/abs/1710.06537"
FUSION = "https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/doc/state_estimation_nodes.rst"
MPNN = "https://arxiv.org/abs/1704.01212"
GAT = "https://arxiv.org/abs/1710.10903"
RGCN = "https://arxiv.org/abs/1703.06103"
DCRNN = "https://arxiv.org/abs/1707.01926"


def save(fig, ident, description, sources, assumptions, tags):
    metadata = fig.write(OUT, ident, FAMILY, description, sources, assumptions, tags)
    metadata['caption'] = metadata['caption'].replace(r'\_', '_').replace(r'\v{c}', 'č').replace(r"\'c", 'ć')
    path = OUT / metadata["source_file"]
    source_comments = "\n".join("% Primary source: " + url for url in sources)
    path.write_text(source_comments + "\n" + path.read_text())
    INDEX.append(metadata)


def note(fig, text, x, y, width=5.0):
    fig.raw(rf"\node[annotation,text width={width}cm] at ({x},{y}) {{{text}}};")


def perception_action():
    f = Figure("Perception--action closed loop", subtitle="Conceptual robot feedback architecture", caption="Conceptual sensing, estimation, control, and physical feedback; ROS control documentation informs the control interface.")
    f.group("software", 1.1, 1.55, 13.2, 2.2)
    f.node("sense", r"Sensing\\$o_t$", 3.0, 2.65, 2.7, 1.05)
    f.node("estimate", r"State estimation\\$\hat{x}_t$", 7.5, 2.65, 2.9, 1.05)
    f.node("policy", r"Policy / controller\\$u_t=\pi(\hat{x}_t,g)$", 12.0, 2.65, 3.2, 1.05)
    f.node("world", r"Robot + environment\\$x_{t+1}=f(x_t,u_t,w_t)$", 3.0, 6.2, 4.1, 1.2)
    f.node("actuate", r"Actuation interface\\command execution", 12.0, 6.2, 3.2, 1.2)
    f.node("goal", r"Task reference $g$", 7.5, 5.05, 2.9, .85)
    f.edge("sense", "estimate", r"observations")
    f.edge("estimate", "policy", r"state")
    f.edge("policy", "actuate", r"command", side="south", to_side="north")
    f.edge("actuate", "world", r"physical input", side="west", to_side="east", label_side="below")
    f.edge("world", "sense", r"new measurements", side="north", to_side="south", style="feedback", label_side="left")
    f.raw(r"\draw[flow,dashed] (goal.east) -- (10.0,5.05) -- (10.0,3.85) -- (11.2,3.85) -- ($(policy.south)+(-.8,0)$);")
    note(f, r"Disturbance $w_t$ acts on the physical system.\\Latency and stability depend on the implementation.", 7.5, 7.55, 9.3)
    save(f, "rg01-perception-action-loop", "A closed physical feedback cycle with an external task reference and an explicit actuation boundary.", [ROS_CONTROL], ["Perception and estimation are conceptual additions around the documented controller/hardware interface.", "Discrete-time notation is illustrative; no timing, stability, or safety guarantee is implied."], ["robotics", "feedback", "perception", "control"])


def hierarchical_policy():
    f = Figure("Hierarchical robot policy", subtitle="Conceptual options hierarchy with temporally extended skills", caption="Conceptual options hierarchy after Sutton, Precup, and Singh (1999); only the selected option emits primitive actions.")
    f.node("state", r"Current state\\$s_t$", 2.0, 2.1, 2.5, .95)
    f.node("selector", r"High-level selector\\$o\sim\mu(o\mid s_t)$", 8.0, 2.1, 3.8, 1.05)
    f.group(r"option library: $o=(I_o,\pi_o,\beta_o)$", 1.35, 3.5, 13.3, 1.95)
    for ident, label, x in [("nav", "Navigate", 3.5), ("reach", "Reach", 8.0), ("grasp", "Grasp", 12.5)]:
        f.node(ident, label + r"\\$\pi_o(a\mid s)$", x, 4.5, 3.25, 1.05)
        f.edge("selector", ident, side="south", to_side="north", via=[(8.0, 3.05), (x, 3.05)], style="control")
    f.node("primitive", r"Primitive action from the active option\\$a_t\sim\pi_o(a\mid s_t)$", 8.0, 6.7, 7.0, 1.1)
    f.edge("state", "selector", r"on selection")
    for ident, x in [("nav", 3.5), ("reach", 8.0), ("grasp", 12.5)]:
        f.edge(ident, "primitive", side="south", to_side="north", via=[(x, 5.9), (8.0, 5.9)])
    f.edge("primitive", "selector", side="east", to_side="east", via=[(15.25, 6.7), (15.25, 2.1)], style="feedback")
    note(f, r"terminate with $\beta_o(s)$", 13.0, 1.65, 4.1)
    note(f, r"Initiation $I_o$: where a skill is available.\quad Termination $\beta_o$: when selection resumes.", 8.0, 8.0, 13.2)
    save(f, "rg02-hierarchical-policy", "A three-skill options hierarchy showing discrete option selection, primitive action emission, and termination feedback.", [OPTIONS], ["Navigate, Reach, and Grasp are illustrative robot skill names, not a reported system from the source.", "State input to each option is implicit; arrows from options denote mutually exclusive active-option routing."], ["robotics", "hierarchical-policy", "options", "temporal-abstraction"])


def mpc():
    f = Figure("Model-predictive control", height=9.3, subtitle="Conceptual receding-horizon optimization and first-action execution", caption="Conceptual MPC after Rawlings, Mayne, and Diehl: optimize a horizon, execute its first input, and replan from the next estimate.")
    f.node("estimate", r"State estimate\\$\hat{x}_t$", 2.3, 2.4, 2.9, .95)
    f.node("opt", r"Constrained optimizer\\$u^*_{t:t+H-1}$", 8.0, 2.4, 3.7, 1.15)
    f.node("plant", r"Physical system\\apply $u_t^*$", 13.6, 2.4, 3.0, 1.15)
    f.node("model", r"Prediction model + objective\\$x_{k+1}=f(x_k,u_k)$\\$x_k\in\mathcal{X},\ u_k\in\mathcal{U}$", 8.0, 4.65, 4.65, 1.65)
    f.edge("estimate", "opt", r"initial condition")
    f.edge("opt", "plant", r"first input only")
    f.edge("model", "opt", side="north", to_side="south")
    f.edge("plant", "estimate", side="south", to_side="south", via=[(13.6, 6.0), (2.3, 6.0)], style="feedback")
    note(f, r"measure, estimate, and repeat at the next sample", 8.0, 6.23, 10.6)
    f.raw(r"\node[anchor=east,font=\scriptsize] at (3.8,7.25) {planned controls};")
    for i, x in enumerate([5.0, 7.3, 9.6, 11.9]):
        fill = "wash" if i == 0 else "white"
        dash = "" if i == 0 else ",dashed"
        label = r"$u_t^*$" if i == 0 else (rf"$u_{{t+{i}}}^*$" if i < 3 else r"$\cdots\ u_{t+H-1}^*$")
        f.raw(rf"\node[box,fill={fill}{dash},minimum width=2.15cm,minimum height=.7cm] at ({x},7.25) {{{label}}};")
    f.raw(r"\draw[flow] (3.95,8.05) -- (13.1,8.05) node[right,font=\scriptsize] {horizon};")
    f.raw(r"\node[annotation] at (5.0,8.35) {executed};\node[annotation] at (9.6,8.35) {future plan is recomputed};")
    save(f, "rg03-model-predictive-control", "An MPC feedback loop paired with a time-indexed planned-input strip that distinguishes first-action execution from future controls.", [MPC], ["The state estimator, objective, constraints, dynamics, and horizon are problem-specific and shown abstractly.", "Feasibility, closed-loop stability, runtime, and safety are not established by this schematic."], ["robotics", "mpc", "optimization", "receding-horizon"])


def sim_to_real():
    f = Figure("Simulation training and robot deployment", subtitle="Conceptual dynamics-randomization transfer with a frozen deployment checkpoint", caption="Conceptual sim-to-real separation after Peng et al. (2018); randomized training does not guarantee successful physical transfer.")
    f.group("training: simulation only", .4, 1.5, 9.3, 6.7)
    f.group(r"rollout workers, shared policy $\theta$", .7, 3.45, 4.9, 3.05)
    f.group("deployment: physical robot", 10.35, 1.5, 5.25, 6.7)
    f.node("random", r"Sample dynamics\\$\xi\sim p(\xi)$", 3.1, 2.5, 4.1, .95)
    for ident, x, y, label in [("sim1",1.9,4.15,"1"),("sim2",4.4,4.15,"2"),("sim3",1.9,5.7,"3"),("simn",4.4,5.7,"n")]:
        f.node(ident, rf"Simulator {label}\\$\xi_{{{label}}}$", x, y, 2.1, .95)
    f.node("learn", r"Policy learner\\update $\theta$", 7.6, 4.9, 2.7, 1.15)
    f.node("checkpoint", r"Trained checkpoint\\$\theta^*$", 7.6, 2.5, 2.75, .95)
    f.node("deploy", r"Frozen policy\\$\pi_{\theta^*}$", 13.0, 3.3, 2.7, 1.05)
    f.node("robot", r"Robot + task\\physical dynamics", 13.0, 6.3, 2.7, 1.15)
    for ident, x in [("sim1",1.9),("sim2",4.4)]:
        f.edge("random", ident, side="south", to_side="north", via=[(3.1,3.25),(x,3.25)])
    f.edge("random", "sim3", side="west", to_side="west", via=[(.7,2.5),(.7,5.7)], style="control")
    f.edge("random", "simn", side="east", to_side="east", via=[(6.05,2.5),(6.05,5.7)], style="control")
    f.edge("sim2", "learn", side="east", to_side="west", via=[(5.8,4.15),(5.8,4.9)])
    f.edge("simn", "learn", side="east", to_side="west", via=[(5.8,5.7),(5.8,4.9)])
    f.edge("sim1", "learn", side="south", to_side="west", via=[(1.9,4.9),(5.8,4.9)])
    f.edge("sim3", "learn", side="north", to_side="west", via=[(1.9,4.9),(5.8,4.9)])
    f.edge("learn", "checkpoint", side="north", to_side="south")
    f.raw(r"\draw[flow,dotted] (learn.south) -- (7.6,7.3) -- (3.1,7.3) -- (3.1,6.5);")
    f.edge("checkpoint", "deploy", side="east", to_side="north", via=[(10.0,2.5),(13.0,2.5)], label=r"copy weights")
    f.edge("deploy", "robot", side="south", to_side="north", label=r"actions", label_side="right")
    f.edge("robot", "deploy", side="west", to_side="west", via=[(10.9,6.3),(10.9,3.3)], style="feedback")
    note(f, r"broadcast policy updates", 4.2, 7.55, 5.8)
    note(f, r"observations", 11.2, 4.9, 2.2)
    note(f, r"rollouts", 7.5, 6.0, 2.7)
    save(f, "rg04-sim-to-real", "A grid of randomized simulators feeds a learner; only a checkpoint crosses into the isolated physical deployment loop.", [SIM_REAL], ["Parallel simulator grid and a frozen checkpoint are conceptual implementation choices.", "The figure omits the source method's recurrent policy, omniscient critic, and task-specific training details.", "No physical transfer, reliability, timing, or safety guarantee is implied."], ["robotics", "sim-to-real", "domain-randomization", "training-deployment"])


def sensor_fusion():
    f = Figure("Robot sensor fusion", subtitle="Conceptual loosely coupled state estimation with heterogeneous measurements", caption=r"Conceptual predict--correct fusion informed by robot\_localization documentation; frame and covariance treatment are essential.")
    sensors = [("imu", r"IMU\\angular rate / acceleration", 2.3), ("wheel", r"Wheel odometry\\velocity estimate", 4.45), ("vision", r"Visual odometry\\pose estimate", 6.6)]
    for ident, label, y in sensors:
        f.node(ident, label, 2.0, y, 3.0, 1.1)
        f.node(ident+"prep", r"Time / frame handling\\selected fields + covariance", 5.8, y, 3.25, 1.1)
        f.edge(ident, ident+"prep")
    f.group("recursive estimator", 8.1, 1.55, 4.1, 5.85)
    f.node("predict", r"Predict\\$\hat{x}_{t|t-1},P_{t|t-1}$", 10.15, 2.6, 3.2, 1.2)
    f.node("correct", r"Correct with available\\measurements\\$\hat{x}_{t|t},P_{t|t}$", 10.15, 5.4, 3.2, 1.45)
    f.node("output", r"Fused state\\+ uncertainty", 14.0, 5.4, 2.75, 1.1)
    f.edge("predict", "correct", side="south", to_side="north", label=r"prior")
    for ident, _, y in sensors:
        f.edge(ident+"prep", "correct", side="east", to_side="west", via=[(7.7,y),(7.7,5.4)])
    f.edge("correct", "output")
    f.edge("correct", "predict", side="east", to_side="east", via=[(12.6,5.4),(12.6,2.6)], style="feedback")
    note(f, r"next sample", 13.3, 3.7, 2.0)
    note(f, r"$P$: state covariance. Measurements can arrive at different times; fusion choices depend on observability and noise modeling.", 8.0, 7.95, 14.3)
    save(f, "rg05-sensor-fusion", "Three measurement streams converge into a recursive prediction/correction estimator and expose both state and uncertainty.", [FUSION, "https://index.ros.org/p/robot_localization/"], ["The three selected sensor sources and the layout are illustrative, not a package launch configuration.", "Time/frame handling is conceptual; the diagram does not require simultaneous arrival or claim an explicit synchronization node.", "The estimator may use an EKF or UKF; equations intentionally omit filter-specific details."], ["robotics", "sensor-fusion", "state-estimation", "uncertainty"])


def message_passing():
    f = Figure("Graph message passing", subtitle="Conceptual one-hop aggregation followed by a node-state update", caption="Conceptual MPNN update after Gilmer et al. (2017); the same local rule is applied across graph nodes.")
    f.group(r"local graph neighborhood $\mathcal{N}(v)$", .45, 1.55, 6.9, 6.6)
    f.node("v", r"$h_v^{(\ell)}$", 4.0, 4.65, 1.15, 1.15, "circle")
    for ident, label, x, y in [("u1", "1",1.6,2.6),("u2","2",1.6,6.6),("u3","3",6.0,2.6),("u4","4",6.0,6.6)]:
        f.node(ident, rf"$h_{{u_{label}}}^{{(\ell)}}$", x, y, 1.1, 1.1, "circle")
        f.edge(ident, "v", rf"$m_{{u_{label}\to v}}$", side="south" if y<4 else "north", to_side="north" if y<4 else "south")
    f.edge("u1", "u2", side="south", to_side="north", style="undirected")
    f.edge("u3", "u4", side="south", to_side="north", style="undirected")
    f.node("message", r"Message on each edge\\$m_{u\to v}=M_\ell(h_v^{(\ell)},h_u^{(\ell)},e_{uv})$", 11.3, 2.55, 7.0, 1.3)
    f.node("aggregate", r"Permutation-invariant aggregation\\$m_v=\sum_{u\in\mathcal{N}(v)}m_{u\to v}$", 11.3, 4.75, 5.4, 1.3)
    f.node("update", r"Node update\\$h_v^{(\ell+1)}=U_\ell(h_v^{(\ell)},m_v)$", 11.3, 6.95, 5.4, 1.3)
    f.edge("message", "aggregate", side="south", to_side="north")
    f.edge("aggregate", "update", side="south", to_side="north")
    note(f, r"$e_{uv}$ is an optional edge feature.\\Graph size and hidden width are unspecified.", 11.3, 8.05, 7.0)
    save(f, "rg06-graph-message-passing", "A true local graph neighborhood accompanies explicit edge-message, symmetric aggregation, and node-update equations.", [MPNN], ["The small graph and sum aggregator are illustrative instances of the MPNN framework.", "Undirected context edges are shown without arrows; directed arrows indicate messages into the selected node only."], ["graph-learning", "message-passing", "aggregation", "gnn"])


def graph_attention():
    f = Figure("Graph attention", subtitle="Conceptual masked neighborhood attention with multiple heads", caption=r"Conceptual GAT layer after Veli\v{c}kovi\'c et al. (2018); each head normalizes attention over the permitted neighborhood.")
    f.group("allowed neighborhood", .45, 1.55, 5.95, 6.55)
    f.node("u1", r"$h_j$", 1.65, 2.65, 1.0, 1.0, "circle")
    f.node("u2", r"$h_k$", 1.65, 5.65, 1.0, 1.0, "circle")
    f.node("target", r"$h_i$", 4.65, 4.15, 1.0, 1.0, "circle")
    f.edge("u1", "target", r"$\alpha_{ij}$")
    f.edge("u2", "target", r"$\alpha_{ik}$")
    f.raw(r"\draw[flow] (target.north) .. controls (4.65,2.7) and (6.15,3.15) .. (target.east);")
    f.raw(r"\node[font=\scriptsize,fill=wash,inner sep=1pt] at (5.55,3.0) {$\alpha_{ii}$};")
    f.node("excluded", r"$h_q$", 4.65, 6.9, 1.0, 1.0, "circle")
    note(f, r"$q\notin\mathcal{N}(i)$: masked", 2.7, 7.65, 4.9)
    f.node("scores", r"Shared score function\\$e_{ij}=a(Wh_i,Wh_j)$", 8.8, 2.55, 3.7, 1.2)
    f.node("softmax", r"Neighborhood softmax\\$\alpha_{ij}=\frac{\exp e_{ij}}{\sum_{k\in\mathcal{N}(i)}\exp e_{ik}}$", 13.2, 2.55, 4.0, 1.3)
    f.edge("scores", "softmax")
    for ident, label, x in [("head1","1",8.0),("head2","2",11.0),("headk","K",14.0)]:
        f.node(ident, rf"Head {label}\\$\sum_j\alpha^{{({label})}}_{{ij}}W^{{({label})}}h_j$", x, 4.95, 2.6, 1.2)
        f.edge("softmax", ident, side="south", to_side="north", via=[(13.2,3.65),(x,3.65)])
    f.node("combine", r"Combine heads\\concatenate, then nonlinearity", 11.0, 7.1, 5.3, 1.1)
    for ident, x in [("head1",8.0),("head2",11.0),("headk",14.0)]:
        f.edge(ident, "combine", side="south", to_side="north", via=[(x,6.1),(11.0,6.1)])
    save(f, "rg07-graph-attention", "A masked graph neighborhood, self-attention loop, local softmax, and parallel attention-head fanout/merge.", [GAT], ["The depicted layer uses concatenated heads; the source also describes head averaging in a final layer.", "Self-loops are included in the conceptual permitted neighborhood.", "Head count and graph size are symbolic rather than a reported benchmark configuration."], ["graph-learning", "attention", "gat", "multihead"])


def graph_readout():
    f = Figure("Graph-level readout", subtitle="Conceptual permutation-invariant aggregation of node representations", caption="Conceptual graph readout after Gilmer et al. (2017); a symmetric set aggregation produces one graph representation.")
    f.group("encoded graph", .45, 1.55, 5.8, 6.55)
    positions=[("v1",1.6,2.7),("v2",4.85,2.7),("v3",3.25,4.65),("v4",1.6,6.6),("v5",4.85,6.6)]
    for i,(ident,x,y) in enumerate(positions,1):
        f.node(ident,rf"$h_{i}$",x,y,1.0,1.0,"circle")
    for a,b in [("v1","v2"),("v1","v3"),("v2","v3"),("v3","v4"),("v3","v5"),("v4","v5")]:
        f.edge(a,b,style="undirected")
    f.group("unordered node states", 7.0, 1.8, 2.2, 5.85)
    for i,y in enumerate([2.6,3.6,4.6,5.6,6.6],1):
        f.node("h"+str(i),rf"$\phi(h_{i})$",8.1,y,1.6,.65,"tensor")
    f.node("pool",r"Symmetric pool\\$g=\sum_{v\in V}\phi(h_v)$",11.4,4.6,3.1,1.6)
    f.node("predict",r"Graph head\\$\hat{y}=\rho(g)$",14.5,4.6,2.25,1.1)
    for i in range(1,6):
        f.edge("h"+str(i),"pool",side="east",to_side="west",via=[(9.5, [2.6,3.6,4.6,5.6,6.6][i-1]),(9.5,4.6)])
    f.edge("pool","predict")
    f.raw(r"\draw[flow] (6.35,4.6) -- (6.85,4.6);")
    note(f,r"Any node ordering gives the same sum.\\The learned maps $\phi$ and $\rho$ depend on the task.",11.3,8.05,8.4)
    save(f,"rg08-graph-readout","An encoded graph is treated as an unordered set of node states and pooled into a graph embedding and graph-level output.",[MPNN],["The sum-of-transformed-states readout is an illustrative invariant instance, not the complete readout used in every MPNN.","Only node states are visualized; tasks may also use edge or global attributes."],["graph-learning","readout","graph-level","permutation-invariance"])


def heterogeneous_graph():
    f=Figure("Heterogeneous graph network",subtitle="Conceptual typed relations with relation-specific message transforms",caption="Conceptual relational GNN after Schlichtkrull et al. (2018); each relation has its own transform before node aggregation.")
    f.group("example schema",.45,1.55,7.1,6.0)
    f.node("a1",r"Author\\$a_1$",1.6,2.65,1.45,1.0,"circle")
    f.node("a2",r"Author\\$a_2$",1.6,6.25,1.45,1.0,"circle")
    f.node("p1",r"Paper\\$p_1$",4.2,2.65,1.65,1.0)
    f.node("p2",r"Paper\\$p_2$",4.2,6.25,1.65,1.0)
    f.node("venue",r"Venue\\$v$",6.55,4.45,1.55,1.0)
    f.edge("a1","p1",r"writes")
    f.edge("a2","p2",r"writes")
    f.edge("p1","p2",r"cites",side="south",to_side="north",label_side="left")
    f.edge("p1","venue",r"in",side="east",to_side="north")
    f.edge("p2","venue",r"in",side="east",to_side="south")
    f.node("writes",r"Incoming authors\\$m_{\rm writes}=\sum_j c_{i,r}^{-1}W_{\rm writes}h_j$",10.0,2.6,4.1,1.25)
    f.node("cites",r"Incoming citing papers\\$m_{\rm cites}=\sum_j c_{i,r}^{-1}W_{\rm cites}h_j$",10.0,4.5,4.1,1.25)
    f.node("inv",r"Venue via inverse relation\\$m_{{\rm in}^{-1}}=\sum_j c_{i,r}^{-1}W_{{\rm in}^{-1}}h_j$",10.0,6.4,4.1,1.25)
    f.node("update",r"Paper update\\$h'_i=\sigma\!\left(W_0h_i+\sum_r m_r\right)$",14.0,4.5,3.1,1.9)
    for ident,y in [("writes",2.6),("cites",4.5),("inv",6.4)]:
        f.edge(ident,"update",side="east",to_side="west",via=[(12.25,y),(12.25,4.5)])
    note(f,r"Node types: author, paper, venue.\quad Relation inverses are added explicitly for reverse-direction messages.",8.0,8.0,14.2)
    save(f,"rg09-heterogeneous-graph","A typed author/paper/venue graph is paired with three relation-specific message channels and a self-term node update.",[RGCN],["The author/paper/venue schema is an original illustrative graph, not a source benchmark.","Inverse published-in relations are explicitly assumed to permit venue-to-paper messages.","Relation normalization c_(i,r) is symbolic and each sum is restricted to the named incoming relation; basis decomposition and training objectives are omitted."],["graph-learning","heterogeneous-graph","relations","rgcn"])


def spatiotemporal():
    f=Figure("Spatiotemporal graph forecasting",subtitle="Conceptual spatial neighborhoods repeated along an observed time window",caption="Conceptual graph-recurrent forecasting after Li et al. (2018); topology and temporal state inform node forecasts.")
    f.group("observed sequence: spatial graph at each time",.45,1.55,8.9,6.0)
    columns=[(1,1.7,r"$t-2$"),(2,4.1,r"$t-1$"),(3,6.5,r"$t$")]
    rows=[(1,2.85),(2,4.6),(3,6.35)]
    for c,x,t in columns:
        f.raw(rf"\node[font=\scriptsize] at ({x},1.95) {{{t}}};")
        for r,y in rows:
            ident=f"h{r}{c}"
            f.node(ident,rf"$h_{{{r},{['t-2','t-1','t'][c-1]}}}$",x,y,1.15,1.15,"circle")
        f.edge(f"h1{c}",f"h2{c}",side="south",to_side="north",style="undirected")
        f.edge(f"h2{c}",f"h3{c}",side="south",to_side="north",style="undirected")
    for r,y in rows:
        f.edge(f"h{r}1",f"h{r}2",side="east",to_side="west")
        f.edge(f"h{r}2",f"h{r}3",side="east",to_side="west")
    f.node("state",r"$H_t$",8.55,4.6,.7,4.8,"tensor")
    for r,y in rows:
        f.edge(f"h{r}3","state",side="east",to_side="west",via=[(7.7,y),(7.7,4.6)])
    f.node("decoder",r"Recurrent\\forecast\\decoder",10.35,4.6,2.1,1.7)
    f.edge("state","decoder")
    f.group("future node values",11.8,1.9,3.8,5.7)
    for j,x in enumerate([12.8,14.5],1):
        f.raw(rf"\node[font=\scriptsize] at ({x},2.35) {{$t+{j}$}};")
        for i,y in rows:
            f.node(f"pred{i}{j}",rf"$\hat{{x}}_{{{i},t+{j}}}$",x,y+.55,1.45,.8,"tensor")
    f.raw(r"\draw[flow] (decoder.east) -- (11.65,4.6);")
    note(f,r"Vertical: spatial edges.\quad Horizontal: temporal state propagation.\\Per-time observations enter the encoder; individual input arrows are omitted.",7.9,8.15,14.3)
    save(f,"rg10-spatiotemporal-graph","A graph-by-time lattice feeds an encoder state, a recurrent decoder, and a node-by-horizon forecast grid.",[DCRNN],["The three-node chain, three observed times, and two forecast steps are illustrative and not DCRNN's reported dimensions.","Cells denote hidden states; per-time observation injection, diffusion filters, gates, and scheduled sampling are omitted.","Undirected vertical lines abstract spatial neighborhoods; the source DCRNN uses directed-graph diffusion.","This is a conceptual family diagram rather than an exact DCRNN computational graph."],["graph-learning","spatiotemporal","forecasting","graph-recurrent"])


def main():
    for build in [perception_action,hierarchical_policy,mpc,sim_to_real,sensor_fusion,message_passing,graph_attention,graph_readout,heterogeneous_graph,spatiotemporal]:
        build()
    assert len(INDEX)==10
    (OUT/"index.json").write_text(json.dumps(INDEX,indent=2)+"\n")
    print(f"Wrote {len(INDEX)} figures to {OUT}")


if __name__=="__main__":
    main()
