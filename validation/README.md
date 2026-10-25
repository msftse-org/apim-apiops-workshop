# Customer-readiness validation

Validated **25 October 2026**, using the native `@azure-tools/apiops-cli@1.0.5` executable. The public customer path and the author's corporate-network installation were checked separately.

## Public installation outside the corporate network

[GitHub-hosted compatibility run](https://github.com/msftse-org/apim-apiops-workshop/actions/runs/40197294045) passed on Ubuntu with **Node.js 22 and 24**:

- Package metadata and installation directly from `https://registry.npmjs.org/`.
- CLI version assertion and APIM/API Center help commands.
- GitHub Actions and Azure DevOps `apiops init`, including generated prompt directories.

This temporary validation run used **no Azure credentials, Azure login or deployment**. The default branch retains its offline content checks. The run's commit preserves the exact probe definition.

On the author's corporate machine, direct public-registry access returned `ENOTCONN`, while both a clean installation and the documented local-prefix fallback succeeded through its already-configured registry. This is a local network difference, not a customer prerequisite or evidence of a missing public package. The customer instructions use standard npm behavior and document organization-approved mirrors separately.

## Fresh Azure customer path

Started with a clean clone, an isolated CLI installation and a **new dedicated resource group**. Created APIM Consumption and API Center Free in West Europe with the Lab 01 commands. Executed **21 literal Bash blocks** from Labs 00–10, including all main deployment/extraction exercises. A private test harness supplied target values and stopped on errors; deployment operations themselves were the documented native commands.

| Check | Observed result |
|---|---|
| Tools, account, tenant and cloud assertions | Passed |
| Resource-provider checks and APIM readiness | Passed |
| Fresh resource creation | Passed |
| Dev / QA publish and status / echo requests | Passed, HTTP 200 and expected headers/body |
| Release change and rollback | Dev v1 → v2 → v1; QA remained v2 |
| Incremental / override-only plans | 1 PUT / 0 PUTs |
| Full / exact / dependency / pattern extraction | Passed |
| Secret redaction and publish rejection | Redacted fixture, expected exit 2 |
| Filter + delete rejection | Expected exit 2 |
| Commit-scoped deletion | Exactly one disposable named value |
| Stale local-file removal | Passed |
| API Center seed / backup / replay / metadata-only | Passed |
| Both pipeline scaffold platforms | Generated, conflict exit 1, force succeeded |
| Final assertions | All passed |
| Whole-group cleanup | Passed; delete completed and group existence returned false |

Azure execution platform: **macOS, Bash 3.2.57, Node.js 26.7.0, Azure CLI 2.89.1**. The public Linux checks above validate installation/help/scaffolding, not the Azure deployment labs on Linux.

[Machine-readable evidence](customer-readiness.json) includes hashes of the executed command blocks. [Earlier existing-service results](native-cli-results.json) retain the preceding 18-block validation record.

## Corrections made during the customer audit

- Required Bash, sequential labs and one shell session; added recovery instructions for shared variables.
- Added checks for installed tools, placeholders, selected tenant/subscription, Azure public cloud and supported curl flags.
- Pinned local authentication to `AzureCliCredential` and cleared inherited `COMMIT_ID`.
- Added provider-registration guidance and an explicit APIM readiness wait.
- Added bounded polling for deployment propagation, including transient HTTP failures.
- Replaced final printouts with assertions for versions, headers, counts, deletion scope and artifact presence.
- Added a local-prefix installation fallback that preserves native `apiops` commands.
- Added Bash syntax checks for every fenced lab command block to the offline CI.

## What a passing run does not guarantee

Customers still need permitted Azure regions/SKUs, sufficient quota, resource-provider registration, resource access and allowed network endpoints. Corporate policies can deny creation or writes even when the commands are correct. The echo lab uses an external public service and can be affected by its availability.

Interactive login for a new user, every OS/Node combination, all APIM resource types and tiers, Key Vault, private networking, interactive Copilot and hosted Azure deployments were not verified. Run this workshop in a dedicated sandbox. No claim is made that every customer tenant will behave identically.

The public repository contains no Azure target values, deployment identity or live deployment workflow. Raw Azure logs and customer identifiers remain private.
