# 15 Tool Templates for Multi-Agent LLM Orchestration with Power BI (PBIR) — Revised

> This revised PBIR (Power BI Integration Repository) report applies the critic's requested changes. It defines exactly 15 distinct tool templates for multi-agent orchestration with Power BI, each with inputs, outputs, exact REST endpoints (workspace/group form), required Azure AD permission scopes (delegated vs application), separation of LLM vs non-LLM responsibilities, security guidance, sample prompts, implementation notes, curl snippets, and complexity estimates.

Notes & sources
- Power BI REST API documentation (primary authoritative links used inline per operation):
  - Imports: https://learn.microsoft.com/en-us/rest/api/power-bi/imports
  - Reports: https://learn.microsoft.com/en-us/rest/api/power-bi/reports
  - Datasets (including Refresh): https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset
  - Embed Token / GenerateToken: https://learn.microsoft.com/en-us/rest/api/power-bi/embed-token/reports-generate-token-in-group
  - General Power BI REST API index: https://learn.microsoft.com/en-us/rest/api/power-bi/

- Assumptions explicitly called out where PBIR internals or organization-specific policies are not covered by public docs. Validation steps are suggested at the end of this report.

--------------------------------------------------------------------------------

CONCISE LIST — 15 TOOL TEMPLATES (numbered, one-line purpose)

1. Import-PBIX: Upload a .pbix to a workspace (create content).
2. Export-Report: Export a report to .pbix or file format.
3. Update-Report-Content: Update report content using a source report (report swap).
4. Rebind-Report: Rebind a report to a different dataset (change dataset binding).
5. Generate-Embed-Token: Create embed tokens (view/edit) with optional RLS effective identities.
6. Start-Dataset-Refresh: Trigger (standard/enhanced) dataset refresh requests.
7. Get-Refresh-History: Retrieve refresh history and status for a dataset.
8. Cancel-Refresh: Cancel an in-progress enhanced refresh operation.
9. Get-Reports-List: List reports in a workspace.
10. Clone-Report: Clone an existing report in a workspace.
11. Update-Datasources: Update data sources for paginated reports (RDL) or reports' data source settings.
12. Manage-Gateway-Datasource: Bind or update dataset datasource to a gateway.
13. Manage-Workspace-Roles: Assign workspace roles / manage access to preserve least privilege.
14. Deploy-CI-Artifact: CI-driven deployment: import/update across staging->prod workspaces (promotion).
15. XMLA-Run-TMSL: Run XMLA/TMSL commands for semantic model operations (partitions, process, deploy) — Premium/PremiumPerUser required.

---

For each tool below: Inputs, Outputs, sample payload(s), sample output(s), Power BI REST API endpoints and docs (workspace-level forms where applicable), Azure AD permission scopes (delegated vs application), example Azure AD app settings (client credential vs delegated guidance), LLM vs non-LLM responsibilities and rationale, security considerations, agent roles & two sample prompts, implementation notes (SDKs/libraries, limitations, infra), time/complexity estimate, and sample curl calls where applicable.

Note: all REST endpoints use base URL https://api.powerbi.com and are shown in the v1.0/myorg form with workspace (group) path when workspace-specific.

---

### 1) Import-PBIX

- Purpose: Import a .pbix file into a specified workspace (create content).

- Inputs
  - workspaceId: string (GUID)
  - fileName: string
  - fileBytes: multipart file stream
  - conflictAction: string ("CreateOrOverwrite" | "Abort")

- Sample input JSON (conceptual)
  { "workspaceId":"...", "fileName":"sales-report.pbix", "file":"<multipart>" }

- Outputs
  - importId: string
  - reportId: string
  - status: string

- Sample output
  { "id":"...","importState":"Succeeded","reports":[{"id":"...","name":"Sales Report"}] }

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/imports
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/imports/post-import-in-group

- Permissions (minimum)
  - Delegated: Content.Create, Report.ReadWrite.All
  - Application: Content.Create, Dataset.ReadWrite.All (admin consent required)

- Azure AD guidance
  - CI: app-only (client credentials), certificate or secret in Key Vault; grant admin consent for application permissions.
  - Dev: delegated interactive flow with Report.ReadWrite.All for ad-hoc uploads.

- LLM vs non-LLM
  - LLM: choose file naming, conflict policy, and pre-checks.
  - Non-LLM: perform multipart upload, poll import status.

- Security
  - Store secrets in Key Vault, limit app to target workspace, short-lived tokens.
  - Preserve RLS by avoiding delete/recreate workflows; prefer update operations.

