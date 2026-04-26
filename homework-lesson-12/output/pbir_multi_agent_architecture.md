# Integrating Agent-based Automation with PBIR Workflows — High-Level Product & Architecture Brief

## Executive Summary
This brief describes a high-level product and architecture plan for an LLM multi-agent system that can author, edit, validate, and publish Power BI reports stored in the PBIR (Power BI Enhanced Report) format. It covers: agent roles and capabilities, recommended orchestration patterns, technical integration points with Power BI (Desktop, Service/Fabric, REST & Git workflows), security and governance controls, CI/CD and validation practices for PBIR artifacts, end-to-end workflows (create/edit/inject DAX/promote), and a proposed technology stack and implementation roadmap with milestones.

Key design principles
- Treat PBIR artifacts as first-class, source-controlled JSON artifacts. All agent edits go through Git + CI gates; direct edits to live workspaces are gated and audited.
- Use a router/orchestrator agent that coordinates specialized subagents (authoring, DAX, QA/validation, publishing) to keep responsibilities small and auditable.
- Prefer tool-calls (PBIR CLI / pbir-utils / Power BI Desktop/Service APIs) to raw LLM suggestions: LLMs write suggested diffs/patches, but deterministic tools apply and validate them.
- Enforce least privilege: service principals with scoped permission, secrets managed in Key Vault/Secrets Manager, and immutable audit logs.
- Validate PBIR JSON semantics and business correctness in CI before merging/publishing.

---

## 1) PBIR format — authoritative reference & important facts
- PBIR (Power BI Enhanced Report Format) stores the report layer as a folder of JSON files: definition.pbir (report metadata), per-page and per-visual JSON files, plus optional reportExtensions.json (report-level extension measures and visual calculation placeholders). PBIR replaces the legacy single report.json representation and is designed to be source-control friendly.
- Key files and locations (typical):
  - <Report>.Report/definition/definition.pbir — core metadata and dataset reference.
  - <Report>.Report/definition/reportExtensions.json — optional; contains report-layer DAX extension measures. Must be removed entirely if empty to avoid deserialization issues.
  - pages/ and per-visual files — each page, visual, and bookmark is a separate JSON file enabling small diffs.
  - .pbi/localSettings.json — local settings (should be gitignored).
- PBIR tooling and ecosystem:
  - Power BI Desktop Projects (PBIP) implements PBIR; Desktop validates PBIR on open.
  - PBIR schemas live as schema URLs inside JSON files and are used for schema validation.
  - Community/third-party tooling (e.g., pbir-utils) offers sanitize, validate, extract, visualize, and CI helper commands. Use them as deterministic tools invoked by agents rather than relying solely on LLM edits.

Notable behaviors & limitations
- reportExtensions.json is optional but brittle: leaving an empty skeleton can cause deserialization failures. When moving extension measures to the model, delete reportExtensions.json and update references.
- During preview/transition some REST/export flows may still use legacy representation; design to detect exported format and convert via tooling or Desktop automation.
- Power BI Desktop validation is authoritative: agents should validate locally using pbir-utils and, when necessary, a controlled Desktop runner.

Sources (selected)
- Microsoft Docs: Create a Power BI report in enhanced report format (PBIR)
- Microsoft Docs: Power BI Desktop project report folder (files & subfolders)
- GitHub: powerbi-desktop-samples — definition.pbir schema
- pbir-utils (third-party/community) CLI & docs

---

## 2) Best practice patterns for LLM multi-agent systems
Patterns to adopt
- Router + specialized subagents: a Router/Orchestrator classifies requests and dispatches specialized agents (Authoring, DAX Author, PBIR Validator, CI/CD Agent, Publishing Agent, Security/Audit Agent).
- Skills & tools: expose deterministic functions as tools (pbir-utils CLI, git, REST APIs) that agents can call.
- RAG for knowledge & policies: index internal policies, naming conventions, approved DAX snippets, and dataset catalogs for retrieval.
- Handoffs & transactionality: represent in-progress changes as feature branches and PRs; every agent action produces an auditable artifact.
- Parallelization where safe: allow parallel authoring for disjoint pages; serialize merges and rely on CI validations.

Tradeoffs
- More agents = clearer separation of concerns but higher orchestration cost and latency. Use caching and deterministic tooling to reduce repeated LLM calls.
- Keep side-effecting operations outside of LLMs (use tools) to reduce risk.

---

## 3) Integration points with Power BI & Fabric
Primary integration surfaces
- Power BI Desktop (Projects / PBIP): authoritative for PBIR creation/conversion and validation.
- PBIR filesystem (Git repo): store PBIR folders in Git; agents operate on these files and create PRs.
- Power BI / Fabric REST APIs: publish, import, and manage reports in workspaces.
- Fabric Git Integration: workspace ↔ Git synchronization (where available).
- Embedding APIs: for post-publish embedding/token flows.
- Semantic model artifacts (TMDL, modelReference.json): maintain consistency when agents alter dataset references.

