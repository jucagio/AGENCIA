# Skills to Create — Implementation Roadmap
## Nueva Documentación de Capacidades del Equipo

**Owner:** Jade (Directora Intel & Capacitaciones)
**Status:** Ready for April 2026 creation sprint
**Total estimated effort:** 95 hours (Jade's responsibility)

---

## SKILLS PRIORITY LIST (Q2 2026)

### TIER 1 — FOUNDATIONAL (Create first, April)

#### 1. Claude Agent SDK Multi-Agent Orchestration
**File:** `.claude/skills/claude-agent-sdk-multi-agent.md`
**Created by:** Jade
**Effort:** 20 hours
**Timeline:** Week of April 8-12
**Target audience:** All agents (Jarvis, Sasha, Brook, Cinthya, Alejo)
**Key topics:**
- Tool-use-first architecture (Claude's advantage vs other SDKs)
- Agent invocation as tools (sub-agents pattern)
- MCP integration (Playwright, Slack, GitHub, 500+ MCP servers)
- Comparison: Claude SDK vs LangGraph vs CrewAI (when to use each)
- Error handling & retries in multi-agent flows
- Token optimization (max_tokens, streaming, etc.)
- Code examples: invoking sub-agents in parallel

**Success criteria:**
- Cinthya can build workflows invoking 5+ agents in parallel
- Jarvis understands when to use Claude SDK vs LangGraph
- All agents know how to call sub-agents

**Dependencies:** None (foundational)

---

#### 2. LangGraph Advanced Patterns
**File:** `.claude/skills/langgraph-advanced.md`
**Created by:** Jade
**Effort:** 15 hours
**Timeline:** Week of April 15-19 (after Claude SDK)
**Target audience:** Cinthya (primary), Sasha (backend agents), Brook (if integrating agents in frontend)
**Key topics:**
- Stateful agent loops (ReAct pattern, explicit)
- Checkpoints (persistence, recovery)
- Memory management (short-term, long-term, semantic)
- Conditional branching & routing
- Error handling & recovery
- Integration with LangChain tools
- LangSmith observability (tracing, debugging)
- Comparison: LangGraph for complex workflows vs Claude SDK for simpler coordination

**Success criteria:**
- Cinthya builds 3+ production workflows with LangGraph
- Workflows have checkpoints & survive restarts
- LangSmith dashboards show performance

**Dependencies:** Claude Agent SDK skill (must understand tool-use-first first)

---

#### 3. Supabase Production Patterns
**File:** `.claude/skills/supabase-production-patterns.md`
**Created by:** Jade (based on Sasha's audit)
**Effort:** 10 hours
**Timeline:** Week of April 15-19 (parallel with LangGraph)
**Target audience:** Sasha (primary), Brook (frontend querying), Alejo (performance decisions)
**Key topics:**
- RLS best practices (performance optimization, indexing strategies)
- Query optimization (100x performance gains via indexes)
- Realtime architecture (WebSocket, RLS filtering)
- Edge Functions (serverless business logic)
- Storage patterns (file organization, security)
- Connection pooling (PgBouncer config)
- Multi-tenancy patterns
- Cost optimization (query audit, unused indexes)
- Migration strategies (without downtime)

**Success criteria:**
- All queries <100ms on large tables
- Realtime events <50ms latency
- Zero N+1 queries in production
- Cost reduced 20%+ via optimization

**Dependencies:** Sasha must complete RLS audit first

---

#### 4. GitHub Actions 2.0 DevSecOps Pipeline
**File:** `.claude/skills/github-actions-devsecops.md`
**Created by:** Jade (based on Sasha + Alejo design)
**Effort:** 10 hours
**Timeline:** Week of April 22-26 (after architecture complete)
**Target audience:** Sasha (lead), Alejo (architecture), all developers (usage)
**Key topics:**
- GitHub Actions 2.0 features (egress firewall, cost optimization)
- IaC with Terraform/Pulumi + GitHub Actions
- SAST/DAST tools integration (security scanning)
- OWASP Top 10 automation (validation in CI/CD)
- Artifact caching & optimization
- Secrets management (best practices)
- Matrix builds (parallel testing)
- Custom actions (reusable workflows)
- Debugging workflows (tmate, logging)
- Cost optimization (new runner pricing 39% cheaper)

**Success criteria:**
- All PRs scanned for OWASP Top 10
- Deployment <30 minutes
- 0 failed production deployments due to infra
- GitHub Actions bill 30%+ lower than before

**Dependencies:** Alejo's architecture design must be done first

---

### TIER 2 — QUALITY & FRONTEND (Create mid-April)

#### 5. Vitest + Browser Mode Testing
**File:** `.claude/skills/vitest-browser-testing.md`
**Created by:** Jade (based on Brook's experience)
**Effort:** 15 hours
**Timeline:** Week of April 22-26 (parallel)
**Target audience:** Brook (lead), Erik (visual regression), all developers
**Key topics:**
- Jest → Vitest migration path
- Browser Mode (real Chromium, not jsdom)
- Visual regression testing (toMatchScreenshot)
- Performance assertions (measuring render time)
- Unit vs integration vs browser tests (when to use each)
- Mocking & stubbing in Vitest
- Coverage targets & enforcement
- Parallel test execution
- CI/CD integration with Vitest
- Debugging failing tests

**Success criteria:**
- Jest fully replaced by Vitest
- Test suite runs in 2-4 seconds (not 8-12)
- Visual regression tests pass for all UI changes
- 0 test flakiness in CI/CD

**Dependencies:** None (but GitHub Actions DevSecOps should be ready for CI/CD)

---

#### 6. Update "Web Builder" with Next.js 15 + Tailwind 4
**File:** `.claude/skills/web-builder-nextjs15.md` (update existing)
**Created by:** Jade (based on Erik's design)
**Effort:** 10 hours
**Timeline:** Week of April 22-26 (parallel)
**Target audience:** Brook (frontend), Erik (design), Cinthya (landing pages)
**Key topics:**
- Next.js 15 new features (app router maturity)
- React 19 optimizations (use/async, etc.)
- Tailwind CSS 4 (@theme directive, OKLCH colors)
- shadcn/ui latest components
- Design system setup (Figma → code)
- Performance optimization (image optimization, code splitting)
- Framer Motion animations (new features)
- SEO best practices with Next.js 15
- Deployment on Vercel (edge functions)
- TypeScript strict mode setup

**Success criteria:**
- All new projects use Next.js 15 stack
- Performance score >90 on Lighthouse
- Design system fully documented in Figma + codebase
- Zero design vs code discrepancies

**Dependencies:** None

---

### TIER 3 — SECURITY & OPTIMIZATION (Create late April)

#### 7. FastAPI Production Security Checklist
**File:** `.claude/skills/fastapi-production-security.md`
**Created by:** Jade (based on Sasha's audit)
**Effort:** 10 hours
**Timeline:** Week of April 29-May 3
**Target audience:** Sasha (primary), Alejo (architecture review), all backend developers
**Key topics:**
- OWASP Top 10 for APIs
- Authentication & authorization (JWT best practices)
- Input validation (Pydantic v2)
- HTTPS & TLS configuration
- CORS configuration (security vs functionality)
- Rate limiting & DDoS protection
- SQL injection prevention (Pydantic queries)
- Secrets management (environment variables)
- Error handling (don't leak sensitive info)
- Security headers (HSTS, CSP, etc.)
- Audit logging & monitoring
- Deployment security (containers, secrets, etc.)

**Success criteria:**
- All APIs pass OWASP checklist
- 0 security findings in audits
- Secrets never exposed in logs/errors
- Rate limiting prevents abuse

**Dependencies:** None

---

#### 8. Browser Automation with Chrome DevTools MCP
**File:** `.claude/skills/chrome-devtools-mcp.md`
**Created by:** Jade (based on Erik's testing)
**Effort:** 15 hours
**Timeline:** Week of April 29-May 3
**Target audience:** Erik (visual testing), Sasha (debugging/automation), Brook (e2e testing)
**Key topics:**
- Chrome DevTools MCP server setup
- Local automation (no network latency)
- Debugging remote browsers (VS Code integration)
- Performance profiling (CPU, memory, network)
- Visual testing & screenshots
- Network monitoring (requests, responses)
- Console logging & error catching
- Device emulation (mobile testing)
- MCP integration with Claude Code
- Examples: automated visual QA, debugging prod issues

**Success criteria:**
- Visual regression tests automated
- <1 second to debug remote browser issue
- Performance bottlenecks identified via MCP
- All UI changes have visual diffs

**Dependencies:** Vitest + Browser Mode skill (complementary)

---

#### 9. TDD & Code Coverage Enforcement
**File:** `.claude/skills/tdd-code-coverage.md`
**Created by:** Jade (based on Ego's metrics)
**Effort:** 10 hours
**Timeline:** Week of April 29-May 3
**Target audience:** Ego (enforcement), all developers (implementation), Jarvis (policy)
**Key topics:**
- TDD workflow (red-green-refactor)
- Unit vs integration test balance
- Coverage targets (80%+ for main branches)
- Mutation testing (code quality validation)
- Branch coverage (all code paths tested)
- Test naming conventions
- Test organization (AAA pattern)
- Continuous coverage tracking
- CI/CD gates (block merges below 80%)
- Code review checklist for tests

**Success criteria:**
- >80% code coverage on all main branches
- 0 bugs reported post-launch (tests catch them)
- Test review as strict as code review
- Team confident in refactoring (tests provide safety)

**Dependencies:** Vitest + Browser Mode skill

---

### TIER 4 — ADVANCED & REFERENCE (Create later)

#### 10. System Design Patterns for Agencia
**File:** `.claude/skills/system-design-patterns.md`
**Created by:** Alejo (with Jade's help)
**Effort:** 10 hours
**Timeline:** Early May (Alejo ownership)
**Target audience:** Alejo (mentoring), Jarvis (decisions), Sasha (architecture)
**Key topics:**
- Clean Architecture layers (entities, use cases, interface adapters)
- SOLID principles (dependency inversion, etc.)
- Design patterns (Factory, Strategy, Dependency Injection, etc.)
- Microservices vs monolith (when to use each)
- Event-driven architecture
- CQRS (command query responsibility segregation)
- Agent-based architecture patterns
- Scalability patterns (sharding, caching, async)
- Case studies: Uber, Netflix, Spotify scaling

**Success criteria:**
- All architecture decisions cited against patterns
- Alejo can mentor Sasha on pattern selection
- New projects follow established patterns
- Technical debt decisions documented vs patterns

**Dependencies:** None (reference material)

---

#### 11. Scalability & System Design for Agencia
**File:** `.claude/skills/scalability-system-design.md`
**Created by:** Alejo (with Jade's help)
**Effort:** 10 hours
**Timeline:** Early May (Alejo ownership)
**Target audience:** Jarvis (strategic), Alejo (architecture), Sasha (backend)
**Key topics:**
- Scaling databases (replication, sharding)
- Caching strategies (Redis, CDN, app-level)
- Load balancing (sticky sessions, etc.)
- Async processing (queues, background jobs)
- Monitoring & alerting (scale awareness)
- Cost optimization (scale efficiently)
- Case study: Scaling from 100 to 1M users
- Agent-based system scaling (10x/100x)

**Success criteria:**
- Architecture scales to 10x/100x user load
- Cost per user decreases with scale
- Monitoring catches bottlenecks early

**Dependencies:** System Design Patterns skill

---

#### 12. LangSmith Observability for Agent Auditing
**File:** `.claude/skills/langsmith-observability.md`
**Created by:** Jade (Q3, after LangGraph stable)
**Effort:** 15 hours
**Timeline:** July 2026 (Q3)
**Target audience:** Ego (metrics), Cinthya (workflows), Jarvis (dashboards)
**Key topics:**
- LangSmith setup & configuration
- Tracing agent workflows (step-by-step)
- Performance metrics (latency, token usage, cost)
- Debugging failed agent runs
- Feedback collection (improve agents over time)
- Dashboards for agent performance
- Cost tracking (per agent, per workflow)
- A/B testing workflows
- Privacy & data retention policies

**Success criteria:**
- All agents instrumented with LangSmith
- Ego generates weekly performance report
- Cost tracked per agent per project
- Bottlenecks visible in dashboards

**Dependencies:** LangGraph skill (must be stable first)

---

## SKILLS UPDATE SCHEDULE

### Week of April 8-12 (Week 2)
- ✅ Claude Agent SDK Multi-Agent Orchestration (Jade, 20h)

### Week of April 15-19 (Week 3)
- ✅ LangGraph Advanced Patterns (Jade, 15h)
- ✅ Supabase Production Patterns (Jade, 10h)

### Week of April 22-26 (Week 4)
- ✅ GitHub Actions 2.0 DevSecOps Pipeline (Jade, 10h)
- ✅ Vitest + Browser Mode Testing (Jade, 15h)
- ✅ Update "Web Builder" with Next.js 15 + Tailwind 4 (Jade, 10h)

### Week of April 29-May 3 (Week 5)
- ✅ FastAPI Production Security Checklist (Jade, 10h)
- ✅ Browser Automation with Chrome DevTools MCP (Jade, 15h)
- ✅ TDD & Code Coverage Enforcement (Jade, 10h)

### Early May (Alejo ownership)
- ✅ System Design Patterns for Agencia (Alejo, 10h)
- ✅ Scalability & System Design (Alejo, 10h)

### July 2026 (Q3, after LangGraph stable)
- ✅ LangSmith Observability for Agent Auditing (Jade, 15h)

---

## TOTAL EFFORT BREAKDOWN

| Phase | Skills | Hours | Owner |
|-------|--------|-------|-------|
| Week 2 (Apr 8-12) | 1 | 20h | Jade |
| Week 3 (Apr 15-19) | 2 | 25h | Jade |
| Week 4 (Apr 22-26) | 3 | 35h | Jade |
| Week 5 (Apr 29-May 3) | 3 | 35h | Jade |
| Early May | 2 | 20h | Alejo |
| July (Q3) | 1 | 15h | Jade |
| **TOTAL** | **12** | **150h** | **Jade + Alejo** |

**Jade's load:** 125 hours ≈ 6 weeks of full-time work (spread across 8 weeks = 75% utilization)
**Alejo's load:** 20 hours ≈ 1 week of work (after architecture design)

---

## SKILL TEMPLATE STRUCTURE

Each skill file should follow this structure:

```markdown
# SKILL: [Title]
## Owned by: [Agent name]
## Updated: [Date]

### Overview
[Brief description of what this skill covers]

### When to use this skill
[Scenarios where this skill is most relevant]

### Key concepts
- Concept 1: explanation
- Concept 2: explanation

### Implementation patterns
[Code examples, configuration, best practices]

### Common mistakes to avoid
[Pitfalls and how to prevent them]

### Integration with other skills
[How this skill works with other agent capabilities]

### References
[Links to official docs, research papers, etc.]

### Examples from Agencia projects
[Real-world usage in current projects]
```

---

## SUCCESS CRITERIA FOR ALL SKILLS

- [ ] Each skill is <5000 words (scannable by agents)
- [ ] Code examples are copy-paste ready
- [ ] Links to all 2026-current documentation
- [ ] Integrated into agent workflow (mentioned in @jade, @sasha, etc. prompts)
- [ ] Updated monthly by Jade (new docs, deprecations, best practices)
- [ ] Tested by target agent before full rollout

---

## OWNER & TIMELINE

**Primary owner:** Jade (Directora Intel & Capacitaciones)
**Secondary owner:** Alejo (for system design skills)
**Approval:** Jarvis

**Deliverable:** By end of May 2026, all 12 skills documented and team trained.

**Status:** 🟢 READY FOR CREATION SPRINT (April 8 start)

---

**Last updated:** April 5, 2026
**Next review:** April 8, 2026 (kickoff meeting)