- Agent roles
  - orchestrator, uploader

- Prompts
  - Concise: "Import ./sales-report.pbix to workspace {workspaceId} as 'Sales Report'." 
  - Multi-step: "1) Validate PBIX; 2) Upload to staging {stagingId}; 3) Run smoke tests; 4) Return importId." 

- Implementation
  - SDKs: msal, requests/axios, pbi-tools
  - Limitations: large PBIX require temporary upload (Premium); SP behavior varies by tenant
  - Infra: Key Vault, CI runner, staging workspace
  - Estimate: 3–5 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/imports?datasetDisplayName={displayName}" \
    -H "Authorization: Bearer {access_token}" \
    -F "file=@/path/to/sales-report.pbix"

---

### 2) Export-Report

- Purpose: Export a report to .pbix or supported archive for backup or diffing.

- Inputs
  - workspaceId: string
  - reportId: string
  - exportFormat: string ("PBIX" | "RDL" etc.)

- Outputs
  - exportJobId or file stream
  - fileUrl (temporary)

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/ExportTo (ExportTo / Export To File endpoints vary)
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports

- Permissions
  - Delegated: Report.Read.All
  - Application: Report.Read.All

- LLM vs non-LLM
  - LLM: choose what/when to export and retention names
  - Non-LLM: call export endpoint, poll, store file securely

- Security
  - Use delegated tokens for user exports, app-only for automated backups; store exports in secure Blob with short SAS

- Agent roles
  - backup-agent, downloader

- Prompts
  - Concise: "Export report {reportId} from {workspaceId} as PBIX" 
  - Multi-step: "1) Check report size; 2) Start export; 3) Upload to backup storage; 4) Return URL." 

- Implementation
  - SDKs: msal, requests/axios, pbi-tools for extraction
  - Limitations: not all reports exportable; some live connections block PBIX export
  - Infra: secure blob storage, CI runner
  - Estimate: 2–4 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/ExportTo" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"format":"PBIX"}'

---

### 3) Update-Report-Content

- Purpose: Replace or update a report's content from a source report (preserve reportId and tiles when possible).

- Inputs
  - workspaceId: string
  - targetReportId: string
  - sourceReportId or importId

- Outputs
  - status
  - updatedReportId

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/UpdateReportContent
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/update-report-content-in-group

- Permissions
  - Delegated/Application: Report.ReadWrite.All, Dataset.ReadWrite.All

- LLM vs non-LLM
  - LLM: safety checks, propose whether to update or to create a new report
  - Non-LLM: execute UpdateReportContent, validate results

- Security
  - Use service principal in CI; keep secrets in Key Vault; preserve RLS by avoiding dataset recreation

- Agent roles
  - content-decider, updater

- Prompts
  - Concise: "Update content of report {targetReportId} in {workspaceId} with source {sourceReportId}." 
  - Multi-step: "1) Backup target; 2) Validate compatibility; 3) Execute UpdateReportContent; 4) Run smoke tests." 

- Implementation
  - SDKs: msal, requests, pbi-tools
  - Limitations: schema mismatches can cause user-visible breaks; test in staging
  - Estimate: 2–4 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{targetReportId}/UpdateReportContent" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"sourceReportId":"{sourceReportId}"}'

---

### 4) Rebind-Report

- Purpose: Rebind a report to a different datasetId (change the data source binding).

- Inputs
  - workspaceId: string
  - reportId: string
  - targetDatasetId: string

- Outputs
  - status, reportId

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/Rebind
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/rebind-report-in-group

- Permissions
  - Delegated/Application: Report.ReadWrite.All, Dataset.ReadWrite.All

- LLM vs non-LLM
  - LLM: select target dataset mapping
  - Non-LLM: call Rebind, validate the report now uses the new dataset

- Security
  - Minimize privileges of the executor; test with GenerateToken to validate RLS for sample users

- Agent roles
  - mapper, binder

- Prompts
  - Concise: "Rebind report {reportId} to dataset {targetDatasetId} in {workspaceId}." 
  - Multi-step: "1) Validate dataset schema and measures; 2) Rebind; 3) Run tests using sample RLS identities." 

- Implementation
  - SDKs: msal, requests; pbi-tools for pre-checks
  - Limitations: rebind may require permissions across workspaces; RLS implications must be validated
  - Estimate: 1–2 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/Rebind" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"datasetId":"{datasetId}"}'

---

