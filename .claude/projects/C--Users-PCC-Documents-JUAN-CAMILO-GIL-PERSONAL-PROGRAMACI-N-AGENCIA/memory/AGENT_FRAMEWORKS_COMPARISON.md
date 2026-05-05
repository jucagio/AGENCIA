# Agent Frameworks Comparison 2026
## Decision Matrix: Claude SDK vs LangGraph vs CrewAI

**Context:** Agencia needs to choose primary frameworks for:
- Multi-agent coordination (Jarvis managing agents)
- Workflow automation (Cinthya building complex workflows)
- Backend agents (Sasha building AI-powered APIs)

**Recommendation:** Use BOTH Claude SDK + LangGraph (complementary, not competing)

---

## FRAMEWORK COMPARISON TABLE

| Aspect | Claude SDK | LangGraph | CrewAI | OpenAI Agents |
|--------|-----------|-----------|--------|----------------|
| **Created by** | Anthropic | LangChain | CrewAI Inc | OpenAI |
| **Stars (GitHub)** | Growing fast | 50k+ | 25k+ | Closed-source |
| **Monthly searches** | N/A | 27.1k (highest) | 14.8k | Medium |
| **Release status** | 2026 Q1 (stable) | Production-ready | Stable | March 2026 |
| **Language(s)** | Python, JavaScript | Python | Python | Python, JS |
| **MCP integration** | Deepest (500+ MCPs) | Basic | None | API-only |
| **Learning curve** | Easy (tool-use native) | Medium-Hard | Medium | Hard |
| **Best for** | Simple-medium complexity | Complex stateful workflows | Team-based task orchestration | Enterprise API integration |
| **Performance** | Fast | Medium | Medium | Depends on API |
| **Production readiness** | High | Very High | Medium | High |
| **Community** | Growing | Largest | Growing | Large (enterprise) |
| **Cost** | Usage-based (Claude API) | Free (LangChain) | Free (CrewAI) | Usage-based (OpenAI API) |
| **Scalability** | Excellent | Excellent | Good | Depends on OpenAI |

---

## DETAILED COMPARISON

### Claude SDK (Anthropic)
**Philosophy:** "Tool-use-first agents" — Claude is the agent, tools extend its capabilities.

#### Strengths
✅ **Deepest MCP integration** — 500+ MCP servers with one config line
✅ **Simple architecture** — no complex orchestration frameworks needed
✅ **Tool-use native** — Claude's native capability (not bolted-on)
✅ **Sub-agents as tools** — invoking other agents is first-class
✅ **Latest model features** — always aligned with Claude's newest capabilities
✅ **Best for Agencia** — aligns with Anthropic's ecosystem
✅ **Agentic edge** — Anthropic designed this for agent workflows

#### Weaknesses
❌ **No state persistence** — agents reset between calls (must build manually)
❌ **Limited observability** — no built-in dashboards/tracing (but MCP compatible)
❌ **No checkpoints** — can't pause/resume long-running workflows
❌ **Token usage higher** — doesn't optimize context window like LangGraph
❌ **Learning curve for sub-agents** — requires understanding tool invocation

#### Best Use Cases
- 🎯 Coordinating Jarvis (CEO) with sub-agents (Sasha, Brook, Erik)
- 🎯 Real-time agent interactions (no persistence needed)
- 🎯 Leveraging MCP servers (Playwright, GitHub, Slack, 500+ integrations)
- 🎯 Simple tool-use patterns (classification, extraction, routing)

#### Agencia Fit: **EXCELLENT** (Recommended as primary)

---

### LangGraph (LangChain)
**Philosophy:** "Explicit state machine" — workflow is graph of nodes, edges define control flow.

#### Strengths
✅ **Stateful workflows** — explicit state management, persistence
✅ **Checkpoints** — pause/resume long-running workflows
✅ **Observable** — LangSmith integration (production dashboards, cost tracking)
✅ **Flexible memory** — short-term, long-term, semantic memory
✅ **Conditional routing** — explicit control flow (if/else, loops)
✅ **Production-hardened** — highest adoption in production (27.1k monthly searches)
✅ **Error recovery** — built-in retry logic, fallback paths
✅ **Token optimization** — manages context window efficiently

