# Tech Adoption Matrix 2026
## Matriz Operacional de Adopción Tecnológica para la Agencia

---

## 1. ORQUESTACIÓN & AGENTES

### Claude Agent SDK (Anthropic)
| Aspecto | Detalle |
|--------|---------|
| **Repo** | Anthropic/Claude Agent SDK |
| **¿Qué es?** | SDK oficial de Anthropic para construir agentes con tool-use nativo, MCP integration, multi-agent coordination |
| **¿Por qué ahora?** | 2026 — año de agentes autónomos; Anthropic mató competidores; es el default |
| **Agente lead** | Jade (investigación + skill) |
| **Agentes que lo usan** | TODOS — especialmente Cinthya, Sasha, Brook |
| **Beneficiarios directos** | Jarvis (coordina agentes), Cinthya (workflows), Jade (capacitación) |
| **Timeline** | 4 semanas (investigación + skill + capacitación) |
| **Inversión** | Jade 20h + Cinthya 40h = 1.5 semanas de trabajo |
| **Skills creadas** | "Claude Agent SDK Multi-Agent Orchestration" |
| **Conflicto con** | Nada — complementa a LangGraph |
| **Métricas de éxito** | Todos los agentes pueden invocar sub-agentes en paralelo; reducción de manual coordination |

### LangGraph (LangChain)
| Aspecto | Detalle |
|--------|---------|
| **Repo** | langchain-ai/langgraph |
| **¿Qué es?** | Framework de bajo nivel para stateful agents con checkpoints, observability (LangSmith), streaming |
| **¿Por qué ahora?** | 27.1k búsquedas mensuales (highest adoption); production-ready; mejor que CrewAI para workflows complejos |
| **Agente lead** | Cinthya (implementación) |
| **Agentes que lo usan** | Cinthya (n8n → LangGraph migration), Sasha (backend agents) |
| **Beneficiarios directos** | Cinthya (workflows reutilizables), Jarvis (observability) |
| **Timeline** | 4 semanas (después de Claude SDK learning) |
| **Inversión** | Cinthya 50h (hands-on); Jade 15h (research) = 2 semanas |
| **Skills creadas** | "LangGraph Advanced Patterns" — checkpoints, memory, routing |
| **Conflicto con** | Complementa a Claude SDK; no conflict |
| **Métricas de éxito** | 50% más workflows automatizados; 80% code reuse en agents |

### n8n 2.0 + Awesome Templates
| Aspecto | Detalle |
|--------|---------|
| **Repo** | n8n-io/n8n + enescingoz/awesome-n8n-templates |
| **¿Qué es?** | Workflow automation platform (fair-code); 280+ community templates; native AI + LangChain |
| **¿Por qué ahora?** | Ya lo usa Cinthya; v2.0 (Dec 2025) mejoró AI agent node; 182.4k stars |
| **Agente lead** | Cinthya (experta) |
| **Agentes que lo usan** | Cinthya (workflows), Jade (automation), Sasha (alerts) |
| **Beneficiarios directos** | Cinthya (acelera builds), equipo (menos manual tasks) |
| **Timeline** | Immediate — update n8n skill con v2.0 features |
| **Inversión** | Jade 10h (update skill); Cinthya 5h (testing) = 0.5 semanas |
| **Skills creadas** | Update "n8n Expert" skill con new v2.0 AI node features |
| **Conflicto con** | Nada — complementa a LangGraph (n8n vs code-based workflows) |
| **Métricas de éxito** | 100% de reportes weekly automatizados; <5min para crear nuevo workflow |

---

## 2. TESTING & QUALITY ASSURANCE

### Vitest + Browser Mode
| Aspecto | Detalle |
|--------|---------|
| **Repo** | vitest-dev/vitest |
| **¿Qué es?** | Test runner 3-5x más rápido que Jest; Browser Mode (real Chromium); visual regression |
| **¿Por qué ahora?** | 14M descargas/semana (crecimiento 350% YoY); Jest estancado; Vitest es now |
| **Agente lead** | Brook (lead), Jade (capacitación) |
| **Agentes que lo usan** | Brook (testing), Erik (visual regression), Sasha (integration tests) |
| **Beneficiarios directos** | Brook (3-5x más rápido), equipo (feedback loop) |
| **Timeline** | 3 semanas (migración gradual) |
| **Inversión** | Brook 40h (migration) + Erik 20h (visual tests) + Jade 15h = 1.75 semanas |
| **Skills creadas** | Update "Web Builder" skill with Vitest + visual testing |
| **Conflicto con** | Reemplaza Jest completamente (no breaking change si migran bien) |
| **Métricas de éxito** | Jest → Vitest migration complete; 2-4 sec test suite (vs 8-12 sec); 0 test failures |