### 5) Generate-Embed-Token

- Purpose: Create embed tokens for reports/datasets with optional effective identities (RLS).

- Inputs
  - workspaceId: string
  - reportId: string
  - identities: array (optional: username, roles, datasets)
  - lifetimeInMinutes: int

- Outputs
  - token, tokenId, expiration

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/GenerateToken
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/embed-token/reports-generate-token-in-group

- Permissions
  - Delegated/Application: Report.Read.All, Dataset.Read.All (for RLS); Content.Create if creating content

- LLM vs non-LLM
  - LLM: build appropriate identities and roles from user intent
  - Non-LLM: call GenerateToken, manage token cache and revocation

- Security
  - Short-lived tokens only; do not log tokens; store service principal secrets in Key Vault

- Agent roles
  - token-provider, identity-resolver

- Prompts
  - Concise: "Generate a view token for {reportId} for user {userEmail} with role sales for 15 minutes." 
  - Multi-step: "1) Validate user AAD roles; 2) Construct identities payload; 3) Call GenerateToken; 4) Return token." 

- Implementation
  - SDKs: msal, requests/axios
  - Limitations: identity propagation delays after rebinds for AAS/Azure Analysis Services
  - Estimate: 1–2 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/GenerateToken" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"accessLevel":"View","identities":[{"username":"john@contoso.com","roles":["sales"],"datasets":["{datasetId}"]}],"lifetimeInMinutes":15}'

---

### 6) Start-Dataset-Refresh

- Purpose: Start standard or enhanced dataset refresh.

- Inputs
  - workspaceId: string
  - datasetId: string
  - refresh payload (type, objects etc.)

- Outputs
  - requestId/location, status

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset

- Permissions
  - Delegated/Application: Dataset.ReadWrite.All

- LLM vs non-LLM
  - LLM: schedule refresh and select partition vs full
  - Non-LLM: call API, poll status, log results

- Security
  - Use Key Vault for any credentials; ensure service principal is limited to target dataset

- Agent roles
  - scheduler, executor, monitor

- Prompts
  - Concise: "Start enhanced refresh on dataset {datasetId} for table Customer." 
  - Multi-step: "1) Check last refresh times; 2) If older than 6 hours, start refresh; 3) Return requestId and status." 

- Implementation
  - SDKs: msal, requests/axios
  - Limitations: certain features require Premium/PPU; respect rate limits
  - Estimate: 2–3 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"type":"full","objects":[{"table":"Customer"}],"timeout":"01:00:00"}'

---

### 7) Get-Refresh-History

- Purpose: Retrieve refresh history.

- Inputs
  - workspaceId, datasetId, top

- Outputs
  - array of refresh entries

- REST endpoint
  - GET https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/get-refresh-history-in-group

- Permissions
  - Delegated/Application: Dataset.Read.All

- LLM vs non-LLM
  - LLM: analyze trends and recommend remediation
  - Non-LLM: fetch history and parse

- Security
  - Read-only; preserve logs in secure store

- Agent roles
  - monitor, analyzer

- Prompts
  - Concise: "Get last 10 refreshes for dataset {datasetId}." 
  - Multi-step: "1) Fetch history for last 24h; 2) Identify failures; 3) For each, fetch error details and collate." 

- Implementation
  - SDKs: msal, requests
  - Estimate: 1 day

- Sample curl
  curl -X GET "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes?$top=10" \
    -H "Authorization: Bearer {access_token}"

---

### 8) Cancel-Refresh

- Purpose: Cancel an in-flight enhanced refresh.

- Inputs
  - workspaceId, datasetId, requestId

- Outputs
  - status

- REST endpoint
  - DELETE https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes/{requestId}
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/cancel-refresh-in-group

- Permissions
  - Dataset.ReadWrite.All

- LLM vs non-LLM
  - LLM: detect criteria to cancel (timeout thresholds)
  - Non-LLM: perform DELETE and handle confirmation

- Security
  - Audit cancellations

- Agent roles
  - watchdog, canceller

- Prompts
  - Concise: "Cancel refresh {requestId} for dataset {datasetId}." 
  - Multi-step: "1) If refresh >60min, cancel; 2) Log and notify owner." 

- Implementation
  - SDKs: msal, requests
  - Estimate: 1 day

- Sample curl
  curl -X DELETE "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes/{requestId}" \
    -H "Authorization: Bearer {access_token}"

---

### 9) Get-Reports-List

- Purpose: List reports and metadata in a workspace.

