# Coverage and boundaries

Every customer-facing deployment and extraction step calls the native `apiops` CLI. Azure CLI handles account selection and provisioning, Git handles change history, and curl/jq inspect results. No deployment wrapper is required.

| Capability | Lab | Measured scope |
|---|---|---|
| CLI installation/help | 00 | Published npm package 1.0.5 |
| Full publish and JSON dry-run | 02 | Dev and QA configuration |
| OpenAPI, operation policies, backend, fragment, named values | 02/05 | Status/echo runtime and extraction |
| Products and tags | 02/05 | Publish and association |
| Prefixes and environment overrides | 04 | Shared gateway namespaces |
| Incremental change and rollback | 03 | One named-value PUT and Git revert |
| Override-only commit | 04 | Zero incremental PUTs, full publish |
| Filters and dependency expansion | 05 | Exact, full, wildcard/exclusion and filtered publish |
| Secret redaction and rejection | 06 | Synthetic value only |
| Commit-scoped deletion and remove-stale | 06 | One disposable named value |
| API Center | 07 | Seed, backup, same-instance replay, metadata-only variants |
| Both init platforms | 08 | Scaffolds, prompts, overwrite conflict and force |
| CLI output and diagnostics | 09 | Native help, JSON, debug logs, exit codes |
| Verification | 10 | Real endpoint and artifact assertions |
| Cleanup | 11 | Instructions only; reference group retained |

See [validation](../validation/README.md) for measured results and any corrections. The local command blocks are the tested customer path. GitHub repository CI checks content offline and has no Azure deployment connection.

APIM workspaces, additional protocols, revisions/version sets, loggers/diagnostics, gateways, subscriptions and other resource combinations need dedicated fixtures or different tiers. Key Vault, pipeline secret injection, interactive Copilot, hosted CI deployments, sovereign clouds and private networking are not claimed as tested integrations here. API Center workspaces are distinct from APIM workspaces.

This synthetic, unauthenticated sample uses APIM Consumption and a shared dev/QA gateway. The pinned package improves repeatability but is not a security certification. Review current upstream dependency advisories, permissions, secret management, environment isolation and approval practices before production adoption.