### Testing Best Practices (TDD)
| Aspecto | Detalle |
|--------|---------|
| **Repo** | ComposioHQ/test-driven-development skill |
| **¿Qué es?** | Skill para TDD patterns, coverage targets, mutation testing |
| **¿Por qué ahora?** | Ego necesita métricas; no hay TDD enforced actualmente |
| **Agente lead** | Jade (skill research), Ego (enforcement) |
| **Agentes que lo usan** | Sasha, Brook, Erik (everyone writing code) |
| **Beneficiadores directos** | Ego (audit coverage), Jarvis (quality gate) |
| **Timeline** | 2 semanas (skill + policy setup) |
| **Inversión** | Jade 15h + Ego 10h = 1 semana |
| **Skills creadas** | "Test-Driven Development for the Agencia" — coverage targets, CI checks |
| **Conflicto con** | Nada — complementa Vitest |
| **Métricas de éxito** | >80% code coverage on all main branches; 0 bugs reported post-launch |

---

## 3. SECURITY & INFRASTRUCTURE

### GitHub Actions 2.0 + DevSecOps
| Aspecto | Detalle |
|--------|---------|
| **Repo** | GitHub Actions documentation + DevSecOps IaC patterns |
| **¿Qué es?** | Modernizado CI/CD con egress firewall, Kubernetes ARC, 39% cheaper runners |
| **¿Por qué ahora?** | 2026 DevSecOps is mandatory; GitHub reduced costs; security-by-default |
| **Agente lead** | Sasha (lead), Alejo (architecture), Cinthya (automation) |
| **Agentes que lo usan** | Sasha (security scanning), Alejo (IaC), Jarvis (deployments) |
| **Beneficiadores directos** | Sasha (automate OWASP), Jarvis (40% faster deployments) |
| **Timeline** | 4 semanas (design + implementation) |
| **Inversión** | Sasha 60h + Alejo 30h + Cinthya 20h = 2.75 semanas |
| **Skills creadas** | "GitHub Actions 2.0 DevSecOps Pipeline" — SAST, DAST, IaC |
| **Conflicto con** | Deprecates manual deployments (intentional) |
| **Métricas de éxito** | 100% of PRs scanned for OWASP; <30 min to production; 0 infra incidents |

### FastAPI Security Checklist
| Aspecto | Detalle |
|--------|---------|
| **Repo** | VolkanSah/Securing-FastAPI-Applications |
| **¿Qué es?** | Complete guide to FastAPI security: auth, validation, HTTPS, secrets management |
| **¿Por qué ahora?** | Sasha builds APIs; OWASP Top 10 compliance is now mandatory |
| **Agente lead** | Sasha (lead), Jade (skill creation) |
| **Agentes que lo usan** | Sasha (all APIs), Alejo (architecture review) |
| **Beneficiadores directos** | Sasha (production-ready APIs), Alejo (security audit) |
| **Timeline** | 2 semanas (audit + skill) |
| **Inversión** | Sasha 20h + Jade 15h = 1.75 semanas |
| **Skills creadas** | "FastAPI Production Security Checklist" — JWT, validation, CORS, secrets |
| **Conflicto con** | Nada — complementa FastAPI Expert skill |
| **Métricas de éxito** | All APIs pass OWASP checklist; 0 security findings in audits |