- Inputs
  - workspaceId, top, filter

- Outputs
  - array of reports

- REST endpoint
  - GET https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/get-reports-in-group

- Permissions
  - Report.Read.All

- LLM vs non-LLM
  - LLM: determine filters and summary logic
  - Non-LLM: execute GET and format result

- Security
  - Limit output to accessible workspaces; redact sensitive names if needed

- Agent roles
  - discovery, cache

- Prompts
  - Concise: "List reports in {workspaceId}." 
  - Multi-step: "1) Get reports; 2) For each, get datasetId and last refresh; 3) Return summary." 

- Implementation
  - SDKs: msal, requests
  - Estimate: 1 day

- Sample curl
  curl -X GET "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports" \
    -H "Authorization: Bearer {access_token}"

---

### 10) Clone-Report

- Purpose: Create a copy of a report in the same or different workspace.

- Inputs
  - workspaceId, reportId, targetWorkspaceId, newName

- Outputs
  - newReportId

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/Clone
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/clone-report-in-group

- Permissions
  - Report.ReadWrite.All

- LLM vs non-LLM
  - LLM: name & target selection
  - Non-LLM: call clone and validate

- Security
  - Ensure executor has access to target workspace

- Agent roles
  - copier, validator

- Prompts
  - Concise: "Clone report {reportId} to {targetWorkspaceId} as {newName}." 
  - Multi-step: "1) Validate source; 2) Clone; 3) Rebind datasets if needed; 4) Report status." 

- Implementation
  - SDKs: msal, requests
  - Estimate: 1–2 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/Clone" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"name":"{newName}","targetWorkspaceId":"{targetGroupId}"}'

---

### 11) Update-Datasources

- Purpose: Update report/dataset datasource details or credentials.

- Inputs
  - workspaceId, reportId/datasetId, updateRequests (array of connection updates)

- Outputs
  - status, updated items

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/UpdateDatasources
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/update-datasources-in-group

- Permissions
  - Report.ReadWrite.All, Dataset.ReadWrite.All

- LLM vs non-LLM
  - LLM: choose mapping between env-specific connection strings
  - Non-LLM: fetch secrets from Key Vault and call UpdateDatasources

- Security
  - Never expose creds to LLM; use Key Vault

- Agent roles
  - migrator, update-executor

- Prompts
  - Concise: "Update datasource {dsId} for {reportId} to server {server}." 
  - Multi-step: "1) Map env; 2) Fetch credentials; 3) Call UpdateDatasources; 4) Test connectivity." 

- Implementation
  - SDKs: msal, requests, Key Vault SDK
  - Estimate: 2–3 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/UpdateDatasources" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"updateRequests":[{"datasourceId":"{dsId}","connectionDetails":{"server":"sql"}}]}'

---

### 12) Manage-Gateway-Datasource

- Purpose: Bind datasets to gateways or update gateway datasource credentials.

- Inputs
  - gatewayId, datasourceId, connectionDetails, datasetId

- Outputs
  - status, bound resources

- REST endpoints
  - Gateways API: https://learn.microsoft.com/en-us/rest/api/power-bi/gateways
  - Bind to gateway: POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/BindToGateway
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/bind-to-gateway-in-group

- Permissions
  - Gateway.ReadWrite.All, Dataset.ReadWrite.All

- LLM vs non-LLM
  - LLM: choose which gateway datasource to use
  - Non-LLM: perform binding and credential updates

- Security
  - Gateway creds in Key Vault; require admin approval for production

- Agent roles
  - gateway-operator, approver

- Prompts
  - Concise: "Bind dataset {datasetId} to gateway {gatewayId} datasource {datasourceId}." 
  - Multi-step: "1) Validate gateway health; 2) Fetch secret; 3) Bind dataset; 4) Confirm connectivity." 

- Implementation
  - SDKs: msal, requests
  - Estimate: 3–5 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/BindToGateway" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"gatewayObjectId":"{gatewayId}","datasourceObjectId":"{datasourceId}"}'

---

### 13) Manage-Workspace-Roles

- Purpose: Add or remove workspace members and assign roles.

- Inputs
  - workspaceId, identifier (user/group/service principal), role

- Outputs
  - status, assignedRole

- REST endpoint
  - POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/users
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/groups/add-group-user

- Permissions
  - Workspace.ReadWrite.All (application) or Report.ReadWrite.All + group-level consent

- LLM vs non-LLM
  - LLM: recommend role assignments
  - Non-LLM: execute API calls and audit