Practical guidance
- Prefer editing PBIR in Git with CI validation; only publish after CI passes.
- Use pbir-utils (third-party/community) for deterministic operations (sanitize, validate). 
- Orchestrate Desktop conversions via secure Windows runners when necessary.

---

## 4) Security & governance for automated editing
Principles
- Least privilege and scoped credentials: use service principals/managed identities with minimal permissions.
- Secrets & key management: central secret store with short-lived credentials (Azure Key Vault / HashiCorp Vault).
- Auditability & immutable logs: log every agent action with prompts/response hashes, diffs, and commit IDs.
- CI gates & review policies: require automated validations plus human sign-off for high-risk changes.
- Static & dynamic validation: combine schema validation with dynamic tests (preview screenshots, sample dataset refresh, DAX tests).
- Sandboxing & safe rollout: deploy to a sandbox workspace for review before production promotion.
- Change signing & artifact integrity: CI signs artifacts; publishing agent verifies signatures before deploy.

Attack surface & mitigations
- Malicious LLM output: block direct LLM-executed side effects; validate all outputs with deterministic validators.
- Corrupt PBIR edits: run schema validation and Desktop open checks; maintain automated rollbacks.
- Credential compromise: use short-lived tokens, rotation, and anomaly monitoring.

---

## 5) CI/CD patterns for PBIR in Git
Repository layout & branching
- Typical structure: src/<ReportName>.Report/definition + pages + resources, with pbir config at repo root.
- Branching: feature branches per change; agents always create PRs with rationale and validations.

Pipeline stages
1. Pre-apply checks (local): LLM produces diffs; agent runs local deterministic checks (JSON schema, pbir-utils sanitize/validate).
2. CI validation on PR: schema checks, linting, DAX static checks, behavioral tests (render previews) and performance checks where feasible.
3. Policy checks & gating: dataset swaps or model changes require approvers.
4. Merge & release: merge triggers publish to sandbox, smoke tests, and after approval promotion to production.
5. Post-publish verification & audit: run telemetry checks and persist logs.

Tools
- CI runners: GitHub Actions / Azure DevOps / self-hosted Windows runners.
- Validation tools: pbir-utils (third-party/community), DAX linters, JSON schema validators.
- Signing: Git commit signing or signed release blobs via pipeline.

---

## 6) Workflows (create, edit, inject DAX, promote)
Actors (agents): Router/Orchestrator, Authoring Agent, DAX Agent, PBIR Validator Agent, Git/CI Agent, Publishing Agent, Security/Policy Agent.

Workflows (high-level)
A) Create a new report
1. User intent submitted.
2. Router fetches dataset metadata.
3. Authoring Agent generates report skeleton or PBIR fragments.
4. DAX Agent generates measures.
5. PBIR Validator runs (pbir-utils, desktop validation).
6. Git/CI Agent creates PR with diffs and rationale.
7. CI runs full validation. If approved, Publishing Agent deploys to sandbox then production.

B) Edit existing report (small visual change)
1. Router classifies request and identifies files.
2. Authoring Agent generates minimal change.
3. PBIR Validator runs.
4. Git/CI Agent makes PR; CI validates and reviewer approves; publish.

C) Inject or modify DAX
1. Router invokes DAX Agent with model context.
2. DAX Agent creates candidate DAX plus complexity estimate.
3. Run DAX static analysis/unit tests; recommend model migration if re-usable.
4. PBIR Validator ensures validity; high-risk model migrations require human approval.

D) Promote to production
- Merge to main and CI success triggers Publishing Agent which verifies signatures, publishes to sandbox, runs smoke tests and promotes to production after approvals.

---

## 7) Recommended tech stack & communication patterns
LLM & orchestration
- LLM models: enterprise-grade provided models (e.g., OpenAI/Anthropic/enterprise LLM) or on-prem alternatives for sensitive data.
- Agent framework: LangChain or AutoGen for modular agents and tool invocation.

PBIR tooling & integration
- pbir-utils (third-party/community) CLI for sanitize/validate/extract/visualize.
- Power BI Desktop automation for conversions/validation in Windows runners.
- Power BI / Fabric REST APIs & Fabric Git Integration for publishing.

CI/CD & Git
- Git provider: GitHub / Azure DevOps.
- CI runners: GitHub Actions, Azure DevOps, self-hosted Windows runners for Desktop automation.
- Artifact signing: pipeline-based signing (sigstore/GPG/Git commit signing).

