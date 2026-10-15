#!/usr/bin/env python3
"""Generate 15 original, source-backed agent/software architecture figures."""
from pathlib import Path
import json

from atlaslib import Figure

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "atlas" / "agents"
INDEX = []


def note(f, text, x, y, w=4, anchor="center"):
    f.raw(r"\node[annotation,anchor=" + anchor + ",text width=" + str(w) + r"cm] at (" + str(x) + "," + str(y) + ") {" + text + "};")


def path(f, points, style="data", label="", at=None, label_side="above"):
    """Exact paths/ports for protocols and paired read/write messages."""
    opts = {"data": "", "control": ",dashed", "feedback": ",dotted", "both": ",<->", "undirected": ",-"}[style]
    route = " -- ".join(p if isinstance(p, str) else f"({p[0]},{p[1]})" for p in points)
    f.raw(r"\draw[flow" + opts + "] " + route + ";")
    f._custom_edges = getattr(f, "_custom_edges", 0) + 1
    if label:
        if at is None:
            raise ValueError("Exact-path labels require a position")
        f.raw(r"\node[font=\scriptsize,fill=white,inner sep=1.5pt,anchor=" + {"above": "south", "below": "north", "left": "east", "right": "west"}[label_side] + "] at (" + str(at[0]) + "," + str(at[1]) + ") {" + label + "};")


def emit(f, id, description, sources, assumptions, tags):
    if len(f.caption) > 140:
        raise ValueError("Caption exceeds 140 characters: " + id)
    m = f.write(OUT, id, "agents", description, sources=sources,
                assumptions=["Conceptual original schematic; implementation details and dimensions vary.", *assumptions], tags=tags)
    m["edges"] += getattr(f, "_custom_edges", 0)
    INDEX.append(m)


def react():
    f = Figure("ReAct: interleaved reasoning, action, and observation", subtitle="Conceptual inference loop | solid: data; dashed: invocation; dotted: feedback",
               caption="Each observation updates the trajectory before another action or a final response is selected.")
    f.group("Agent context and decision process", 3.4, 1.7, 7.2, 5.6)
    f.node("request", "Task / query", 1.45, 3.0, 2.25, .85)
    f.node("context", r"Trajectory\\task + history\\observations", 5.0, 3.0, 2.8, 1.25, "store")
    f.node("policy", r"Reason / choose\\action or finish", 8.7, 3.0, 2.8, 1.1)
    f.node("call", r"Task-specific\\action", 8.7, 5.25, 2.5, .9)
    f.node("observe", r"Observation\\result or error", 5.0, 5.25, 2.6, .95)
    f.node("world", r"Tool / external\\environment", 13.45, 5.25, 3.0, 1.1)
    f.node("answer", "Final response", 13.45, 3.0, 3.0, .85)
    f.edge("request", "context", "input")
    f.edge("context", "policy")
    f.edge("policy", "answer", "finish")
    f.edge("policy", "call", "action", side="south", to_side="north")
    f.edge("call", "world", "invoke", style="control")
    f.edge("world", "observe", side="south", to_side="south", via=[(13.45,6.55),(5.0,6.55)])
    f.edge("observe", "context", "append", side="north", to_side="south", style="feedback", label_side="left")
    note(f, "The environment may change between actions; observations are inputs, not correctness certificates.", 8.0, 7.9, 12)
    emit(f, "agents-01-react-loop", "A ReAct-style agent explicitly feeds tool observations back into its trajectory context, with a separate finish path.",
         ["https://arxiv.org/abs/2210.03629"],
         ["The diagram abstracts the paper's thought/action/observation sequence and does not expose or prescribe private model reasoning.", "The finish criterion is task dependent; no convergence or correctness guarantee is implied."],
         ["agent", "ReAct", "feedback", "tools"])


def planning():
    f = Figure("Plan and execute with progress-aware replanning", subtitle="Conceptual workflow | plan state is separate from tool execution",
               caption="An explicit plan drives execution; completed-step evidence supports either replanning or a final response.")
    f.group("Run state and controller", 6.0, 2.25, 7.3, 5.55)
    f.node("task", "Task", 1.4, 3.7, 2.0, .8)
    f.node("planner", "Planner", 4.0, 3.7, 2.3, .9)
    f.node("plan", r"Ordered plan\\$(s_1,s_2,\ldots)$", 7.9, 3.7, 3.0, 1.1, "store")
    f.node("executor", r"Step executor\\current $s_i$", 11.6, 3.7, 2.6, 1.1)
    f.node("tools", "Tools", 14.35, 5.5, 2.3, .9)
    f.node("record", r"Completed steps\\and observations", 11.6, 6.9, 2.8, 1.0, "store")
    f.node("replan", r"Replan / finish\\using progress", 7.9, 6.9, 3.0, 1.0)
    f.node("response", "Final response", 4.0, 6.9, 2.6, .9)
    f.edge("task", "planner")
    f.edge("planner", "plan", "propose")
    f.edge("plan", "executor", style="control")
    f.edge("executor", "tools", "invoke", side="east", to_side="north", via=[(14.35,3.7)], style="control")
    f.edge("tools", "record", "result", side="south", to_side="east", via=[(14.35,6.9)])
    f.edge("record", "replan")
    f.edge("replan", "plan", "revise remaining steps", side="north", to_side="south", style="feedback", label_side="left")
    f.edge("replan", "response", "finish")
    note(f, "A step can use one or more tools. Serial steps are illustrated; dependency-aware parallel execution is a separate design choice.", 7.9, 1.65, 13)
    emit(f, "agents-02-plan-execute", "An original U-shaped view of the official plan-and-execute pattern, separating planner, ordered plan, executor, and progress-based replanning.",
         ["https://www.langchain.com/blog/planning-agents", "https://arxiv.org/abs/2305.04091"],
         ["Illustrates serial plan steps, not a dependency scheduler.", "Progress is passed to a replan/finish controller; criteria and iteration bounds are application choices."],
         ["agent", "planning", "execution", "state"])


