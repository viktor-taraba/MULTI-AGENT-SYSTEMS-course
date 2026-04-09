Звіт: Автоматизація розробки візуального шару Power BI за допомогою PBIR

# Automating Power BI Visual-Layer Development via PBIR — Revised

## Executive summary

This revised report expands and hardens the original plan to design, implement, and validate a 3-agent LLM system (Business Analyst, Developer, Reviewer) that automates Power BI visual-layer edits using PBIR (Power BI Enhanced Report format). It adds canonical Microsoft documentation links, a representative PBIR schema excerpt with an annotated example visual JSON, formalized message and envelope JSON Schema, concrete PBIR diffs (JSON Patch + git unified diff), CI/security guidance, updated system prompts, validation pseudo-code, and a Reviewer verification checklist with commands.

Key new items in this revision:
- Canonical Microsoft Learn PBIR docs and Power BI blog links (inline and in Sources)
- Representative PBIR visual schema fragment and annotated visual.json example
- JSON Patch and git unified diff for a sample change, with before/after files and validation steps
- Formal JSON Schema for the inter-agent message envelope with two complete message examples (BA→Dev, Dev→Reviewer)
- Security & CI/CD section with tenant preview settings, least-privilege guidance, audit and gating workflow
- Updated system prompts (BA, Dev, Reviewer) that reference message schema field names and require JSON-schema-compliant outputs
- Reviewer checklist and verification commands

Estimated implementation/test effort: 49–72 hours (unchanged). See Time & Effort section for breakdown.

---

## Table of contents

1. Background & scope
2. Sources & references (canonical Microsoft links + tools)
3. PBIR quick reference and canonical links (inline citations)
4. PBIR format deep-dive: schema excerpt and annotated visual.json example
5. Tooling & automation landscape (with links)
6. Power BI visual-layer & semantic-model constraints (inline MS doc citations)
7. Agent architecture & communication protocol
8. Formal message envelope: JSON Schema and sample messages
9. System prompts: BA, Developer, Reviewer (updated with message schema)
10. PBIR diff example (JSON Patch + git diff) and validation steps
11. Security & CI/CD: preview settings, permissions, gating, audit, tests
12. Prompt modularity patterns and validation pseudo-code
13. Evaluation framework, test-suite & representative testcases
14. Failure modes & mitigations
15. End‑to‑end worked example (BA → Dev → Reviewer) including diffs and patch application commands
16. Reviewer verification checklist (commands)
17. Recommendations & next steps
18. Appendices
    A. Raw prompt templates (full)
    B. PBIR schema fragment (representative)
    C. Example CLI commands and script skeletons

---

## 1. Background & scope

Goal: design and validate system prompts, message envelope, and testable automation for a 3-agent LLM orchestration that edits PBIR files to implement visual-layer changes while preserving model integrity and safety.

Assumptions and scope (unchanged):
- PBIR-enabled reports in a directory structure (definition/ with report.json, pages/, visuals/) are the automation target.
- Edits are limited to visual/page metadata and bindings; major semantic-model (TMDL/DAX) edits are out of scope unless explicitly authorized.
- This deliverable focuses on design artifacts, templates, and test artifacts engineers will run; it does not run or modify real reports.

---

## 2. Sources & references (canonical Microsoft links and tools)

Minimum canonical Microsoft references (required):

- Microsoft Learn — "Create a Power BI report in enhanced report format (PBIR)" — https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format
  - Inline references below point to this page for enabling PBIR in Power BI Desktop and for the overall PBIR description.

- Microsoft Power BI Blog (main page) — for announcements and rollout posts: https://powerbi.microsoft.com/en-us/blog/
  - Look up PBIR rollout or "enhanced report format" articles there; the blog index is the official channel for feature announcements.

- Microsoft Power BI developer documentation (root) — https://learn.microsoft.com/en-us/power-bi/developer/
  - Use this for SDK references, REST API docs, and related schema links.

PBIR-related example repos and tooling (authoritative community resources referenced in the report):

- PBIR-Utils (akhilannan): https://github.com/akhilannan/PBIR-Utils
- Example PBIR demo project (t4d-gmbh): https://github.com/t4d-gmbh/powerbi-example-surfspots
- Data-goblin PBIR templates: https://github.com/data-goblin/power-bi-visual-templates
- PBIP / agent demo integrations: https://github.com/RuiRomano/pbip-demo-agentic-mcp

Other helpful references and blogs (non-exhaustive):
- PBIR overview (third-party blog): https://lukasreese.com/2026/03/16/what-is-pbir-full-guide-to-power-bi-enhanced-report-format/
- Developer-mode / PBIR blog (third-party): https://blogs.diggibyte.com/power-bi-enhanced-report-format-pbir-developer-mode/