#### Weaknesses
❌ **Steeper learning curve** — must understand graph architecture
❌ **More boilerplate** — requires explicit node/edge definitions
❌ **Slower for simple tasks** — overkill for basic tool-use
❌ **Less MCP integration** — MCPs work, but not as seamlessly as Claude SDK
❌ **Heavier dependencies** — larger library footprint

#### Best Use Cases
- 🎯 Complex workflows with state (Cinthya's n8n replacements)
- 🎯 Long-running processes that must survive restarts
- 🎯 Production monitoring & cost tracking (via LangSmith)
- 🎯 Workflows with branching logic (if/else, parallel execution)
- 🎯 Memory-intensive agents (retrieval, knowledge graphs)

#### Agencia Fit: **EXCELLENT** (Recommended as secondary for workflows)

---

### CrewAI
**Philosophy:** "Role-based agents" — agents have roles, can collaborate like a team.

#### Strengths
✅ **Intuitive for teams** — agents have defined roles (CEO, engineer, etc.)
✅ **Collaboration primitives** — agents can delegate, ask for help
✅ **Simple setup** — less boilerplate than LangGraph
✅ **Good for hierarchical tasks** — matches Agencia's org structure
✅ **Growing community** — 14.8k monthly searches

#### Weaknesses
❌ **Less mature** — smaller production footprint than LangGraph
❌ **No state persistence** — workflows reset (unlike LangGraph)
❌ **No observability** — no built-in tracing/dashboards
❌ **MCP support** — none (MCPs not integrated)
❌ **Token optimization** — not as efficient as LangGraph
❌ **Less flexible** — role-based model can be limiting

#### Best Use Cases
- 🎯 Hierarchical team orchestration (but Agencia already has that)
- 🎯 Simple collaboration workflows
- 🎯 Learning/teaching multi-agent concepts

#### Agencia Fit: **EVALUATE LATER** (Not recommended for Q2; monitor for future use)

---

### OpenAI Agents SDK
**Philosophy:** "Function calling at scale" — lightweight wrappers around function calling.

#### Strengths
✅ **Enterprise backing** — OpenAI support & stability
✅ **Tight API integration** — native to OpenAI ecosystem
✅ **Simple** — less code than competitors
✅ **Known quantity** — if using GPT-4

#### Weaknesses
❌ **Vendor lock-in** — only works with OpenAI models
❌ **No MCP support** — MCPs not available
❌ **Weaker models** — Agencia uses Claude (better for reasoning)
❌ **No state persistence** — like Claude SDK (must build manually)
❌ **Less community** — smaller ecosystem
❌ **Agencia misaligned** — we're Anthropic-focused

#### Best Use Cases
- 🎯 OpenAI-only shops
- 🎯 GPT-4 preferred (not Agencia's case)

#### Agencia Fit: **NOT RECOMMENDED** (Avoid due to vendor lock-in)

---

## RECOMMENDATION FOR AGENCIA

### Primary: Claude SDK
**When to use:** Coordination between Jarvis and agents, simple tool-use, leveraging MCPs.

```python
# Example: Jarvis invoking Sasha + Brook in parallel
@jarvis
def coordinate_feature():
    backend_result = invoke_tool("sasha_design_api")
    frontend_result = invoke_tool("brook_design_ui")
    return combine_results(backend_result, frontend_result)
```

**Adoption:** Week of April 8-12 (Jade creates skill)

---

### Secondary: LangGraph
**When to use:** Complex workflows with state, Cinthya's automations, long-running processes.

```python
# Example: Cinthya workflow with checkpoints
workflow = StateGraph(WorkflowState)
workflow.add_node("extract_data", extract_node)
workflow.add_node("transform_data", transform_node)
workflow.add_node("validate_data", validate_node)
workflow.add_conditional_edges(
    "validate_data",
    validation_check,
    {"valid": "save_data", "invalid": "error_handler"}
)
```

**Adoption:** Week of April 15-19 (after Claude SDK, Jade creates skill)

---

### Monitor: CrewAI
**Status:** Evaluate quarterly. Use if Agencia needs hierarchical team orchestration beyond what Claude SDK + LangGraph provides.

---

## INTEGRATION STRATEGY

```
                    JARVIS (CEO)
                       |
        ┌──────────────┼──────────────┐
        │              │              │
    SASHA (Backend)   BROOK (Frontend) ERIK (Design)
    (Claude SDK)      (Claude SDK)      (Claude SDK)
        │
        │ Complex workflows
        └──> LangGraph (Cinthya orchestration)
                │
          [Checkpoints]
          [LangSmith observability]
          [Memory management]
```

**How it works:**
1. Jarvis (CEO) coordinates with agents using Claude SDK (simple tool-use)
2. Each agent can invoke sub-tools via Claude SDK
3. Cinthya builds complex workflows using LangGraph for stateful processing
4. LangGraph integrates with Claude Agent SDK (Claude as the reasoner)
5. LangSmith monitors all LangGraph workflows

---

## IMPLEMENTATION ROADMAP

### April (Week 2-4): Claude SDK + Skills
- Jade researches Claude SDK (20h)
- Jade creates "Claude Agent SDK Multi-Agent Orchestration" skill
- Team learns tool-use patterns
- Jarvis starts using Claude SDK for agent coordination

### April (Week 3-4): LangGraph + Skills
- Jade researches LangGraph (15h)
- Jade creates "LangGraph Advanced Patterns" skill
- Cinthya learns LangGraph (hands-on)
- First LangGraph workflow in production (simple one)

### May: Full Integration
- LangGraph workflows for complex automations
- Claude SDK for real-time agent coordination
- LangSmith dashboards (observability)
- Monitoring & optimization

### Q3: CrewAI Evaluation (Optional)
- Monitor CrewAI evolution
- Evaluate if it's useful for specific workflows
- No decision needed until Q3

---

## KEY DIFFERENCES FOR AGENCIA

| Scenario | Use Claude SDK | Use LangGraph | Use CrewAI |
|----------|---|---|---|
| Jarvis coordinating agents | ✅ Claude SDK | ❌ No | ❌ No |
| Cinthya's complex workflows | ⚠️ Possible | ✅ LangGraph | ❓ Maybe |
| Sasha's backend APIs | ✅ Claude SDK | ⚠️ Overkill | ❌ No |
| Erik's design automation | ✅ Claude SDK | ❌ No | ❌ No |
| Long-running batch processes | ❌ No | ✅ LangGraph | ⚠️ Possible |
| Real-time agent interactions | ✅ Claude SDK | ❌ No | ✅ CrewAI |
| Observability & monitoring | ⚠️ Via MCP | ✅ LangSmith | ❌ No |

---

## RESEARCH SOURCES

- [The Agent Framework Landscape: LangChain vs Claude SDK](https://medium.com/@richardhightower/the-agent-framework-landscape-langchain-deep-agents-vs-claude-agent-sdk-1dfed14bb311)
- [LangGraph + Claude Agent SDK Ultimate Guide 2026](https://www.mager.co/blog/2026-03-07-langgraph-claude-agent-sdk-ultimate-guide/)
- [Best Multi-Agent Frameworks 2026](https://gurusup.com/blog/best-multi-agent-frameworks-2026)
- [Framework Comparison: LangGraph vs CrewAI](https://letsdatascience.com/blog/ai-agent-frameworks-compared)
- [Langfuse Framework Rankings (27.1k searches/month)](https://langfuse.com/blog/2026-agent-framework-rankings)

---

**Owner:** Jade (Directora Intel & Capacitaciones)
**Approved by:** Jarvis (CEO)
**Status:** ✅ Ready for implementation
**Date:** April 5, 2026