def protocol():
    f = Figure("Tool-call and result protocol", subtitle="Conceptual message sequence | one call shown; further calls may follow",
               caption="The application executes the function and returns output linked to the model's call identifier.")
    f.group("Application process / conversation state", 6.0, 1.35, 4.0, 6.8)
    f.node("model", "Model", 3.0, 1.8, 2.4, .65)
    f.node("app", "Application", 8.0, 1.8, 2.8, .65)
    f.node("tool", r"Tool\\implementation", 13.0, 1.8, 3.2, .85)
    f.raw(r"\foreach \x in {3,8,13} {\draw[soft,dashed,line width=.4pt] (\x,2.2) -- (\x,7.4);}")
    messages = [
        (8,3,2.75,"(1) Prompt and tool schema", "data"),
        (3,8,3.6,r"(2) Call: name, arguments, id $c$", "data"),
        (8,13,4.45,"(3) Validate and invoke", "control"),
        (13,8,5.3,"(4) Function result or error", "data"),
        (8,3,6.15,r"(5) Tool output linked to $c$", "data"),
        (3,8,7.0,"(6) Answer or more calls", "data"),
    ]
    for a,b,y,label,style in messages:
        path(f,[(a,y),(b,y)],style,label,((a+b)/2,y-.02))
    note(f, r"Preserve call ids\\and conversation items.", 8.0, 7.7, 3.55)
    note(f, r"Application-owned validation\\and execution policy.", 13.0, 7.7, 3.7)
    emit(f, "agents-03-tool-protocol", "An original three-lane sequence diagram of the OpenAI function-call/output contract, with application-side execution authority and call-id linkage.",
         ["https://developers.openai.com/api/docs/guides/function-calling"],
         ["Uses generic names for a single illustrative function call; concrete API item types differ by API.", "Validation and execution policy are application responsibilities and are shown as explicit application steps."],
         ["protocol", "tool calling", "sequence", "application boundary"])


def reflection():
    f = Figure("Bounded reflection and revision", subtitle="Original controller around a self-feedback refinement pattern",
               caption="Feedback can guide a revision, while a stopping rule or revision budget bounds the loop; feedback may itself be wrong.")
    f.group(r"Shared task / rubric; revision count $r$", 2.45, 1.8, 10.4, 5.95)
    f.node("input", "Task and rubric", 1.35, 4.4, 2.1, .95)
    f.node("draft", r"Current candidate\\$y^{(r)}$", 4.2, 4.4, 2.6, 1.1, "store")
    f.node("critic", r"Feedback generator\\task-specific critique", 7.8, 2.8, 2.85, 1.05)
    f.node("feedback", r"Feedback\\$f^{(r)}$", 11.25, 2.8, 2.65, .95)
    f.node("gate", r"Stop / continue\\candidate + feedback\\$r < R$?", 8.0, 5.35, 3.1, 1.35)
    f.node("revise", r"Revision generator\\$y^{(r+1)}$", 4.2, 6.9, 2.8, 1.0)
    f.node("output", r"Selected candidate\\and stop reason", 14.1, 6.9, 2.9, 1.0)
    f.edge("input", "draft")
    f.edge("draft", "critic", side="north", to_side="west", via=[(4.2,2.8)])
    f.edge("critic", "feedback")
    f.edge("draft", "gate", side="east", to_side="west", via=[(5.9,4.4),(5.9,5.35)])
    f.edge("feedback", "gate", side="south", to_side="east", via=[(11.25,5.35)])
    f.edge("gate", "revise", "continue", side="south", to_side="east", via=[(8.0,6.9)], style="control")
    f.edge("revise", "draft", "increment $r$", side="north", to_side="south", style="feedback", label_side="left")
    path(f,[(9.55,5.8),(14.1,5.8),"(output.north)"],"data","stop",(12.7,5.75))
    note(f, r"$R$ is an application-chosen maximum; the critic is not an independent correctness oracle.", 8.0, 8.15, 13)
    emit(f, "agents-04-bounded-reflection", "An original bounded refinement controller inspired by Self-Refine, with candidate, self-feedback, revision, and explicit stop/budget paths.",
         ["https://arxiv.org/abs/2303.17651"],
         ["The finite revision budget and recorded stop reason are explicit design additions, not claimed paper guarantees.", "Task and rubric remain available to generation, feedback, and revision; arrows emphasize changing artifacts."],
         ["agent", "self-refine", "reflection", "bounded loop"])