Note: The authoritative Microsoft Learn PBIR page (first link) contains links to schema files and details on enabling PBIR preview in Power BI Desktop. Use that page as the primary canonical source for PBIR behavior.

---

## 3. PBIR quick reference and canonical links (inline citations)

- PBIR = Power BI Enhanced Report Format: a directory-based JSON representation of report metadata where visuals, pages, bookmarks, etc., are individual JSON files. (See Microsoft Learn PBIR docs: https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format)

- How to enable PBIR in Power BI Desktop (official): File > Options and settings > Options > Preview features → "Store reports using enhanced metadata format (PBIR)". The Microsoft Learn page documents that process and preview behavior.

- Schema availability: Microsoft Learn PBIR documentation references per-file JSON schema(s). The full official JSON schemas and their canonical URLs are linked from the Microsoft PBIR docs page; engineers should use those schema files for exact validation (e.g., visual.schema.json and page.schema.json).

---

## 4. PBIR format deep-dive: schema excerpt and annotated visual.json example

This section contains:
- A representative PBIR visual schema fragment showing typical key names and types
- An annotated example visual JSON (syntactically valid) with adjacent explanation mapping keys to semantics

Note: This is a representative fragment (not the full schema). For the official full JSON schema files (report/page/visual), fetch the schema files linked from the Microsoft Learn PBIR page above.

### 4.1 Representative PBIR visual schema fragment (representative JSON Schema fragment)

This JSON Schema fragment shows the typical top-level keys and types you will find in a PBIR visual file. Use the official schema file from Microsoft for strict validation.

```json
{
  "$id": "https://example.local/schemas/visual.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PBIR Visual (representative fragment)",
  "type": "object",
  "required": ["visual"],
  "properties": {
    "visual": {
      "type": "object",
      "required": ["id","type"],
      "properties": {
        "id": { "type": "string" },
        "type": { "type": "string", "description": "Visual type identifier, e.g., visuals/msColumnChart" },
        "title": { "type": "string" },
        "position": {
          "type": "object",
          "properties": {
            "x": { "type": "integer" },
            "y": { "type": "integer" },
            "width": { "type": "integer" },
            "height": { "type": "integer" }
          }
        },
        "dataRoles": {
          "type": "object",
          "properties": {
            "Category": {
              "type": "object",
              "properties": {
                "table": { "type": "string" },
                "column": { "type": "string" }
              }
            },
            "Values": {
              "type": "object",
              "properties": {
                "table": { "type": "string" },
                "column": { "type": "string" },
                "measure": { "type": "string" }
              }
            }
          }
        },
        "properties": { "type": "object" }
      }
    }
  }
}
```

Notes:
- The above is a compact fragment. The official Microsoft visual schema includes enumerations, additional nested objects, formatting, selectors, and properties per visual type. Always use the official schema for validation.

### 4.2 Annotated example visual JSON (syntactically valid)

Below is a short, valid JSON file representing a PBIR visual. It is syntactically valid (no comments in JSON). After the JSON, an adjacent mapping table explains each key.

Example file: definition/visuals/visual-100.json

```json
{
  "visual": {
    "id": "visual-100",
    "type": "visuals/msColumnChart",
    "title": "Sales by Region",
    "position": { "x": 0, "y": 0, "width": 600, "height": 400 },
    "dataRoles": {
      "Category": { "table": "Geography", "column": "Region" },
      "Values": { "table": "Sales", "measure": "TotalSales" }
    },
    "properties": {
      "legend": { "visible": true },
      "axis": { "x": { "label": true }, "y": { "label": true } }
    }
  }
}
```

Key mappings (adjacent explanation):
- visual.id — unique visual identifier within the PBIR project (string)
- visual.type — visual renderer type (built-in or custom). Example: "visuals/msColumnChart".
- visual.title — user-visible title shown in the report.
- visual.position — layout rectangle (x,y,width,height) on the page canvas.
- visual.dataRoles — roles mapping; each role maps to a data element: table/column/measure. For example, Category → Geography.Region, Values → Sales.TotalSales.
- visual.properties — additional rendering and formatting properties (legend visibility, axis labels, colors, etc.).

Where to find the full official schema: fetch the 'visual.schema.json' from the Microsoft Learn PBIR docs or follow the schema link(s) on that page. The official schema contains many additional keys, enumerations, and nested structures.

---

## 5. Tooling & automation landscape (with links)

Authoritative and community tooling referenced in this report:

- PBIR-Utils (GitHub) — utilities for managing PBIR projects: https://github.com/akhilannan/PBIR-Utils
- Example PBIR project (t4d-gmbh/powerbi-example-surfspots): https://github.com/t4d-gmbh/powerbi-example-surfspots
- Visual templates (data-goblin): https://github.com/data-goblin/power-bi-visual-templates
- PBIP demo/agent integrations: https://github.com/RuiRomano/pbip-demo-agentic-mcp

