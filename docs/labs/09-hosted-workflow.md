# Lab 09: Hosted GitHub workflow

**Outcome:** validate the repository in GitHub Actions, then optionally deploy to your Azure lab using workload identity federation.

## Offline validation

Open **Actions → Validate workshop** and inspect its latest run. It parses JSON/XML, checks artifact contracts and documentation links, and checks script syntax. This workflow needs no Azure credentials.

## Azure workflow

The `azure-workshop.yml` workflow uses manual dispatch, Azure OIDC and the pinned CLI. Configure repository variables `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `APIM_RESOURCE_GROUP`, `APIM_SERVICE_NAME`, `APIC_SERVICE_NAME` and `AZURE_LOCATION`.

Create a dedicated Entra application/service principal and a federated credential for this exact repository and its `main` branch. Use audience `api://AzureADTokenExchange` and issuer `https://token.actions.githubusercontent.com`. Grant Azure API Management Service Contributor on the dedicated APIM resource. API Center write access is only required if extending the workflow to catalog exercises. Keep role assignments scoped to the lab.

Run **Azure workshop** manually:

1. Select `preview` to execute the dev publish plan and review its artifact.
2. Select `publish` to deploy the canonical dev baseline and verify dev v1.
3. Inspect the job log and uploaded result artifact. No client secret is required.

The workflow runs only from `main`; forks need their own Azure identity, variables and federation subject. Do not reuse the instructor identity in a fork. Keep deployment authorization with trusted maintainers. The generated init workflows remain separate learning examples.

See [validation results](../../validation/README.md) for the exact hosted runs executed for the reference workshop. If identity provisioning is unavailable in your tenant, the local Azure CLI exercises remain usable.

[Next: Validation](10-validation.md)