def supervisor():
    f = Figure("Supervisor with tool-wrapped specialist agents", subtitle="Conceptual centralized orchestration | each specialist has a separate local context",
               caption="The supervisor supplies scoped tasks and combines returned results; specialists do not directly answer the user.")
    f.group("Main-agent state", 3.25, 1.6, 3.7, 6.1)
    f.node("user", "User request", 1.45, 3.25, 2.25, .8)
    f.node("answer", "User response", 1.45, 5.65, 2.25, .8)
    f.node("supervisor", r"Supervisor\\route and synthesize", 5.1, 4.45, 2.9, 1.2)
    f.node("state", r"Conversation and\\coordination state", 5.1, 6.9, 2.9, 1.0, "store")
    for i,(y,name,tools) in enumerate([(2.4,"Research specialist","Search / sources"),(4.6,"Data specialist","Query tools"),(6.8,"Code specialist","Execution tools")],1):
        f.group(f"Specialist {i} boundary", 8.35, y-.8, 7.1, 1.6)
        f.node(f"agent{i}", name, 10.0, y, 2.8, .9)
        f.node(f"tool{i}", tools, 13.65, y, 2.7, .9)
        f.edge(f"agent{i}",f"tool{i}",style="control")
    f.edge("user","supervisor",side="east",to_side="north",via=[(3.0,3.25),(5.1,3.25)])
    f.edge("supervisor","answer",side="west",to_side="east",via=[(3.0,4.45),(3.0,5.65)])
    path(f,[(4.8,5.05),(4.8,6.4)],"data","update",(4.7,5.85),"left")
    path(f,[(5.4,6.4),(5.4,5.05)],"data","read",(5.5,5.85),"right")
    for i,y in enumerate([2.4,4.6,6.8],1):
        sy = {1:3.98,2:4.45,3:4.93}[i]
        elbow = {1:7.3,2:7.65,3:7.3}[i]
        path(f,[(6.55,sy),(elbow,sy),(elbow,y-.2),(8.6,y-.2)],"control")
        ry={1:4.13,2:4.7,3:4.99}[i]
        path(f,[(8.6,y+.2),(7.95,y+.2),(7.95,ry),(6.55,ry)],"data")
    note(f,"Dashed: scoped task invocation. Solid return paths: specialist results. Local tool results are abstracted inside each boundary.",10.6,8.1,9.5)
    emit(f,"agents-05-supervisor","An original supervisor-centered topology showing scoped specialist invocation, result returns, main-agent conversation state, and local tool boundaries.",
         ["https://docs.langchain.com/oss/python/langchain/multi-agent/subagents"],
         ["Specialists are tool wrapped and return to the supervisor; no direct specialist-to-user path is shown.","Local tool-call/result detail is abstracted; specialties are illustrative."],
         ["multi-agent","supervisor","state","boundaries"])


def research():
    f = Figure("Parallel research with evidence reduction", subtitle="Original map-and-reduce workflow | concurrency does not imply independent evidence",
               caption="Scoped research branches return source-linked claims; the reducer checks coverage and resolves conflicts before synthesis.")
    f.group("Concurrent worker contexts",5.75,1.45,6.2,6.05)
    f.node("question","Research question",1.45,4.45,2.35,.95)
    f.node("scope",r"Assign\\research scopes",4.0,4.45,2.4,1.1)
    for i,(y,scope) in enumerate([(2.35,"Scope A"),(4.45,"Scope B"),(6.55,"Scope C")],1):
        f.node(f"worker{i}",r"Researcher " + str(i) + r"\\" + scope,7.25,y,2.4,1.0)
        f.node(f"evidence{i}",r"Claims + caveats\\source ids",10.4,y,2.5,1.15,"store")
        f.edge("scope",f"worker{i}",side="east",to_side="west",via=[(5.4,4.45),(5.4,y)],style="control")
        f.edge(f"worker{i}",f"evidence{i}")
    f.node("reduce",r"Reducer\\coverage, conflicts,\\source checks",13.75,4.45,2.8,1.35)
    f.node("synthesis",r"Source-backed\\synthesis",13.75,7.4,2.8,.9)
    f.edge("question","scope")
    f.edge("evidence1","reduce",side="east",to_side="north",via=[(13.75,2.35)])
    f.edge("evidence2","reduce")
    f.edge("evidence3","reduce",side="east",to_side="east",via=[(15.5,6.55),(15.5,4.45)])
    f.edge("reduce","synthesis",side="south",to_side="north")
    note(f,"A reducer can identify missing evidence and disagreements; it does not make unsupported claims true.",6.8,8.0,10.7)
    emit(f,"agents-06-parallel-research","An original fan-out/fan-in research design with scoped parallel workers, explicit evidence packets, and a reducer before final synthesis.",
         ["https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/","https://docs.langchain.com/oss/python/langgraph/workflows-agents"],
         ["Applies map/reduce and orchestrator/worker ideas to research; this is not a reproduction of the MapReduce system architecture.","Coverage checks and conflict resolution are application steps; shared source bias can remain."],
         ["multi-agent","parallel","research","reducer"])