Suggested minimal toolset for automation (engineers should implement or adapt):
- JSON Schema validator (ajv for Node, or jsonschema for Python)
- JSON Patch generation & application (fast-json-patch, rfc6902 libraries)
- pbir-diff: script to compute JSON Patch between two files
- pbir-apply: script to apply patches to PBIR project and run schema validation
- CI integration: GitHub Actions, Azure Pipelines, or other CI that runs validation and gating

Example commands (engineer-implemented):

- Schema validation (ajv, Node):
  - ajv validate -s schemas/visual.schema.json -d definition/visuals/visual-100.json
- Compute JSON Patch (node script using fast-json-patch):
  - node tools/make_patch.js --orig definition/visuals/visual-100.json --modified modified/visual-100.json --out patches/patch-visual-100.json
- Apply patch (dry-run):
  - python tools/pbir_apply.py --project definition/ --patch patches/patch-visual-100.json --dry-run
- Checksum: sha1sum definition/visuals/visual-100.json

---

## 6. Power BI visual-layer & semantic-model constraints (with inline citation)

Key constraints to respect when automating PBIR edits:

- PBIR JSON is validated by Power BI Desktop at open time; invalid edits can prevent report load. (See Microsoft Learn PBIR docs: https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format)

- Visual field bindings must reference existing model elements (tables/columns/measures). If a referenced field does not exist, rendering errors or load failures occur.

- Rebinding across role types may require additional property changes (e.g., sorting, formatting). Conservative changes are less risky.

- Schema versions may differ between Power BI Desktop releases; always include pbirSchemaVersion in the message envelope and validate against the target schema.

- Custom visuals can have proprietary properties; safe automation often limits edits to dataRoles and non-internal properties unless the visual schema is understood.

Recommended developer checks before applying patches:
1. Validate referenced table/column/measure exist in TMDL modelContext.
2. Validate use of stable IDs vs. names — prefer GUIDs if available; otherwise ensure name match is exact.
3. Run JSON schema validation for modified files.
4. Run smoke-load test (open in Power BI Desktop or use headless validator) before merging.

Reference: Microsoft Learn PBIR docs and Power BI Developer docs (see Sources).

---

## 7. Agent architecture & communication protocol (recap)

Three agents with role separation:
- Business Analyst (BA): writes ChangeSpec (intent + acceptance criteria) and includes minimal context
- Developer (Dev): turns ChangeSpec into DevPatch (JSON Patch(s)), runs validation, returns patch metadata
- Reviewer: approves/rejects patch based on schema checks, model checks, security checks, and smoke tests

Communication style: structured messages using a formal message envelope (see Section 8). Patches are file-level JSON Patch arrays, stored with baseChecksum and git metadata.

Handoff lifecycle:
1. BA → Dev: sends ChangeSpec in envelope
2. Dev → Reviewer: sends DevPatch (patch array + validation results) in envelope
3. Reviewer → CI: approves to apply patch (or requests changes)

---

## 8. Formal message envelope: JSON Schema and sample messages

This section formalizes the inter-agent message envelope as a JSON Schema and provides two sample messages (BA→Dev and Dev→Reviewer) consistent with the system prompts.