Security & infra
- Secrets: Azure Key Vault / HashiCorp Vault.
- Identity: Azure AD app registrations / managed identities.
- Networking: secure VNet isolation for runners; restrict egress.
- Monitoring: Azure Monitor / Log Analytics / SIEM.

Data & knowledge
- RAG index store: vector DB (Azure Cognitive Search, Pinecone, Milvus) for policies and dataset catalogs.
- Metadata catalog: a service that exposes dataset schema & table names to agents.

Messaging & orchestration
- Orchestration: Router agent for sync flows; message broker (Azure Service Bus / RabbitMQ) for async jobs (rendering, Desktop conversions).

---

## 8) Implementation roadmap & milestones (6–12 months)
Phase 0: Discovery & safe prototyping (2–4 weeks)
- Inventory reports; PoC where LLM generates single visual JSON file; run pbir-utils validate locally.

Phase 1: PBIR tooling & deterministic pipeline (4–8 weeks)
- Integrate pbir-utils CLI into CI; create pbir-sanitize.yaml and pbir-rules.yaml; implement PBIR Validator Agent.

Phase 2: DAX authoring & test harness (6–10 weeks)
- Build DAX Agent with static checks and unit test harness.

Phase 3: Multi-agent orchestration & RAG (6–8 weeks)
- Implement Router + specialized agents; add RAG index for policies and dataset catalog.

Phase 4: Desktop automation & preview (6–10 weeks)
- Secure Windows runner for Desktop conversions and render previews.

Phase 5: Publish automation & governance (6–8 weeks)
- Implement Publishing Agent, artifact signing, policy workflows, and full audit logging.

Phase 6: Canary & roll-out (4–8 weeks)
- Start with limited reports/teams; collect metrics and iterate.

Phase 7: Scale & harden (ongoing)
- Optimize performance, RAG indexing, and fine-tune prompts or models if allowed.

---

## 9) Operational metrics & KPIs
- CI pass rate for agent PRs (goal > 95%)
- % automated edits vs manual edits
- Mean time to incorporate agent suggestion (MTTI)
- Validation failures per 100 PRs
- Audit trail completeness
- Rollback/publish failures (target: zero unplanned production rollbacks)

---

## 10) Practical recommendations
- Start conservative: agents propose PRs; humans approve production deploys initially.
- Keep pbir-utils and Desktop validation as authoritative validators.
- Build deterministic functions (apply_diff, run_validate, generate_preview) and have agents call them.
- Maintain human-in-the-loop for high-risk DAX/model changes.

---

## Appendix A — Example agent responsibilities (concise)
- Router/Orchestrator Agent: Accepts user intent, classifies request, orchestrates subagents, invokes security checks.
- Authoring Agent (Report Builder): Produces PBIR fragments (visual JSON, page scaffolding) using dataset metadata and style guidelines.
- DAX Agent (Calc Author): Generates DAX, runs static analysis and unit tests, recommends model migration where appropriate.
- PBIR Validator Agent: Runs JSON schema checks, pbir-utils sanitize/validate, and Desktop open checks producing validation reports.
- Git/CI Agent: Creates branch/PR, populates PR metadata with LLM rationale & references, ensures pipeline triggers and collects validation artifacts.
- Publishing Agent: Verifies artifact signatures, publishes to sandbox and production workspaces via REST/Git Integration, records audit logs.
- Security/Policy Agent: Enforces naming, data sensitivity, external connection rules, and blocks/flags risky changes for human review.

---

## Appendix B — Sample PBIR folder map
A concise example of a PBIR project folder structure used by agents, CI/CD, and developers. Each line is a file or folder you typically see in a PBIR-driven workflow.

/project-root/
- README.md
- pbir.yaml               # project-level PBIR config (build rules, metadata)
- /data/
- data-sources.yaml       # definitions for Ingest Agent
- /m_queries/
- 01_Customers.m
- 02_Sales.m
- /model/
- model.json              # serialized model definition (tables, relationships)
- measures.dax            # centralized DAX measures and measure templates
- /reports/
- sales_report.pbir       # report artifact (PBIR format)
- /visuals/
- custom_visuals/         # packaged custom visuals used by the report
- /ci/
- pipeline.yml            # CI pipeline invoking pbir-utils (validate/sanitize) and agents
- /scripts/
- extract_metadata.py     # helper scripts that call pbir-utils or agents
- /docs/
- validation_rules.yaml   # QA rules consumed by Validation Agent

---

## Sources & References
- Microsoft Learn: Create a Power BI report in enhanced report format (PBIR)
- Microsoft Learn: Power BI Desktop project report folder (files & subfolders)
- GitHub: powerbi-desktop-samples — definition.pbir schema
- pbir-utils (third-party/community) — GitHub & docs