def debate():
    f = Figure("Debate with an explicit adjudicator", subtitle="Original bounded two-round design informed by multiagent debate",
               caption="Agents revise after reading both arguments; a separate adjudicator records a decision and any unresolved disagreement.")
    f.group("Two illustrative debate rounds",1.4,2.3,13.2,4.3)
    f.node("question","Question + rubric",8,1.6,4.1,.7)
    f.node("a0",r"Agent A\\initial answer",3.1,3.2,3.0,1.0)
    f.node("b0",r"Agent B\\initial answer",12.9,3.2,3.0,1.0)
    f.node("transcript",r"Shared transcript\\both initial arguments",8.0,3.2,3.5,1.0,"store")
    f.node("a1",r"Agent A\\revised answer",3.1,5.6,3.0,1.0)
    f.node("b1",r"Agent B\\revised answer",12.9,5.6,3.0,1.0)
    f.node("judge",r"Adjudicator\\decision + disagreement",8.0,7.5,4.0,1.0)
    f.edge("question","a0",side="west",to_side="north",via=[(3.1,1.6)])
    f.edge("question","b0",side="east",to_side="north",via=[(12.9,1.6)])
    f.edge("a0","transcript","argument")
    f.edge("b0","transcript","argument")
    f.edge("transcript","a1",side="south",to_side="north",via=[(8,4.35),(3.1,4.35)])
    f.edge("transcript","b1",side="south",to_side="north",via=[(8,4.35),(12.9,4.35)])
    f.edge("a1","judge",side="south",to_side="west",via=[(3.1,7.5)])
    f.edge("b1","judge",side="south",to_side="east",via=[(12.9,7.5)])
    note(f,"Each revision sees both arguments.\nNo agent's answer is privileged by the topology.",8,5.55,4.3)
    emit(f,"agents-07-debate-adjudicator","An original two-round debate topology with transcript exchange followed by a distinct adjudicator, rather than assuming consensus is correct.",
         ["https://arxiv.org/abs/2305.14325"],
         ["A separate adjudicator and explicit disagreement output are design additions inspired by the debate pattern.","Two rounds are illustrative; correlated mistakes and adjudicator errors remain possible."],
         ["multi-agent","debate","adjudication","transcript"])


def rag():
    f = Figure("RAG: separate indexing from per-query generation", subtitle="Conceptual retrieval-augmented inference | corpus preparation and serving have different lifecycles",
               caption="Indexing writes document representations; a query retrieves passages that condition the generator alongside the query.")
    f.group("Corpus preparation / index write",.45,1.55,15.1,2.55)
    f.group("Per-query inference / index read",.45,4.9,15.1,3.15)
    f.node("docs",r"Source\\documents",2.0,2.8,2.7,.9)
    f.node("chunk",r"Passage preparation\\stable passage ids",5.6,2.8,2.8,1.05)
    f.node("denc",r"Document encoder\\passage vectors",9.2,2.8,2.8,1.05)
    f.node("index",r"Retrieval index\\vectors + linked passages",13.15,2.8,3.25,1.1,"store")
    f.node("query","Query",2.0,6.0,2.7,.9)
    f.node("qenc",r"Query encoder\\query vector",5.6,6.0,2.8,1.05)
    f.node("retrieve",r"Retrieve passages\\for query",9.2,6.0,2.8,1.05)
    f.node("generate",r"Generator\\query + passages",13.15,6.0,3.25,1.05)
    f.node("answer","Response",13.15,7.5,3.25,.65)
    f.edge("docs","chunk")
    f.edge("chunk","denc")
    f.edge("denc","index","write")
    path(f,["(chunk.north)",(5.6,1.95),(13.15,1.95),"(index.north)"],"data","passage ids + text",(9.3,1.9))
    f.edge("query","qenc")
    f.edge("qenc","retrieve")
    path(f,[(9.0,5.475),(9.0,4.45),(12.85,4.45),(12.85,3.35)],"data","lookup vector",(10.5,4.42))
    path(f,[(13.45,3.35),(13.45,4.7),(9.4,4.7),(9.4,5.475)],"data","passages",(11.5,4.72),"below")
    f.edge("retrieve","generate")
    path(f,[(2.0,6.45),(2.0,7.35),(11.1,7.35),(11.1,6.0),(11.525,6.0)],"data","original query",(6.4,7.3))
    f.edge("generate","answer",side="south",to_side="north")
    emit(f,"agents-08-rag-lifecycles","An original two-lane RAG architecture separating document indexing from query-time encoding, retrieval, and generation, including an explicit query-to-generator path.",
         ["https://arxiv.org/abs/2005.11401"],
         ["Uses a dense retrieval abstraction; training, index refresh, ranking, and passage storage implementations are omitted.","Linked passages are included in the retrieval-index abstraction; no index size or exact tensor dimension is asserted."],
         ["RAG","indexing","retrieval","generation"])