### Supabase RLS Best Practices
| Aspecto | Detalle |
|--------|---------|
| **Repo** | makerkit.dev/tutorials + supabase/realtime |
| **¿Qué es?** | Deep dive on Row Level Security; indexing strategies; 100x performance gains |
| **¿Por qué ahora?** | Brook complaints about slow dashboards; Sasha not optimizing indexes |
| **Agente lead** | Sasha (audit + optimization), Jade (skill) |
| **Agentes que lo usan** | Sasha, Brook (all queries), Alejo (performance) |
| **Beneficiadores directos** | Brook (100x faster dashboards), Alejo (cost savings) |
| **Timeline** | 2 semanas (audit + optimization) |
| **Inversión** | Sasha 20h + Jade 10h = 1.5 semanas |
| **Skills creadas** | "Supabase Production Patterns" — RLS, indexes, Realtime, edge functions |
| **Conflicto con** | Nada — improves existing Supabase Complete skill |
| **Métricas de éxito** | All queries <100ms; Realtime events <50ms; 0 N+1 queries |

---

## 4. FRONTEND & DESIGN

### Next.js 15 + Tailwind 4 + shadcn/ui
| Aspecto | Detalle |
|--------|---------|
| **Repo** | vercel/next.js + tailwindlabs/tailwindcss + shadcn/ui |
| **¿Qué es?** | Modern web stack: React 19, Tailwind 4 (@theme), shadcn/ui components + OKLCH colors |
| **¿Por qué ahora?** | 2026 standard; Tailwind 4 released; React 19 optimizations; shadcn/ui updated |
| **Agente lead** | Erik (lead), Brook (implementation) |
| **Agentes que lo usan** | Erik (design), Brook (frontend), Cinthya (landing pages) |
| **Beneficiadores directos** | Erik (better design systems), Brook (faster development) |
| **Timeline** | 2 weeks (adoption) |
| **Inversión** | Erik 20h + Brook 20h + Jade 10h (skill) = 1.5 semanas |
| **Skills creadas** | Update "Web Builder" skill with Next.js 15 + React 19 + Tailwind 4 |
| **Conflicto con** | Replaces older Next.js + Tailwind 3 (gradual migration OK) |
| **Métricas de éxito** | All new projects use Next.js 15; Tailwind 4 via @theme; shadcn/ui latest |

### Chrome DevTools MCP
| Aspecto | Detalle |
|--------|---------|
| **Repo** | ChromeDevTools/chrome-devtools-mcp |
| **¿Qué es?** | MCP server for Chrome DevTools automation; debugging, performance analysis, visual testing |
| **¿Por qué ahora?** | Erik needs visual regression; Sasha needs remote debugging; available now |
| **Agente lead** | Erik (visual testing), Sasha (debugging) |
| **Agentes que lo usan** | Erik (design QA), Sasha (integration testing), Brook (e2e) |
| **Beneficiadores directos** | Erik (automated visual QA), Sasha (faster debugging) |
| **Timeline** | 2 weeks (skill + adoption) |
| **Inversión** | Jade 15h (skill) + Erik 10h (integration) = 1.25 semanas |
| **Skills creadas** | "Browser Automation with Chrome DevTools MCP" — visual testing, debugging, perf |
| **Conflicto con** | Nada — complementa Vitest Browser Mode |
| **Métricas de éxito** | Visual regression tests automated; <1 sec to debug remote issue |

---

## 5. ARCHITECTURE & SYSTEM DESIGN

### Awesome Design Patterns
| Aspecto | Detalle |
|--------|---------|
| **Repo** | DovAmir/awesome-design-patterns |
| **¿Qué es?** | Curated list of software + architecture patterns; Clean Architecture, SOLID, agent patterns |
| **¿Por qué ahora?** | Alejo needs reference; Jade needs to educate team on patterns; 47.6k stars |
| **Agente lead** | Alejo (owner), Jade (teaching) |
| **Agentes que lo usan** | Alejo (architecture decisions), Sasha, Brook, Erik (implementation) |
| **Beneficiadores directos** | Alejo (design decisions), Jade (teaching material) |
| **Timeline** | Immediate — reference material (not code adoption) |
| **Inversión** | Jade 5h (summary) = 0.25 semanas |
| **Skills creadas** | "System Design Patterns for the Agencia" (Alejo writes this) |
| **Conflicto con** | Nada — reference only |
| **Métricas de éxito** | All architecture decisions documented using patterns; Alejo can cite precedent |