- Security
  - Human approval for Admin role assignments; use AAD groups to manage membership

- Agent roles
  - access-manager, approver

- Prompts
  - Concise: "Add user {userEmail} as Contributor to workspace {workspaceId}." 
  - Multi-step: "1) Validate user in AAD; 2) Add user to workspace with role; 3) Notify owner." 

- Implementation
  - SDKs: msal, requests
  - Estimate: 1–2 days

- Sample curl
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/users" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"identifier":"user@contoso.com","groupUserAccessRight":"Contributor"}'

---

### 14) Deploy-CI-Artifact

- Purpose: Orchestrate CI pipeline to import/update artifacts, run tests, and promote to prod with approvals.

- Inputs
  - artifactLocation, pipeline config (stagingGroupId, prodGroupId), testPlan

- Outputs
  - deploymentId, status, validationResults

- REST endpoints used
  - Imports POST, UpdateReportContent, Rebind, GenerateToken, Refresh — see referenced endpoints above

- Permissions
  - Content.Create, Report.ReadWrite.All, Dataset.ReadWrite.All (Application for CI)

- LLM vs non-LLM
  - LLM: propose promotion/readiness; compose release notes
  - Non-LLM: run pbi-tools, call imports, execute tests, handle approvals

- Security
  - Require PR approval, dry-run in staging, Key Vault for secrets

- Agent roles
  - ci-runner, approver, tester

- Prompts
  - Concise: "Run pipeline for branch {branch} and deploy to staging {stagingId}." 
  - Multi-step: "1) Run linter; 2) Build pbix; 3) Import to staging; 4) Run test plan; 5) Request approval to prod." 

- Implementation
  - SDKs: pbi-tools CLI, msal, GitHub Actions/Azure DevOps
  - Estimate: 5–12 days

- Sample curl (import via CI)
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{stagingGroupId}/imports?datasetDisplayName={displayName}" \
    -H "Authorization: Bearer {access_token}" \
    -F "file=@/path/to/{artifact}.pbix"

---

### 15) XMLA-Run-TMSL

- Purpose: Execute TMSL/XMLA commands against the semantic model (partitions, process, deploy) — requires Premium/PPU.

- Inputs
  - workspaceId, datasetId, xmla/TMSL payload

- Outputs
  - operationId, status, result details

- Endpoint notes
  - Use XMLA client (AMO/XMLA) to connect to the workspace's XMLA endpoint (https://docs.microsoft.com/en-us/power-bi/enterprise/xmla-endpoint)
  - REST refresh alternative exists for some operations, but full XMLA requires AMO/XMLA client

- Permissions
  - Dataset.ReadWrite.All (Delegated/Application)

- LLM vs non-LLM
  - LLM: propose TMSL scripts at a high level
  - Non-LLM: execute scripts via XMLA client, manage retries and logging

- Security
  - Premium capacity access only; service principal profile may be needed; Key Vault for secrets

- Agent roles
  - model-author, xmla-executor, auditor

- Prompts
  - Concise: "Process partition 'P1' on dataset {datasetId}." 
  - Multi-step: "1) Export current partition metadata; 2) Generate TMSL to add incremental partition; 3) Execute TMSL; 4) Return status." 

- Implementation
  - SDKs: xmla-client, ADOMD.NET, pbi-tools for model migration
  - Limitations: XMLA read/write requires Premium or PPU
  - Estimate: 5–10 days

- Sample conceptual curl (most XMLA uses client libs rather than REST)
  curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes" \
    -H "Authorization: Bearer {access_token}" \
    -H "Content-Type: application/json" \
    -d '{"type":"full"}'

---

## Mermaid architecture diagrams (renderable)

1) Cloud orchestration

```mermaid
flowchart LR
  subgraph ClientLayer[Users / Frontend]
    U(User)
  end
  subgraph Orchestration[LLM Orchestration]
    LLM[LLM Coordinator]
    Agents[Agents: Orchestrator, Executor, Monitor]
  end
  subgraph CloudInfra[Azure]
    AD[Azure AD]
    KV[Azure Key Vault]
    CI[CI/CD Runner]
  end
  subgraph PowerBI[Power BI Service]
    PBI[Power BI REST API & Service]
    GW[On-prem Gateway]
    XMLA[XMLA endpoint (Premium)]
  end
  U -->|requests| LLM
  LLM --> Agents
  Agents -->|OAuth token request| AD
  Agents -->|secrets retrieval| KV
  Agents -->|REST calls (imports, refresh, embed)| PBI
  Agents -->|XMLA/TMSL| XMLA
  CI -->|deploy artifacts| Agents
  note right of PBI: "Security boundary: Power BI service; RBAC & Capacity"
  note right of KV: "Secrets/Certs; only Agents & CI access via MI or SP"
```