def hybrid():
    f = Figure("Hybrid retrieval with reciprocal rank fusion", subtitle="Conceptual fusion of independently ranked lexical and dense result lists",
               caption="Fuse document ranks from lexical and dense retrieval, deduplicate by document id, then select the context window.")
    f.group("Lexical retrieval branch",3.4,1.45,6.6,2.8)
    f.group("Dense retrieval branch",3.4,4.85,6.6,2.8)
    f.node("q","Query",1.35,4.5,2.05,.85)
    f.node("terms","Term index",5.0,2.0,2.55,.7,"store")
    f.node("lexical","Lexical retriever",5.0,3.25,2.65,.85)
    f.node("list1",r"Ranked list $L_1$\\$\begin{array}{ccc} A&C&D\\1&2&3\end{array}$",8.35,3.25,2.65,1.4,"store")
    f.node("vectors","Vector index",5.0,5.4,2.55,.7,"store")
    f.node("dense","Dense retriever",5.0,6.65,2.65,.85)
    f.node("list2",r"Ranked list $L_2$\\$\begin{array}{ccc} B&A&D\\1&2&3\end{array}$",8.35,6.65,2.65,1.4,"store")
    f.node("fusion",r"Rank fusion\\by document id",11.75,4.5,2.9,1.1)
    f.node("context",r"Top-$K$\\context",14.65,4.5,1.9,1.0)
    f.edge("q","lexical",side="east",to_side="west",via=[(2.95,4.5),(2.95,3.25)])
    f.edge("q","dense",side="east",to_side="west",via=[(2.95,4.5),(2.95,6.65)])
    f.edge("terms","lexical",side="south",to_side="north")
    f.edge("vectors","dense",side="south",to_side="north")
    f.edge("lexical","list1")
    f.edge("dense","list2")
    f.edge("list1","fusion",side="east",to_side="north",via=[(11.75,3.25)])
    f.edge("list2","fusion",side="east",to_side="south",via=[(11.75,6.65)])
    f.edge("fusion","context")
    note(f,r"$s(d)=\displaystyle\sum_{i:\,d\in L_i}\frac{1}{k+r_i(d)}$",12.2,7.6,6.0)
    note(f,r"$r_i(d)$ is one-based rank; $k>0$ is a chosen rank constant. Example ids are illustrative.",7.9,8.25,14)
    emit(f,"agents-09-hybrid-fusion","An original two-branch hybrid retrieval diagram that fuses lexical and vector rank lists with the reciprocal-rank formula and a document-id merge.",
         ["https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion","https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf"],
         ["Two equal-weight child lists and illustrative document ids are shown; retrieval scores are not added directly.","The rank constant and rank-window sizes are implementation choices; no quality guarantee is implied."],
         ["retrieval","hybrid","RRF","fusion"])


def corrective():
    f = Figure("Corrective RAG with route-dependent evidence", subtitle="Conceptual CRAG control logic | an evaluator selects correct, ambiguous, or incorrect retrieval paths",
               caption="The evaluator selects refined retrieved evidence, web evidence, or both; its routing decisions can still be wrong.")
    f.group("Retrieval evaluation and correction",2.6,1.45,10.1,6.5)
    f.node("query","Query",1.3,3.5,2.05,.85)
    f.node("retrieve",r"Initial\\retrieval",4.0,3.5,2.35,1.0)
    f.node("evaluate",r"Retrieval evaluator\\score evidence relevance",7.25,3.5,2.9,1.1)
    f.node("refine",r"Refine retrieved\\knowledge",11.0,2.45,2.8,1.0)
    f.node("web",r"Query rewrite\\and web search",7.25,6.5,2.9,1.1)
    f.node("assemble",r"Evidence assembly\\route-dependent inputs",11.0,6.5,2.8,1.1)
    f.node("generate",r"Generator\\query + evidence",14.2,4.5,2.7,1.1)
    f.node("answer","Response",14.2,7.3,2.7,.8)
    f.edge("query","retrieve")
    f.edge("retrieve","evaluate")
    f.edge("evaluate","refine",side="east",to_side="west",via=[(9.1,3.5),(9.1,2.45)])
    note(f,"correct or ambiguous",10.5,1.75,4.0)
    f.edge("evaluate","web",side="south",to_side="north",style="control")
    note(f,"incorrect or ambiguous",8.5,5.15,2.0)
    f.edge("refine","assemble",side="south",to_side="north")
    note(f,r"retained\\evidence",10.1,4.55,1.65)
    f.edge("web","assemble")
    f.edge("assemble","generate",side="east",to_side="west",via=[(12.6,6.5),(12.6,4.5)])
    f.edge("generate","answer",side="south",to_side="north")
    note(f,"Paths: correct = refined retrieval; incorrect = web; ambiguous = both. Assembly consumes only selected inputs.",8.0,8.25,14.7)
    emit(f,"agents-10-corrective-rag","An original CRAG logic view with a retrieval evaluator controlling refined-corpus, web-search, and combined-evidence paths into generation.",
         ["https://arxiv.org/abs/2401.15884","https://arxiv.org/html/2401.15884v3"],
         ["Correct/incorrect/ambiguous route semantics follow CRAG; evaluator internals and knowledge-refinement internals are abstracted.","The query is shared request context for evaluation, rewriting, and generation; branch arrows emphasize evidence and route control.","Evidence assembly consumes only route-selected inputs; it does not wait for a branch that was not executed."],
         ["RAG","CRAG","corrective retrieval","conditional control"])


