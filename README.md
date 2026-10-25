# APIM APIOps workshop

Build and manage Azure API Management configuration with the [Azure APIOps CLI](https://github.com/Azure/apiops-cli). Deploy a working Orders API, promote it to QA, change its release, and roll it back. Then explore extraction, dependencies, secrets, scoped deletion, API Center and CI/CD.

The workshop uses **APIM Consumption** and **API Center Free**. Development and QA are separate API namespaces in one gateway, suitable for a low-cost lab. They do not provide separate security or capacity boundaries. The API serves synthetic data without a subscription key. Keep it out of production.

## Start here

```bash
git clone https://github.com/msftse-org/apim-apiops-workshop.git
cd apim-apiops-workshop
bash scripts/install.sh
cp config.example.json config.local.json
# Edit config.local.json with YOUR subscription and globally unique service names.
az login
python3 scripts/resources.py plan
python3 scripts/resources.py provision
python3 scripts/workshop.py doctor
```

Already have the workshop resources? Fill in their names and skip provisioning. Each participant should use their own dedicated resource group or coordinate access with the instructor. Never use these exercises against a shared production gateway.

## Exercises

| Lab | Outcome | Main utility |
|---|---|---|
| [00. Setup](docs/labs/00-setup.md) | Install the pinned CLI and select your sandbox | `install.sh`, `doctor` |
| [01. Resources](docs/labs/01-resources.md) | Create or reuse APIM and API Center | `resources.py` |
| [02. First deployment](docs/labs/02-deploy.md) | Preview and deploy dev + QA, then call the API | `publish --dry-run`, `publish` |
| [03. Release and rollback](docs/labs/03-release.md) | Change v1 to v2 and restore v1 using Git | `--commit-id`, `git revert` |
| [04. Environment overrides](docs/labs/04-overrides.md) | Understand names, routes, values and the override-only trap | `--overrides` |
| [05. Extraction and filters](docs/labs/05-filtering.md) | Extract one API, its dependencies, or a wider baseline | `--filter`, `--no-transitive` |
| [06. Secrets and deletion](docs/labs/06-guards.md) | Observe redaction, rejection and one scoped DELETE | `--delete-unmatched`, `--remove-stale` |
| [07. API Center](docs/labs/07-api-center.md) | Back up and replay metadata and OpenAPI definitions | `apic extract`, `apic publish` |
| [08. CI/CD and Copilot](docs/labs/08-cicd.md) | Generate both pipeline formats and inspect setup prompts | `init`, `--force` |
| [09. Hosted workflow](docs/labs/09-hosted-workflow.md) | Run validation and optional Azure deployment in GitHub Actions | OIDC workflow |
| [10. Validation and troubleshooting](docs/labs/10-validation.md) | Execute the complete suite and inspect evidence | `validate-live`, JSON reports |
| [11. Cleanup](docs/labs/11-cleanup.md) | Review resources and explicitly delete your workshop group | `resources.py cleanup` |

The learning path is estimated at **90–120 minutes**, excluding provisioning and identity setup. This is a planning estimate, not a measured benchmark.

## Repeat the demonstrated flow

```bash
python3 scripts/workshop.py preview --env dev
python3 scripts/workshop.py publish --env dev
python3 scripts/workshop.py publish --env qa
python3 scripts/workshop.py status
python3 scripts/workshop.py cycle
```

`cycle` makes a disposable local Git repository under `.work/`, publishes one changed named value, verifies dev v2, and uses a Git revert to restore dev v1. QA stays on v2. It does not push exercise commits to GitHub.

## Validate the complete workshop

```bash
python3 scripts/validate.py             # Offline artifact and documentation checks
python3 scripts/workshop.py validate-live  # Writes to your configured Azure lab
```

The live suite executes the main workshop commands and assertions. It leaves dev v1 and QA v2 deployed. Logs and target configuration stay in ignored local files. Read [validation results](validation/README.md) for what was actually run, the test date, and remaining coverage limits.

## Repository map

- `apim-artifacts/`: canonical API definitions, policies, backend, named values, product and tag.
- `apic-artifacts/`: API Center catalog example and OpenAPI definition.
- `configuration.*.yaml`: dev/QA overrides using canonical resource names.
- `filter.*.yaml`: explicit filtering of all supported top-level types.
- `scripts/`: install, provision, exercise, verify and cleanup utilities.
- `docs/labs/`: step-by-step instructions with expected outcomes.
- `docs/presentation/`: Microsoft-themed workshop presentation.
- `validation/`: sanitized results and scope statements.
- `.work/`: generated pipelines, snapshots, Git exercises and raw logs (ignored).

## Version and scope

The CLI is built from **1.0.5**, commit [`129fb326`](https://github.com/Azure/apiops-cli/tree/129fb326e6878c2bedd45e8ae4ccb8526de688a4). Installation uses `npm ci` against its lockfile. This pin makes the exercises repeatable, but does not certify the upstream dependency tree as secure. Review current advisories before production use. See [coverage and limitations](docs/coverage.md) and [official sources](docs/sources.md).

APIOps means API configuration as code here. The repository also supplies Copilot prompts to assist setup. This workshop does not demonstrate AI model hosting or autonomous incident remediation.