Caption: Cloud orchestration shows LLM choosing operations and agents performing REST calls to Power BI service. Security boundaries: Azure AD issues tokens, Key Vault stores secrets; CI uses service principal/managed identity. Agents operate with least privilege.

2) Local Desktop flow

```mermaid
flowchart LR
  Dev[Developer/Desktop]
  LLM[Local LLM Agent]
  LocalAgent[Local Executor]
  AD[Azure AD]
  KV[Key Vault]
  PBI[Power BI Service]
  Storage[Artifact Storage]

  Dev -->|edit pbix| LocalAgent
  LocalAgent -->|upload pbix via import| PBI
  LocalAgent -->|request token| AD
  LocalAgent -->|get secrets| KV
  LLM -->|plan promotion| LocalAgent
  Storage -->|artifact| LocalAgent

  note right of LocalAgent: "Runs on dev machine or build agent; avoid long-lived secrets on local devices"
```

Caption: Local/editor flow shows developer/local LLM interactions for authoring; use delegated auth for developer actions and Key Vault for any secrets.

---

## Security checklist (expanded)

1. Azure AD app registration patterns
   - CI/service principal app: create app registration, add application permissions (Dataset.ReadWrite.All, Report.ReadWrite.All, Content.Create as needed), use certificate or client secret in Key Vault, grant admin consent.
   - Developer/delegated app: use delegated permissions for interactive flows (Report.Read.All, Dataset.Read.All), request consent during login.

2. Key Vault & Managed Identity
   - Store client secrets, certificates, connection strings, and HSM keys in Key Vault.
   - Use managed identity or federated credentials for CI where supported (GitHub OIDC federation) to avoid long-lived secrets.

3. Least privilege
   - Give service principal workspace-level role rather than tenant-wide admin.
   - Use AAD groups for workspace role assignments and limit direct user assignments.

4. CI/CD gates
   - PR required for changes to PBIR artifacts, run Inspector & Linter in PR checks.
   - Dry-run deployment to staging workspace before production promotion.
   - Manual approval required for actions that alter RLS or workspace Admin roles.

5. Token usage & rotation
   - Use MSAL libraries and short-lived access tokens; rotate client secrets/certs per policy.

6. Preserve RLS
   - Validate RLS post-deploy using Generate-Embed-Token with sample identities; do not alter RLS silently during rebinds.

7. Audit & logging
   - Log all agent actions with correlation IDs to Azure Monitor; redact tokens.

8. Links
   - Power BI REST API: https://learn.microsoft.com/en-us/rest/api/power-bi/
   - Import docs: https://learn.microsoft.com/en-us/rest/api/power-bi/imports
   - UpdateReportContent: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/update-report-content-in-group
   - Generate Token: https://learn.microsoft.com/en-us/rest/api/power-bi/embed-token/reports-generate-token-in-group
   - XMLA: https://learn.microsoft.com/en-us/power-bi/enterprise/xmla-endpoint

---

## Assumptions & validation steps

- PBIR internal structure: assume PBIR/PBIP maps report metadata to `definition/` JSON files (report.json, pages/*, model.json). Validate by extracting a PBIX via pbi-tools or Developer Mode and inspecting `definition/` files.
- Service principal behavior: tenant-level setting required to allow Service Principals to call Power BI APIs — validate in Power BI Admin Portal (Tenant settings).

Validation quick steps
1. Register test app in AAD and request Report.Read.All; validate GET reports in a test workspace.
2. Create service principal, grant app-only permission, and enable in Power BI tenant; test import.
3. Use pbi-tools or pbip extract to confirm PBIR JSON structure.

---

## Appendix: consolidated endpoints & permissions
(See each tool section for per-tool endpoints. Key reference endpoints:)
- Imports (create): POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/imports
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/imports
- UpdateReportContent: POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/UpdateReportContent
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/update-report-content-in-group
- GenerateToken: POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/GenerateToken
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/embed-token/reports-generate-token-in-group
- Refresh dataset: POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes
  - Docs: https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset

---

If you want the final Markdown saved to a different filename, or separate per-tool markdown files, I can export them individually. 

Saved to: pbir_multi_agent_tools_report.md