def memory():
    f = Figure("Thread state and cross-session memory", subtitle="Conceptual agent memory | explicit reads, state updates, and selected long-term writes",
               caption="Thread-scoped history supports the current run; namespaced long-term memory is read and updated across sessions.")
    f.group("Current thread / session id",.65,1.65,9.35,5.95)
    f.group("Cross-thread namespace",10.65,1.65,4.9,6.45)
    f.node("history",r"Thread state\\messages + task state",3.0,2.85,3.25,1.15,"store")
    f.node("context",r"Context builder\\relevant state",7.2,2.85,3.0,1.1)
    f.node("input","New user message",3.0,5.65,3.0,.9)
    f.node("agent",r"Agent step\\model + tools",7.2,5.65,3.0,1.1)
    f.node("long",r"Long-term store\\namespaced records",13.1,2.85,3.65,1.15,"store")
    f.node("write",r"Memory write policy\\extract / curate / save",13.1,5.65,3.65,1.1)
    f.node("next",r"Later session\\context builder",13.1,7.35,3.65,.9)
    f.edge("history","context","read")
    f.edge("context","agent",side="south",to_side="north")
    f.edge("input","agent","input")
    f.edge("agent","history",side="west",to_side="south",via=[(5.15,5.65),(5.15,4.15),(3,4.15)],style="feedback")
    note(f,r"append messages\\and results",3.35,4.65,3.0)
    f.edge("long","context","recall",side="west",to_side="east")
    f.edge("agent","write","candidate memory")
    f.edge("write","long","selected write",side="north",to_side="south",label_side="right")
    path(f,[(14.925,2.85),(15.25,2.85),(15.25,7.35),(14.925,7.35)],"data")
    note(f,"recall",15.15,7.9,1.1)
    note(f,"Memory records are application data. Retention, scope, and write rules are explicit application choices.",7.8,8.25,14.5)
    emit(f,"agents-11-memory-scopes","An original two-boundary memory diagram showing current-thread state reads and feedback updates, plus selected writes and cross-session reads of a namespaced long-term store.",
         ["https://docs.langchain.com/oss/python/concepts/memory","https://arxiv.org/abs/2310.08560"],
         ["The memory write policy is an illustrative application component, not an automatic guarantee of accurate memories.","Memory recall is an explicit data retrieval operation; no online model training is shown."],
         ["agent","memory","state","session boundaries"])


def event_workflow():
    f = Figure("Event-driven agent workflow with durable state", subtitle="Original asynchronous design | message identity, task dispatch, and recovery state are explicit",
               caption="Events drive state transitions and task dispatch; deduplication and recovery depend on persistence and worker semantics.")
    f.group("Workflow coordinator / durable state",3.0,1.45,9.7,6.2)
    for id,y,label in [("user",2.3,"User request"),("tool",4.5,"Tool completion"),("timer",6.7,"Timer / signal")]:
        f.node(id,label,1.35,y,2.15,.8)
    f.node("inbox",r"Inbox / dedup\\event identifier",4.5,4.5,2.65,1.1)
    f.node("log",r"Append-only\\event log",7.65,2.35,2.8,1.0,"store")
    f.node("handler",r"Agent event handler\\state transition",7.65,4.5,2.8,1.1)
    f.node("checkpoint",r"Checkpoint\\workflow state",7.65,6.7,2.8,1.0,"store")
    f.node("outbox",r"Task outbox\\dispatch intent",11.15,4.5,2.65,1.1,"store")
    f.node("worker",r"Tool / worker\\execute task",14.3,4.5,2.7,1.1)
    f.node("completion",r"Completion event\\result or failure",14.3,7.0,2.7,1.0)
    for id,y in [("user",2.3),("tool",4.5),("timer",6.7)]:
        f.edge(id,"inbox",side="east",to_side="west",via=[(2.8,y),(2.8,4.5)])
    f.edge("inbox","log",side="north",to_side="west",via=[(4.5,2.35)])
    f.edge("log","handler","consume",side="south",to_side="north")
    f.edge("handler","outbox")
    f.edge("outbox","worker",style="control")
    f.edge("worker","completion","result",side="south",to_side="north")
    f.edge("completion","inbox",side="south",to_side="south",via=[(14.3,8.05),(4.5,8.05)],style="feedback")
    path(f,[(7.35,5.05),(7.35,6.2)],"data","persist",(7.2,5.65),"left")
    path(f,[(7.95,6.2),(9.35,6.2),(9.35,5.45),(7.95,5.45),(7.95,5.05)],"data","load",(9.4,5.85),"right")
    emit(f,"agents-12-event-workflow","An original asynchronous agent coordinator with event inbox, deduplication identity, append-only log, state checkpoint, task outbox, worker, and completion-event feedback.",
         ["https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing","https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply"],
         ["An original event-driven agent design informed by event-sourcing and asynchronous request/reply patterns; no exactly-once guarantee is claimed.","The figure does not prescribe a distributed transaction between event log, checkpoint, and outbox; consistency and retry behavior require implementation choices."],
         ["agent","events","asynchronous","durable state"])