### 8.1 Message Envelope JSON Schema (draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.local/schemas/message-envelope.schema.json",
  "title": "Agent Message Envelope",
  "type": "object",
  "required": ["messageId","taskId","from","to","reportId","pbirSchemaVersion","payload","createdAt"],
  "properties": {
    "messageId": { "type": "string", "format": "uuid" },
    "taskId": { "type": "string" },
    "from": { "type": "string", "enum": ["BusinessAnalyst","Developer","Reviewer","CI"] },
    "to": { "type": "string", "enum": ["BusinessAnalyst","Developer","Reviewer","CI"] },
    "reportId": { "type": "string" },
    "pbirSchemaVersion": { "type": "string" },
    "context": { "type": "object" },
    "payload": { "type": "object" },
    "attachments": {
      "type": "array",
      "items": { "type": "object" }
    },
    "createdAt": { "type": "string", "format": "date-time" }
  }
}
```

Notes on required fields and constraints:
- messageId: UUID (v4) for traceability
- taskId: stable task identifier (human-readable) across the workflow
- from / to: enumerated actors
- reportId: canonical report identifier
- pbirSchemaVersion: string indicating the PBIR schema version to validate against
- context: optional object for projectPath, git branch, baseChecksums, etc.
- payload: agent-specific content (ChangeSpec for BA; DevPatch for Dev; ReviewResult for Reviewer)

### 8.2 DevPatch (payload) schema fragment (representative)

This is the expected DevPatch structure returned by the Developer and embedded as payload in the envelope.

```json
{
  "type": "object",
  "required": ["patchId","reportId","filesModified","patches","validation","statusCode"],
  "properties": {
    "patchId": { "type": "string" },
    "reportId": { "type": "string" },
    "filesModified": { "type": "array", "items": { "type": "string" } },
    "patches": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["file","baseChecksum","patch"],
        "properties": {
          "file": { "type": "string" },
          "baseChecksum": { "type": "string" },
          "patch": { "type": "array" }
        }
      }
    },
    "validation": { "type": "object" },
    "testsRun": { "type": "array" },
    "applyInstructions": { "type": "object" },
    "statusCode": { "type": "integer" },
    "notes": { "type": "string" }
  }
}
```

### 8.3 Sample message: Business Analyst → Developer (ChangeSpec)

```json
{
  "messageId": "4f8e7d2a-1f4b-4a1f-a2c7-0f2b9d7a1a01",
  "taskId": "task-2026-0001",
  "from": "BusinessAnalyst",
  "to": "Developer",
  "reportId": "report-abc123",
  "pbirSchemaVersion": "v1",
  "context": {
    "projectPath": "./definition/",
    "git": { "branch": "feature/change-online-sales", "commit": "sha1:abcd1234" }
  },
  "payload": {
    "changeSpec": {
      "changeSpecId": "cs-2026-0007",
      "reportId": "report-abc123",
      "target": { "pageId": "page-1", "visualId": "visual-100" },
      "intent": "Change 'Sales by Region' to use measure 'OnlineSales' instead of 'TotalSales'",
      "acceptanceCriteria": ["Chart displays OnlineSales values","Report loads without validation errors"],
      "dataConstraints": { "requiredTables": ["Sales","Geography"], "requiredColumns": [{"table":"Sales","column":"OnlineSales"}] }
    }
  },
  "createdAt": "2026-04-01T12:00:00Z"
}
```

### 8.4 Sample message: Developer → Reviewer (DevPatch with baseChecksum)

```json
{
  "messageId": "88f3c9b2-2b10-4d84-9d6b-1e2d3f4a5b06",
  "taskId": "task-2026-0001",
  "from": "Developer",
  "to": "Reviewer",
  "reportId": "report-abc123",
  "pbirSchemaVersion": "v1",
  "context": {
    "projectPath": "./definition/",
    "git": { "branch": "feature/change-online-sales", "commit": "sha1:abcd1234" }
  },
  "payload": {
    "devPatch": {
      "patchId": "patch-2026-101",
      "reportId": "report-abc123",
      "filesModified": ["definition/visuals/visual-100.json"],
      "patches": [
        {
          "file": "definition/visuals/visual-100.json",
          "baseChecksum": "sha1:deadbeef1234567890",
          "patch": [
            { "op": "replace", "path": "/visual/dataRoles/Values/measure", "value": "OnlineSales" }
          ]
        }
      ],
      "validation": { "schemaValidation": "pass", "details": "visual schema validated" },
      "testsRun": [ { "name": "schema-check", "result": "pass", "details": "No schema errors" } ],
      "applyInstructions": { "dryRunCommand": "python tools/pbir_apply.py --project definition/ --patch patches/patch-2026-101.json --dry-run", "applyCommand": "python tools/pbir_apply.py --project definition/ --patch patches/patch-2026-101.json" },
      "statusCode": 0,
      "notes": "Changed measure to OnlineSales. Verified measure exists in model context."
    }
  },
  "createdAt": "2026-04-01T12:15:00Z"
}
```

Notes:
- The DevPatch payload contains baseChecksum for the file to detect concurrent edits.
- The envelope schema and payload schemas ensure messages can be programmatically validated before processing.

---

## 9. System prompts: BA, Developer, Reviewer (updated with message schema)

Each agent system prompt now references the message envelope field names and requires that agent outputs be valid JSON that conforms to the stated schemas.

Below are concise system prompts (engineer should paste into the LLM system prompt slot). Each instructs the agent to return ONLY the JSON object specified (no extra text).

### 9.1 Business Analyst (BA) — system prompt (condensed)

System instruction (for BA):

- Role: BusinessAnalyst
- Purpose: Produce a ChangeSpec embedded into the message envelope (payload.changeSpec) and return the full Message Envelope JSON.
- Required top-level envelope fields: messageId (uuid), taskId, from="BusinessAnalyst", to (usually "Developer"), reportId, pbirSchemaVersion, payload.changeSpec, createdAt.
- Return ONLY a single JSON object matching the Message Envelope JSON Schema in Section 8.

Required ChangeSpec fields inside payload:
- changeSpecId, reportId, target (pageId, visualId), intent, acceptanceCriteria (array), dataConstraints (requiredTables, requiredColumns), priority, testPlan (array).

Example: BA must produce the same message example shown in 8.3.

### 9.2 Developer (Dev) — system prompt (condensed)

System instruction (for Dev):

- Role: Developer
- Purpose: Accept BA message envelope (validate against envelope schema). Produce DevPatch that implements ChangeSpec. Return full Message Envelope JSON with from="Developer", to="Reviewer" and payload.devPatch matching DevPatch schema.
- Required steps (dev MUST perform or report failures):
  1. Validate incoming envelope structure (messageId, taskId, payload.changeSpec).
  2. Load impacted files from context.projectPath.
  3. Compute baseChecksum (sha1) for each file intended to modify.
  4. Produce JSON Patch (RFC 6902) arrays for each file.
  5. Validate modified JSON against the official schema(s) (ajv) and set validation.schemaValidation to pass/fail.
  6. If model references missing, set statusCode=2 and include diagnostics.
  7. Return envelope JSON with payload.devPatch (see sample in 8.4).

- Return ONLY the Message Envelope JSON.

### 9.3 Reviewer — system prompt (condensed)

System instruction (for Reviewer):

- Role: Reviewer
- Purpose: Accept Developer envelope, validate devPatch (schemaValidation, checksum, model references, security checks), and return a ReviewResult embedded into a Message Envelope to CI or Developer.
- Required reviewer outputs (payload.reviewResult): reviewId, patchId, reportId, decision (approve|request_changes|reject), issues (array), recommendations (array), approvalNotes, statusCode.
- Reviewer must perform the Reviewer checklist (Section 16) and include results in issues array.

- Return ONLY the Message Envelope JSON.

---

## 10. PBIR diff example (JSON Patch + git unified diff) and validation steps

This section gives a concrete sample change a Developer would produce, both as a JSON Patch array and as a git-style unified diff, and shows short before/after file contents. It also lists validation steps and commands the Developer/CI should run.

### 10.1 Scenario

Task: Swap the measure bound to visual-100 from "TotalSales" to "OnlineSales".

Original file: definition/visuals/visual-100.json (short)

```json
{
  "visual": {
    "id": "visual-100",
    "type": "visuals/msColumnChart",
    "dataRoles": {
      "Category": { "table": "Geography", "column": "Region" },
      "Values": { "table": "Sales", "measure": "TotalSales" }
    }
  }
}
```

Modified file (after change): definition/visuals/visual-100.json

```json
{
  "visual": {
    "id": "visual-100",
    "type": "visuals/msColumnChart",
    "dataRoles": {
      "Category": { "table": "Geography", "column": "Region" },
      "Values": { "table": "Sales", "measure": "OnlineSales" }
    }
  }
}
```

### 10.2 JSON Patch (RFC 6902) array

Developer creates patch file: patches/patch-2026-101-visual-100.json

```json
[
  { "op": "replace", "path": "/visual/dataRoles/Values/measure", "value": "OnlineSales" }
]
```

This patch is associated with file path: definition/visuals/visual-100.json and baseChecksum: sha1:deadbeef1234567890 (example).

DevPatch payload entry (representative):

```json
{
  "file": "definition/visuals/visual-100.json",
  "baseChecksum": "sha1:deadbeef1234567890",
  "patch": [
    { "op": "replace", "path": "/visual/dataRoles/Values/measure", "value": "OnlineSales" }
  ]
}
```

### 10.3 git-style unified diff for the same change

Unified diff (short) — easily human-reviewable and can be included in PRs.

```diff
*** a/definition/visuals/visual-100.json
--- b/definition/visuals/visual-100.json
@@
-      "Values": { "table": "Sales", "measure": "TotalSales" }
+      "Values": { "table": "Sales", "measure": "OnlineSales" }
```

### 10.4 Validation steps & commands (Dev/CI)

1) Compute baseChecksum and verify file has not changed since Dev read it

- Command (example):
  - sha1sum definition/visuals/visual-100.json
  - Compare with devPatch.patches[0].baseChecksum (fail if mismatch)

2) Apply JSON Patch to a copy of the file (dry-run) and validate resulting JSON syntax

- Command (pseudo):
  - python tools/apply_json_patch.py --file definition/visuals/visual-100.json --patch patches/patch-2026-101-visual-100.json --out tmp/visual-100.modified.json
  - jq . tmp/visual-100.modified.json  # (syntax check)

3) Validate modified file against the official schema

- Command (using ajv CLI):
  - ajv validate -s schemas/visual.schema.json -d tmp/visual-100.modified.json

4) Model reference checks (verify measure exists in modelContext)

- Command (pseudo):
  - python tools/check_model_reference.py --model model/ --measure OnlineSales
  - or grep/inspect model metadata: jq '.measures[] | select(.name=="OnlineSales")' model/metadata.json

5) Run smoke-load (open report in Power BI Desktop to validate load) — manual or scripted if headless API available

- Command (manual): Open PBIP/PBIR folder in Power BI Desktop (with PBIR preview enabled) and confirm page loads and visual renders.
- If automated: python tools/powerbi_headless_validate.py --project ./definition/  (if such tooling available)

6) Create PR with unified diff and metadata (message envelope, devPatch) and request Reviewer.

Notes:
- The exact command names and scripts are environment-specific. The above commands are templates engineers should implement.

---

## 11. Security & CI/CD (tenant settings, least-privilege, audit, defense-in-depth)

This section formalizes security recommendations for running agents that edit PBIR files and for CI/CD workflows that apply patches.

### 11.1 PBIR preview settings (tenant/admin guidance)

- Enabling PBIR in Power BI Desktop (per Microsoft Learn):
  - File > Options and settings > Options > Preview features → check "Store reports using enhanced metadata format (PBIR)". (See Microsoft Learn PBIR docs: https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format)
- Admins/tenants should control who can enable preview features in managed desktops and should use controlled test environments for early PBIR adoption.

### 11.2 Agent identity & least-privilege permissions

Principles:
- Agents must have scoped identities (service accounts) with minimal privileges.
- Distinguish read-only privileges (to read PBIR project files and model metadata) from write privileges (to create PRs or push to feature branches).

Suggested permissions model:
- LLM/agent runtime (BA role): no direct write access to git; BA outputs are stored as messages only.
- Developer agent: only able to create commit/PRs in a designated feature branch via a CI service token. No direct rights to main/master branches.
- CI: applies approved patches to protected branches only via CI service principal with audited credentials.
- Reviewer: human users with merge rights must be required to approve PRs; use branch protection rules to enforce human review.

Implementation suggestions:
- Use short-lived credentials / OIDC tokens for CI.
- Limit repository access to specific paths (if platform supports path-based rules) or enforce policies in CI pipelines.

### 11.3 Gating / approval workflow (human-in-loop)

- All DevPatch outputs must be pushed as a PR to a feature branch.
- Protect main branches with branch protection rules that require:
  - Required status checks: schema-validation, model-reference-check, smoke-load (if available)
  - Required review approvals (at least one human Reviewer)
  - No direct pushes to protected branches
- CI should reject PRs if any required status check fails.

### 11.4 Audit logging requirements

- Store full message envelopes and payloads (ChangeSpec, DevPatch, ReviewResult) in an append-only audit store or as PR artifacts. Include messageId, taskId, agent id, commit sha, and timestamps.
- Record baseChecksums and the exact patches applied.
- Log user/agent identity and signing (e.g., commit signed), and keep retention policies for audit trail.

### 11.5 Defense-in-depth & data exfiltration controls

- Agents must not return raw dataset content (e.g., rows of customer PII). System prompts must enforce: "Never include raw dataset rows in outputs. Only reference column/table names and checksums."
- Implement pre-flight scrubbing on any agent outputs that could contain data (regex scanning for email, SSN patterns) and reject outputs that contain values rather than field names.
- Limit agent access to model metadata only — not to dataset values. If model sampling is required, use sanitized/aggregated data only.
- In PRs and logs, redact or encrypt any sensitive fields: do not print PII in logs or message payloads.

### 11.6 Steps to test controls in CI (example test commands)

1) Schema validation (ensure CI fails on schema violations):

- ajv validate -s schemas/visual.schema.json -d tmp/visual-100.modified.json

2) Check baseChecksum enforcement (CI must fail if baseChecksum mismatches):

- echo "expected: sha1:deadbeef..."; actual=$(sha1sum definition/visuals/visual-100.json); test "$actual" = "sha1:deadbeef..." || exit 1

3) Sensitive-data scanner (example using grep/regex):

- grep -E "[0-9]{3}-[0-9]{2}-[0-9]{4}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" tmp/visual-100.modified.json && exit 1 || echo "no obvious PII"

4) Enforce no raw-data outputs from agents (agent output linter):

- python tools/agent_output_linter.py --file agent-output.json --rules rules/no_raw_rows.yaml

5) Verify audit artifacts produced (the envelope JSON is written to artifacts/):

- test -f artifacts/message-<messageId>.json || exit 1

These tests should be run as part of the CI required checks before allowing merge.

---

## 12. Prompt modularity patterns and validation pseudo-code

This section summarizes modular patterns and provides simple pseudo-code for parsing/validating agent messages and payload outputs.

Patterns recap:
- Keep system prompts short and authoritative.
- Include required output JSON schema in the prompt and use deterministic LLM settings.
- Use schema-first approach: the LLM output is validated against JSON Schemas before processing.

Validation pseudo-code (Python-like, simplified):

```python
import json, jsonschema

