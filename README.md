# APIM APIOps workshop

A customer workshop using the **real `apiops` command line**. Customers sign in to their own Azure tenant and subscription, then execute each command themselves. There is no Python deployment wrapper and no Azure deployment connection configured in this repository.

Deploy an Orders API to Azure API Management, promote its configuration to QA, change a release and roll it back. Explore extraction, filtering, dependencies, secret redaction, scoped deletion, API Center and pipeline generation.

## Start here

Requirements: **Node.js 22+, npm, Azure CLI, Git, jq and curl**. Commands use Bash on macOS/Linux or WSL. Configure a Git name/email for the commit exercises. You do not need Python to follow the labs.

```bash
git clone https://github.com/msftse-org/apim-apiops-workshop.git
cd apim-apiops-workshop
export WORKSHOP_ROOT="$PWD"
npm install -g @azure-tools/apiops-cli@1.0.5
apiops --version
cp .env.example .env
# Edit .env with YOUR tenant, subscription, names and publisher email.
source .env
az login --tenant "$TENANT_ID"
az account set --subscription "$AZURE_SUBSCRIPTION_ID"
az account show --query '{tenant:tenantId,subscription:id,name:name}' -o table
```

Use a dedicated sandbox resource group. Ask your Azure administrator for the privileges needed to create resources and manage their API configuration. If you already have a dedicated APIM and API Center, enter their names and skip resource creation. The labs never require access to the author's Azure environment.

## Workshop path

| Lab | What the customer runs | What to observe |
|---|---|---|
| [00. CLI and Azure login](docs/labs/00-setup.md) | `npm`, `apiops --help`, `az login` | Correct CLI, tenant and subscription |
| [01. Azure resources](docs/labs/01-resources.md) | `az group`, `az apim`, `az rest` | APIM Consumption and API Center Free |
| [02. Deploy dev and QA](docs/labs/02-deploy.md) | `apiops publish`, `--dry-run`, `curl` | Two routes, HTTP 200, environment headers |
| [03. Change and roll back](docs/labs/03-release.md) | `git commit`, `--commit-id`, `git revert` | Dev v1, v2, v1; QA stays v2 |
| [04. Environment overrides](docs/labs/04-overrides.md) | `--overrides`, full/incremental publish | Override-only changes need full publish |
| [05. Extract and filter](docs/labs/05-filtering.md) | `apiops extract`, `--filter`, `--no-transitive` | Dependencies, wildcards and exclusions |
| [06. Secrets and deletion](docs/labs/06-guards.md) | Secret extraction, `--delete-unmatched`, `--remove-stale` | Redaction, rejection and one scoped DELETE |
| [07. API Center](docs/labs/07-api-center.md) | `apiops apic extract/publish` | Metadata, specifications and replay |
| [08. Generate pipelines](docs/labs/08-cicd.md) | `apiops init`, `--force` | GitHub/Azure DevOps scaffolds and Copilot prompts |
| [09. CLI output and automation](docs/labs/09-cli-utilities.md) | `--help`, `--format json`, `--log-level` | Plans, counts and exit codes |
| [10. Verify results](docs/labs/10-validation.md) | `curl`, `jq`, artifact inspection | Match the expected outcomes |
| [11. Cleanup](docs/labs/11-cleanup.md) | `az resource list`, `az group delete` | Remove your own dedicated lab group |

Estimated workshop time: **90–120 minutes**, excluding provisioning. This is a planning estimate, not a measured benchmark.

## The first real deployment command

After setup and provisioning:

```bash
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts \
  --overrides configuration.dev.yaml \
  --dry-run
```

Remove `--dry-run` to apply the configuration. Every subsequent lab shows its actual CLI flags and expected results.

## Files

- `apim-artifacts/` and `apic-artifacts/`: canonical configuration and specifications.
- `configuration.dev.yaml` / `configuration.qa.yaml`: environment overrides.
- `filter.*.yaml` and `examples/`: explicit filters and disposable fixtures.
- `docs/labs/`: customer commands and explanations.
- `docs/presentation/`: Microsoft-themed PowerPoint and workshop links.
- `validation/`: sanitized measured results and coverage.
- `.env` and `.work/`: your local configuration and outputs, excluded from Git.

The repository's GitHub Actions workflow performs **offline content checks only**. Generated deployment pipeline examples stay in your local `.work/` directory. Connecting them to Azure is a separate customer-owned decision.

## Scope

The lab uses APIM Consumption and API Center Free. Dev and QA are namespaces in one gateway, not isolated security/capacity boundaries. The sample API returns synthetic data without subscription authentication. Consumption usage may incur charges.

CLI package version: **1.0.5**. See [validation](validation/README.md), [coverage](docs/coverage.md) and [official sources](docs/sources.md). The workshop covers all top-level CLI command families, not every resource type, APIM tier or option combination. APIOps here means API configuration as code; it does not operate an AI model service.