def approval():
    f = Figure("Human approval checkpoint before side effects", subtitle="Conceptual pause-and-resume control | approval is a runtime input",
               caption="Persist the proposal and paused state, obtain a human decision, then resume to execute or cancel.")
    f.group("Paused / resumed workflow runtime",2.6,3.2,10.0,4.8)
    f.node("request","Requested task",1.3,4.5,2.05,.9)
    f.node("proposal",r"Prepare concrete\\action proposal",4.15,4.5,2.6,1.1)
    f.node("pause",r"Interrupt\\before execution",7.45,4.5,2.7,1.1)
    f.node("reviewer",r"Human reviewer\\proposal and context",7.45,2.05,3.5,1.0)
    f.node("resume",r"Resume decision\\approve / reject",10.95,4.5,2.8,1.1)
    f.node("state",r"Persist paused state\\thread + proposal",7.45,7.0,3.0,1.1,"store")
    f.node("execute",r"Approved:\\execute action",14.2,3.6,2.8,1.0)
    f.node("cancel",r"Rejected:\\cancel action",14.2,6.3,2.8,.9)
    f.edge("request","proposal")
    f.edge("proposal","pause")
    f.edge("pause","reviewer",side="north",to_side="south")
    f.edge("pause","state","save",side="south",to_side="north")
    f.edge("reviewer","resume","decision",side="east",to_side="north",via=[(10.95,2.05)],style="control")
    f.edge("state","resume","restore",side="east",to_side="south",via=[(10.95,7.0)])
    f.edge("resume","execute",side="east",to_side="west",via=[(12.65,4.5),(12.65,3.6)],style="control")
    f.edge("resume","cancel",side="east",to_side="west",via=[(12.65,4.5),(12.65,6.3)],style="control")
    note(f,"The stored thread identifies the paused run. The action is not dispatched while this checkpoint is waiting.",8.0,8.35,14)
    emit(f,"agents-13-human-approval","An original pause-and-resume approval architecture with persisted proposal state, a human review boundary, and explicit approve/execute and reject/cancel paths.",
         ["https://docs.langchain.com/oss/python/langgraph/interrupts"],
         ["Illustrates a workflow configured to interrupt before the side effect; the checkpoint is not a general guarantee of all tool safety.","Authentication, proposal freshness, and replay/side-effect idempotency are application concerns beyond this conceptual figure."],
         ["agent","human in the loop","approval","checkpoint"])


def sandbox():
    f = Figure("Sandboxed code execution with explicit result capture", subtitle="Original host/runtime workflow | policy and isolation boundaries are separate components",
               caption="Validate and launch code under an explicit runtime policy; return captured outputs and deliberately exported artifacts.")
    f.group("Host execution service",3.4,1.55,6.15,6.4)
    f.group("Configured sandbox boundary",10.3,1.55,5.25,6.4)
    f.node("agent",r"Agent\\code request",1.7,3.4,2.7,1.1)
    f.node("validate",r"Validate request\\arguments + policy",5.0,3.4,2.65,1.1)
    f.node("launch",r"Runtime launcher\\resource limits",8.0,3.4,2.6,1.1)
    f.node("process",r"Code process\\isolated runtime",12.9,3.4,3.5,1.15)
    f.node("policy",r"Execution policy\\mounts / network / limits",5.0,6.4,2.65,1.2,"store")
    f.node("capture",r"Result capture\\stdout, stderr, exit status",8.0,6.4,2.65,1.2)
    f.node("files",r"Ephemeral files\\exported artifacts",12.9,6.4,3.5,1.15,"store")
    f.edge("agent","validate")
    f.edge("validate","launch",style="control")
    f.edge("launch","process","launch",style="control")
    f.edge("policy","validate",side="north",to_side="south",style="control")
    f.edge("policy","launch",side="east",to_side="south",via=[(6.5,6.4),(6.5,4.65),(8,4.65)],style="control")
    f.edge("process","files","writes",side="south",to_side="north")
    f.edge("files","capture","exported files")
    path(f,[(11.15,3.4),(10.0,3.4),(10.0,5.1),(8.0,5.1),(8.0,5.8)],"data","execution outputs",(9.0,5.05))
    f.edge("capture","agent",side="south",to_side="south",via=[(8,7.8),(1.7,7.8)],style="feedback")
    note(f,"Isolation and allowed access depend on runtime and configuration; the boundary is not a claim of perfect containment.",8,8.4,14.5)
    emit(f,"agents-14-sandbox-execution","An original execution-service workflow with request validation, configured runtime launch, resource/access policy, sandboxed process, ephemeral files, and captured-result feedback.",
         ["https://gvisor.dev/docs/architecture_guide/intro/","https://gvisor.dev/docs/user_guide/quick_start/docker/"],
         ["The generic workflow is informed by gVisor's runtime isolation boundary; it is not a diagram of the Sentry/Gofer internals.","Resource limits, mounts, network access, and artifact export are illustrative configured controls; no perfect-containment guarantee is implied."],
         ["agent","sandbox","code execution","security boundary"])