### System Design Primer
| Aspecto | Detalle |
|--------|---------|
| **Repo** | donnemartin/system-design-primer |
| **¿Qué es?** | Learn system design; scalability patterns, case studies (Uber scaling to 2000 engineers) |
| **¿Por qué ahora?** | Alejo needs this for mentoring; Jarvis needs for 10x/100x scalability decisions |
| **Agente lead** | Alejo (owner), Jade (teaching) |
| **Agentes que lo usan** | Alejo (architecture), Jarvis (strategic decisions), Sasha (backend design) |
| **Beneficiadores directos** | Alejo (mentoring), Jarvis (scalability planning) |
| **Timeline** | Ongoing reference |
| **Inversión** | Jade 5h (summary for Alejo) = 0.25 semanas |
| **Skills creadas** | "Scalability & System Design for Agencia" (Alejo writes this) |
| **Conflicto con** | Nada — reference |
| **Métricas de éxito** | All architecture decisions scale to 10x/100x; documented |

---

## 6. MONITORING & OBSERVABILITY (FUTURE)

### LangSmith (Observability for LangGraph)
| Aspecto | Detalle |
|--------|---------|
| **Repo** | langchain-ai/langsmith |
| **¿Qué es?** | Production monitoring for LangGraph agents; traces, logs, performance metrics |
| **¿Por qué ahora?** | After LangGraph adoption; Ego needs metrics on agent performance |
| **Agente lead** | Ego (metrics owner), Cinthya (integration) |
| **Agentes que lo usan** | Cinthya (LangGraph workflows), Sasha (backend agents), Jarvis (dashboards) |
| **Beneficiadores directos** | Ego (audit metrics), Jarvis (performance tracking) |
| **Timeline** | 3 weeks (after LangGraph stabilizes) |
| **Inversión** | Cinthya 20h + Ego 15h = 1.75 semanas |
| **Skills creadas** | "LangSmith Observability for Agent Auditing" |
| **Conflicto con** | Nada — depends on LangGraph adoption first |
| **Métricas de éxito** | All agents have traces in LangSmith; Ego generates weekly performance report |

---

## 7. HIRING & ORGANIZATIONAL

### Sub-Agente de DevOps (NEW)
| Aspecto | Detalle |
|--------|---------|
| **Role** | DevOps Engineer / Sub-Agente Infrastructure |
| **Reports to** | Jarvis (CEO) |
| **Responsibilities** | CI/CD, IaC (Terraform), GitHub Actions, cloud optimization, deployments |
| **Why now?** | Alejo bottleneck; infrastructure growing; need dedicated role |
| **Timeline** | Hiring start: June 2026; onboard: July 2026 |
| **Investment** | $3-5k/month (FTE) or $2k/month (sub-agente model) |
| **ROI** | Sasha freed up 40% (backend features); Alejo 30% (architecture); faster deploys |
| **Conflict** | None — frees up time for others |
| **Success metrics** | <30 min deployments; 99.9% uptime; IaC fully versioned |

---

## 8. PRIORITY MATRIX: ADOPT NOW vs LATER

### ADOPT NOW (Q2 2026 — April to June)
1. **Vitest + Browser Mode** — 3 weeks, 3-5x impact immediately
2. **GitHub Actions 2.0 DevSecOps** — 4 weeks, critical security
3. **Supabase RLS Optimization** — 2 weeks, 100x performance
4. **Claude Agent SDK** — 4 weeks, foundational for all agents
5. **Next.js 15 + Tailwind 4** — 2 weeks, design system
6. **LangGraph** — 4 weeks (after Claude SDK), replaces manual coordination

### ADOPT Q3 (July-September)
1. **LangSmith** — after LangGraph is stable
2. **Chrome DevTools MCP** — after Vitest + Browser Mode
3. **FastAPI Security Checklist** — as part of ongoing audits
4. **Sub-Agente DevOps** — if budget approved

### MONITOR (Keep an eye on)
1. **CrewAI** — simpler than LangGraph, might fit some use cases
2. **OpenClaw** — viral (210k+ stars); evaluate if relevant
3. **Langflow** — low-code visual builder; Cinthya could delegate to this

---

## DECISION SPREADSHEET FOR JARVIS

