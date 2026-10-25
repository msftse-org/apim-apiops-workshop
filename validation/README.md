# Native CLI validation

Validated **25 October 2026** with the installed `@azure-tools/apiops-cli@1.0.5` executable. The test executed the literal Bash command blocks in customer Labs 02–10, using locally supplied sandbox identifiers. **18 command blocks completed successfully.** No Python deployment wrapper was used.

[Machine-readable results](native-cli-results.json) record the package integrity, passed blocks, observed values and coverage limits.

| Check | Observed result |
|---|---|
| Dev and QA full publish / previews | Passed |
| Runtime status and echo calls | HTTP 200 |
| Release and rollback | dev v1 → v2 → v1; QA v2 |
| Incremental change plan | 1 PUT |
| Override-only commit preview | 0 PUTs; full publish exercised |
| Dependency / exact extraction | 11 / 7 resources |
| Full extraction | Completed |
| Filtered publish | Completed |
| Wildcard and exclusion | Environment included; release excluded |
| Synthetic secret extraction | `*** REDACTED ***` |
| Redaction / filter-delete rejection | Expected exit 2 |
| Commit-scoped deletion | Exactly 1 NamedValue DELETE |
| Remove stale | Obsolete extracted file removed |
| API Center seed, backup and replay | Completed |
| API Center metadata-only extract/publish | Completed, no specification files in metadata snapshot |
| GitHub Actions and Azure DevOps init | Both generated files; conflict exit 1; force succeeded |
| Help, JSON and debug output | Completed |
| Final endpoint verification | dev v1 and QA v2 |

## What the validation caught

The first immediate read after publishing v2 still returned v1 during gateway propagation. Lab 03 now includes a visible Bash/curl retry loop before asserting a release. The revised command blocks passed. A dry-run remains a plan rather than an Azure acceptance guarantee.

## Boundaries

The CLI package installed successfully through the test environment's configured npm registry. A separate direct connection check to registry.npmjs.org failed with `ENOTCONN`; availability from every customer network was not verified. The package version and integrity are recorded rather than assuming a source checkout and published tarball are identical.

The reference APIM Consumption and API Center Free resources already existed. Read-only resource checks were performed; fresh provisioning was not repeated for this command validation. The original sandbox setup created the resources. Whole-resource-group cleanup was intentionally not executed because the reference demo remains available.

Interactive Azure login uses each customer's own account. Interactive Copilot, hosted deployments, Key Vault, private networking, other APIM tiers and every supported resource type remain outside the measured coverage.

The public repository has **no Azure deployment workflow, target variables, or federation identity**. Its GitHub Actions workflow only checks content offline. Raw Azure logs and local identifiers are excluded from the public evidence.