def serving():
    f = Figure("Distributed inference with tensor-parallel serving", subtitle="Conceptual serving path | one replica; two illustrative ranks; rank count and placement vary",
               caption="A scheduler dispatches active sequences to a tensor-parallel replica; local KV state supports iterative token generation.")
    f.group("Serving coordinator",3.75,1.5,3.35,5.9)
    f.group("One tensor-parallel replica",7.5,1.5,5.15,5.9)
    f.node("client",r"Client / API\\request",1.6,4.0,2.65,1.1)
    f.node("queue","Request queue",5.4,2.25,2.65,.9,"store")
    f.node("scheduler",r"Scheduler\\active batch",5.4,4.0,2.65,1.1)
    f.node("batch",r"Sequence and\\batch state",5.4,6.55,2.65,1.0,"store")
    f.node("kv0",r"Local KV state",9.7,2.0,3.0,.65,"store")
    f.node("rank0",r"Rank 0 worker\\model shard",9.7,3.25,3.0,1.0)
    f.node("rank1",r"Rank 1 worker\\model shard",9.7,5.4,3.0,1.0)
    f.node("kv1",r"Local KV state",9.7,6.65,3.0,.65,"store")
    f.node("stream",r"Token / text\\response stream",14.3,3.25,2.7,1.0)
    f.edge("client","queue",side="east",to_side="west",via=[(3.2,4),(3.2,2.25)])
    f.edge("queue","scheduler",side="south",to_side="north")
    f.edge("scheduler","rank0",side="east",to_side="west",via=[(7.25,4),(7.25,3.25)],style="control")
    f.edge("scheduler","rank1",side="east",to_side="west",via=[(7.25,4),(7.25,5.4)],style="control")
    path(f,["(kv0.south)","(rank0.north)"],"both")
    path(f,["(rank1.south)","(kv1.north)"],"both")
    path(f,[(11.2,3.5),(11.9,3.5),(11.9,5.15),(11.2,5.15)],"both")
    note(f,r"Tensor-parallel\\collectives",9.7,4.3,3.0)
    f.edge("rank0","stream","tokens")
    path(f,[(5.1,4.55),(5.1,6.05)],"data","update",(5.0,5.35),"left")
    path(f,[(5.7,6.05),(5.7,4.55)],"data","read",(5.8,5.35),"right")
    path(f,[(14.3,3.75),(14.3,7.9),(1.6,7.9),(1.6,4.55)],"data","incremental response",(8,7.85))
    note(f,"KV arrows denote per-rank state access; read/write details and token-selection placement are abstracted.",8,8.4,14.2)
    emit(f,"agents-15-distributed-serving","An original distributed inference serving topology with a request queue, active-batch scheduler, a two-rank tensor-parallel replica, per-rank KV state, collective communication, and a client response stream.",
         ["https://docs.vllm.ai/en/latest/serving/parallelism_scaling/","https://arxiv.org/abs/2309.06180"],
         ["Two ranks are illustrative; exact placement, parallelism degree, batch policy, and KV-cache management vary.","A representative leader output path is shown; sampling/detokenization and backend-specific control/data exchange are abstracted.","KV state arrows indicate state access, not a claim that one rank only reads while another only writes."],
         ["serving","distributed inference","tensor parallelism","KV cache"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for make in [react,planning,protocol,reflection,supervisor,research,debate,rag,hybrid,corrective,memory,event_workflow,approval,sandbox,serving]:
        make()
    if len(INDEX) != 15:
        raise AssertionError("Expected exactly 15 figures")
    (OUT / "index.json").write_text(json.dumps(INDEX, indent=2) + "\n")
    print(f"Generated {len(INDEX)} figures in {OUT}")


if __name__ == "__main__":
    main()