| Tech | Priority | Timeline | Invest (h) | Lead | Decision | Budget | Go/No-Go |
|------|----------|----------|-----------|------|----------|--------|----------|
| Claude Agent SDK | P1-Critical | 4w | 60h | Jade | Adopt | Time only | GO |
| LangGraph | P1-Critical | 4w | 70h | Cinthya | Adopt | Time only | GO |
| Vitest + Browser Mode | P1-High | 3w | 75h | Brook | Adopt | Time only | GO |
| GitHub Actions 2.0 | P1-High | 4w | 110h | Sasha + Alejo | Adopt | ~$500 (runners) | GO |
| Supabase RLS | P1-High | 2w | 30h | Sasha | Adopt | Time only | GO |
| Next.js 15 + Tailwind 4 | P2-Medium | 2w | 50h | Erik + Brook | Adopt | Time only | GO |
| FastAPI Security | P2-Medium | 2w | 35h | Sasha | Adopt | Time only | GO |
| Chrome DevTools MCP | P2-Medium | 2w | 25h | Erik | Adopt | Time only | GO |
| LangSmith | P3-Future | 3w (Q3) | 35h | Cinthya | Evaluate Q3 | TBD | HOLD |
| Sub-Agente DevOps | P2-High | Hiring Q2 | N/A | Jarvis | Propose to JC | $3-5k/mo | ASK JC |
| Design Patterns Skill | P3-Reference | 0.5w | 10h | Alejo + Jade | Create | Time only | GO |

---

## SUMMARY: WHO DOES WHAT, WHEN

### **Jade (Directora Intel & Capacitaciones) — 95 hours**
- Claude Agent SDK research + skill (20h)
- LangGraph research (15h)
- Update n8n Expert skill (10h)
- Update Web Builder skill (10h)
- Supabase Production Patterns skill (10h)
- FastAPI Security skill (10h)
- Chrome DevTools MCP skill (15h)
- Timeline: 4-5 semanas

### **Sasha (Backend & Security) — 145 hours**
- GitHub Actions 2.0 + OWASP automation (60h)
- Supabase RLS audit + optimization (20h)
- FastAPI security audit (20h)
- LangGraph integration testing (20h)
- Chrome DevTools MCP integration (5h)
- Timeline: 5-6 semanas

### **Brook (Frontend & BD) — 90 hours**
- Vitest + Browser Mode migration (40h)
- Next.js 15 + Tailwind 4 adoption (20h)
- Web Builder skill testing (10h)
- LangGraph frontend integration (10h)
- FastAPI API testing (10h)
- Timeline: 4-5 semanas

### **Erik (Design) — 50 hours**
- Vitest visual regression setup (20h)
- Next.js 15 + Tailwind 4 design system (20h)
- Chrome DevTools MCP visual testing (10h)
- Timeline: 2-3 semanas

### **Cinthya (Automation) — 75 hours**
- Claude Agent SDK learning (20h)
- LangGraph advanced patterns (50h)
- n8n v2.0 testing (5h)
- Timeline: 3-4 semanas

### **Alejo (Architect) — 60 hours**
- GitHub Actions 2.0 architecture design (30h)
- Supabase performance architecture (10h)
- System Design Patterns skill (10h)
- LangGraph architecture decisions (10h)
- Timeline: 2-3 semanas

### **Ego (Auditor) — 30 hours**
- TDD enforcement + metrics (15h)
- Security scanning validation (10h)
- Agent performance tracking setup (5h)
- Timeline: 2 weeks

### **Jarvis (CEO) — Decisions Only**
- Approve/reject each technology
- Budget decisions
- Hiring decisions

---

## ESTIMATED TOTAL EFFORT

| Phase | Hours | Weeks | Team members |
|-------|-------|-------|--------------|
| Q2 2026 (April-June) | 545h | 11 weeks | All except Ego (20h only) |
| Q3 2026 (July-Sept) | 35h (LangSmith) | 3 weeks | Cinthya + Ego |
| **Total** | **580h** | **14 weeks** | **Distributed** |

**Per person (average):** 73 hours = ~3.5 weeks of full-time work across Q2 + Q3.

**Reality check:** 545h ÷ 6 people = 91h per person if evenly distributed ≈ 4.5 weeks.
**But workload isn't even:** Sasha (145h), Brook (90h), Cinthya (75h), Jade (95h) carry the load.

---

**Owner:** Jarvis (CEO)
**Status:** Ready for Saturday Board Meeting (April 12)
**Last updated:** April 5, 2026