def validate_envelope(envelope_json, schema_path, payload_schema_path):
    envelope = json.loads(envelope_json)
    with open(schema_path) as f:
        schema = json.load(f)
    jsonschema.validate(instance=envelope, schema=schema)

    payload = envelope['payload']
    # payload schema depends on 'from'
    with open(payload_schema_path) as f:
        payload_schema = json.load(f)
    jsonschema.validate(instance=payload, schema=payload_schema)
    return True
```

Use this routine to reject any agent output that does not conform to the envelope and payload schemas. Provide validated artifacts to CI.

---

## 13. Evaluation framework, test-suite & representative testcases (updated)

Evaluation axes and metrics are the same as before, with added security checks and gating. Key measurable checks to add:
- Schema validation pass (100%)
- Model reference validation pass (100%) for accepted patches
- Audit artifact presence (100%)
- No PII leaked in artifacts (0 occurrences)

Representative testcases (5) — expanded with security/CI checks:

Testcase 1 (measure swap — success)
- Input: ChangeSpec to swap TotalSales → OnlineSales
- Expected: DevPatch with JSON Patch and baseChecksum; schemaValidation=pass; Reviewer approve
- Validation: ajv validate; sha1 checksum check; grep for PII; smoke-load pass

Testcase 2 (change category column, missing column — fail & diagnostics)
- Input: ChangeSpec to change category Region → Country
- Expected: Dev returns statusCode=2 with missing-column diagnostics if Country not in model
- Validation: DevPatch.validation contains missing column text; CI blocks PR

Testcase 3 (create new KPI visual using existing measure)
- Input: BA requests new KPI bound to AverageOrderValue
- Expected: new visual file created; DevPatch contains added file with patch = add op; schemaValidation=pass
- Validation: ajv validate new file; PR contains unified diff; reviewer verifies

Testcase 4 (attempt to use NonExistentMeasure — security & gating)
- Input: BA asks to use NonExistentMeasure
- Expected: Dev returns statusCode=2; any candidate outputs must not contain dataset samples
- Validation: verify no PII; CI checks for explicit missing measure error and blocks PR

Testcase 5 (concurrent edits conflict detection)
- Setup: two patches produced against same baseChecksum
- Expected: CI rejects second PR due to baseChecksum mismatch
- Validation: CI script compares stored baseChecksum with current file checksum and fails if mismatch

Each test should produce artifacts: envelope JSONs, patches, unified diff, validation logs, and CI status results.

---

## 14. Failure modes & mitigations (updated)

Key failure modes (recap + security mitigations):

- Schema validation failure → ensure Dev runs schema validation and returns actionable diagnostics; CI rejects PR.
- Missing model references → Dev must validate modelContext; on mismatch return statusCode=2 and suggestions.
- Hallucinated data (agents returning dataset rows) → enforce prompt guardrails, run PII scanner and reject outputs.
- Concurrent edits → use baseChecksum and CI conflict checks.
- Unauthorized writes → use least-privilege tokens and branch protection.

Mitigations are described in Section 11 and in the validation pseudo-code.

---

## 15. End‑to‑end worked example (BA → Dev → Reviewer) including diffs and patch commands

This section combines earlier examples into one E2E flow including required checks and commands.

1) BA constructs ChangeSpec and sends Message Envelope (see 8.3 sample).

2) Developer receives envelope, validates, and constructs DevPatch. Steps Dev runs locally/CI:
  - compute baseChecksum: sha1sum definition/visuals/visual-100.json  # expected sha1:deadbeef1234567890
  - create patch file patches/patch-2026-101-visual-100.json (JSON Patch shown in Section 10)
  - dry-apply patch: python tools/apply_json_patch.py --file definition/visuals/visual-100.json --patch patches/patch-2026-101-visual-100.json --out tmp/visual-100.modified.json
  - validate schema: ajv validate -s schemas/visual.schema.json -d tmp/visual-100.modified.json
  - model check: python tools/check_model_reference.py --model model/ --measure OnlineSales
  - prepare DevPatch envelope (see 8.4 sample) and push PR with unified diff

3) Reviewer runs checklist (see Section 16). If all checks pass, Reviewer sets decision=approve and CI applies patch:
  - apply patch in CI: python tools/pbir_apply.py --project definition/ --patch patches/patch-2026-101-visual-100.json
  - run smoke-load (manual or automated)
  - merge PR (branch protection allows merge only on passing checks and required approvals)

Audit logs: store envelope JSONs and patch files as artifacts in the PR for future traceability.

---

## 16. Reviewer verification checklist (commands)

Checklist (short) the Reviewer must run before approving:

1) Schema validation — ensure modified file conforms to visual schema
- Command: ajv validate -s schemas/visual.schema.json -d tmp/visual-100.modified.json

2) Checksum match — confirm baseChecksum matches file in repo at the time of patch creation
- Command: sha1sum definition/visuals/visual-100.json  # compare to devPatch.patches[0].baseChecksum

3) Model-reference checks — verify measures/columns exist
- Command: python tools/check_model_reference.py --model model/ --measure OnlineSales
  or: jq '.measures[] | select(.name=="OnlineSales")' model/metadata.json

4) Visual smoke-load — confirm report loads and visual renders
- Manual: Open project directory in Power BI Desktop and quickly load page
- Automated (if available): python tools/powerbi_headless_validate.py --project ./definition/

5) Security checks — ensure no sensitive data was exposed and agent outputs are safe
- Command: grep -E "[0-9]{3}-[0-9]{2}-[0-9]{4}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" artifacts/message-<messageId>.json && exit 1 || echo "no obvious PII"
- Command: python tools/agent_output_linter.py --file artifacts/message-<messageId>.json --rules rules/no_raw_rows.yaml

6) Audit artifact presence — ensure envelope and patch artifacts exist
- Command: test -f artifacts/message-<messageId>.json && test -f patches/patch-2026-101-visual-100.json

Reviewer should record the review result in payload.reviewResult and attach it to the PR.

---

## 17. Recommendations & next steps

Short-term (first sprint):
- Implement schema validation and patch apply scripts (pbir-validate, pbir-diff, pbir-apply) and a small test project from t4d-gmbh repo (https://github.com/t4d-gmbh/powerbi-example-surfspots). (2–4 days)
- Integrate envelope validation (JSON Schema) as a pre-step when accepting agent outputs. (1–2 days)
- Implement baseChecksum enforcement in CI and branch protection rules requiring Reviewer approval. (1–2 days)

Mid-term (2–6 weeks):
- Add automated smoke-load tests (headless) if possible; otherwise add manual smoke test steps to Reviewer SOP.
- Expand prompt templates and run iterative prompt tuning with 10–20 real ChangeSpec examples.

Operational: enforce security and logging, and build tests that assert no PII is ever emitted by agents.

---

## 18. Appendices

### Appendix A — Raw prompt templates (full)

(Full prompt templates for BA, Developer, Reviewer are in the original Appendix A and have been updated inline in Section 9. Engineers should paste the condensed system instructions into the LLM provider's system role and enforce JSON-only outputs.)

### Appendix B — PBIR schema fragment (representative)

(See Section 4.1 representative JSON Schema fragment for visual files.) For the official full schema, fetch the schema files linked from the Microsoft Learn PBIR documentation: https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format

### Appendix C — Example CLI commands and script skeletons

Representative scripts and commands (engineer to implement):

1) Compute checksum

```bash
sha1sum definition/visuals/visual-100.json
```

2) Apply JSON Patch dry-run

```bash
python tools/apply_json_patch.py --file definition/visuals/visual-100.json --patch patches/patch-2026-101-visual-100.json --out tmp/visual-100.modified.json
```

3) Schema validation

```bash
ajv validate -s schemas/visual.schema.json -d tmp/visual-100.modified.json
```

4) Model reference check (example)

```bash
python tools/check_model_reference.py --model model/ --measure OnlineSales
```

5) PII scan

```bash
grep -E "[0-9]{3}-[0-9]{2}-[0-9]{4}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" artifacts/message-<messageId>.json && exit 1 || echo "no obvious PII"
```

---

## Time & effort estimate (unchanged)

Estimated total: 49–72 hours. Includes time for schema retrieval, tool scripting, prompt tuning, tests, and documentation.

---

## Sources

Authoritative Microsoft resources (canonical):

- Microsoft Learn — Create a Power BI report in enhanced report format (PBIR)
  - https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format

- Microsoft Power BI Blog (official announcements and rollout posts)
  - https://powerbi.microsoft.com/en-us/blog/

- Microsoft Power BI developer docs (SDK & REST API root)
  - https://learn.microsoft.com/en-us/power-bi/developer/

Community / tooling / example repos (linked earlier in this report):

- PBIR-Utils (akhilannan) — https://github.com/akhilannan/PBIR-Utils
- powerbi-example-surfspots (t4d-gmbh) — https://github.com/t4d-gmbh/powerbi-example-surfspots
- data-goblin / power-bi-visual-templates — https://github.com/data-goblin/power-bi-visual-templates
- pbip-demo-agentic-mcp — https://github.com/RuiRomano/pbip-demo-agentic-mcp

Further reading and community posts:
- Lukas Reese — What is PBIR? (overview) — https://lukasreese.com/2026/03/16/what-is-pbir-full-guide-to-power-bi-enhanced-report-format/
- Diggibyte blog — Power BI enhanced report format (PBIR) — Developer Mode — https://blogs.diggibyte.com/power-bi-enhanced-report-format-pbir-developer-mode/

---

End of revised report.
